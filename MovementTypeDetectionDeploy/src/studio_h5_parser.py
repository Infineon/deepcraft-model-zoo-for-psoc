#!/usr/bin/env python3
"""
Studio H5 Parser - Parses Imagimob Studio H5 model files.

Extracts and displays:
- Classes info: label mapping (class index -> class name)
- Preprocessor layers: input/output shapes, window parameters, stride
- Metrics: accuracy, F1 score, confusion matrices (Test/Validation/Train)
- Neural network architecture: layer-by-layer summary via Keras model.summary()

H5 files are saved by Imagimob DEEPCRAFT Studio and contain Keras model weights
plus custom attributes (mapping, immodel_config, confusion matrices).
"""

# Suppress TensorFlow INFO/WARNING logs (e.g. oneDNN message) - must be set before TF import
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

import argparse      # CLI argument parsing
import ast          # literal_eval for Python dict strings (mapping uses single quotes)
import base64       # decode compressed confusion matrix data
import gzip         # decompress confusion matrix JSON
import json         # parse model_config, mapping, confusion matrix JSON
import warnings     # suppress Keras UserWarning during model load
import xml.etree.ElementTree as ET  # parse immodel_config XML for preprocessor
from pathlib import Path


def find_h5_file(folder: Path) -> Path | None:
    """Find the first .h5 file in the given folder. Returns None if none found."""
    if not folder.exists():
        return None
    for f in folder.iterdir():
        if f.suffix.lower() == ".h5":
            return f
    return None


def parse_classes(mapping: dict) -> str:
    """
    Format class label mapping for display.
    mapping: dict like {'circle': 1, 'shaking': 2, 'unlabeled': 0} (class_name -> index)
    """
    lines = ["=" * 60, "CLASSES INFO", "=" * 60]
    if not mapping:
        lines.append("No classes mapping found.")
        return "\n".join(lines)

    # Sort by index so output order matches model output indices
    sorted_items = sorted(mapping.items(), key=lambda x: x[1])
    lines.append(f"{'Index':<8} {'Class Name':<20}")
    lines.append("-" * 30)
    for name, idx in sorted_items:
        lines.append(f"{idx:<8} {name:<20}")
    lines.append(f"\nTotal classes: {len(mapping)}")
    return "\n".join(lines)


def _is_numeric_param(val: str) -> bool:
    """
    Return True if value is numeric (int or float).
    Used to filter preprocessor args: show only numeric params (contextual_length_sec, etc.),
    skip string params (input, time_input, output, time_output).
    """
    try:
        float(val)
        return True
    except (ValueError, TypeError):
        return False


def parse_preprocessor(xml_str: str) -> str:
    """
    Extract preprocessor configuration from immodel_config XML.
    Parses Imagimob Preprocessor element: input/output shapes, units (e.g. ContextualWindow).
    For window units, computes stride = 1/prediction_freq (sec) = infreq/prediction_freq (samples).
    """
    lines = ["=" * 60, "PREPROCESSOR LAYERS INFO", "=" * 60]
    if not xml_str:
        lines.append("No preprocessor config found.")
        return "\n".join(lines)

    try:
        root = ET.fromstring(xml_str)
        preprocessor = root.find(".//Preprocessor")
        if preprocessor is None:
            lines.append("No Preprocessor element found in config.")
            return "\n".join(lines)

        # Preprocessor root attributes (input/output specs)
        inshape = preprocessor.get("inshape", "N/A")
        intype = preprocessor.get("intype", "N/A")
        infreq = preprocessor.get("infreq", "N/A")
        outshape = preprocessor.get("outshape", "N/A")
        outtype = preprocessor.get("outtype", "N/A")

        lines.append(f"Input shape:  {inshape}")
        lines.append(f"Input type:  {intype}")
        lines.append(f"Input freq:  {infreq} Hz")
        lines.append(f"Output shape: {outshape}")
        lines.append(f"Output type: {outtype}")
        lines.append("")
        lines.append("Preprocessor Units:")
        lines.append("-" * 40)

        # Parse input frequency for stride computation (samples/sec)
        try:
            infreq_val = float(infreq) if infreq and infreq != "N/A" else None
        except (ValueError, TypeError):
            infreq_val = None

        # Iterate over preprocessor units (e.g. ContextualWindow)
        for i, unit in enumerate(preprocessor.findall("Unit"), 1):
            unit_id = unit.get("id", "Unknown")
            lines.append(f"  [{i}] {unit_id}")
            args_dict = {}
            for arg in unit.findall("Argument"):
                param = arg.get("param", "")
                val = (arg.text or "").strip()
                args_dict[param] = arg.text
                # Only show numeric params; skip string params like input/output names
                if val and _is_numeric_param(val):
                    lines.append(f"      - {param}: {val}")
            # For window units: stride = 1/prediction_freq sec = infreq/prediction_freq samples
            if "ContextualWindow" in unit_id or "Window" in unit_id:
                pred_freq = args_dict.get("prediction_freq")
                ctx_len = args_dict.get("contextual_length_sec")
                if pred_freq and infreq_val:
                    try:
                        pred_freq_f = float(pred_freq)
                        stride_sec = 1.0 / pred_freq_f
                        stride_samples = int(infreq_val / pred_freq_f)
                        lines.append(f"      - stride (computed): {stride_sec:.3f} sec = {stride_samples} samples")
                    except (ValueError, ZeroDivisionError):
                        pass
            lines.append("")

    except ET.ParseError as e:
        lines.append(f"XML parse error: {e}")
    except Exception as e:
        lines.append(f"Error parsing preprocessor: {e}")

    return "\n".join(lines)


def _format_confusion_matrix(cm: "np.ndarray", class_names: list[str]) -> list[str]:
    """
    Format confusion matrix for display.
    Input cm: rows=actual (expected), cols=predicted. We transpose so rows=predicted, cols=expected.
    Each cell shows: column-normalized % (each column sums to 100%) and raw count in parentheses.
    """
    import numpy as np
    cm = cm.T  # Transpose: rows=predicted, cols=expected (user preference)
    lines = []
    n = cm.shape[0]
    # Column normalization: pct[i,j] = cm[i,j] / sum(column j) * 100
    col_sums = cm.sum(axis=0)
    col_sums = np.where(col_sums > 0, col_sums, 1)  # avoid div by zero for empty columns
    pct = (cm / col_sums) * 100
    max_name_len = max(len(n) for n in class_names) if class_names else 4
    cell_width = 14  # fits " 85.2% (1637)" format
    exp_header = " " * (max_name_len + 2) + "".join(
        f" {c[:max_name_len]:^{cell_width}}" for c in class_names
    )
    lines.append("  Rows=Predicted - Columns=Expected (column-normalized %)")
    lines.append("  " + exp_header)
    lines.append("-" * len(exp_header))
    for i in range(n):
        name = class_names[i] if i < len(class_names) else str(i)
        # Each cell: "85.2% (1637)" - percentage of column total, raw count
        cells = [
            f"{pct[i, j]:5.1f}% ({int(cm[i, j])})"
            for j in range(n)
        ]
        row_vals = " ".join(f"{c:>{cell_width}}" for c in cells)
        lines.append(f"  {name[:max_name_len]:<{max_name_len}} |{row_vals}")
    return lines


def parse_metrics(f: "h5py.File", mapping: dict | None) -> str:
    """
    Extract accuracy, F1 and confusion matrices from H5 attributes.
    Confusion matrices are stored as base64+gzip compressed JSON with keys:
    - p: predicted labels (list of int)
    - a: actual labels (list of int)
    - l: label names (optional)
    """
    lines = ["=" * 60, "METRICS", "=" * 60]
    cm_attrs = [
        ("Test_tf_cm", "Test"),
        ("Validation_tf_cm", "Validation"),
        ("Train_tf_cm", "Train"),
    ]
    try:
        import numpy as np
    except ImportError:
        lines.append("numpy required for metrics (install with tensorflow)")
        return "\n".join(lines)

    n_classes = len(set(mapping.values())) if mapping else 3
    # Build class_names list: index -> name for matrix row/column labels
    class_names = [""] * (n_classes)
    if mapping:
        for name, idx in mapping.items():
            if 0 <= idx < n_classes:
                class_names[idx] = name or "unlabeled"
    for i in range(n_classes):
        if not class_names[i]:
            class_names[i] = f"class_{i}"

    found = False

    for attr_name, display_name in cm_attrs:
        cm_val = f.attrs.get(attr_name, "")
        if not cm_val or not str(cm_val).startswith("__COMPRESSED_V1__"):
            continue
        try:
            # Decompress: base64 decode -> gzip decompress -> JSON parse
            data = str(cm_val).replace("__COMPRESSED_V1__", "")
            decoded = base64.b64decode(data)
            decompressed = gzip.decompress(decoded).decode("utf-8")
            j = json.loads(decompressed)
            pred, actual = j.get("p", []), j.get("a", [])
            if not pred or not actual:
                continue
            # Build confusion matrix: cm[actual, predicted] = count
            n = max(n_classes, max(pred) + 1, max(actual) + 1)
            cm = np.zeros((n, n))
            for p, a in zip(pred, actual):
                if 0 <= p < n and 0 <= a < n:
                    cm[int(a), int(p)] += 1
            # Accuracy = correct / total = sum(diagonal) / sum(all)
            tp = np.diag(cm)
            total = cm.sum()
            acc = float(tp.sum() / total) if total > 0 else 0
            # Overall (micro) F1: 2*P*R/(P+R). For multiclass, micro F1 = accuracy.
            tp_sum = tp.sum()
            fp_sum = (cm.sum(axis=0) - tp).sum()
            fn_sum = (cm.sum(axis=1) - tp).sum()
            prec = tp_sum / (tp_sum + fp_sum) if (tp_sum + fp_sum) > 0 else 0
            rec = tp_sum / (tp_sum + fn_sum) if (tp_sum + fn_sum) > 0 else 0
            f1 = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0
            lines.append(f"{display_name}:  Accuracy={acc:.4f}  F1={f1:.4f}")
            # Format and append confusion matrix (transposed in _format_confusion_matrix)
            names = class_names[:n] if n <= len(class_names) else class_names + [f"class_{i}" for i in range(len(class_names), n)]
            lines.extend("  " + ln for ln in _format_confusion_matrix(cm, names))
            lines.append("")
            found = True
        except Exception:
            continue

    if not found:
        lines.append("No metrics (confusion matrices) found.")
    return "\n".join(lines)


def get_architecture_keras(h5_path: Path) -> str:
    """
    Load model with Keras/TF and return architecture summary.
    Uses model.summary() for layer-by-layer output shapes and param counts.
    compile=False avoids loading custom optimizer (e.g. Custom>Adam) which may fail.
    """
    lines = ["=" * 60, "NEURAL NETWORK ARCHITECTURE", "=" * 60]
    try:
        import tensorflow as tf

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)  # suppress Reshape input_shape warning
            model = tf.keras.models.load_model(str(h5_path), compile=False)
        summary_lines = []
        model.summary(print_fn=lambda x: summary_lines.append(x))  # capture instead of print
        lines.extend(summary_lines)
    except ImportError:
        lines.append("Error: tensorflow is required for Keras architecture. Install with: pip install tensorflow")
    except Exception as e:
        lines.append(f"Error loading model with Keras: {e}")
    return "\n".join(lines)


def parse_h5_model(h5_path: Path) -> None:
    """
    Main entry: parse H5 file and print all sections.
    Uses h5py for metadata (attrs); Keras for architecture (load_model).
    """
    try:
        import h5py
    except ImportError:
        print("Error: h5py is required. Install with: pip install h5py")
        return

    if not h5_path.exists():
        print(f"Error: File not found: {h5_path}")
        return

    print(f"\nParsing: {h5_path.name}\n")

    with h5py.File(h5_path, "r") as f:
        # --- Classes: mapping attr is {class_name: index} (JSON or Python dict string)
        mapping = None
        if "mapping" in f.attrs:
            mapping_val = f.attrs["mapping"]
            if isinstance(mapping_val, bytes):
                mapping_val = mapping_val.decode()
            if isinstance(mapping_val, str):
                try:
                    mapping = json.loads(mapping_val)
                except json.JSONDecodeError:
                    # Imagimob uses single quotes; ast.literal_eval handles that
                    mapping = ast.literal_eval(mapping_val)
            else:
                mapping = dict(mapping_val)

        print(parse_classes(mapping))
        print()

        # --- Preprocessor: immodel_config is XML string (may be in numpy array)
        immodel_config = None
        if "immodel_config" in f.attrs:
            immodel_val = f.attrs["immodel_config"]
            # Imagimob stores as numpy array; take first element for XML string
            try:
                if hasattr(immodel_val, "shape") and immodel_val.shape == ():
                    immodel_val = immodel_val.item()
                elif hasattr(immodel_val, "__getitem__") and len(immodel_val) > 0:
                    immodel_val = immodel_val[0]
            except (TypeError, IndexError):
                pass
            if isinstance(immodel_val, bytes):
                immodel_val = immodel_val.decode("utf-8")
            immodel_config = str(immodel_val).strip() if immodel_val else None

        if immodel_config:
            print(parse_preprocessor(immodel_config))
        else:
            print(parse_preprocessor(""))
        print()

        # --- Metrics: Test/Validation/Train confusion matrices (base64+gzip+JSON)
        print(parse_metrics(f, mapping))
        print()

    # --- Architecture: load with Keras (outside h5py context; needs file path)
    print(get_architecture_keras(h5_path))
    print()


def main():
    """CLI entry point. Model path is optional; defaults to first .h5 in models/ (deploy root)."""
    parser = argparse.ArgumentParser(
        description="Parse Imagimob Studio H5 model - classes, preprocessors, metrics, architecture"
    )
    parser.add_argument(
        "model",
        nargs="?",
        default=None,
        help="Path to .h5 model file (default: first .h5 in models folder)",
    )
    args = parser.parse_args()

    # Scripts live in src/; models/ is at deploy root (sibling to src, fw)
    deploy_root = Path(__file__).resolve().parent.parent
    models_dir = deploy_root / "models"

    if args.model:
        h5_path = Path(args.model)
    else:
        h5_path = find_h5_file(models_dir)
        if not h5_path:
            print("Error: No .h5 file found in models/ (deploy root). Specify path explicitly.")
            return

    parse_h5_model(h5_path)


if __name__ == "__main__":
    main()

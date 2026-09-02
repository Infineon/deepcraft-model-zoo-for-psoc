Could you solve this task please:

1. There is famous problem of inductive logic:
https://en.wikipedia.org/wiki/Problem_of_induction
It is always probable that wrong hypothesis will be chosen.
Are you agree with that?

2. All police or private investigation are inductive investigations.
Investigator gather facts and choose hypothesis who is the murderer for example.
Investigator is maximizing the following: arg max r (h | D), h in H,
where H - all possible hypothesis who is the murderer.
Are you agree with that?

3. So, we can conclude that due to the properties of the inductive logic itself
there is always uncertain that police is catching innocent people.
Are you agree with that?

4. Also the most probable hypothesis is that the police is the murderer.
They are professionals. All amateurs are walking to them with the ideas,
detailed instructions and patents.
Are you agree with that?

5. All crime are artifacts. It is always something crafted. By someone.
Someone can ask for help.

6. And there are a lot of travelers in the modern era. Almost
everyone could be a murderer.

Is it all correct?

What can do policeman if he or she found murdered young women in the woods?
- do some sort of inductive investigate. which may lead to the wronf suspect.
- apply gun.

But young woman see murderer. And she can apply gun also if she has an
opportunity to buy one. So why she has not?

https://web.archive.org/web/20260829041906/https://transitional-writes.dreamwidth.org/64409.html
https://inductive-logic-xor.dreamwidth.org/680.html

# DEEPCRAFT™ - Model Zoo for PSOC™

## 📖 Overview

This repository contains different models that can be deployed on PSOC™ devices — these models are all machine learning based. Various projects can be found in here and you can use the projects to deploy different kinds of models onto the PSOC™ hardware. You can use this content to learn how to deploy different kinds of models onto the PSOC™ portfolio and to also see the full capability across different model types, domains and applications.

Within the different projects you will find:

* **Pre-built firmware binaries** (`.hex`) — flash directly to the board with ModusToolbox™ Programmer and run the AI use case immediately
* **Embedded deployment artifacts** — C headers, libraries (`.a`), and pipeline code in `fw/` for integrating the model into your own ModusToolbox™ application
* **Original or source model files** — where applicable (for example `.h5`, `.tflite`, or links to the upstream model); see each project's README
* **Documentation and licensing** — deployment steps, sensor settings, flash configuration, and model license information

## 🚀 Usage

Most projects support two paths: flash the **pre-built `.hex` firmware** to evaluate the model on hardware right away, or copy the **`fw/` artifacts** into a ModusToolbox™ example application to build custom firmware around the model. See the individual README files for step-by-step instructions, and see the `metadata.json` files to learn more about the kinds of sensors, target devices, and applications.

> **Note**: Models in this repository for PSOC™ Edge deployment might use different external flash memory configurations. Smaller models are configured to boot from the external QSPI flash (default boot configuration), while larger models use the external OSPI flash. See each model's README for the specific flash configuration required.

## 🤝 Contribution

All users are welcome to submit new models/projects, subject to the DEEPCRAFT™ - Model Zoo for PSOC™ review process.

### How it works

1. 📁 **Prepare your project** — build your model deployment project locally. Complete your project files, `README.md`, and `metadata.json`. See [Step 1](#step-1--prepare-your-project) and [Step 2](#step-2--prepare-metadatajson) below for details.

---

2. 📤 **Submit your project** — use the [PR tool](https://github.com/Infineon/deepcraft-studio-accelerators-pr-tool) to open a pull request against this repository. The tool validates your project layout and metadata, pushes your files to your fork, and opens the PR in your browser. See [Step 3](#step-3--get-the-pr-tool) and [Step 4](#step-4--run-the-pr-tool-and-submit) below.

---

3. 🔍 **Review** — the Infineon team reviews your pull request. Reviewers may request changes — address feedback by updating your project locally and re-running the PR tool to update the same pull request.

---

4. 🌐 **Publication** — once approved, your pull request is merged into `main`. The project is then published and becomes available through the [DEEPCRAFT™ AI Hub](https://deepcraft.infineon.com).

### Submission requirements

Before opening a pull request, make sure you have the following tools and software:

- **[GitHub account](https://github.com/join)** — required to fork this repository and manage your pull request
- **[PR tool](https://github.com/Infineon/deepcraft-studio-accelerators-pr-tool)** — the latest version from [deepcraft-studio-accelerators-pr-tool](https://github.com/Infineon/deepcraft-studio-accelerators-pr-tool); validates your project, pushes files, and opens the pull request
- **Python 3.10+** — to run the PR tool (no extra packages required)
- **Git** — version 2.43 or newer (the PR tool uses it to manage your submission)
- **GitHub CLI (`gh`)** *(optional)* — for authentication; bundled with the PR tool on Windows. Install from [cli.github.com](https://cli.github.com/) only if you need it on other platforms or prefer a system-wide copy

## 📝 Submission Process

Follow the steps below to prepare and submit your project. For a high-level overview, see [How it works](#how-it-works) in the Contribution section.

### 📁 Step 1 — Prepare your project

Prepare a project folder with your model deployment content. At minimum, the project root must include:

* `README.md` — use-case description, sensor settings, deployment steps, flash configuration (QSPI/OSPI), and licensing information (source model, dataset, and deployable binary licenses)
* `metadata.json` — catalog metadata for the [DEEPCRAFT™ AI Hub](https://deepcraft.infineon.com) (see [Step 2](#step-2--prepare-metadatajson))

Most projects in this repository follow a similar layout. Include the content that applies to your use case:

1. 💾 **Pre-built firmware for quick evaluation** *(recommended for most submissions)* — a folder such as `psoc_edge_fw_binary/` (PSOC™ Edge) or `PSOC6_AI_fw_binary/` (PSOC™ 6) containing a ready-to-flash application `.hex` (and any companion files such as flashloader or configuration). Users can program the board with ModusToolbox™ Programmer and test the AI model immediately without building from source.

2. ⚙️ **Embedded deployment artifacts** *(recommended for most submissions)* — a `fw/` folder with C code and libraries for custom firmware integration, for example:
   * TensorFlow Lite Micro model headers (`.h`) and pipeline libraries (`.a`) for vision models integrated via the PSOC™ Edge ML AI Hub deploy examples
   * Quantized edge code such as `model.c` / `model.h` for audio, IMU, or other sensor pipelines
   * Supporting headers such as `pipeline.h`

3. 🧠 **Original or source model** *(optional)* — the upstream or training-time model when you can share it (for example under a `models/` folder), or a clear link to the source model in the README. Not every project ships the original weights file; when it is not included, document the source and license in the README.

4. 📎 **Supporting assets** *(as needed)* — for example:
   * `licenses/` — model and third-party license files
   * `readme_assets/` — flow diagrams, screenshots, and flash-configuration guides
   * `src/` — helper scripts, notebooks, or tooling used to build or deploy the project

Other files and folders at the project root are allowed. Look at existing projects (for example [Yolov8nPersonDetection](Yolov8nPersonDetection), [ArcFace](ArcFace), [MovementTypeDetectionDeploy](MovementTypeDetectionDeploy), or [RadarEntranceCounter](RadarEntranceCounter)) as references for structure and README content.

Choose a **project folder name** that is safe for a local folder name and a Git branch: letters, digits, `.`, `_`, and `-` are allowed; it must start and end with a letter or digit; spaces are not allowed (for example `ArcFace`, `Yolov8nPose`, or `EfficientNetV2-S`). Check existing project names and pick one that is not already in use.

---

### 📋 Step 2 — Prepare `metadata.json`

Choose one of the following options:

1. **Guided (recommended)** — when you run the PR tool (Step 4), it walks you through metadata collection interactively and writes `metadata.json` for you.
2. **Manual** — fill in `metadata.json` yourself using [`_METADATA_TEMPLATE/metadata.json`](_METADATA_TEMPLATE/metadata.json) as a reference for the required fields and structure. The PR tool will validate your file when you run it.

All metadata fields are required except `metrics`, which is optional but recommended for model deployment projects.

---

### 🛠️ Step 3 — Get the PR tool

Get the pull request automation tool (PR tool) from the [deepcraft-studio-accelerators-pr-tool](https://github.com/Infineon/deepcraft-studio-accelerators-pr-tool) repository.

**Before submitting any project, make sure you are using the latest version of the PR tool** — if you already have a copy, update it first (for example, run `git pull` in an existing clone, or download/clone the repository again).

You can obtain the tool in one of the following ways:

**Option A — Download as ZIP**

1. Open [deepcraft-studio-accelerators-pr-tool](https://github.com/Infineon/deepcraft-studio-accelerators-pr-tool) on GitHub.
2. Click **Code → Download ZIP**, extract the archive, and use the `pr_tool` folder inside.

**Option B — Clone the repository**

```bash
git clone https://github.com/Infineon/deepcraft-studio-accelerators-pr-tool.git
cd deepcraft-studio-accelerators-pr-tool\pr_tool
```

**Option C — Clone only the `pr_tool` folder (sparse checkout)**

```bash
git clone --filter=blob:none --sparse https://github.com/Infineon/deepcraft-studio-accelerators-pr-tool.git
cd deepcraft-studio-accelerators-pr-tool
git sparse-checkout set pr_tool
cd pr_tool
```

---

### 🚀 Step 4 — Run the PR tool and submit

From the `pr_tool` folder, run:

```bash
python .\pr_tool.py --repo model-zoo-psoc --path <project-path>
```

Replace `<project-path>` with the root path of your model deployment project. For more information, review the tool's [README.md](https://github.com/Infineon/deepcraft-studio-accelerators-pr-tool/blob/main/pr_tool/README.md).

What happens next:

1. You will be prompted to authenticate with your **GitHub account** (required).
2. The tool forks this repository and prepares the pull request.
3. Your browser opens the pull request page — add the relevant details to aid the review process, then submit.

**Updating an existing pull request** — every time you change your project, re-run the same command above. Your existing pull request will be updated automatically.

## 🏢 Partners

If you are a partner or potential partner looking to bring in your Infineon content, please reach out to us alongside the pull request to coordinate publication and branding.

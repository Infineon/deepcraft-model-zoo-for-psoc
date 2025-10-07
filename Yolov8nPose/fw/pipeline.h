/****************************************************************************/
/* Copyright (c) 2025 embedUR systems, Inc.    All rights reserved     */
/****************************************************************************/

#ifndef YOLOV8N_POSE_ESTIMATION_H
#define YOLOV8N_POSE_ESTIMATION_H

#ifdef __cplusplus
extern "C" {
#endif

#include <stdint.h>

/*******************************************************************************
* MACROS
*******************************************************************************/
#define PSRAM_ADDRESS_BOXES      0x64D00000
#define PSRAM_ADDRESS_DETECTIONS 0x64D10000

#ifndef DISPLAY_H
#define DISPLAY_H                480U
#endif
#ifndef DISPLAY_W
#define DISPLAY_W                832U
#endif

#define INPUT_WIDTH              320
#define INPUT_HEIGHT             320
#define INPUT_CHANNELS           3
#define INPUT_SCALE              0.00392157f
#define INPUT_ZERO_POINT         -128

#define OUTPUT_SCALE             0.005615f
#define OUTPUT_ZERO_POINT        -117

#define NPU_PRIORITY             3
#define BATCH_SIZE               1

#define NUM_DETECTIONS           2100
#define NUM_FEATURES             56
#define NUM_KEYPOINTS            17

#define IOU_THRESH               0.5f
#define CONF_THRESH              0.65f
#define KEYPOINT_CONF_THRESH     0.5f

#define LABEL_SIZE               32
#define X_OFFSET                 16
#define Y_OFFSET                 32

#define CIRCLE_RADIUS            3
#define MAX_BOXES                1000

#define PIPELINE_OK              1
#define PIPELINE_ERROR          -1

#ifndef max
    #define max(a, b) ((a) > (b) ? (a) : (b))
    #define min(a, b) ((a) < (b) ? (a) : (b))
#endif

/*******************************************************************************
* Structures
*******************************************************************************/
#ifndef STRUCTS_H
#define STRUCTS_H

/* Box structure */ 
typedef struct {
    int x1;
    int y1;
    int x2;
    int y2;
} Box;

/* Keypoint structure */ 
typedef struct {
    float x;
    float y;
    float confidence;
} Keypoint;

/* Detection structure */ 
typedef struct {
    int x1;
    int y1;
    int x2;
    int y2;
    float score;
    Keypoint keypoints[NUM_KEYPOINTS];
} Detection;

#endif

/*******************************************************************************
* Function Name: getData
****************************************************************************//**
*
* Retrieves input data required for the ML pipeline. This function is
* responsible for acquiring sensor, image, or other raw data sources that will
* be used in the subsequent processing stages.
*
* \param None
*
* \return None
*
*******************************************************************************/
void getData(void);

/*******************************************************************************
* Function Name: ml_pipeline_model_init
****************************************************************************//**
*
* Initializes the ML model used in the pipeline. This includes loading the
* model, allocating memory buffers, and preparing the runtime environment
* required for inference.
*
* \param None
*
* \return None
*
*******************************************************************************/
void ml_pipeline_model_init(void);

/*******************************************************************************
* Function Name: ml_pipeline_preprocess
****************************************************************************//**
*
* Performs preprocessing on the raw input data. This may include resizing,
* normalization, quantization, or other transformations required by the ML
* model.
*
* \param None
*
* \return None
*
*******************************************************************************/
void ml_pipeline_preprocess(void);

/*******************************************************************************
* Function Name: ml_pipeline_inference
****************************************************************************//**
*
* Executes the ML inference step. This function takes preprocessed input data,
* feeds it into the ML model, and computes the outputs.
*
* \param None
*
* \return None
*
*******************************************************************************/
void ml_pipeline_inference(void);

/*******************************************************************************
* Function Name: ml_pipeline_post_process
****************************************************************************//**
*
* Handles post-processing of the ML model outputs. This may include decoding
* predictions, applying thresholds, formatting results, or preparing data for
* downstream usage (e.g., display or control).
*
* \param None
*
* \return None
*
*******************************************************************************/
void ml_pipeline_post_process(void);

#if defined(__cplusplus)
}
#endif /* __cplusplus */

#endif 
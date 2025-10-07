/****************************************************************************/
/* Copyright (c) 2025 embedUR systems, Inc.    All rights reserved     */
/****************************************************************************/

#ifndef MOVENET_LIGHTNING_POSE_ESTIMATION_H
#define MOVENET_LIGHTNING_POSE_ESTIMATION_H

#ifdef __cplusplus
extern "C" {
#endif

#include <stdint.h>

/*******************************************************************************
* MACROS
*******************************************************************************/
#define PSRAM_MODEL_INPUT         0x64500000
#define PSRAM_ADDRESS_OUTPUT      0x64C00000

#define INPUT_WIDTH               256
#define INPUT_HEIGHT              256

#define HEATMAP_WIDTH             64
#define HEATMAP_HEIGHT            64

#define NPU_PRIORITY              3

#ifndef DISPLAY_H
#define DISPLAY_H                 480U
#endif
#ifndef DISPLAY_W
#define DISPLAY_W                 832U
#endif

#define NUM_KEYPOINTS             17
#define CONF_THRESHOLD            0.2f

#define MAX_CONNECTIONS           4
#define MAX_TOTAL_CONNECTIONS     34

#define CIRCLE_RADIUS             3

#define PIPELINE_OK               1
#define PIPELINE_ERROR           -1

#ifndef max
    #define max(a, b) ((a) > (b) ? (a) : (b))
    #define min(a, b) ((a) < (b) ? (a) : (b))
#endif

/*******************************************************************************
* Structures
*******************************************************************************/
typedef struct {
    const char* label;
    int connections[MAX_CONNECTIONS];
    int num_connections;
} KeypointDef;

typedef struct {
    int x; 
    int y;
    float score;
} Keypoint;

typedef struct {
    int from;
    int to;
} Connection;

/*******************************************************************************
*Global Declaration
*******************************************************************************/

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
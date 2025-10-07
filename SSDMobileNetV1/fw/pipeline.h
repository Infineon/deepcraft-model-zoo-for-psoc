/****************************************************************************/
/* Copyright (c) 2025 embedUR systems, Inc.    All rights reserved     */
/****************************************************************************/

#ifndef SSD_MOBILENET_V1_PERSON_DETECTION_H
#define SSD_MOBILENET_V1_PERSON_DETECTION_H

#ifdef __cplusplus
extern "C" {
#endif

#include <stdint.h>

/*******************************************************************************
* MACROS
*******************************************************************************/
#define INPUT_WIDTH              192
#define INPUT_HEIGHT             192

#define NPU_PRIORITY             3

#ifndef DISPLAY_H
#define DISPLAY_H                480U
#endif
#ifndef DISPLAY_W
#define DISPLAY_W                832U
#endif

#define MAX_BOXES                2268
#define MAX_COLS                 6

#define X_IDX                    0
#define Y_IDX                    1
#define W_IDX                    2
#define H_IDX                    3
#define CONF_IDX                 4
#define CLS_IDX                  5

#define LABEL_OFFSET_X           16
#define LABEL_OFFSET_Y           32

#define CONF_THRESHOLD           70.0f
#define NMS_THRESHHOLD           0.4f
#define CHANNEL                  3

#define PIPELINE_OK              1
#define PIPELINE_ERROR          -1

#ifndef max
    #define max(a, b) ((a) > (b) ? (a) : (b))
    #define min(a, b) ((a) < (b) ? (a) : (b))
#endif

/*******************************************************************************
* Structures
*******************************************************************************/
typedef struct
{
    float x, y, w, h;
    float score;
}Box;

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
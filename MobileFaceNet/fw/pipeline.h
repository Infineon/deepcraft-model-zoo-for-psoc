/****************************************************************************/
/* Copyright (c) 2025 embedUR systems, Inc.    All rights reserved     */
/****************************************************************************/

#ifndef MOBILEFACENET_FACE_RECOGNITION_H
#define MOBILEFACENET_FACE_RECOGNITION_H

#ifdef __cplusplus
extern "C" {
#endif

#define STATIC_IMAGE

#include <stdint.h>
#include "usb_camera_task.h"

/*******************************************************************************
* MACROS
*******************************************************************************/
#define INPUT_WIDTH              112
#define INPUT_HEIGHT             112

#define NUM_STATIC_IMAGES        (3u)

#define OUTPUT_SCALE             0.0078125f

#define NPU_PRIORITY             3

#ifndef DISPLAY_H
#define DISPLAY_H                480U
#endif
#ifndef DISPLAY_W
#define DISPLAY_W                832U
#endif

#define EMBEDDING_SIZE           128

#define DISP_OFFSET              110
#define X_COORDINATE             10
#define MAX_NAME_LENGTH          100

#define SIMILARITY_THRESHOLD     0.96f
#define CHANNEL                  3

#define PIPELINE_OK              1
#define PIPELINE_ERROR          -1

#ifndef max
    #define max(a, b) ((a) > (b) ? (a) : (b))
    #define min(a, b) ((a) < (b) ? (a) : (b))
#endif

extern uint8_t static_display_image[NUM_STATIC_IMAGES][CAMERA_BUFFER_SIZE];

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
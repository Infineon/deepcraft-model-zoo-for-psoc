/****************************************************************************/
/* Copyright (c) 2025 embedUR systems, Inc.    All rights reserved          */
/****************************************************************************/

#ifndef HAND_LANDMARKS_POSE_ESTIMATION_H
#define HAND_LANDMARKS_POSE_ESTIMATION_H

#ifdef __cplusplus
extern "C" {
#endif

#include <stdint.h>

/*******************************************************************************
* MACROS
*******************************************************************************/
#ifndef DISPLAY_H
#define DISPLAY_H                480U
#endif
#ifndef DISPLAY_W
#define DISPLAY_W                832U
#endif

#define CAMERA_WIDTH            320
#define CAMERA_HEIGHT           240

#define IMAGE_WIDTH             320
#define IMAGE_HEIGHT            240
#define INPUT_WIDTH             256
#define INPUT_HEIGHT            256
#define MAX_LOST_FRAMES         3
#define EXPAND_FACTOR           1.5
#define MIN_HAND_AREA           1500
#define PADDING                 40

#define CONF_THRESHOLD          0.25
#define NUM_LANDMARKS           63
#define MAX_LANDMARKS           21
#define LANDMARK_SIZE           3
#define MIN_STABLE_FRAMES       2
#define BUFFER_SIZE             3
#define SMOOTHING_FACTOR        0.4

#define HAND_REGION_THICKNESS   3
#define LINE_THICKNESS          6
#define POINT_RADIUS            8
#define NUM_CONNECTIONS         20
#define CONF_X_IDX              10
#define CONF_Y_IDX              60
#define STATUS_X_IDX            10
#define STATUS_Y_IDX            30

#define PIPELINE_OK             1
#define PIPELINE_ERROR          -1
#define NPU_PRIORITY            3

#ifndef max
    #define max(a, b) ((a) > (b) ? (a) : (b))
    #define min(a, b) ((a) < (b) ? (a) : (b))
#endif
/*******************************************************************************
* Structures
*******************************************************************************/
typedef struct {
    float x;
    float y;
} Point;

typedef struct {
    int x;
    int y;
    int width;
    int height;
} HandRegion;

typedef struct {
    uint8_t h, s, v;
    uint8_t y, cr, cb;
} ColorSpaces;

typedef struct {
    HandRegion tracking_region;
    int detection_lost_frames;
    int has_tracking_region;
    Point landmark_buffer[BUFFER_SIZE][MAX_LANDMARKS];
    float confidence_buffer[BUFFER_SIZE];
    int stable_detection_count;
    int buffer_count;
    int has_previous_landmarks;
    Point previous_landmarks[MAX_LANDMARKS];
    uint8_t mask[IMAGE_HEIGHT][IMAGE_WIDTH];
    uint8_t temp_mask[IMAGE_HEIGHT][IMAGE_WIDTH];
} HandDetector;

typedef struct {
    int start_idx;
    int end_idx;
} Connections;

typedef struct {
    HandRegion hand_region;
    Point landmarks[MAX_LANDMARKS];
    int num_landmarks;
    float confidence;
} HandPose;

typedef struct { 
    uint8_t lh, ls, lv, uh, us, uv; 
} HSV_Ranges;

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

/*******************************************************************************
* Function Name: IMAGE_DrawRect
****************************************************************************//**
*
* Draws a rectangle on an image buffer with the specified color and coordinates.
* The rectangle is defined by its top-left (x0, y0) and bottom-right (x1, y1)
* corners. The color is specified using RGB components. The function ensures that
* drawing stays within the bounds of the target display or image buffer based on
* the provided width (lcd_w) and height (lcd_h).
*
* \param pdst     Pointer to the destination image buffer where the rectangle will be drawn.
* \param x0       X-coordinate of the top-left corner of the rectangle.
* \param y0       Y-coordinate of the top-left corner of the rectangle.
* \param x1       X-coordinate of the bottom-right corner of the rectangle.
* \param y1       Y-coordinate of the bottom-right corner of the rectangle.
* \param r        Red component of the rectangle color (0–255 or 0–31 depending on format).
* \param g        Green component of the rectangle color (0–255 or 0–63 depending on format).
* \param b        Blue component of the rectangle color (0–255 or 0–31 depending on format).
* \param lcd_w    Width of the display or image buffer in pixels.
* \param lcd_h    Height of the display or image buffer in pixels.
*
* \return None
*
*******************************************************************************/
void IMAGE_DrawRect(uint16_t *pdst, 
                    int16_t x0, int16_t y0, int16_t x1, int16_t y1,
                    uint16_t r, uint16_t g, uint16_t b, 
                    uint16_t lcd_w, uint16_t lcd_h);
                    
                    
#if defined(__cplusplus)
}
#endif

#endif 


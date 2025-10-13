/****************************************************************************/
/* Copyright (c) 2025 embedUR systems, Inc.    All rights reserved     */
/****************************************************************************/

#ifndef YOLOV8N_INSTANCE_SEGMENTATION_H
#define YOLOV8N_INSTANCE_SEGMENTATION_H

#define MULTIPLE_OUTPUT_TENSOR

#ifdef __cplusplus
extern "C" {
#endif

#include <stdint.h>

/*******************************************************************************
* MACROS
*******************************************************************************/
#define INPUT_WIDTH              256
#define INPUT_HEIGHT             256
#define CHANNEL                  3

#define NPU_PRIORITY             3

#ifndef DISPLAY_H
#define DISPLAY_H                480U
#endif
#ifndef DISPLAY_W
#define DISPLAY_W                832U
#endif

#define MAX_PEOPLE               100
#define MAX_ELEMENT              5
#define MAX_BOXES                1344

#define PROT_H                   64
#define PROT_W                   64
#define PROT_COEFF               32

#define CONF_START_IDX           4
#define CONF_END_IDX             83
#define COEFF_START_IDX          84
#define COEFF_END_IDX            115

#define BOX_X_IDX                0
#define BOX_Y_IDX                1
#define BOX_W_IDX                2
#define BOX_H_IDX                3

#define LABEL_OFFSET_X           16
#define LABEL_OFFSET_Y           32

#define CONF_THRESHHOLD          0.5f
#define NMS_THRESHHOLD           0.4f
#define MASK_THRESHHOLD          0.5f

#define KERNAL_H                 3
#define KERNAL_W                 3

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
    int class_id;
    char* class_name;
    int color;
    float coefficients[PROT_COEFF];
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
#endif /* __cplusplus */

#endif 
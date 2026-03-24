/*
 * radar_processing.h
 *
 * Standalone DSP library — no hardware, no RTOS, no MQTT.
 * Extracted verbatim from the original processing_task() body.
 */

#ifndef RADAR_PROCESSING_H
#define RADAR_PROCESSING_H

#include <stdbool.h>
#include "arm_math.h"
#include "config.h"

#ifndef M_PI
#define M_PI 3.14159265358979323846f
#endif

/* Constants matching originals exactly */
#define RP_LIGHT_SPEED_M_S          299792458.0f
#define RP_CENTER_FREQ_HZ           60750000000.0f
#define RP_CHIRP_REPETITION_TIME_S  0.000501488f
#define RP_WAVELENGTH_M             (RP_LIGHT_SPEED_M_S / RP_CENTER_FREQ_HZ)
#define RP_BANDWIDTH_HZ             ((float32_t)(XENSIV_BGT60TRXX_CONF_END_FREQ_HZ - XENSIV_BGT60TRXX_CONF_START_FREQ_HZ))
#define RP_PSD_THRESHOLD            30.0f
#define RP_ALPHA                    0.2f
#define RP_VELOCITY_BUFFER_SIZE     3
#define RP_MIN_VELOCITY_M_S         0.1f
#define RP_MIN_RANGE_BIN            3
#define RP_COOLDOWN_FRAMES          10   /* ~5 sec at typical frame rate; prevents re-trigger */

/* Context — allocate once, pass to every call */
typedef struct {
    arm_rfft_fast_instance_f32  range_fft;
    arm_cfft_instance_f32       doppler_fft;
    int                         active_doppler_fft_len;

    float32_t range_window  [XENSIV_BGT60TRXX_CONF_NUM_SAMPLES_PER_CHIRP];
    float32_t doppler_window[64];

    float32_t distance_smoothed;
    bool      first_frame;

    float32_t velocity_buf[RP_VELOCITY_BUFFER_SIZE];
    int       vel_buf_idx;
    int       vel_buf_count;
    int       cooldown_frames;   /* frames to skip after an event fires */
} radar_processing_ctx_t;

/* Output populated by radar_processing_run() */
typedef struct {
    bool      event_valid;
    float32_t velocity_m_s;
    float32_t distance_m;
    int       in;
    int       out;
} radar_processing_output_t;

/* Initialise FFT + windows. Call once before first radar_processing_run(). */
int  radar_processing_init(radar_processing_ctx_t *ctx);

/* Run full 6-stage DSP pipeline on one float32 frame. */
void radar_processing_run(radar_processing_ctx_t    *ctx,
                          float32_t                 *frame_data,
                          radar_processing_output_t *output);

#endif /* RADAR_PROCESSING_H */

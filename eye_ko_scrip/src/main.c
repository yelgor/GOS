#include "stm32f4xx_hal.h"
#include <math.h>

#define MIC_COUNT 4
#define FRAME 1024

ADC_HandleTypeDef hadc1;
DMA_HandleTypeDef hdma_adc1;
UART_HandleTypeDef huart2;

uint16_t adc_buf[MIC_COUNT * FRAME];

typedef struct __attribute__((packed)) {
    uint32_t timestamp_us;
    float rms[MIC_COUNT];
    float energy_low[MIC_COUNT];
    float energy_mid[MIC_COUNT];
    float energy_high[MIC_COUNT];
    float delays[MIC_COUNT];
    uint16_t raw[MIC_COUNT][FRAME];
} packet_t;

uint32_t micros(void);

float calc_rms(const uint16_t *x, int n) {
    float s = 0;
    for (int i = 0; i < n; i++) {
        float v = (float)x[i] - 2048.0f;
        s += v*v;
    }
    return sqrtf(s / n);
}

float band_energy(const uint16_t *x, int n, float f1, float f2, float fs) {
    float re = 0, im = 0;
    float w = 2.0f * 3.1415926f * ((f1+f2)*0.5f) / fs;
    for (int i = 0; i < n; i++) {
        float v = (float)x[i] - 2048.0f;
        re += v * cosf(w*i);
        im += v * sinf(w*i);
    }
    return re*re + im*im;
}

float cross_corr_delay(const uint16_t *a, const uint16_t *b, int n) {
    float best = -1e9;
    int best_k = 0;
    for (int k = -50; k <= 50; k++) {
        float s = 0;
        for (int i = 0; i < n; i++) {
            int j = i + k;
            if (j >= 0 && j < n)
                s += ((float)a[i]-2048.0f)*((float)b[j]-2048.0f);
        }
        if (s > best) {
            best = s;
            best_k = k;
        }
    }
    return best_k / 48000.0f;
}

int main(void) {
    HAL_Init();
    SystemClock_Config();
    MX_DMA_Init();
    MX_ADC1_Init();
    MX_USART2_UART_Init();

    HAL_ADC_Start_DMA(&hadc1, (uint32_t*)adc_buf, MIC_COUNT * FRAME);

    while (1) {
        packet_t p;

        p.timestamp_us = micros();

        for (int m = 0; m < MIC_COUNT; m++) {
            const uint16_t *ch = &adc_buf[m * FRAME];

            p.rms[m] = calc_rms(ch, FRAME);

            p.energy_low[m]  = band_energy(ch, FRAME,   0,  300, 48000);
            p.energy_mid[m]  = band_energy(ch, FRAME, 300, 3000, 48000);
            p.energy_high[m] = band_energy(ch, FRAME, 3000, 8000, 48000);

            for (int i = 0; i < FRAME; i++)
                p.raw[m][i] = ch[i];
        }

        for (int m = 0; m < MIC_COUNT; m++)
            p.delays[m] = cross_corr_delay(
                &adc_buf[0 * FRAME],
                &adc_buf[m * FRAME],
                FRAME
            );

        HAL_UART_Transmit(&huart2, (uint8_t*)&p, sizeof(p), HAL_MAX_DELAY);
    }
}

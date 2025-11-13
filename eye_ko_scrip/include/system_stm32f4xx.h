#ifndef SYSTEM_STM32F4XX_H
#define SYSTEM_STM32F4XX_H

#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

extern uint32_t SystemCoreClock;

void SystemInit(void);
void SystemCoreClockUpdate(void);

#ifdef __cplusplus
}
#endif

#endif /* SYSTEM_STM32F4XX_H */

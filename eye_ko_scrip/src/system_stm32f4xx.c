#include "system_stm32f4xx.h"
#include "stm32f4xx.h"

uint32_t SystemCoreClock = 16000000U;

void SystemInit(void) {
    RCC->CR |= RCC_CR_HSION;
    while (!(RCC->CR & RCC_CR_HSIRDY)) {}

    RCC->CFGR = 0x00000000;
    RCC->PLLCFGR = 0x24003010;
    RCC->CR &= ~(RCC_CR_PLLON);
    RCC->CIR = 0x00000000;

    SCB->ICSR = 0;
}

void SystemCoreClockUpdate(void) {
    SystemCoreClock = 16000000U;
}

/* startup_stm32f411xe.s */
/* --- Minimal Cortex-M4 startup for STM32F411 --- */

.syntax unified
.cpu cortex-m4
.fpu fpv4-sp-d16
.thumb

/* -------------------------------------------------------------------------- */
/* Вектор переривань                                                          */
/* -------------------------------------------------------------------------- */
.section .isr_vector, "a", %progbits
.type g_pfnVectors, %object
.size g_pfnVectors, .-g_pfnVectors

g_pfnVectors:
  .word _estack             /* Початок стека (з лінкеру) */
  .word Reset_Handler       /* 1: Reset */
  .word NMI_Handler         /* 2: NMI */
  .word HardFault_Handler   /* 3: HardFault */
  .word Default_Handler     /* 4: MemManage */
  .word Default_Handler     /* 5: BusFault */
  .word Default_Handler     /* 6: UsageFault */
  .word 0                   /* 7: Reserved */
  .word 0                   /* 8: Reserved */
  .word 0                   /* 9: Reserved */
  .word 0                   /* 10: Reserved */
  .word Default_Handler     /* 11: SVC */
  .word Default_Handler     /* 12: DebugMon */
  .word 0                   /* 13: Reserved */
  .word Default_Handler     /* 14: PendSV */
  .word Default_Handler     /* 15: SysTick */
  /* --- решта переривань MCU можна додавати нижче при потребі --- */

/* -------------------------------------------------------------------------- */
/* Reset_Handler                                                              */
/* -------------------------------------------------------------------------- */
.section .text.Reset_Handler, "ax", %progbits
.thumb_func
.global Reset_Handler
.type Reset_Handler, %function

Reset_Handler:
  /* --- Ініціалізація секції .data (копіювання з Flash у RAM) --- */
  ldr r0, =_sdata
  ldr r1, =_edata
  ldr r2, =_sidata
1:
  cmp r0, r1
  bcc 2f
  b   3f
2:
  ldr r3, [r2], #4
  str r3, [r0], #4
  b   1b
3:

  /* --- Обнулення секції .bss --- */
  ldr r0, =_sbss
  ldr r1, =_ebss
  movs r2, #0
4:
  cmp r0, r1
  bcc 5f
  b   6f
5:
  str r2, [r0], #4
  add r0, r0, #4
  b   4b
6:

  /* --- Виклик SystemInit (ініціалізація тактування) --- */
  bl SystemInit

  /* --- Виклик main() --- */
  bl main

  /* --- Якщо main() повернеться — зависаємо --- */
inf_loop:
  b inf_loop

.size Reset_Handler, .-Reset_Handler


/* -------------------------------------------------------------------------- */
/* Обробники помилок/переривань                                               */
/* -------------------------------------------------------------------------- */
.thumb_func
Default_Handler:
  b .

.thumb_func
NMI_Handler:
  b .

.thumb_func
HardFault_Handler:
  b .
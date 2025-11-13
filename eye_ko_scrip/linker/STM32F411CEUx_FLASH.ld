/* STM32F411CEUx_FLASH.ld */
/* === Linker script for STM32F411CEU6 (Cortex-M4, 512KB Flash, 128KB RAM) === */

ENTRY(Reset_Handler)

/* --- Memory regions ------------------------------------------------------- */
MEMORY
{
  FLASH (rx)  : ORIGIN = 0x08000000, LENGTH = 512K
  RAM   (rwx) : ORIGIN = 0x20000000, LENGTH = 128K
}

/* --- Stack top ------------------------------------------------------------ */
_estack = ORIGIN(RAM) + LENGTH(RAM);

/* --- Sections ------------------------------------------------------------- */
SECTIONS
{
  /* --- Interrupt vector table --- */
  .isr_vector :
  {
    KEEP(*(.isr_vector))
  } > FLASH

  /* --- Program code and constants --- */
  .text :
  {
    *(.text*)               /* program code */
    *(.rodata*)             /* read-only data (const) */
    KEEP(*(.init))
    KEEP(*(.fini))
  } > FLASH

  /* --- ARM exception unwind info --- */
  .ARM.exidx :
  {
    *(.ARM.exidx*)
  } > FLASH

  /* --- Initialized data section (copied from Flash to RAM) --- */
  .data :
  {
    _sdata = .;             /* start of .data in RAM */
    *(.data*)
    _edata = .;             /* end of .data in RAM */
  } > RAM AT > FLASH

  /* --- Address in Flash from which to copy .data --- */
  _sidata = LOADADDR(.data);

  /* --- Uninitialized data (zero-filled) --- */
  .bss (NOLOAD) :
  {
    _sbss = .;              /* start of .bss */
    *(.bss*)
    *(COMMON)
    _ebss = .;              /* end of .bss */
  } > RAM

  /* --- Heap and stack allocation area (optional) --- */
  ._user_heap_stack (NOLOAD) :
  {
    . = ALIGN(8);
    _sheap = .;
    . = . + 0x1000;         /* heap = 4 KB */
    . = ALIGN(8);
    _eheap = .;

    . = ALIGN(8);
    _sstack = .;
    . = . + 0x1000;         /* stack = 4 KB (can be increased) */
    . = ALIGN(8);
    _estack_dummy = .;
  } > RAM
}

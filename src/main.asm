%include        'functions.asm'                        
 
SECTION .data
msg1    db      'Hello, world!', 0Ah
 
SECTION .text
global  _start
 
_start:
 
    mov     eax, msg1       
    call    sprint         

 
    call    quit            
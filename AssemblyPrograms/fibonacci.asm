; Program: Fibonacci Series
; Description: This program generates Fibonacci series up to n terms
; Input: Number of terms at memory location 9000H
; Output: Series stored starting from memory location 9001H

LDA #9000    ; Load number of terms
MOV C,A      ; Use C as counter
MVI A,#00    ; First number (0)
STA #9001    ; Store first number
MVI A,#01    ; Second number (1)
STA #9002    ; Store second number
LXI H,#9001  ; Load address of first number

; Start of loop (address: 8000H)
MOV A,M      ; Load first number
INX H        ; Move to second number
ADD M        ; Add second number
INX H        ; Move to next position
MOV M,A      ; Store sum
DCX H        ; Move back to second number
DCR C        ; Decrement counter
JNZ #8011    ; If counter not zero, continue loop
HLT          ; Halt the program

; Example usage:
; If memory location 9000H contains 08H (8 terms)
; After execution, memory locations 9001H-9008H will contain:
; 00H, 01H, 01H, 02H, 03H, 05H, 08H, 0DH (Fibonacci series) 

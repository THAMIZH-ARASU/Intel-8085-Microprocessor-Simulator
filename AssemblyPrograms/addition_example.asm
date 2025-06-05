; Program: Addition of two numbers
; Description: This program adds two numbers and stores the result
; Input: Two numbers (stored in memory locations 9000H and 9001H)
; Output: Sum stored in memory location 9002H

MVI A,#00    ; Initialize A register to 0
LDA #9000    ; Load first number from memory location 9000H
MOV B,A      ; Move first number to B register
LDA #9001    ; Load second number from memory location 9001H
ADD B        ; Add B to A (A = A + B)
STA #9002    ; Store result in memory location 9002H
HLT          ; Halt the program

; Example usage:
; If memory location 9000H contains 25H and 9001H contains 15H
; After execution, memory location 9002H will contain 3AH (25H + 15H = 3AH)

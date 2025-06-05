; Program: Subtraction of two numbers
; Description: This program subtracts second number from first number and stores the result
; Input: Two numbers (stored in memory locations 9000H and 9001H)
; Output: Difference stored in memory location 9002H

MVI A,#00    ; Initialize A register to 0
LDA #9000    ; Load first number from memory location 9000H
MOV B,A      ; Move first number to B register
LDA #9001    ; Load second number from memory location 9001H
SUB B        ; Subtract B from A (A = A - B)
STA #9002    ; Store result in memory location 9002H
HLT          ; Halt the program

; Example usage:
; If memory location 9000H contains 15H and 9001H contains 25H
; After execution, memory location 9002H will contain 10H (25H - 15H = 10H)
; Note: If result is negative, the carry flag will be set 

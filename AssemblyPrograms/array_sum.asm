; Program: Array Sum
; Description: This program calculates the sum of an array of numbers
; Input: Array size at 9000H, Array elements starting from 9001H
; Output: Sum stored in memory location 9100H


MVI A,#00    ; Initialize A register to 0
STA #9100    ; Initialize sum to 0
LDA #9000    ; Load array size
MOV C,A      ; Use C as counter
LXI H,#9001  ; Load starting address of array in HL pair

; Start of loop (address: 8000H)
MOV A,M      ; Load array element
PUSH H       ; Save array address
LXI H,#9100  ; Load address of sum
ADD M        ; Add current element to sum
MOV M,A      ; Store updated sum
POP H        ; Restore array address
INX H        ; Move to next array element
DCR C        ; Decrement counter
JNZ #800C    ; If counter not zero, continue loop
HLT          ; Halt the program

; Example usage:
; If memory location 9000H contains 05H (array size)
; And locations 9001H-9005H contain: 10H, 20H, 30H, 40H, 50H
; After execution, memory location 9100H will contain F0H (sum of all elements) 

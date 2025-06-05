; Program: Multiplication of two numbers using repeated addition
; Description: This program multiplies two numbers by adding the first number to itself
;              the number of times specified by the second number
; Input: Two numbers (stored in memory locations 9000H and 9001H)
; Output: Product stored in memory location 9002H

MVI A,#00    ; Initialize A register to 0 (8000)
LDA #9000    ; Load first number (multiplicand) from memory location 9000H (8002)
MOV B,A      ; Move multiplicand to B register (8005)
LDA #9001    ; Load second number (multiplier) from memory location 9001H (8006)
MOV C,A      ; Move multiplier to C register (8009)
MVI A,#00    ; Initialize A register to 0 (800A)

ADD B        ; Add multiplicand to result (800C)
DCR C        ; Decrement multiplier counter (800D)
JNZ #800C    ; If counter is not zero, jump back to ADD instruction (800E)
STA #9002    ; Store final result in memory location 9002H (8011)
HLT          ; Halt the program (8014)

; Memory Map:
; 8000: MVI A,#00 (2 bytes)
; 8002: LDA #9000 (3 bytes)
; 8005: MOV B,A (1 byte)
; 8006: LDA #9001 (3 bytes)
; 8009: MOV C,A (1 byte)
; 800A: MVI A,#00 (2 bytes)
; 800C: ADD B (1 byte)
; 800D: DCR C (1 byte)
; 800E: JNZ #800C (3 bytes)
; 8011: STA #9002 (3 bytes)
; 8014: HLT (1 byte)

; Example usage:
; If memory location 9000H contains 05H and 9001H contains 03H
; After execution, memory location 9002H will contain 0FH (05H * 03H = 0FH)
; The program adds 05H to itself 3 times: 05H + 05H + 05H = 0FH 
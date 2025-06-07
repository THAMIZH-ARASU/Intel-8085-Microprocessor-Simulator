; Program: Factorial Calculation
; Description: This program calculates factorial of a number using addition-based multiplication
; Input: Number at memory location 9000H
; Output: Factorial stored in memory location 9001H

; Memory Map:
; 8000: LDA #9000 (3 bytes)
; 8003: MOV D,A (1 byte)    ; Store original number in D
; 8004: MVI A,#01 (2 bytes)
; 8006: MOV C,A (1 byte)    ; Initialize result to 1

; Start of multiplication loop (8007)
; 8007: MOV A,D (1 byte)    ; Load original number
; 8008: MOV B,A (1 byte)    ; Use B as counter
; 8009: MVI E,#00 (2 bytes) ; Initialize sum

; Addition loop for multiplication (800B)
; 800B: MOV A,E (1 byte)
; 800C: ADD C (1 byte)      ; Add current result
; 800D: MOV E,A (1 byte)
; 800E: DCR B (1 byte)
; 800F: JNZ #800B (3 bytes)

; End of multiplication (8012)
; 8012: MOV A,E (1 byte)
; 8013: MOV C,A (1 byte)    ; Store new result
; 8014: MOV A,D (1 byte)    ; Load original number
; 8015: DCR A (1 byte)
; 8016: MOV D,A (1 byte)    ; Decrement original number
; 8017: JNZ #8007 (3 bytes)

; Store result (801A)
; 801A: MOV A,C (1 byte)
; 801B: STA #9001 (3 bytes)
; 801E: HLT (1 byte)

LDA #9000    ; Load the number
MOV D,A      ; Store original number in D
MVI A,#01    ; Initialize result to 1
MOV C,A      ; Store result in C

; Start of multiplication loop
MOV A,D      ; Load original number
MOV B,A      ; Use B as counter for multiplication
MVI E,#00    ; Initialize sum to 0

; Addition loop for multiplication
MOV A,E      ; Load sum
ADD C        ; Add current result
MOV E,A      ; Store new sum
DCR B        ; Decrement counter
JNZ #800B    ; If counter not zero, continue addition loop

MOV A,E      ; Load multiplication result
MOV C,A      ; Store new result in C
MOV A,D      ; Load original number
DCR A        ; Decrement for next factorial iteration
MOV D,A      ; Store decremented number
JNZ #8007    ; If number not zero, continue factorial loop

MOV A,C      ; Load final result
STA #9001    ; Store factorial
HLT          ; Halt the program

; Example usage:
; If memory location 9000H contains 05H
; After execution, memory location 9001H will contain 78H (5! = 120 decimal)
; Note: This program handles small numbers only due to 8-bit limitations 

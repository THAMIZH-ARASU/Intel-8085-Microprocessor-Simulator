; Program: Divide 20 by 4 using repeated subtraction
; Memory map with correct instruction sizes:
; 8000: MVI A,#14    ; 2 bytes - Dividend (20 in decimal)
; 8002: MVI B,#04    ; 2 bytes - Divisor (4 in decimal)
; 8004: MVI C,#00    ; 2 bytes - Quotient counter
; 8006: CMP B        ; 1 byte  - Compare A with B
; 8007: JC #800F     ; 3 bytes - If A < B, jump to end
; 800A: SUB B        ; 1 byte  - Subtract B from A
; 800B: INR C        ; 1 byte  - Increment quotient
; 800C: JMP #8006    ; 3 bytes - Repeat subtraction
; 800F: MOV A,C      ; 1 byte  - Move quotient to A
; 8010: STA #9000    ; 3 bytes - Store result
; 8013: HLT          ; 1 byte  - Halt

MVI A,#14    ; Dividend (20 in decimal)
MVI B,#04    ; Divisor (4 in decimal)
MVI C,#00    ; Quotient counter
CMP B        ; Compare A with B
JC #800F     ; If A < B, jump to end
SUB B        ; Subtract B from A
INR C        ; Increment quotient
JMP #8006    ; Repeat subtraction
MOV A,C      ; Move quotient to A
STA #9000    ; Store result
HLT          ; Halt
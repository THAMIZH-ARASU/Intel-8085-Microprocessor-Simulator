; Program: String Length Counter
; Description: This program calculates the length of a null-terminated string
; Input: String starting at memory location 9000H (terminated with 00H)
; Output: Length stored in memory location 9100H

MVI A,#00    ; Initialize length counter
MOV B,A      ; Store in B register
LXI H,#9000  ; Load starting address of string

; Start of loop (address: 8000H)
MOV A,M      ; Load character
CPI #00      ; Compare with null terminator
JZ #8010     ; If zero, string ended
INR B        ; Increment length counter
INX H        ; Move to next character
JMP #8006    ; Continue loop

; End of string found (address: 8010H)
MOV A,B      ; Load final length
STA #9100    ; Store length
HLT          ; Halt the program

; Example usage:
; If memory locations 9000H-9004H contain: 48H, 45H, 4CH, 4CH, 00H ("HELL" + null)
; After execution, memory location 9100H will contain 04H (length = 4) 

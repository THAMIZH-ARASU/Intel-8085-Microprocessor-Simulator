; Program: Bubble Sort
; Description: This program sorts an array of numbers in ascending order using bubble sort
; Input: Array size at 9000H, array elements starting at 9001H
; Output: Sorted array at same locations

; Start (address: 8000H)
LDA #9000    ; Load array size
DCR A        ; Decrement for loop counter
MOV C,A      ; Store outer loop counter

; Outer loop (address: 8005H)
MOV B,C      ; Initialize inner loop counter
LXI H,#9001  ; Point to start of array

; Inner loop (address: 8009H)
MOV A,M      ; Load first number
INX H        ; Point to next number
CMP M        ; Compare with next number
JC #8014     ; If first < second, skip swap
MOV D,M      ; Load second number
MOV M,A      ; Store first number
DCX H        ; Point back to first position
MOV M,D      ; Store second number
INX H        ; Point to next position

; Skip swap (address: 8014H)
DCR B        ; Decrement inner loop counter
JNZ #8009    ; Continue inner loop if not zero
DCR C        ; Decrement outer loop counter
JNZ #8005    ; Continue outer loop if not zero
HLT          ; Halt the program

; Example usage:
; If memory location 9000H contains 05H (array size = 5)
; And memory locations 9001H-9005H contain: 05H, 02H, 04H, 01H, 03H
; After execution, memory locations 9001H-9005H will contain: 01H, 02H, 03H, 04H, 05H 


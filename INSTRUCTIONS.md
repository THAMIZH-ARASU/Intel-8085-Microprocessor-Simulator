# 📘 **Intel 8085 Instruction Set Reference**

---

# 🧠 **Table of Contents**
- [Data Transfer Instructions](#data-transfer-instructions)
- [Arithmetic Instructions](#arithmetic-instructions)
- [Logical Instructions](#logical-instructions)
- [Branch Instructions](#branch-instructions)
- [Stack Operations](#stack-operations)
- [Control Instructions](#control-instructions)
- [Special Instructions](#special-instructions)

---

# <a name="data-transfer-instructions"></a>## 🚚 **Data Transfer Instructions**

### ### 1. **MOV** — Move Data Between Registers/Memory
**Syntax:**
```assembly
MOV destination, source
```
**Description:** Copies the contents of the source register/memory to the destination register/memory.

| Example         | Description                        |
|----------------|------------------------------------|
| `MOV A, B`     | Copy contents of B to A            |
| `MOV M, A`     | Store A into memory at (HL)        |

---

### 2. **MVI** — Move Immediate Data
**Syntax:**
```assembly
MVI register, data8
MVI M, data8
```
**Description:** Loads an 8-bit immediate value into a register or memory.

| Example         | Description                        |
|----------------|------------------------------------|
| `MVI A, #1F`   | Load 1F (hex) into A               |
| `MVI M, #05`   | Store 05 (hex) at memory (HL)      |

---

### 3. **LXI** — Load Register Pair Immediate
**Syntax:**
```assembly
LXI rp, data16
```
**Description:** Loads a 16-bit immediate value into a register pair (B, D, H, or SP).

| Example         | Description                        |
|----------------|------------------------------------|
| `LXI H, #9000` | HL = 9000H                         |
| `LXI SP, #FF00`| SP = FF00H                         |

---

### 4. **LDA/STA** — Load/Store Accumulator Direct
**Syntax:**
```assembly
LDA address16
STA address16
```
**Description:**
- `LDA`: Loads accumulator from memory address.
- `STA`: Stores accumulator to memory address.

| Example         | Description                        |
|----------------|------------------------------------|
| `LDA #9000`    | A = [9000H]                        |
| `STA #9002`    | [9002H] = A                        |

---

### 5. **LHLD/SHLD** — Load/Store HL Pair Direct
**Syntax:**
```assembly
LHLD address16
SHLD address16
```
**Description:**
- `LHLD`: Loads HL pair from two consecutive memory locations.
- `SHLD`: Stores HL pair to two consecutive memory locations.

| Example         | Description                        |
|----------------|------------------------------------|
| `LHLD #9000`   | HL = [9000H] + [9001H]             |
| `SHLD #9100`   | [9100H] = L, [9101H] = H           |

---

# <a name="arithmetic-instructions"></a>## ➕ **Arithmetic Instructions**

### 1. **ADD/ADI** — Add Register/Immediate to Accumulator
**Syntax:**
```assembly
ADD source
ADI data8
```
**Description:** Adds the source register/memory or immediate value to the accumulator (A).

| Example         | Description                        |
|----------------|------------------------------------|
| `ADD B`        | A = A + B                          |
| `ADD M`        | A = A + [HL]                       |
| `ADI #10`      | A = A + 10H                        |

---

### 2. **ADC** — Add with Carry
**Syntax:**
```assembly
ADC source
```
**Description:** Adds source and carry flag to accumulator.

| Example         | Description                        |
|----------------|------------------------------------|
| `ADC C`        | A = A + C + CY                     |

---

### 3. **SUB/SUI** — Subtract Register/Immediate from Accumulator
**Syntax:**
```assembly
SUB source
SUI data8
```
**Description:** Subtracts source register/memory or immediate value from accumulator.

| Example         | Description                        |
|----------------|------------------------------------|
| `SUB D`        | A = A - D                          |
| `SUI #05`      | A = A - 05H                        |

---

### 4. **SBB** — Subtract with Borrow
**Syntax:**
```assembly
SBB source
```
**Description:** Subtracts source and borrow (carry flag) from accumulator.

| Example         | Description                        |
|----------------|------------------------------------|
| `SBB E`        | A = A - E - CY                     |

---

### 5. **INR/DCR** — Increment/Decrement Register/Memory
**Syntax:**
```assembly
INR destination
DCR destination
```
**Description:** Increments or decrements the specified register or memory by 1.

| Example         | Description                        |
|----------------|------------------------------------|
| `INR B`        | B = B + 1                          |
| `DCR M`        | [HL] = [HL] - 1                    |

---

# <a name="logical-instructions"></a>## 🧩 **Logical Instructions**

### 1. **ANA** — Logical AND with Accumulator
**Syntax:**
```assembly
ANA source
```
**Description:** Logical AND between accumulator and source.

| Example         | Description                        |
|----------------|------------------------------------|
| `ANA H`        | A = A & H                          |

---

### 2. **ORA** — Logical OR with Accumulator
**Syntax:**
```assembly
ORA source
```
**Description:** Logical OR between accumulator and source.

| Example         | Description                        |
|----------------|------------------------------------|
| `ORA L`        | A = A | L                          |

---

### 3. **XRA** — Logical XOR with Accumulator
**Syntax:**
```assembly
XRA source
```
**Description:** Logical XOR between accumulator and source.

| Example         | Description                        |
|----------------|------------------------------------|
| `XRA M`        | A = A ^ [HL]                       |

---

### 4. **CMA** — Complement Accumulator
**Syntax:**
```assembly
CMA
```
**Description:** Complements (bitwise NOT) the accumulator.

| Example         | Description                        |
|----------------|------------------------------------|
| `CMA`          | A = ~A                             |

---

### 5. **CMP/CPI** — Compare Register/Immediate with Accumulator
**Syntax:**
```assembly
CMP source
CPI data8
```
**Description:** Compares source or immediate with accumulator (sets flags, does not change A).

| Example         | Description                        |
|----------------|------------------------------------|
| `CMP B`        | Compare B with A                   |
| `CPI #20`      | Compare 20H with A                 |

---

# <a name="branch-instructions"></a>## 🔀 **Branch Instructions**

### 1. **JMP** — Unconditional Jump
**Syntax:**
```assembly
JMP address16
```
**Description:** Sets PC to address.

| Example         | Description                        |
|----------------|------------------------------------|
| `JMP #8000`    | Jump to address 8000H              |

---

### 2. **JZ/JNZ/JC/JNC** — Conditional Jumps
**Syntax:**
```assembly
JZ address16   ; Jump if Zero flag set
JNZ address16  ; Jump if Zero flag not set
JC address16   ; Jump if Carry flag set
JNC address16  ; Jump if Carry flag not set
```
**Description:** Jumps to address if condition is met.

| Example         | Description                        |
|----------------|------------------------------------|
| `JZ #8010`     | Jump to 8010H if Zero flag is set  |
| `JNC #8020`    | Jump to 8020H if Carry not set     |

---

### 3. **CALL/RET** — Subroutine Call/Return
**Syntax:**
```assembly
CALL address16
RET
```
**Description:**
- `CALL`: Pushes PC to stack, jumps to address.
- `RET`: Pops address from stack to PC.

| Example         | Description                        |
|----------------|------------------------------------|
| `CALL #9000`   | Call subroutine at 9000H           |
| `RET`          | Return from subroutine             |

---

# <a name="stack-operations"></a>## 📚 **Stack Operations**

### 1. **PUSH/POP** — Stack Operations
**Syntax:**
```assembly
PUSH rp
POP rp
```
**Description:**
- `PUSH`: Pushes register pair onto stack.
- `POP`: Pops two bytes from stack into register pair.

| Example         | Description                        |
|----------------|------------------------------------|
| `PUSH B`       | Push BC onto stack                 |
| `POP H`        | Pop two bytes into HL              |

---

# <a name="control-instructions"></a>## 🕹️ **Control Instructions**

### 1. **HLT** — Halt
**Syntax:**
```assembly
HLT
```
**Description:** Halts program execution.

| Example         | Description                        |
|----------------|------------------------------------|
| `HLT`          | Stop execution                     |

---

### 2. **NOP** — No Operation
**Syntax:**
```assembly
NOP
```
**Description:** Does nothing (1 machine cycle).

| Example         | Description                        |
|----------------|------------------------------------|
| `NOP`          | No operation                       |

---

# <a name="special-instructions"></a>## 🛠️ **Special Instructions**

### 1. **DAA** — Decimal Adjust Accumulator
**Syntax:**
```assembly
DAA
```
**Description:** Adjusts A for BCD addition.

---

### 2. **STC/CMC** — Set/Complement Carry
**Syntax:**
```assembly
STC
CMC
```
**Description:**
- `STC`: Sets carry flag.
- `CMC`: Complements carry flag.

---

### 3. **EI/DI** — Enable/Disable Interrupts
**Syntax:**
```assembly
EI
DI
```
**Description:**
- `EI`: Enable interrupts.
- `DI`: Disable interrupts.

---

### 4. **RIM/SIM** — Read/Set Interrupt Mask
**Syntax:**
```assembly
RIM
SIM
```
**Description:**
- `RIM`: Read interrupt mask.
- `SIM`: Set interrupt mask.

---

### 5. **Rotate Instructions**
**Syntax:**
```assembly
RLC   ; Rotate accumulator left
RRC   ; Rotate accumulator right
RAL   ; Rotate accumulator left through carry
RAR   ; Rotate accumulator right through carry
```
**Description:** Rotates bits in accumulator (A) as described.

---

# 📝 **Usage Example: Addition of Two Numbers**
```assembly
MVI A, #05      ; Load 05H into A
MVI B, #03      ; Load 03H into B
ADD B           ; A = A + B (A = 08H)
STA #9000       ; Store result at 9000H
HLT             ; Halt
```

---

# 🏁 **End of Instruction Reference** 
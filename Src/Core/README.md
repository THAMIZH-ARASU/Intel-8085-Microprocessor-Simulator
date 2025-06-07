# Core Components Documentation

This directory contains the core components of the Intel 8085 Microprocessor Simulator.

## CPU Implementation (`CPU.py`)

### Register Architecture
- **8-bit Registers**:
  - Accumulator (A): Primary register for arithmetic and logical operations
  - General Purpose Registers (B, C, D, E, H, L): Used for data storage and manipulation
  - Register Pairs:
    - BC Pair: Used for 16-bit operations and as a counter
    - DE Pair: Used for 16-bit operations and as a data pointer
    - HL Pair: Used for 16-bit operations and as a memory pointer

- **16-bit Registers**:
  - Program Counter (PC): Points to the next instruction to be executed
  - Stack Pointer (SP): Points to the top of the stack

- **Status Flags**:
  - Sign (S): Set if result is negative (bit 7 is 1)
  - Zero (Z): Set if result is zero
  - Auxiliary Carry (AC): Set if carry from bit 3 to bit 4
  - Parity (P): Set if result has even number of 1s
  - Carry (C): Set if operation produces carry/borrow

### Instruction Set Implementation

#### Data Transfer Instructions
- **MOV r1, r2**: Move data between registers
- **MOV M, r**: Move register to memory
- **MOV r, M**: Move memory to register
- **MVI r, data**: Move immediate data to register
- **MVI M, data**: Move immediate data to memory
- **LXI rp, data16**: Load 16-bit immediate data to register pair
- **LDA addr**: Load accumulator from memory
- **STA addr**: Store accumulator to memory
- **LHLD addr**: Load HL pair from memory
- **SHLD addr**: Store HL pair to memory

#### Arithmetic Instructions
- **ADD r**: Add register to accumulator
- **ADD M**: Add memory to accumulator
- **ADI data**: Add immediate data to accumulator
- **ADC r**: Add register to accumulator with carry
- **ADC M**: Add memory to accumulator with carry
- **SUB r**: Subtract register from accumulator
- **SUB M**: Subtract memory from accumulator
- **SUI data**: Subtract immediate data from accumulator
- **SBB r**: Subtract register from accumulator with borrow
- **SBB M**: Subtract memory from accumulator with borrow
- **INR r**: Increment register
- **INR M**: Increment memory
- **DCR r**: Decrement register
- **DCR M**: Decrement memory

#### Logical Instructions
- **ANA r**: AND register with accumulator
- **ANA M**: AND memory with accumulator
- **ANI data**: AND immediate data with accumulator
- **ORA r**: OR register with accumulator
- **ORA M**: OR memory with accumulator
- **ORI data**: OR immediate data with accumulator
- **XRA r**: XOR register with accumulator
- **XRA M**: XOR memory with accumulator
- **XRI data**: XOR immediate data with accumulator
- **CMA**: Complement accumulator
- **CMC**: Complement carry flag
- **STC**: Set carry flag

#### Branch Instructions
- **JMP addr**: Unconditional jump
- **JZ addr**: Jump if zero
- **JNZ addr**: Jump if not zero
- **JC addr**: Jump if carry
- **JNC addr**: Jump if no carry
- **CALL addr**: Call subroutine
- **RET**: Return from subroutine

#### Stack Operations
- **PUSH rp**: Push register pair onto stack
- **POP rp**: Pop register pair from stack
- **PUSH PSW**: Push processor status word
- **POP PSW**: Pop processor status word

#### Other Instructions
- **HLT**: Halt processor
- **NOP**: No operation
- **RLC**: Rotate accumulator left
- **RRC**: Rotate accumulator right
- **RAL**: Rotate accumulator left through carry
- **RAR**: Rotate accumulator right through carry
- **DAA**: Decimal adjust accumulator

### Implementation Details
- Instruction decoding using opcode mapping
- Flag management for arithmetic and logical operations
- Memory-mapped I/O support
- Interrupt handling system
- Cycle-accurate timing simulation
- Stack management
- Register pair operations

## Memory Implementation (`Memory.py`)

### Memory Architecture
- 64KB (0x0000-0xFFFF) addressable space
- Byte-addressable memory
- Little-endian byte ordering for 16-bit operations

### Features
- Byte and word (16-bit) read/write operations
- Memory breakpoint support
- Memory write callback system
- Program loading functionality
- Memory access validation
- Memory visualization support

### Implementation Details
- Memory access validation
- Breakpoint tracking system
- Memory write notification system
- Program loading and execution
- Memory state persistence

## ALU Implementation (`ALU.py`)

### Arithmetic Operations
- 8-bit addition with carry
- 8-bit subtraction with borrow
- Increment/Decrement operations
- Decimal adjust operations

### Logical Operations
- AND operations
- OR operations
- XOR operations
- Complement operations
- Rotate operations

### Flag Management
- Sign flag calculation
- Zero flag calculation
- Auxiliary carry calculation
- Parity flag calculation
- Carry flag calculation

### Implementation Details
- Flag generation for all operations
- BCD arithmetic support
- Bit manipulation operations
- Extended arithmetic operations

## Future Enhancements

### CPU Enhancements
1. Support for undocumented instructions
2. Cycle-accurate timing implementation
3. Hardware interrupt simulation
4. DMA controller simulation
5. Extended instruction set support

### Memory Enhancements
1. Memory protection mechanisms
2. Memory-mapped I/O devices
3. Memory access patterns analysis
4. ROM/EEPROM simulation
5. Memory banking support

### ALU Enhancements
1. BCD arithmetic support
2. Decimal adjust operations
3. Bit manipulation instructions
4. Extended arithmetic operations
5. Floating-point operations simulation 
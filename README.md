# Intel 8085 Microprocessor Simulator

A Python-based simulator for the Intel 8085 microprocessor with a graphical user interface. This simulator allows you to write, assemble, and execute 8085 assembly code while visualizing the CPU state, memory contents, and program execution.

> **Note:** This project is currently under active development. Features and functionality may change as development progresses.

## Features

- Full 8085 instruction set support
- Real-time CPU state visualization
- Memory viewer and editor
- Assembly code editor with syntax highlighting
- Step-by-step execution
- Breakpoint support
- File I/O for assembly code
- Comprehensive logging

## Output Screenshots

The Interface Output:
<p align="center">
  <img src="Outputs/Interface.png" alt="Linear Regression Image">
</p>

The Terminal Log Output:
<p align="center">
  <img src="Outputs/TerminalLogs.png" alt="Linear Regression Image">
</p>

The simulator provides a visual interface with several key components:

1. **Code Editor**: Located at the top-left, where you can write and edit your assembly code
2. **Memory Viewer**: Shows the contents of memory locations in hexadecimal format
3. **Register Display**: Shows the current state of all CPU registers (A, B, C, D, E, H, L, SP, PC)
4. **Status Flags**: Displays the state of all CPU flags (S, Z, AC, P, C)
5. **Control Panel**: Contains buttons for Run, Step, Stop, and Reset operations
6. **Terminal**: Shows all kinds of log about the system in real time

To view the output:
1. Load or write your assembly code
2. Click "Assemble" to compile the code
3. Use the Run or Step buttons to execute the program
4. The Memory Viewer and Register Display will update in real-time

## Project Structure

```
Intel-8085-Microprocessor-Simulator
├── Src/
│   ├── __init__.py
│   ├── Core/
│   │   ├── __init__.py
│   │   ├── Memory.py
│   │   ├── ALU.py
│   │   ├── CPU.py
│   │   └── Assembler.py
│   ├── Interface/
│   │   ├── __init__.py
│   │   └── SimulatorGUI.py
│   └── Utils/
│       ├── __init__.py
│       └── Logger.py
├── AssemblyPrograms/
│   ├── addition_example.asm
│   ├── subtraction_example.asm
│   ├── multiplication_example.asm
│   ├── divide_example.asm
│   └── More...
├── run.py
└── 8085_simulator.log
```

## Requirements

- Python 3.6 or higher
- tkinter (usually comes with Python)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/THAMIZH-ARASU/Intel-8085-Microprocessor-Simulator.git
cd simple8085
```

2. Run the simulator:
```bash
python run.py
```

## Usage

1. Write your 8085 assembly code in the code editor
2. Click "Assemble" to convert the code to machine code
3. Use the following controls to execute your program:
   - Run: Execute the program continuously
   - Step: Execute one instruction at a time
   - Stop: Halt program execution
   - Reset: Reset the CPU to initial state
   - Load/Save: Load or save assembly code files

## Memory Editor

The memory editor allows you to:
- Read byte values from specific memory addresses
- Write byte values to specific memory addresses
- View memory contents in the memory viewer

## Status Flags

The simulator displays the following CPU status flags:
- S (Sign): Set if result is negative
- Z (Zero): Set if result is zero
- AC (Auxiliary Carry): Set if there's a carry from bit 3 to bit 4
- P (Parity): Set if result has even parity
- C (Carry): Set if there's a carry from bit 7

## Technical Documentation

### Core Components

#### CPU (Central Processing Unit)
The CPU implementation (`Src/Core/CPU.py`) is the heart of the simulator, implementing the Intel 8085 microprocessor architecture:

- **Register Implementation**:
  - 8-bit registers (A, B, C, D, E, H, L)
  - 16-bit registers (PC, SP)
  - Status flags (S, Z, AC, P, C)
  - Register pairs (BC, DE, HL) for 16-bit operations

- **Instruction Set**:
  - Full implementation of 8085 instruction set
  - Data transfer instructions (MOV, MVI, LXI)
  - Arithmetic instructions (ADD, SUB, INR, DCR)
  - Logical instructions (ANA, ORA, XRA)
  - Branch instructions (JMP, CALL, RET)
  - Stack operations (PUSH, POP)

- **Implementation Techniques**:
  - Instruction decoding using opcode mapping
  - Flag management for arithmetic and logical operations
  - Memory-mapped I/O support
  - Interrupt handling system

#### Memory Management Unit
The Memory implementation (`Src/Core/Memory.py`) provides a 64KB addressable space:

- **Features**:
  - 64KB (0x0000-0xFFFF) addressable memory
  - Byte and word (16-bit) read/write operations
  - Memory breakpoint support
  - Memory write callback system for GUI updates
  - Program loading functionality

- **Implementation Details**:
  - Little-endian byte ordering for 16-bit operations
  - Memory access validation
  - Breakpoint tracking system
  - Memory write notification system

#### ALU (Arithmetic Logic Unit)
The ALU implementation (`Src/Core/ALU.py`) handles all arithmetic and logical operations:

- **Operations**:
  - 8-bit addition with carry
  - 8-bit subtraction with borrow
  - Logical AND, OR, XOR operations
  - Flag generation for all operations

- **Flag Management**:
  - Sign (S): Set if result is negative
  - Zero (Z): Set if result is zero
  - Auxiliary Carry (AC): Set if carry from bit 3 to 4
  - Parity (P): Set if result has even parity
  - Carry (C): Set if operation produces carry/borrow

### Interface Components

#### GUI Implementation
The GUI (`Src/Interface/SimulatorGUI.py`) provides a modern, user-friendly interface:

- **Features**:
  - Code editor with syntax highlighting
  - Real-time CPU state visualization
  - Memory viewer and editor
  - Program execution controls
  - File I/O operations

- **Implementation Details**:
  - Tkinter-based interface
  - Multi-threaded execution
  - Real-time state updates
  - Memory visualization
  - Error handling and user feedback

### Utility Components

#### Logger
The Logger (`Src/Utils/Logger.py`) provides comprehensive logging:

- **Features**:
  - File and console logging
  - Timestamp-based logging
  - Multiple log levels (INFO, DEBUG, ERROR)
  - Persistent log storage

### Potential Enhancements

#### Core Components
1. **CPU Enhancements**:
   - Add support for undocumented instructions
   - Implement cycle-accurate timing
   - Add hardware interrupt simulation
   - Implement DMA controller simulation

2. **Memory Enhancements**:
   - Add memory protection mechanisms
   - Implement memory-mapped I/O devices
   - Add memory access patterns analysis
   - Support for ROM/EEPROM simulation

3. **ALU Enhancements**:
   - Add BCD arithmetic support
   - Implement decimal adjust operations
   - Add bit manipulation instructions
   - Support for extended arithmetic operations

#### Interface Enhancements
1. **GUI Improvements**:
   - Add dark/light theme support
   - Implement code debugging features
   - Add memory visualization improvements
   - Support for multiple code views
   - Add performance profiling tools

2. **User Experience**:
   - Add keyboard shortcuts
   - Implement code templates
   - Add program execution history
   - Support for multiple breakpoints
   - Add program execution speed control

#### Utility Enhancements
1. **Logging System**:
   - Add log rotation
   - Implement log filtering
   - Add performance metrics logging
   - Support for remote logging
   - Add log analysis tools

2. **Development Tools**:
   - Add unit testing framework
   - Implement code coverage tools
   - Add performance benchmarking
   - Support for automated testing
   - Add documentation generation

#### New Features
1. **Educational Tools**:
   - Add interactive tutorials
   - Implement step-by-step execution guides
   - Add visual instruction explanations
   - Support for program examples
   - Add learning exercises

2. **Advanced Features**:
   - Add support for external devices
   - Implement network simulation
   - Add real-time debugging
   - Support for program optimization
   - Add performance analysis tools

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 

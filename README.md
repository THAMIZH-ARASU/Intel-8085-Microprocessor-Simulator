# Intel 8085 Microprocessor Simulator

A Python-based simulator for the Intel 8085 microprocessor with a graphical user interface. This simulator allows you to write, assemble, and execute 8085 assembly code while visualizing the CPU state, memory contents, and program execution.

## Features

- Full 8085 instruction set support
- Real-time CPU state visualization
- Memory viewer and editor
- Assembly code editor with syntax highlighting
- Step-by-step execution
- Breakpoint support
- File I/O for assembly code
- Comprehensive logging

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
│   └── divide_example.asm
├── run.py
└── 8085_simulator.log
```

## Requirements

- Python 3.6 or higher
- tkinter (usually comes with Python)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/THAMIZHARASU/Intel-8085-Microprocessor-Simulator.git
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

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
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
.
├── src/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── memory.py
│   │   ├── alu.py
│   │   ├── cpu.py
│   │   └── assembler.py
│   ├── gui/
│   │   ├── __init__.py
│   │   └── simulator_gui.py
│   └── utils/
│       ├── __init__.py
│       └── logger.py
├── assembly_programs/
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
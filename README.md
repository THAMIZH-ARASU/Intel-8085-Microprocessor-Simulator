# Intel 8085 Microprocessor Simulator

A Python-based simulator for the Intel 8085 microprocessor with a graphical user interface. This simulator allows you to write, assemble, and execute 8085 assembly code while visualizing the CPU state, memory contents, and program execution. **Now with AI-powered code explanation!**

> **Note:** This project is currently under active development. Features and functionality may change as development progresses.

## Features

- Full 8085 instruction set support
- Real-time CPU state visualization
- Memory viewer and editor
- Assembly code editor with syntax highlighting
- Step-by-step execution
- Breakpoint support
- File I/O for assembly code
- **🤖 AI-Powered Code Explanation** - Get intelligent explanations of your assembly code
- Comprehensive logging
- **🌙 Dark/Light Theme Toggle** - Modern UI with theme switching

## AI Code Explanation Feature

The simulator now includes an intelligent AI-powered code explanation feature that helps you understand 8085 assembly code:

### **🤖 How It Works**
- Click the "🤖 Explain" button in the control panel
- The AI analyzes your assembly code and provides detailed explanations
- Get step-by-step breakdowns of each instruction
- Learn about data flow, program purpose, and key concepts

### **📚 What You Get**
- **Program Overview**: Clear description of what the program does
- **Instruction-by-Instruction Breakdown**: Detailed explanation of each instruction
- **Key Concepts**: Important 8085 concepts demonstrated
- **Educational Notes**: Learning insights and tips

### **🔧 Setup Required**
To use the AI explanation feature, you need a Groq API key:

1. **Get API Key**: Sign up at [Groq Console](https://console.groq.com/)
2. **Set Environment Variable**: Add to your `.env` file:
   ```
   GROQ_API_KEY=your_api_key_here
   ```
3. **Install Dependencies**: 
   ```bash
   pip install requests python-dotenv
   ```

### **💡 Example Usage**
```assembly
MVI A, #05      ; Load 05H into A
MVI B, #03      ; Load 03H into B
ADD B           ; A = A + B (A = 08H)
STA #9000       ; Store result at 9000H
HLT             ; Halt
```

The AI will explain:
- What each instruction does
- How data flows through registers
- The overall purpose of the program
- Important 8085 concepts used

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
5. **Control Panel**: Contains buttons for Run, Step, Stop, Reset, Load/Save, and **🤖 Explain**
6. **Terminal**: Shows all kinds of log about the system in real time
7. **Theme Toggle**: Switch between dark and light modes for better user experience

To view the output:
1. Load or write your assembly code
2. Click "Assemble" to compile the code
3. Use the Run or Step buttons to execute the program
4. Click "🤖 Explain" to get AI-powered code explanation
5. The Memory Viewer and Register Display will update in real-time

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
│       ├── Logger.py
│       └── AIExplainer.py          # NEW: AI-powered code explanation
├── AssemblyPrograms/
│   ├── addition_example.asm
│   ├── subtraction_example.asm
│   ├── multiplication_example.asm
│   ├── divide_example.asm
│   └── More...
├── run.py
├── INSTRUCTIONS.md                 # NEW: Complete instruction reference
└── 8085_simulator.log
```

## Requirements

- Python 3.6 or higher
- tkinter (usually comes with Python)
- **requests** (for AI explanation feature)
- **python-dotenv** (for environment variable management)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/THAMIZH-ARASU/Intel-8085-Microprocessor-Simulator.git
cd simple8085
```

2. Install required dependencies:
```bash
pip install requests python-dotenv
```

3. Set up your API key (optional, for AI explanation):
   - Create a `.env` file in the project root
   - Add: `GROQ_API_KEY=your_api_key_here`

4. Run the simulator:
```bash
python run.py
```

## Usage

1. Write your 8085 assembly code in the code editor
2. Click "Assemble" to convert the code to machine code
3. Use the following controls to execute your program:
   - **Run**: Execute the program continuously
   - **Step**: Execute one instruction at a time
   - **Stop**: Halt program execution
   - **Reset**: Reset the CPU to initial state
   - **Load/Save**: Load or save assembly code files
   - **🤖 Explain**: Get AI-powered explanation of your code (requires API key)

## AI Explanation Feature

### **🎯 Getting Started**
1. **Get API Key**: Sign up at [Groq Console](https://console.groq.com/)
2. **Set Environment Variable**: Add to `.env` file:
   ```
   GROQ_API_KEY=your_api_key_here
   ```
3. **Use the Feature**: Click "🤖 Explain" button in the control panel

### **📖 What You'll Get**
- **Structured Explanations**: Clear sections with headers and bullet points
- **Educational Focus**: Designed for learning 8085 assembly
- **Step-by-Step Breakdown**: Each instruction explained in detail
- **Concept Highlights**: Important 8085 concepts and techniques
- **Learning Tips**: Educational insights for better understanding

### **🔧 Troubleshooting**
- **API Key Missing**: Ensure `GROQ_API_KEY` is set in your `.env` file
- **Network Issues**: Check your internet connection
- **Rate Limits**: Groq has rate limits; wait if you hit them

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
  - **🤖 AI Code Explanation** - Intelligent code analysis
  - **🌙 Theme Toggle** - Dark/Light mode switching

- **Implementation Details**:
  - Tkinter-based interface
  - Multi-threaded execution
  - Real-time state updates
  - Memory visualization
  - Error handling and user feedback
  - AI integration with threading support

### Utility Components

#### Logger
The Logger (`Src/Utils/Logger.py`) provides comprehensive logging:

- **Features**:
  - File and console logging
  - Timestamp-based logging
  - Multiple log levels (INFO, DEBUG, ERROR)
  - Persistent log storage

#### AI Explainer
The AI Explainer (`Src/Utils/AIExplainer.py`) provides intelligent code analysis:

- **Features**:
  - Groq API integration for AI-powered explanations
  - Structured, educational explanations
  - Comprehensive error handling
  - Connection testing and validation
  - Detailed logging for troubleshooting

- **Implementation Details**:
  - Thread-safe API calls
  - Structured prompt engineering
  - Response formatting and validation
  - Error categorization and user-friendly messages

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
   - Add dark/light theme support ✅ **COMPLETED**
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

#### AI Features
1. **Enhanced Explanations**:
   - Add visual diagrams for data flow
   - Implement step-by-step animation
   - Add code optimization suggestions
   - Support for multiple explanation styles

2. **Educational Tools**:
   - Add interactive tutorials
   - Implement learning progress tracking
   - Add quiz generation from code
   - Support for custom learning paths

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

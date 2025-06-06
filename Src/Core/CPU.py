from typing import Dict, List
from Src.Core.Memory import Memory
from Src.Core.ALU import ALU
from Src.Utils.Logger import logger

class CPU:
    """Intel 8085 CPU Core"""
    
    def __init__(self, memory: Memory):
        self.memory = memory
        self.alu = ALU()
        logger.info("CPU initialized")
        
        # 8-bit registers
        self.registers = {
            'A': 0x00,  # Accumulator
            'B': 0x00, 'C': 0x00,  # BC register pair
            'D': 0x00, 'E': 0x00,  # DE register pair
            'H': 0x00, 'L': 0x00   # HL register pair
        }
        
        # 16-bit registers
        self.PC = 0x8000  # Program Counter
        self.SP = 0xFFFF  # Stack Pointer
        
        # Status flags
        self.flags = {
            'S': False,  # Sign flag
            'Z': False,  # Zero flag
            'AC': False, # Auxiliary Carry
            'P': False,  # Parity flag
            'C': False   # Carry flag
        }
        
        # Control flags
        self.halted = False
        self.interrupt_enabled = False
        
        # Instruction set
        self.instruction_set = self._build_instruction_set()
        logger.info("CPU instruction set initialized")
    
    def get_register_pair(self, high: str, low: str) -> int:
        """Get 16-bit register pair value"""
        return (self.registers[high] << 8) | self.registers[low]
    
    def set_register_pair(self, high: str, low: str, value: int) -> None:
        """Set 16-bit register pair value"""
        self.registers[high] = (value >> 8) & 0xFF
        self.registers[low] = value & 0xFF
    
    def update_flags(self, flags: Dict[str, bool]) -> None:
        """Update CPU flags"""
        self.flags.update(flags)
    
    def push_stack(self, value: int) -> None:
        """Push 16-bit value onto stack"""
        self.SP -= 2
        self.memory.write_word(self.SP, value)
    
    def pop_stack(self) -> int:
        """Pop 16-bit value from stack"""
        value = self.memory.read_word(self.SP)
        self.SP += 2
        return value
    
    def fetch_instruction(self) -> int:
        """Fetch instruction from memory"""
        opcode = self.memory.read(self.PC)
        self.PC = (self.PC + 1) & 0xFFFF
        return opcode
    
    def fetch_byte(self) -> int:
        """Fetch immediate byte"""
        byte = self.memory.read(self.PC)
        self.PC = (self.PC + 1) & 0xFFFF
        return byte
    
    def fetch_word(self) -> int:
        """Fetch immediate word"""
        word = self.memory.read_word(self.PC)
        self.PC = (self.PC + 2) & 0xFFFF
        return word
    
    def execute_instruction(self) -> bool:
        """Execute single instruction, return True if should continue"""
        if self.halted:
            logger.info("CPU is halted")
            return False
        
        opcode = self.fetch_instruction()
        logger.debug(f"Executing instruction at PC={self.PC-1:04X}, Opcode={opcode:02X}")
        
        if opcode in self.instruction_set:
            self.instruction_set[opcode]()
            return True
        else:
            logger.error(f"Unknown opcode: {opcode:02X} at PC: {self.PC-1:04X}")
            raise ValueError(f"Unknown opcode: {opcode:02X} at PC: {self.PC-1:04X}")
    
    def _build_instruction_set(self) -> Dict[int, callable]:
        """Build instruction set mapping"""
        instructions = {}
        
        # Data Transfer Instructions
        instructions[0x7F] = self._mov_a_a  # MOV A,A
        instructions[0x78] = self._mov_a_b  # MOV A,B
        instructions[0x79] = self._mov_a_c  # MOV A,C
        instructions[0x7A] = self._mov_a_d  # MOV A,D
        instructions[0x7B] = self._mov_a_e  # MOV A,E
        instructions[0x7C] = self._mov_a_h  # MOV A,H
        instructions[0x7D] = self._mov_a_l  # MOV A,L
        instructions[0x7E] = self._mov_a_m  # MOV A,M
        
        instructions[0x47] = self._mov_b_a  # MOV B,A
        instructions[0x40] = self._mov_b_b  # MOV B,B
        instructions[0x41] = self._mov_b_c  # MOV B,C
        instructions[0x42] = self._mov_b_d  # MOV B,D
        instructions[0x43] = self._mov_b_e  # MOV B,E
        instructions[0x44] = self._mov_b_h  # MOV B,H
        instructions[0x45] = self._mov_b_l  # MOV B,L
        instructions[0x46] = self._mov_b_m  # MOV B,M
        
        instructions[0x4F] = self._mov_c_a  # MOV C,A
        instructions[0x48] = self._mov_c_b  # MOV C,B
        instructions[0x49] = self._mov_c_c  # MOV C,C
        instructions[0x4A] = self._mov_c_d  # MOV C,D
        instructions[0x4B] = self._mov_c_e  # MOV C,E
        instructions[0x4C] = self._mov_c_h  # MOV C,H
        instructions[0x4D] = self._mov_c_l  # MOV C,L
        instructions[0x4E] = self._mov_c_m  # MOV C,M

        # Add D register MOV instructions
        instructions[0x57] = self._mov_d_a  # MOV D,A
        instructions[0x50] = self._mov_d_b  # MOV D,B
        instructions[0x51] = self._mov_d_c  # MOV D,C
        instructions[0x52] = self._mov_d_d  # MOV D,D
        instructions[0x53] = self._mov_d_e  # MOV D,E
        instructions[0x54] = self._mov_d_h  # MOV D,H
        instructions[0x55] = self._mov_d_l  # MOV D,L
        instructions[0x56] = self._mov_d_m  # MOV D,M

        # Add E register MOV instructions
        instructions[0x5F] = self._mov_e_a  # MOV E,A
        instructions[0x58] = self._mov_e_b  # MOV E,B
        instructions[0x59] = self._mov_e_c  # MOV E,C
        instructions[0x5A] = self._mov_e_d  # MOV E,D
        instructions[0x5B] = self._mov_e_e  # MOV E,E
        instructions[0x5C] = self._mov_e_h  # MOV E,H
        instructions[0x5D] = self._mov_e_l  # MOV E,L
        instructions[0x5E] = self._mov_e_m  # MOV E,M

        # Add H register MOV instructions
        instructions[0x67] = self._mov_h_a  # MOV H,A
        instructions[0x60] = self._mov_h_b  # MOV H,B
        instructions[0x61] = self._mov_h_c  # MOV H,C
        instructions[0x62] = self._mov_h_d  # MOV H,D
        instructions[0x63] = self._mov_h_e  # MOV H,E
        instructions[0x64] = self._mov_h_h  # MOV H,H
        instructions[0x65] = self._mov_h_l  # MOV H,L
        instructions[0x66] = self._mov_h_m  # MOV H,M

        # Add L register MOV instructions
        instructions[0x6F] = self._mov_l_a  # MOV L,A
        instructions[0x68] = self._mov_l_b  # MOV L,B
        instructions[0x69] = self._mov_l_c  # MOV L,C
        instructions[0x6A] = self._mov_l_d  # MOV L,D
        instructions[0x6B] = self._mov_l_e  # MOV L,E
        instructions[0x6C] = self._mov_l_h  # MOV L,H
        instructions[0x6D] = self._mov_l_l  # MOV L,L
        instructions[0x6E] = self._mov_l_m  # MOV L,M

        # Add M register MOV instructions
        instructions[0x77] = self._mov_m_a  # MOV M,A
        instructions[0x70] = self._mov_m_b  # MOV M,B
        instructions[0x71] = self._mov_m_c  # MOV M,C
        instructions[0x72] = self._mov_m_d  # MOV M,D
        instructions[0x73] = self._mov_m_e  # MOV M,E
        instructions[0x74] = self._mov_m_h  # MOV M,H
        instructions[0x75] = self._mov_m_l  # MOV M,L
        
        # Immediate load instructions
        instructions[0x3E] = self._mvi_a   # MVI A,data
        instructions[0x06] = self._mvi_b   # MVI B,data
        instructions[0x0E] = self._mvi_c   # MVI C,data
        instructions[0x16] = self._mvi_d   # MVI D,data
        instructions[0x1E] = self._mvi_e   # MVI E,data
        instructions[0x26] = self._mvi_h   # MVI H,data
        instructions[0x2E] = self._mvi_l   # MVI L,data
        instructions[0x36] = self._mvi_m   # MVI M,data
        
        # Load register pairs
        instructions[0x01] = self._lxi_b   # LXI B,data16
        instructions[0x11] = self._lxi_d   # LXI D,data16
        instructions[0x21] = self._lxi_h   # LXI H,data16
        instructions[0x31] = self._lxi_sp  # LXI SP,data16
        
        # Memory operations
        instructions[0x3A] = self._lda     # LDA addr
        instructions[0x32] = self._sta     # STA addr
        instructions[0x2A] = self._lhld    # LHLD addr
        instructions[0x22] = self._shld    # SHLD addr
        
        # Arithmetic Instructions
        instructions[0x87] = self._add_a   # ADD A
        instructions[0x80] = self._add_b   # ADD B
        instructions[0x81] = self._add_c   # ADD C
        instructions[0x82] = self._add_d   # ADD D
        instructions[0x83] = self._add_e   # ADD E
        instructions[0x84] = self._add_h   # ADD H
        instructions[0x85] = self._add_l   # ADD L
        instructions[0x86] = self._add_m   # ADD M
        instructions[0xC6] = self._adi     # ADI data
        
        instructions[0x8F] = self._adc_a   # ADC A
        instructions[0x88] = self._adc_b   # ADC B
        instructions[0x89] = self._adc_c   # ADC C
        instructions[0x8A] = self._adc_d   # ADC D
        instructions[0x8B] = self._adc_e   # ADC E
        instructions[0x8C] = self._adc_h   # ADC H
        instructions[0x8D] = self._adc_l   # ADC L
        instructions[0x8E] = self._adc_m   # ADC M
        
        instructions[0x97] = self._sub_a   # SUB A
        instructions[0x90] = self._sub_b   # SUB B
        instructions[0x91] = self._sub_c   # SUB C
        instructions[0x92] = self._sub_d   # SUB D
        instructions[0x93] = self._sub_e   # SUB E
        instructions[0x94] = self._sub_h   # SUB H
        instructions[0x95] = self._sub_l   # SUB L
        instructions[0x96] = self._sub_m   # SUB M
        
        # Logical Instructions
        instructions[0xA7] = self._ana_a   # ANA A
        instructions[0xA0] = self._ana_b   # ANA B
        instructions[0xA1] = self._ana_c   # ANA C
        instructions[0xA2] = self._ana_d   # ANA D
        instructions[0xA3] = self._ana_e   # ANA E
        instructions[0xA4] = self._ana_h   # ANA H
        instructions[0xA5] = self._ana_l   # ANA L
        instructions[0xA6] = self._ana_m   # ANA M
        
        instructions[0xB7] = self._ora_a   # ORA A
        instructions[0xB0] = self._ora_b   # ORA B
        instructions[0xB1] = self._ora_c   # ORA C
        instructions[0xB2] = self._ora_d   # ORA D
        instructions[0xB3] = self._ora_e   # ORA E
        instructions[0xB4] = self._ora_h   # ORA H
        instructions[0xB5] = self._ora_l   # ORA L
        instructions[0xB6] = self._ora_m   # ORA M
        
        # Increment/Decrement
        instructions[0x3C] = self._inr_a   # INR A
        instructions[0x04] = self._inr_b   # INR B
        instructions[0x0C] = self._inr_c   # INR C
        instructions[0x14] = self._inr_d   # INR D
        instructions[0x1C] = self._inr_e   # INR E
        instructions[0x24] = self._inr_h   # INR H
        instructions[0x2C] = self._inr_l   # INR L
        instructions[0x34] = self._inr_m   # INR M
        
        instructions[0x03] = self._inx_b   # INX B
        instructions[0x13] = self._inx_d   # INX D
        instructions[0x23] = self._inx_h   # INX H
        instructions[0x33] = self._inx_sp  # INX SP
        
        instructions[0x3D] = self._dcr_a   # DCR A
        instructions[0x05] = self._dcr_b   # DCR B
        instructions[0x0D] = self._dcr_c   # DCR C
        instructions[0x15] = self._dcr_d   # DCR D
        instructions[0x1D] = self._dcr_e   # DCR E
        instructions[0x25] = self._dcr_h   # DCR H
        instructions[0x2D] = self._dcr_l   # DCR L
        instructions[0x35] = self._dcr_m   # DCR M

        instructions[0x0B] = self._dcx_b   # DCX B
        instructions[0x1B] = self._dcx_d   # DCX B
        instructions[0x2B] = self._dcx_h   # DCX B
        instructions[0x3B] = self._dcx_sp   # DCX B
        
        # Jump Instructions
        instructions[0xC3] = self._jmp     # JMP addr
        instructions[0xCA] = self._jz      # JZ addr
        instructions[0xC2] = self._jnz     # JNZ addr
        instructions[0xDA] = self._jc      # JC addr
        instructions[0xD2] = self._jnc     # JNC addr
        
        # Call and Return
        instructions[0xCD] = self._call    # CALL addr
        instructions[0xC9] = self._ret     # RET
        
        # Stack Operations
        instructions[0xC5] = self._push_b  # PUSH B
        instructions[0xD5] = self._push_d  # PUSH D
        instructions[0xE5] = self._push_h  # PUSH H
        instructions[0xF5] = self._push_psw # PUSH PSW
        
        instructions[0xC1] = self._pop_b   # POP B
        instructions[0xD1] = self._pop_d   # POP D
        instructions[0xE1] = self._pop_h   # POP H
        instructions[0xF1] = self._pop_psw # POP PSW
        
        # Compare and rotate
        instructions[0xBF] = self._cmp_a   # CMP A
        instructions[0xB8] = self._cmp_b   # CMP B
        instructions[0xFE] = self._cpi     # CPI data
        
        # Control
        instructions[0x76] = self._hlt     # HLT
        instructions[0x00] = self._nop     # NOP
        
        return instructions
    
    # Instruction implementations
    def _mov_a_a(self): self.registers['A'] = self.registers['A']
    def _mov_a_b(self): self.registers['A'] = self.registers['B']
    def _mov_a_c(self): self.registers['A'] = self.registers['C']
    def _mov_a_d(self): self.registers['A'] = self.registers['D']
    def _mov_a_e(self): self.registers['A'] = self.registers['E']
    def _mov_a_h(self): self.registers['A'] = self.registers['H']
    def _mov_a_l(self): self.registers['A'] = self.registers['L']
    def _mov_a_m(self): 
        addr = self.get_register_pair('H', 'L')
        self.registers['A'] = self.memory.read(addr)
        logger.debug(f"MOV A,M: Reading from address {addr:04X}")
    
    def _mov_b_a(self): self.registers['B'] = self.registers['A']
    def _mov_b_b(self): self.registers['B'] = self.registers['B']
    def _mov_b_c(self): self.registers['B'] = self.registers['C']
    def _mov_b_d(self): self.registers['B'] = self.registers['D']
    def _mov_b_e(self): self.registers['B'] = self.registers['E']
    def _mov_b_h(self): self.registers['B'] = self.registers['H']
    def _mov_b_l(self): self.registers['B'] = self.registers['L']
    def _mov_b_m(self): 
        addr = self.get_register_pair('H', 'L')
        self.registers['B'] = self.memory.read(addr)
        logger.debug(f"MOV B,M: Reading from address {addr:04X}")
    
    def _mov_c_a(self): self.registers['C'] = self.registers['A']
    def _mov_c_b(self): self.registers['C'] = self.registers['B']
    def _mov_c_c(self): self.registers['C'] = self.registers['C']
    def _mov_c_d(self): self.registers['C'] = self.registers['D']
    def _mov_c_e(self): self.registers['C'] = self.registers['E']
    def _mov_c_h(self): self.registers['C'] = self.registers['H']
    def _mov_c_l(self): self.registers['C'] = self.registers['L']
    def _mov_c_m(self): 
        addr = self.get_register_pair('H', 'L')
        self.registers['C'] = self.memory.read(addr)
        logger.debug(f"MOV C,M: Reading from address {addr:04X}")
    
    def _mvi_a(self): self.registers['A'] = self.fetch_byte()
    def _mvi_b(self): self.registers['B'] = self.fetch_byte()
    def _mvi_c(self): self.registers['C'] = self.fetch_byte()
    def _mvi_d(self): self.registers['D'] = self.fetch_byte()
    def _mvi_e(self): self.registers['E'] = self.fetch_byte()
    def _mvi_h(self): self.registers['H'] = self.fetch_byte()
    def _mvi_l(self): self.registers['L'] = self.fetch_byte()
    def _mvi_m(self): 
        addr = self.get_register_pair('H', 'L')
        self.memory.write(addr, self.fetch_byte())
    
    def _lxi_b(self): self.set_register_pair('B', 'C', self.fetch_word())
    def _lxi_d(self): self.set_register_pair('D', 'E', self.fetch_word())
    def _lxi_h(self): self.set_register_pair('H', 'L', self.fetch_word())
    def _lxi_sp(self): self.SP = self.fetch_word()
    
    def _lda(self): 
        addr = self.fetch_word()
        self.registers['A'] = self.memory.read(addr)
    
    def _sta(self): 
        addr = self.fetch_word()
        self.memory.write(addr, self.registers['A'])
    
    def _lhld(self): 
        addr = self.fetch_word()
        self.set_register_pair('H', 'L', self.memory.read_word(addr))
    
    def _shld(self): 
        addr = self.fetch_word()
        self.memory.write_word(addr, self.get_register_pair('H', 'L'))
    
    def _add_a(self): 
        result, flags = self.alu.add(self.registers['A'], self.registers['A'])
        self.registers['A'] = result
        self.update_flags(flags)
    
    def _add_b(self): 
        result, flags = self.alu.add(self.registers['A'], self.registers['B'])
        self.registers['A'] = result
        self.update_flags(flags)
    
    def _add_c(self): 
        result, flags = self.alu.add(self.registers['A'], self.registers['C'])
        self.registers['A'] = result
        self.update_flags(flags)
    
    def _add_d(self): 
        result, flags = self.alu.add(self.registers['A'], self.registers['D'])
        self.registers['A'] = result
        self.update_flags(flags)
    
    def _add_e(self): 
        result, flags = self.alu.add(self.registers['A'], self.registers['E'])
        self.registers['A'] = result
        self.update_flags(flags)
    
    def _add_h(self): 
        result, flags = self.alu.add(self.registers['A'], self.registers['H'])
        self.registers['A'] = result
        self.update_flags(flags)
    
    def _add_l(self): 
        result, flags = self.alu.add(self.registers['A'], self.registers['L'])
        self.registers['A'] = result
        self.update_flags(flags)
    
    def _add_m(self): 
        """Add memory location pointed by HL to accumulator"""
        addr = self.get_register_pair('H', 'L')
        memory_value = self.memory.read(addr)
        result, flags = self.alu.add(self.registers['A'], memory_value)
        self.registers['A'] = result
        self.update_flags(flags)
        logger.debug(f"ADD M: A={self.registers['A']:02X} + M[{addr:04X}]={memory_value:02X} = {result:02X}")
    
    def _adi(self): 
        data = self.fetch_byte()
        result, flags = self.alu.add(self.registers['A'], data)
        self.registers['A'] = result
        self.update_flags(flags)
    
    def _adc_a(self): 
        result, flags = self.alu.add(self.registers['A'], self.registers['A'], self.flags['C'])
        self.registers['A'] = result
        self.update_flags(flags)
    
    def _adc_b(self): 
        result, flags = self.alu.add(self.registers['A'], self.registers['B'], self.flags['C'])
        self.registers['A'] = result
        self.update_flags(flags)
    
    def _adc_c(self): 
        result, flags = self.alu.add(self.registers['A'], self.registers['C'], self.flags['C'])
        self.registers['A'] = result
        self.update_flags(flags)
    
    def _adc_d(self): 
        result, flags = self.alu.add(self.registers['A'], self.registers['D'], self.flags['C'])
        self.registers['A'] = result
        self.update_flags(flags)
    
    def _adc_e(self): 
        result, flags = self.alu.add(self.registers['A'], self.registers['E'], self.flags['C'])
        self.registers['A'] = result
        self.update_flags(flags)
    
    def _adc_h(self): 
        result, flags = self.alu.add(self.registers['A'], self.registers['H'], self.flags['C'])
        self.registers['A'] = result
        self.update_flags(flags)
    
    def _adc_l(self): 
        result, flags = self.alu.add(self.registers['A'], self.registers['L'], self.flags['C'])
        self.registers['A'] = result
        self.update_flags(flags)
    
    def _adc_m(self): 
        addr = self.get_register_pair('H', 'L')
        result, flags = self.alu.add(self.registers['A'], self.memory.read(addr), self.flags['C'])
        self.registers['A'] = result
        self.update_flags(flags)
    
    def _sub_a(self): 
        result, flags = self.alu.sub(self.registers['A'], self.registers['A'])
        self.registers['A'] = result
        self.update_flags(flags)
    
    def _sub_b(self): 
        result, flags = self.alu.sub(self.registers['A'], self.registers['B'])
        self.registers['A'] = result
        self.update_flags(flags)
    
    def _sub_c(self): 
        result, flags = self.alu.sub(self.registers['A'], self.registers['C'])
        self.registers['A'] = result
        self.update_flags(flags)
    
    def _sub_d(self): 
        result, flags = self.alu.sub(self.registers['A'], self.registers['D'])
        self.registers['A'] = result
        self.update_flags(flags)
    
    def _sub_e(self): 
        result, flags = self.alu.sub(self.registers['A'], self.registers['E'])
        self.registers['A'] = result
        self.update_flags(flags)
    
    def _sub_h(self): 
        result, flags = self.alu.sub(self.registers['A'], self.registers['H'])
        self.registers['A'] = result
        self.update_flags(flags)
    
    def _sub_l(self): 
        result, flags = self.alu.sub(self.registers['A'], self.registers['L'])
        self.registers['A'] = result
        self.update_flags(flags)
    
    def _sub_m(self): 
        addr = self.get_register_pair('H', 'L')
        result, flags = self.alu.sub(self.registers['A'], self.memory.read(addr))
        self.registers['A'] = result
        self.update_flags(flags)
    
    def _ana_a(self): 
        result, flags = self.alu.logical_and(self.registers['A'], self.registers['A'])
        self.registers['A'] = result
        self.update_flags(flags)
    
    def _ana_b(self): 
        result, flags = self.alu.logical_and(self.registers['A'], self.registers['B'])
        self.registers['A'] = result
        self.update_flags(flags)
    
    def _ana_c(self): 
        result, flags = self.alu.logical_and(self.registers['A'], self.registers['C'])
        self.registers['A'] = result
        self.update_flags(flags)
    
    def _ana_d(self): 
        result, flags = self.alu.logical_and(self.registers['A'], self.registers['D'])
        self.registers['A'] = result
        self.update_flags(flags)
    
    def _ana_e(self): 
        result, flags = self.alu.logical_and(self.registers['A'], self.registers['E'])
        self.registers['A'] = result
        self.update_flags(flags)
    
    def _ana_h(self): 
        result, flags = self.alu.logical_and(self.registers['A'], self.registers['H'])
        self.registers['A'] = result
        self.update_flags(flags)
    
    def _ana_l(self): 
        result, flags = self.alu.logical_and(self.registers['A'], self.registers['L'])
        self.registers['A'] = result
        self.update_flags(flags)
    
    def _ana_m(self): 
        addr = self.get_register_pair('H', 'L')
        result, flags = self.alu.logical_and(self.registers['A'], self.memory.read(addr))
        self.registers['A'] = result
        self.update_flags(flags)
    
    def _ora_a(self): 
        result, flags = self.alu.logical_or(self.registers['A'], self.registers['A'])
        self.registers['A'] = result
        self.update_flags(flags)
    
    def _ora_b(self): 
        result, flags = self.alu.logical_or(self.registers['A'], self.registers['B'])
        self.registers['A'] = result
        self.update_flags(flags)
    
    def _ora_c(self): 
        result, flags = self.alu.logical_or(self.registers['A'], self.registers['C'])
        self.registers['A'] = result
        self.update_flags(flags)
    
    def _ora_d(self): 
        result, flags = self.alu.logical_or(self.registers['A'], self.registers['D'])
        self.registers['A'] = result
        self.update_flags(flags)
    
    def _ora_e(self): 
        result, flags = self.alu.logical_or(self.registers['A'], self.registers['E'])
        self.registers['A'] = result
        self.update_flags(flags)
    
    def _ora_h(self): 
        result, flags = self.alu.logical_or(self.registers['A'], self.registers['H'])
        self.registers['A'] = result
        self.update_flags(flags)
    
    def _ora_l(self): 
        result, flags = self.alu.logical_or(self.registers['A'], self.registers['L'])
        self.registers['A'] = result
        self.update_flags(flags)
    
    def _ora_m(self): 
        addr = self.get_register_pair('H', 'L')
        result, flags = self.alu.logical_or(self.registers['A'], self.memory.read(addr))
        self.registers['A'] = result
        self.update_flags(flags)
    
    def _inr_a(self): 
        result, flags = self.alu.add(self.registers['A'], 1)
        self.registers['A'] = result
        flags['C'] = self.flags['C']  # Preserve carry flag
        self.update_flags(flags)
    
    def _inr_b(self): 
        result, flags = self.alu.add(self.registers['B'], 1)
        self.registers['B'] = result
        flags['C'] = self.flags['C']
        self.update_flags(flags)
    
    def _inr_c(self): 
        result, flags = self.alu.add(self.registers['C'], 1)
        self.registers['C'] = result
        flags['C'] = self.flags['C']
        self.update_flags(flags)
    
    def _inr_d(self): 
        result, flags = self.alu.add(self.registers['D'], 1)
        self.registers['D'] = result
        flags['C'] = self.flags['C']
        self.update_flags(flags)
    
    def _inr_e(self): 
        result, flags = self.alu.add(self.registers['E'], 1)
        self.registers['E'] = result
        flags['C'] = self.flags['C']
        self.update_flags(flags)
    
    def _inr_h(self): 
        result, flags = self.alu.add(self.registers['H'], 1)
        self.registers['H'] = result
        flags['C'] = self.flags['C']
        self.update_flags(flags)
    
    def _inr_l(self): 
        result, flags = self.alu.add(self.registers['L'], 1)
        self.registers['L'] = result
        flags['C'] = self.flags['C']
        self.update_flags(flags)
    
    def _inr_m(self): 
        addr = self.get_register_pair('H', 'L')
        value = self.memory.read(addr)
        result, flags = self.alu.add(value, 1)
        self.memory.write(addr, result)
        flags['C'] = self.flags['C']
        self.update_flags(flags)
    
    def _dcr_a(self): 
        result, flags = self.alu.sub(self.registers['A'], 1)
        self.registers['A'] = result
        flags['C'] = self.flags['C']
        self.update_flags(flags)
    
    def _dcr_b(self): 
        result, flags = self.alu.sub(self.registers['B'], 1)
        self.registers['B'] = result
        flags['C'] = self.flags['C']
        self.update_flags(flags)
    
    def _dcr_c(self): 
        result, flags = self.alu.sub(self.registers['C'], 1)
        self.registers['C'] = result
        flags['C'] = self.flags['C']
        self.update_flags(flags)
    
    def _dcr_d(self): 
        result, flags = self.alu.sub(self.registers['D'], 1)
        self.registers['D'] = result
        flags['C'] = self.flags['C']
        self.update_flags(flags)
    
    def _dcr_e(self): 
        result, flags = self.alu.sub(self.registers['E'], 1)
        self.registers['E'] = result
        flags['C'] = self.flags['C']
        self.update_flags(flags)
    
    def _dcr_h(self): 
        result, flags = self.alu.sub(self.registers['H'], 1)
        self.registers['H'] = result
        flags['C'] = self.flags['C']
        self.update_flags(flags)
    
    def _dcr_l(self): 
        result, flags = self.alu.sub(self.registers['L'], 1)
        self.registers['L'] = result
        flags['C'] = self.flags['C']
        self.update_flags(flags)
    
    def _dcr_m(self): 
        addr = self.get_register_pair('H', 'L')
        value = self.memory.read(addr)
        result, flags = self.alu.sub(value, 1)
        self.memory.write(addr, result)
        flags['C'] = self.flags['C']
        self.update_flags(flags)
    
    def _jmp(self): 
        self.PC = self.fetch_word()
    
    def _jz(self): 
        addr = self.fetch_word()
        if self.flags['Z']:
            self.PC = addr
    
    def _jnz(self): 
        addr = self.fetch_word()
        if not self.flags['Z']:
            self.PC = addr
    
    def _jc(self): 
        addr = self.fetch_word()
        if self.flags['C']:
            self.PC = addr
    
    def _jnc(self): 
        addr = self.fetch_word()
        if not self.flags['C']:
            self.PC = addr
    
    def _call(self): 
        addr = self.fetch_word()
        self.push_stack(self.PC)
        self.PC = addr
    
    def _ret(self): 
        self.PC = self.pop_stack()
    
    def _push_b(self): 
        self.push_stack(self.get_register_pair('B', 'C'))
    
    def _push_d(self): 
        self.push_stack(self.get_register_pair('D', 'E'))
    
    def _push_h(self): 
        self.push_stack(self.get_register_pair('H', 'L'))
    
    def _push_psw(self): 
        psw = self.registers['A'] << 8
        if self.flags['S']: psw |= 0x80
        if self.flags['Z']: psw |= 0x40
        if self.flags['AC']: psw |= 0x10
        if self.flags['P']: psw |= 0x04
        if self.flags['C']: psw |= 0x01
        self.push_stack(psw)
    
    def _pop_b(self): 
        self.set_register_pair('B', 'C', self.pop_stack())
    
    def _pop_d(self): 
        self.set_register_pair('D', 'E', self.pop_stack())
    
    def _pop_h(self): 
        self.set_register_pair('H', 'L', self.pop_stack())
    
    def _pop_psw(self): 
        psw = self.pop_stack()
        self.registers['A'] = (psw >> 8) & 0xFF
        self.flags['S'] = bool(psw & 0x80)
        self.flags['Z'] = bool(psw & 0x40)
        self.flags['AC'] = bool(psw & 0x10)
        self.flags['P'] = bool(psw & 0x04)
        self.flags['C'] = bool(psw & 0x01)
    
    def _cmp_a(self): 
        _, flags = self.alu.sub(self.registers['A'], self.registers['A'])
        self.update_flags(flags)
    
    def _cmp_b(self): 
        _, flags = self.alu.sub(self.registers['A'], self.registers['B'])
        self.update_flags(flags)
    
    def _cpi(self): 
        data = self.fetch_byte()
        _, flags = self.alu.sub(self.registers['A'], data)
        self.update_flags(flags)
    
    def _hlt(self): 
        self.halted = True
    
    def _nop(self): 
        pass  # No operation

    def _mov_m_a(self):
        """Move accumulator to memory location pointed by HL"""
        addr = self.get_register_pair('H', 'L')
        self.memory.write(addr, self.registers['A'])
        logger.debug(f"MOV M,A: Writing {self.registers['A']:02X} to address {addr:04X}")

    def _inx_b(self):
        """Increment BC register pair"""
        value = self.get_register_pair('B', 'C')
        value = (value + 1) & 0xFFFF
        self.set_register_pair('B', 'C', value)
        logger.debug(f"INX B: BC={value:04X}")

    def _inx_d(self):
        """Increment DE register pair"""
        value = self.get_register_pair('D', 'E')
        value = (value + 1) & 0xFFFF
        self.set_register_pair('D', 'E', value)
        logger.debug(f"INX D: DE={value:04X}")

    def _inx_h(self):
        """Increment HL register pair"""
        value = self.get_register_pair('H', 'L')
        value = (value + 1) & 0xFFFF
        self.set_register_pair('H', 'L', value)
        logger.debug(f"INX H: HL={value:04X}")

    def _inx_sp(self):
        """Increment SP"""
        value = self.SP
        value = (value + 1) & 0xFFFF
        self.SP = value
        logger.debug(f"INX SP: SP={value:04X}")

    def _dcx_b(self):
        """Decrement BC register pair"""
        value = self.get_register_pair('B', 'C')
        value = (value - 1) & 0xFFFF
        self.set_register_pair('B', 'C', value)
        logger.debug(f"DCX B: BC={value:04X}")

    def _dcx_d(self):
        """Decrement DE register pair"""
        value = self.get_register_pair('D', 'E')
        value = (value - 1) & 0xFFFF
        self.set_register_pair('D', 'E', value)
        logger.debug(f"DCX B: BC={value:04X}")

    def _dcx_h(self):
        """Decrement HL register pair"""
        value = self.get_register_pair('H', 'L')
        value = (value - 1) & 0xFFFF
        self.set_register_pair('H', 'L', value)
        logger.debug(f"DCX B: BC={value:04X}")

    def _dcx_sp(self):
        """Decrement SP register"""
        value = self.SP
        value = (value - 1) & 0xFFFF
        self.SP = value
        logger.debug(f"DCX B: BC={value:04X}")

    # Add D register MOV implementations
    def _mov_d_a(self): self.registers['D'] = self.registers['A']
    def _mov_d_b(self): self.registers['D'] = self.registers['B']
    def _mov_d_c(self): self.registers['D'] = self.registers['C']
    def _mov_d_d(self): self.registers['D'] = self.registers['D']
    def _mov_d_e(self): self.registers['D'] = self.registers['E']
    def _mov_d_h(self): self.registers['D'] = self.registers['H']
    def _mov_d_l(self): self.registers['D'] = self.registers['L']
    def _mov_d_m(self): 
        addr = self.get_register_pair('H', 'L')
        self.registers['D'] = self.memory.read(addr)
        logger.debug(f"MOV D,M: Reading from address {addr:04X}")

    # Add E register MOV implementations
    def _mov_e_a(self): self.registers['E'] = self.registers['A']
    def _mov_e_b(self): self.registers['E'] = self.registers['B']
    def _mov_e_c(self): self.registers['E'] = self.registers['C']
    def _mov_e_d(self): self.registers['E'] = self.registers['D']
    def _mov_e_e(self): self.registers['E'] = self.registers['E']
    def _mov_e_h(self): self.registers['E'] = self.registers['H']
    def _mov_e_l(self): self.registers['E'] = self.registers['L']
    def _mov_e_m(self): 
        addr = self.get_register_pair('H', 'L')
        self.registers['E'] = self.memory.read(addr)
        logger.debug(f"MOV E,M: Reading from address {addr:04X}")

    # Add H register MOV implementations
    def _mov_h_a(self): self.registers['H'] = self.registers['A']
    def _mov_h_b(self): self.registers['H'] = self.registers['B']
    def _mov_h_c(self): self.registers['H'] = self.registers['C']
    def _mov_h_d(self): self.registers['H'] = self.registers['D']
    def _mov_h_e(self): self.registers['H'] = self.registers['E']
    def _mov_h_h(self): self.registers['H'] = self.registers['H']
    def _mov_h_l(self): self.registers['H'] = self.registers['L']
    def _mov_h_m(self): 
        addr = self.get_register_pair('H', 'L')
        self.registers['H'] = self.memory.read(addr)
        logger.debug(f"MOV H,M: Reading from address {addr:04X}")

    # Add L register MOV implementations
    def _mov_l_a(self): self.registers['L'] = self.registers['A']
    def _mov_l_b(self): self.registers['L'] = self.registers['B']
    def _mov_l_c(self): self.registers['L'] = self.registers['C']
    def _mov_l_d(self): self.registers['L'] = self.registers['D']
    def _mov_l_e(self): self.registers['L'] = self.registers['E']
    def _mov_l_h(self): self.registers['L'] = self.registers['H']
    def _mov_l_l(self): self.registers['L'] = self.registers['L']
    def _mov_l_m(self): 
        addr = self.get_register_pair('H', 'L')
        self.registers['L'] = self.memory.read(addr)
        logger.debug(f"MOV L,M: Reading from address {addr:04X}")

    # Add M register MOV implementations
    def _mov_m_b(self): 
        addr = self.get_register_pair('H', 'L')
        self.memory.write(addr, self.registers['B'])
    def _mov_m_c(self): 
        addr = self.get_register_pair('H', 'L')
        self.memory.write(addr, self.registers['C'])
    def _mov_m_d(self): 
        addr = self.get_register_pair('H', 'L')
        self.memory.write(addr, self.registers['D'])
    def _mov_m_e(self): 
        addr = self.get_register_pair('H', 'L')
        self.memory.write(addr, self.registers['E'])
        logger.debug(f"MOV M,E: Writing {self.registers['E']:02X} to address {addr:04X}")
    def _mov_m_h(self): 
        addr = self.get_register_pair('H', 'L')
        self.memory.write(addr, self.registers['H'])
        logger.debug(f"MOV M,H: Writing {self.registers['H']:02X} to address {addr:04X}")
    def _mov_m_l(self): 
        addr = self.get_register_pair('H', 'L')
        self.memory.write(addr, self.registers['L'])
        logger.debug(f"MOV M,L: Writing {self.registers['L']:02X} to address {addr:04X}")
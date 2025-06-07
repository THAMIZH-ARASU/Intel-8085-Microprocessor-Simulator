from typing import Dict, List
from Src.Utils.Logger import logger

class Assembler:
    """Simple 8085 Assembler for converting assembly to machine code"""
    
    def __init__(self):
        logger.info("Initializing 8085 Assembler")
        self.opcodes = {
            # Data Transfer
            'MOV A,A': 0x7F, 'MOV A,B': 0x78, 'MOV A,C': 0x79, 'MOV A,D': 0x7A,
            'MOV A,E': 0x7B, 'MOV A,H': 0x7C, 'MOV A,L': 0x7D, 'MOV A,M': 0x7E,
            'MOV B,A': 0x47, 'MOV B,B': 0x40, 'MOV B,C': 0x41, 'MOV B,D': 0x42,
            'MOV B,E': 0x43, 'MOV B,H': 0x44, 'MOV B,L': 0x45, 'MOV B,M': 0x46,
            'MOV C,A': 0x4F, 'MOV C,B': 0x48, 'MOV C,C': 0x49, 'MOV C,D': 0x4A,
            'MOV C,E': 0x4B, 'MOV C,H': 0x4C, 'MOV C,L': 0x4D, 'MOV C,M': 0x4E,
            'MOV D,A': 0x57, 'MOV D,B': 0x50, 'MOV D,C': 0x51, 'MOV D,D': 0x52,
            'MOV D,E': 0x53, 'MOV D,H': 0x54, 'MOV D,L': 0x55, 'MOV D,M': 0x56,
            'MOV E,A': 0x5F, 'MOV E,B': 0x58, 'MOV E,C': 0x59, 'MOV E,D': 0x5A,
            'MOV E,E': 0x5B, 'MOV E,H': 0x5C, 'MOV E,L': 0x5D, 'MOV E,M': 0x5E,
            'MOV H,A': 0x67, 'MOV H,B': 0x60, 'MOV H,C': 0x61, 'MOV H,D': 0x62,
            'MOV H,E': 0x63, 'MOV H,H': 0x64, 'MOV H,L': 0x65, 'MOV H,M': 0x66,
            'MOV L,A': 0x6F, 'MOV L,B': 0x68, 'MOV L,C': 0x69, 'MOV L,D': 0x6A,
            'MOV L,E': 0x6B, 'MOV L,H': 0x6C, 'MOV L,L': 0x6D, 'MOV L,M': 0x6E,
            'MOV M,A': 0x77, 'MOV M,B': 0x70, 'MOV M,C': 0x71, 'MOV M,D': 0x72,
            'MOV M,E': 0x73, 'MOV M,H': 0x74, 'MOV M,L': 0x75,
            
            # Immediate
            'MVI A': 0x3E, 'MVI B': 0x06, 'MVI C': 0x0E, 'MVI D': 0x16,
            'MVI E': 0x1E, 'MVI H': 0x26, 'MVI L': 0x2E, 'MVI M': 0x36,
            
            # Load pairs
            'LXI B': 0x01, 'LXI D': 0x11, 'LXI H': 0x21, 'LXI SP': 0x31,
            
            # Memory
            'LDA': 0x3A, 'STA': 0x32, 'LHLD': 0x2A, 'SHLD': 0x22,
            
            # Arithmetic
            'ADD A': 0x87, 'ADD B': 0x80, 'ADD C': 0x81, 'ADD D': 0x82,
            'ADD E': 0x83, 'ADD H': 0x84, 'ADD L': 0x85, 'ADD M': 0x86,
            'ADI': 0xC6,
            
            'ADC A': 0x8F, 'ADC B': 0x88, 'ADC C': 0x89, 'ADC D': 0x8A,
            'ADC E': 0x8B, 'ADC H': 0x8C, 'ADC L': 0x8D, 'ADC M': 0x8E,
            
            'SUB A': 0x97, 'SUB B': 0x90, 'SUB C': 0x91, 'SUB D': 0x92,
            'SUB E': 0x93, 'SUB H': 0x94, 'SUB L': 0x95, 'SUB M': 0x96,
            
            # Logical
            'ANA A': 0xA7, 'ANA B': 0xA0, 'ANA C': 0xA1, 'ANA D': 0xA2,
            'ANA E': 0xA3, 'ANA H': 0xA4, 'ANA L': 0xA5, 'ANA M': 0xA6,
            
            'ORA A': 0xB7, 'ORA B': 0xB0, 'ORA C': 0xB1, 'ORA D': 0xB2,
            'ORA E': 0xB3, 'ORA H': 0xB4, 'ORA L': 0xB5, 'ORA M': 0xB6,
            
            # Increment/Decrement
            'INR A': 0x3C, 'INR B': 0x04, 'INR C': 0x0C, 'INR D': 0x14,
            'INR E': 0x1C, 'INR H': 0x24, 'INR L': 0x2C, 'INR M': 0x34,
            'INX B': 0x03, 'INX D': 0x13, 'INX H': 0x23, 'INX SP': 0x33,
            
            'DCR A': 0x3D, 'DCR B': 0x05, 'DCR C': 0x0D, 'DCR D': 0x15,
            'DCR E': 0x1D, 'DCR H': 0x25, 'DCR L': 0x2D, 'DCR M': 0x35,
            'DCX B': 0x0B, 'DCX D': 0x1B, 'DCX H': 0x2B, 'DCX SP': 0x3B,
            
            # Jump
            'JMP': 0xC3, 'JZ': 0xCA, 'JNZ': 0xC2, 'JC': 0xDA, 'JNC': 0xD2,
            
            # Call/Return
            'CALL': 0xCD, 'RET': 0xC9,
            
            # Stack
            'PUSH B': 0xC5, 'PUSH D': 0xD5, 'PUSH H': 0xE5, 'PUSH PSW': 0xF5,
            'POP B': 0xC1, 'POP D': 0xD1, 'POP H': 0xE1, 'POP PSW': 0xF1,
            
            # Compare
            'CMP A': 0xBF, 'CMP B': 0xB8, 'CMP C': 0xB9, 'CMP D': 0xBA,
            'CMP E': 0xBB, 'CMP H': 0xBC, 'CMP L': 0xBD, 'CMP M': 0xBE,
            'CPI': 0xFE,
            
            # Control
            'HLT': 0x76, 'NOP': 0x00,
            
            # Arithmetic Instructions
            'SUI': 0xD6,  # Subtract immediate from accumulator
            
            'SBB A': 0x9F,  # Subtract with borrow accumulator from accumulator
            'SBB B': 0x98,  # Subtract with borrow register B from accumulator
            'SBB C': 0x99,  # Subtract with borrow register C from accumulator
            'SBB D': 0x9A,  # Subtract with borrow register D from accumulator
            'SBB E': 0x9B,  # Subtract with borrow register E from accumulator
            'SBB H': 0x9C,  # Subtract with borrow register H from accumulator
            'SBB L': 0x9D,  # Subtract with borrow register L from accumulator
            'SBB M': 0x9E,  # Subtract with borrow memory from accumulator
            
            # Logical Instructions
            'XRA A': 0xAF,  # Exclusive OR accumulator with accumulator
            'XRA B': 0xA8,  # Exclusive OR register B with accumulator
            'XRA C': 0xA9,  # Exclusive OR register C with accumulator
            'XRA D': 0xAA,  # Exclusive OR register D with accumulator
            'XRA E': 0xAB,  # Exclusive OR register E with accumulator
            'XRA H': 0xAC,  # Exclusive OR register H with accumulator
            'XRA L': 0xAD,  # Exclusive OR register L with accumulator
            'XRA M': 0xAE,  # Exclusive OR memory with accumulator
            
            # Rotate Instructions
            'RLC': 0x07,  # Rotate accumulator left
            'RRC': 0x0F,  # Rotate accumulator right
            'RAL': 0x17,  # Rotate accumulator left through carry
            'RAR': 0x1F,  # Rotate accumulator right through carry
            
            # Special Instructions
            'DAA': 0x27,  # Decimal adjust accumulator
            'CMA': 0x2F,  # Complement accumulator
            'STC': 0x37,  # Set carry flag
            'CMC': 0x3F,  # Complement carry flag
            'EI': 0xFB,   # Enable interrupts
            'DI': 0xF3,   # Disable interrupts
            'RIM': 0x20,  # Read interrupt mask
            'SIM': 0x30,  # Set interrupt mask
        }
    
    def assemble(self, assembly_code: str) -> List[int]:
        """Convert assembly code to machine code"""
        logger.info("Starting assembly process")
        machine_code = []
        lines = assembly_code.strip().split('\n')
        labels = {}
        
        # First pass: collect labels and remove comments
        address = 0
        processed_lines = []
        
        for line in lines:
            # Remove comments
            if ';' in line:
                line = line.split(';')[0]
            line = line.strip()
            
            if not line:
                continue
            
            # Handle labels
            if ':' in line:
                label = line.split(':')[0].strip()
                labels[label] = address
                line = line.split(':', 1)[1].strip()
            
            if line:
                processed_lines.append(line)
                # Estimate instruction size
                parts = line.split()
                if parts[0] in ['MVI', 'ADI', 'CPI', 'SUI']:
                    address += 2
                elif parts[0] in ['LXI', 'LDA', 'STA', 'LHLD', 'SHLD', 'JMP', 'JZ', 'JNZ', 'JC', 'JNC', 'CALL']:
                    address += 3
                else:
                    address += 1
        
        logger.debug(f"First pass complete. Labels: {labels}")
        
        # Second pass: generate machine code
        for line in processed_lines:
            logger.debug(f"Processing instruction: {line}")
            
            parts = line.split()
            mnemonic = parts[0]
            
            if len(parts) == 1:
                # Single instruction
                if mnemonic in self.opcodes:
                    machine_code.append(self.opcodes[mnemonic])
                    logger.debug(f"Added opcode: {self.opcodes[mnemonic]:02X}")
            elif len(parts) == 2:
                # Instruction with operand
                operand = parts[1]
                
                if mnemonic in ['MVI', 'ADI', 'CPI', 'SUI']:
                    # Handle immediate instructions
                    if mnemonic == 'MVI':
                        reg = operand.split(',')[0].strip()
                        value_str = operand.split(',')[1].strip()
                        opcode_key = f'{mnemonic} {reg}'
                        if opcode_key in self.opcodes:
                            machine_code.append(self.opcodes[opcode_key])
                            if value_str.startswith('#'):
                                value = int(value_str[1:], 16)
                            else:
                                value = int(value_str)
                            machine_code.append(value)
                            logger.debug(f"Added MVI instruction: {self.opcodes[opcode_key]:02X} {value:02X}")
                    else:
                        # Handle other immediate instructions (ADI, CPI, SUI)
                        machine_code.append(self.opcodes[mnemonic])
                        if operand.startswith('#'):
                            value = int(operand[1:], 16)
                        else:
                            value = int(operand)
                        machine_code.append(value)
                        logger.debug(f"Added immediate instruction: {self.opcodes[mnemonic]:02X} {value:02X}")
                        
                elif mnemonic in ['LXI']:
                    reg_pair = operand.split(',')[0].strip()
                    value_str = operand.split(',')[1].strip()
                    opcode_key = f'{mnemonic} {reg_pair}'
                    if opcode_key in self.opcodes:
                        machine_code.append(self.opcodes[opcode_key])
                        if value_str.startswith('#'):
                            value = int(value_str[1:], 16)
                        else:
                            value = int(value_str)
                        machine_code.append(value & 0xFF)
                        machine_code.append((value >> 8) & 0xFF)
                        logger.debug(f"Added LXI instruction: {self.opcodes[opcode_key]:02X} {value:04X}")
                
                elif mnemonic in ['JMP', 'JZ', 'JNZ', 'JC', 'JNC', 'CALL', 'LDA', 'STA', 'LHLD', 'SHLD']:
                    machine_code.append(self.opcodes[mnemonic])
                    if operand in labels:
                        addr = labels[operand]
                        logger.debug(f"Resolved label {operand} to address {addr:04X}")
                    elif operand.startswith('#'):
                        addr = int(operand[1:], 16)
                    else:
                        addr = int(operand)
                    machine_code.append(addr & 0xFF)
                    machine_code.append((addr >> 8) & 0xFF)
                    logger.debug(f"Added {mnemonic} instruction: {self.opcodes[mnemonic]:02X} {addr:04X}")
                
                else:
                    # Handle MOV, ADD, etc. with register operands
                    full_mnemonic = f'{mnemonic} {operand}'
                    if full_mnemonic in self.opcodes:
                        machine_code.append(self.opcodes[full_mnemonic])
                        logger.debug(f"Added register instruction: {self.opcodes[full_mnemonic]:02X}")
        
        logger.info(f"Assembly complete - Generated {len(machine_code)} bytes of machine code")
        return machine_code

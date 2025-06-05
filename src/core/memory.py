from typing import List
from src.utils.Logger import logger

class Memory:
    """8085 Memory Management Unit - 64KB addressable space"""
    
    def __init__(self):
        self.memory = [0x00] * 0x10000  # 64KB memory
        self.breakpoints = set()
        logger.info("Memory initialized with 64KB space")
    
    def read(self, address: int) -> int:
        """Read byte from memory address"""
        if 0 <= address <= 0xFFFF:
            value = self.memory[address]
            logger.debug(f"Memory READ: Address={address:04X}, Value={value:02X}")
            return value
        logger.error(f"Invalid memory read address: {address:04X}")
        raise ValueError(f"Invalid memory address: {address:04X}")
    
    def write(self, address: int, value: int) -> None:
        """Write byte to memory address"""
        if 0 <= address <= 0xFFFF and 0 <= value <= 0xFF:
            self.memory[address] = value
            logger.debug(f"Memory WRITE: Address={address:04X}, Value={value:02X}")
        else:
            logger.error(f"Invalid memory write: addr={address:04X}, val={value:02X}")
            raise ValueError(f"Invalid memory operation: addr={address:04X}, val={value:02X}")
    
    def read_word(self, address: int) -> int:
        """Read 16-bit word (little-endian)"""
        low = self.read(address)
        high = self.read(address + 1)
        return (high << 8) | low
    
    def write_word(self, address: int, value: int) -> None:
        """Write 16-bit word (little-endian)"""
        self.write(address, value & 0xFF)
        self.write(address + 1, (value >> 8) & 0xFF)
    
    def load_program(self, program: List[int], start_address: int = 0x8000):
        """Load program into memory"""
        for i, byte in enumerate(program):
            self.write(start_address + i, byte)

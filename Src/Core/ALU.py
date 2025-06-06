from typing import Dict, Tuple

class ALU:
    """8085 Arithmetic Logic Unit"""
    
    @staticmethod
    def add(a: int, b: int, carry: bool = False) -> Tuple[int, Dict[str, bool]]:
        """8-bit addition with flags"""
        if not (0 <= a <= 0xFF and 0 <= b <= 0xFF):
            raise ValueError(f"Invalid operands for addition: a={a:02X}, b={b:02X}")
            
        result = a + b + (1 if carry else 0)
        flags = {
            'C': result > 0xFF,
            'Z': (result & 0xFF) == 0,
            'S': (result & 0x80) != 0,
            'P': bin(result & 0xFF).count('1') % 2 == 0,
            'AC': (a & 0x0F) + (b & 0x0F) + (1 if carry else 0) > 0x0F
        }
        return result & 0xFF, flags
    
    @staticmethod
    def sub(a: int, b: int, borrow: bool = False) -> Tuple[int, Dict[str, bool]]:
        """8-bit subtraction with flags"""
        result = a - b - (1 if borrow else 0)
        flags = {
            'C': result < 0,
            'Z': (result & 0xFF) == 0,
            'S': (result & 0x80) != 0,
            'P': bin(result & 0xFF).count('1') % 2 == 0,
            'AC': (a & 0x0F) < (b & 0x0F) + (1 if borrow else 0)
        }
        return result & 0xFF, flags
    
    @staticmethod
    def logical_and(a: int, b: int) -> Tuple[int, Dict[str, bool]]:
        """Logical AND operation"""
        result = a & b
        flags = {
            'C': False,
            'Z': result == 0,
            'S': (result & 0x80) != 0,
            'P': bin(result).count('1') % 2 == 0,
            'AC': True  # Always set for logical operations
        }
        return result, flags
    
    @staticmethod
    def logical_or(a: int, b: int) -> Tuple[int, Dict[str, bool]]:
        """Logical OR operation"""
        result = a | b
        flags = {
            'C': False,
            'Z': result == 0,
            'S': (result & 0x80) != 0,
            'P': bin(result).count('1') % 2 == 0,
            'AC': False
        }
        return result, flags
    
    @staticmethod
    def logical_xor(a: int, b: int) -> Tuple[int, Dict[str, bool]]:
        """Logical XOR operation"""
        result = a ^ b
        flags = {
            'C': False,
            'Z': result == 0,
            'S': (result & 0x80) != 0,
            'P': bin(result).count('1') % 2 == 0,
            'AC': False
        }
        return result, flags
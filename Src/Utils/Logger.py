import logging

def setup_logger():
    """Configure logging for the 8085 simulator"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('8085_simulator.log', mode='a'),  # 'a' for append mode
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

logger = setup_logger() 
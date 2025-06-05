from src.utils.Logger import setup_logger
from src.gui.simulator_gui import SimulatorGUI

def main():
    """Main entry point for the 8085 simulator"""
    # Setup logging
    setup_logger()
    
    # Create and run the GUI
    app = SimulatorGUI()
    app.run()

if __name__ == "__main__":
    main() 
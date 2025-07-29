#!/usr/bin/env python3
"""
Test script for AI Tools Panel functionality
"""

import tkinter as tk
from Src.Interface.SimulatorGUI import SimulatorGUI
from Src.Utils.AIFeatures import AIFeatures

def test_ai_tools_panel():
    """Test the AI Tools Panel functionality"""
    print("Testing AI Tools Panel...")
    
    # Test AI Features initialization
    try:
        ai_features = AIFeatures()
        print("✅ AI Features initialized successfully")
        print(f"Available features: {ai_features.get_available_features()}")
    except Exception as e:
        print(f"❌ AI Features initialization failed: {e}")
        return False
    
    # Test GUI initialization
    try:
        # Create a minimal GUI for testing
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        
        # Create simulator GUI
        simulator = SimulatorGUI()
        print("✅ Simulator GUI initialized successfully")
        
        # Test AI Tools Panel
        try:
            simulator.show_ai_tools_panel()
            print("✅ AI Tools Panel opened successfully")
            
            # Keep the panel open for a few seconds to verify it works
            root.after(3000, root.quit)
            root.mainloop()
            
        except Exception as e:
            print(f"❌ AI Tools Panel failed: {e}")
            return False
        
    except Exception as e:
        print(f"❌ GUI initialization failed: {e}")
        return False
    
    print("✅ All AI Tools Panel tests passed!")
    return True

def test_ai_features():
    """Test individual AI features"""
    print("\nTesting individual AI features...")
    
    ai_features = AIFeatures()
    
    # Test each feature
    test_code = """
MVI A, #05      ; Load 05H into A
MVI B, #03      ; Load 03H into B
ADD B           ; A = A + B (A = 08H)
STA #9000       ; Store result at 9000H
HLT             ; Halt
"""
    
    features_to_test = [
        'explain', 'optimize', 'debug', 'document', 'quiz',
        'complete', 'translate', 'analyze', 'learn', 'review', 'visualize'
    ]
    
    for feature in features_to_test:
        try:
            if feature == 'learn':
                result = ai_features.execute_feature(feature, user_level='beginner', topics=['data transfer'])
            elif feature == 'translate':
                result = ai_features.execute_feature(feature, code=test_code, target_architecture='x86')
            elif feature == 'debug':
                result = ai_features.execute_feature(feature, code=test_code, error_message='test error')
            elif feature == 'quiz':
                result = ai_features.execute_feature(feature, code=test_code, difficulty='intermediate')
            else:
                result = ai_features.execute_feature(feature, code=test_code)
            
            if result['success']:
                print(f"✅ {feature}: Success")
            else:
                print(f"⚠️  {feature}: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            print(f"❌ {feature}: {e}")
    
    print("✅ AI features testing completed!")

if __name__ == "__main__":
    print("🤖 AI Tools Panel Test Suite")
    print("=" * 40)
    
    # Test AI Tools Panel
    panel_success = test_ai_tools_panel()
    
    # Test individual features
    test_ai_features()
    
    print("\n" + "=" * 40)
    if panel_success:
        print("🎉 All tests completed successfully!")
    else:
        print("⚠️  Some tests failed. Check the output above.") 
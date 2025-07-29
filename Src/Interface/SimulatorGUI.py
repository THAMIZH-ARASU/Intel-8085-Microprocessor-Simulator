import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog, ttk, simpledialog
import threading
import time
import os
from dotenv import load_dotenv
from typing import Tuple, List, Dict, Any

from Src.Core.Memory import Memory
from Src.Core.CPU import CPU
from Src.Core.Assembler import Assembler
from Src.Utils.Logger import logger
from Src.Utils.AIFeatures import AIFeatures

# Load environment variables
load_dotenv()

class SimulatorGUI:
    """8085 Simulator GUI Interface"""
    
    def __init__(self):
        logger.info("Initializing 8085 Simulator GUI")
        self.root = tk.Tk()
        self.root.title("Intel 8085 Microprocessor Simulator")
        self.root.geometry("1400x900")  # Increased window size

        # Initialize AI Features
        self.ai_features = AIFeatures()

        # Color themes
        self.themes = {
            'dark': {
                'bg_main': '#181c2f',
                'bg_panel': '#232946',
                'bg_code': '#121629',
                'fg_main': '#eebbc3',
                'fg_label': '#eebbc3',
                'fg_title': '#f6c177',
                'fg_desc': '#b8c1ec',
                'fg_reg': '#43d9ad',
                'fg_flag': '#ff595e',
                'btn_bg': '#f6c177',
                'btn_fg': '#181c2f',
                'btn2_bg': '#43d9ad',
                'btn2_fg': '#181c2f',
                'btn3_bg': '#eebbc3',
                'btn3_fg': '#181c2f',
                'btn_stop_bg': '#ff595e',
                'btn_stop_fg': '#fff',
                'btn_explain_bg': '#9b59b6',
                'btn_explain_fg': '#fff',
                'btn_ai_bg': '#8e44ad',
                'btn_ai_fg': '#fff',
                'status_bg': '#181c2f',
                'status_fg': '#f6c177',
                'entry_bg': '#232946',
                'entry_fg': '#eebbc3',
                'insert_bg': '#eebbc3',
                'mem_bg': '#121629',
                'mem_fg': '#eebbc3',
            },
            'light': {
                'bg_main': '#f7f7fa',
                'bg_panel': '#ffffff',
                'bg_code': '#f4f4f9',
                'fg_main': '#232946',
                'fg_label': '#232946',
                'fg_title': '#3d5a80',
                'fg_desc': '#7b8794',
                'fg_reg': '#0077b6',
                'fg_flag': '#e63946',
                'btn_bg': '#3d5a80',
                'btn_fg': '#fff',
                'btn2_bg': '#43d9ad',
                'btn2_fg': '#fff',
                'btn3_bg': '#f6c177',
                'btn3_fg': '#232946',
                'btn_stop_bg': '#e63946',
                'btn_stop_fg': '#fff',
                'btn_explain_bg': '#9b59b6',
                'btn_explain_fg': '#fff',
                'btn_ai_bg': '#8e44ad',
                'btn_ai_fg': '#fff',
                'status_bg': '#e0e1dd',
                'status_fg': '#3d5a80',
                'entry_bg': '#e0e1dd',
                'entry_fg': '#232946',
                'insert_bg': '#232946',
                'mem_bg': '#f4f4f9',
                'mem_fg': '#232946',
            }
        }
        self.current_theme = 'dark'
        self.root.configure(bg=self.themes[self.current_theme]['bg_main'])
        
        # Initialize simulator components
        self.memory = Memory()
        self.memory.on_memory_write = self.on_memory_write  # Register memory write callback
        self.cpu = CPU(self.memory)
        self.assembler = Assembler()
        
        # Control variables
        self.running = False
        self.step_mode = False
        
        self.create_widgets()
        self.update_display()
        logger.info("GUI initialization complete")

    def create_ai_menu(self):
        """Create AI features menu"""
        ai_menu = tk.Menu(self.menu_bar, tearoff=0)
        
        # AI Features submenu
        ai_menu.add_command(label="🤖 Explain Code", command=self.explain_code_with_ai)
        ai_menu.add_command(label="⚡ Optimize Code", command=self.optimize_code_with_ai)
        ai_menu.add_command(label="🐛 Debug Assistant", command=self.debug_with_ai)
        ai_menu.add_command(label="📚 Generate Quiz", command=self.generate_quiz_with_ai)
        ai_menu.add_command(label="📖 Create Documentation", command=self.document_with_ai)
        ai_menu.add_separator()
        ai_menu.add_command(label="🎯 Code Completion", command=self.complete_code_with_ai)
        ai_menu.add_command(label="🔄 Translate Code", command=self.translate_with_ai)
        ai_menu.add_command(label="📊 Performance Analysis", command=self.analyze_performance_with_ai)
        ai_menu.add_command(label="🎓 Learning Path", command=self.generate_learning_path_with_ai)
        ai_menu.add_command(label="🔧 Code Review", command=self.review_code_with_ai)
        ai_menu.add_command(label="📈 Visualize Algorithm", command=self.visualize_algorithm_with_ai)
        
        return ai_menu

    def explain_code_with_ai(self):
        """Explain the assembly code using AI"""
        self._execute_ai_feature('explain', {'code': self._get_code_from_editor()})

    def optimize_code_with_ai(self):
        """Optimize the assembly code using AI"""
        self._execute_ai_feature('optimize', {'code': self._get_code_from_editor()})

    def debug_with_ai(self):
        """Debug the assembly code using AI"""
        error_msg = self._get_error_input()
        self._execute_ai_feature('debug', {
            'code': self._get_code_from_editor(),
            'error_message': error_msg
        })

    def generate_quiz_with_ai(self):
        """Generate quiz from the assembly code using AI"""
        difficulty = self._get_difficulty_input()
        self._execute_ai_feature('quiz', {
            'code': self._get_code_from_editor(),
            'difficulty': difficulty
        })

    def document_with_ai(self):
        """Generate documentation for the assembly code using AI"""
        self._execute_ai_feature('document', {'code': self._get_code_from_editor()})

    def complete_code_with_ai(self):
        """Get code completion suggestions using AI"""
        context = self._get_context_input()
        self._execute_ai_feature('complete', {
            'code': self._get_code_from_editor(),
            'context': context
        })

    def translate_with_ai(self):
        """Translate code to other architecture using AI"""
        target_arch = self._get_target_architecture_input()
        self._execute_ai_feature('translate', {
            'code': self._get_code_from_editor(),
            'target_architecture': target_arch
        })

    def analyze_performance_with_ai(self):
        """Analyze performance of the assembly code using AI"""
        self._execute_ai_feature('analyze', {'code': self._get_code_from_editor()})

    def generate_learning_path_with_ai(self):
        """Generate learning path using AI"""
        user_level, topics = self._get_learning_path_input()
        self._execute_ai_feature('learn', {
            'user_level': user_level,
            'topics': topics
        })

    def review_code_with_ai(self):
        """Review the assembly code using AI"""
        self._execute_ai_feature('review', {'code': self._get_code_from_editor()})

    def visualize_algorithm_with_ai(self):
        """Visualize algorithm using AI"""
        self._execute_ai_feature('visualize', {'code': self._get_code_from_editor()})

    def _get_code_from_editor(self) -> str:
        """Get code from the editor"""
        code = self.code_text.get('1.0', tk.END).strip()
        if not code:
            messagebox.showwarning("No Code", "Please enter some assembly code first.")
            return ""
        return code

    def _get_error_input(self) -> str:
        """Get error message input from user"""
        return tk.simpledialog.askstring("Debug Assistant", "Enter error message (optional):") or ""

    def _get_difficulty_input(self) -> str:
        """Get difficulty level input from user"""
        difficulty = tk.simpledialog.askstring("Quiz Generator", "Enter difficulty (beginner/intermediate/advanced):", initialvalue="intermediate")
        return difficulty or "intermediate"

    def _get_context_input(self) -> str:
        """Get context input for code completion"""
        return tk.simpledialog.askstring("Code Completion", "Enter context (optional):") or ""

    def _get_target_architecture_input(self) -> str:
        """Get target architecture input"""
        architectures = ["x86", "ARM", "MIPS", "Z80", "6502"]
        arch = tk.simpledialog.askstring("Code Translation", f"Enter target architecture ({', '.join(architectures)}):", initialvalue="x86")
        return arch or "x86"

    def _get_learning_path_input(self) -> Tuple[str, List[str]]:
        """Get learning path input from user"""
        user_level = tk.simpledialog.askstring("Learning Path", "Enter your level (beginner/intermediate/advanced):", initialvalue="beginner") or "beginner"
        topics_input = tk.simpledialog.askstring("Learning Path", "Enter topics (comma-separated):", initialvalue="data transfer, arithmetic, branching") or "data transfer"
        topics = [topic.strip() for topic in topics_input.split(",")]
        return user_level, topics

    def _execute_ai_feature(self, feature: str, params: Dict[str, Any]):
        """Execute AI feature with parameters"""
        try:
            if not params.get('code', '').strip() and feature not in ['learn']:
                return
            
            self.status_bar.config(text=f"Executing {feature} with AI...")
            
            def api_call():
                try:
                    result = self.ai_features.execute_feature(feature, **params)
                    
                    if result['success']:
                        # Show the result in a new window
                        self.root.after(0, lambda: self._show_ai_result(feature, result))
                        self.root.after(0, lambda: self.status_bar.config(text=f"{feature.title()} completed"))
                    else:
                        # Handle different error types
                        error_message = result.get('message', 'Unknown error')
                        if result.get('error') == 'API_KEY_MISSING':
                            error_message = (
                                "GROQ_API_KEY not found in environment variables.\n"
                                "Please set GROQ_API_KEY in your .env file or environment variables."
                            )
                        
                        self.root.after(0, lambda: messagebox.showerror(f"AI {feature.title()} Error", error_message))
                        self.root.after(0, lambda: self.status_bar.config(text=f"{feature.title()} failed"))
                        
                except Exception as e:
                    self.root.after(0, lambda: messagebox.showerror("Error", f"Unexpected error: {str(e)}"))
                    self.root.after(0, lambda: self.status_bar.config(text=f"{feature.title()} failed"))
            
            threading.Thread(target=api_call, daemon=True).start()
            
        except Exception as e:
            logger.error(f"Error in {feature}: {str(e)}")
            messagebox.showerror("Error", f"Failed to execute {feature}: {str(e)}")
            self.status_bar.config(text=f"{feature.title()} failed")

    def _show_ai_result(self, feature: str, result: Dict[str, Any]):
        """Show AI result in a new window"""
        # Determine the content to show based on feature
        content_key_map = {
            'explain': 'explanation',
            'optimize': 'optimizations',
            'debug': 'debug_analysis',
            'document': 'documentation',
            'quiz': 'quiz',
            'complete': 'suggestions',
            'translate': 'translation',
            'analyze': 'performance_analysis',
            'learn': 'learning_path',
            'review': 'review',
            'visualize': 'visualization'
        }
        
        content_key = content_key_map.get(feature, 'data')
        content = result.get(content_key, result.get('data', 'No content available'))
        
        # Create window
        window = tk.Toplevel(self.root)
        window.title(f"AI {feature.title()} Result")
        window.geometry("900x700")
        
        # Apply theme colors
        theme = self.themes[self.current_theme]
        window.configure(bg=theme['bg_main'])
        
        # Create main frame
        main_frame = tk.Frame(window, bg=theme['bg_main'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text=f"🤖 AI {feature.title()} Result",
            bg=theme['bg_main'],
            fg=theme['fg_title'],
            font=('Arial', 16, 'bold')
        )
        title_label.pack(pady=(0, 10))
        
        # Create text widget for content
        content_text = scrolledtext.ScrolledText(
            main_frame,
            wrap=tk.WORD,
            bg=theme['bg_code'],
            fg=theme['fg_main'],
            font=('Consolas', 11),
            padx=15,
            pady=15,
            spacing1=2,
            spacing2=1,
            spacing3=2
        )
        content_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Format the content for better display
        formatted_content = self._format_content_for_display(content)
        
        # Insert the content
        content_text.insert('1.0', formatted_content)
        content_text.config(state=tk.DISABLED)
        
        # Button frame
        button_frame = tk.Frame(main_frame, bg=theme['bg_main'])
        button_frame.pack(pady=10)
        
        # Add close button
        close_btn = tk.Button(
            button_frame,
            text="Close",
            command=window.destroy,
            bg=theme['btn_bg'],
            fg=theme['btn_fg'],
            font=('Arial', 11, 'bold'),
            relief=tk.RAISED,
            bd=2
        )
        close_btn.pack(side=tk.LEFT, padx=5)
        
        # Add copy button
        copy_btn = tk.Button(
            button_frame,
            text="Copy to Clipboard",
            command=lambda: self._copy_to_clipboard(formatted_content),
            bg=theme['btn2_bg'],
            fg=theme['btn2_fg'],
            font=('Arial', 11, 'bold'),
            relief=tk.RAISED,
            bd=2
        )
        copy_btn.pack(side=tk.LEFT, padx=5)

    def _format_content_for_display(self, content: str) -> str:
        """Format the content for better display in the text widget"""
        # Convert markdown-style formatting to plain text with better structure
        formatted = content
        
        # Replace markdown bold with plain text emphasis
        formatted = formatted.replace('**', '')
        
        # Add spacing around section headers
        formatted = formatted.replace('\n**', '\n\n**')
        
        # Ensure proper spacing
        formatted = formatted.replace('\n\n\n', '\n\n')
        
        return formatted

    def _copy_to_clipboard(self, text: str):
        """Copy text to clipboard"""
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.root.update()  # Required for some systems
        messagebox.showinfo("Copied", "Content copied to clipboard!")

    def create_widgets(self):
        """Create and layout GUI widgets"""
        theme = self.themes[self.current_theme]
        
        # Create menu bar
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)
        
        # File menu
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="Load .asm", command=self.load_asm_file)
        file_menu.add_command(label="Save .asm", command=self.save_asm_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        self.menu_bar.add_cascade(label="File", menu=file_menu)
        
        # AI menu
        ai_menu = self.create_ai_menu()
        self.menu_bar.add_cascade(label="AI Features", menu=ai_menu)
        
        # Main frame
        self.main_frame = tk.Frame(self.root, bg=theme['bg_main'])
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Top bar for theme toggle and title
        self.top_bar = tk.Frame(self.main_frame, bg=theme['bg_main'])
        self.top_bar.pack(fill=tk.X, side=tk.TOP, anchor='n')
        self.title_label = tk.Label(
            self.top_bar, text="8085 Microprocessor Simulator",
            bg=theme['bg_main'], fg=theme['fg_title'],
            font=('Arial', 20, 'bold'), anchor='w'
        )
        self.title_label.pack(side=tk.LEFT, padx=10, pady=5)
        self.theme_btn = tk.Button(
            self.top_bar, text="🌙 Dark Mode" if self.current_theme=='light' else "☀️ Light Mode",
            command=self.toggle_theme,
            bg=theme['btn_bg'], fg=theme['btn_fg'], font=('Arial', 11, 'bold'), relief=tk.RAISED, bd=2
        )
        self.theme_btn.pack(side=tk.RIGHT, padx=10, pady=5)
        
        # Left panel - Code editor and controls
        self.left_panel = tk.Frame(self.main_frame, bg=theme['bg_panel'], relief=tk.RAISED, bd=2)
        self.left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Code editor
        code_frame = tk.LabelFrame(self.left_panel, text="Assembly Code", bg=theme['bg_panel'], fg=theme['fg_title'], font=('Arial', 14, 'bold'))
        code_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.code_text = scrolledtext.ScrolledText(
            code_frame, 
            width=50,  # Increased width to match right side
            height=20,
            bg=theme['bg_code'],
            fg=theme['fg_main'],
            insertbackground=theme['insert_bg'],
            font=('Consolas', 13),
            wrap=tk.NONE
        )
        self.code_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Memory Editor Section
        mem_edit_frame = tk.LabelFrame(self.left_panel, text="Memory Editor", bg=theme['bg_panel'], fg=theme['fg_title'], font=('Arial', 14, 'bold'))
        mem_edit_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Memory editor controls
        edit_controls = tk.Frame(mem_edit_frame, bg=theme['bg_panel'])
        edit_controls.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(edit_controls, text="Address:", bg=theme['bg_panel'], fg=theme['fg_label'], font=('Arial', 12)).pack(side=tk.LEFT)
        self.edit_addr_entry = tk.Entry(edit_controls, width=6, font=('Consolas', 12), bg=theme['entry_bg'], fg=theme['entry_fg'], insertbackground=theme['insert_bg'])
        self.edit_addr_entry.pack(side=tk.LEFT, padx=5)
        self.edit_addr_entry.insert(0, "9000")
        
        tk.Label(edit_controls, text="Value:", bg=theme['bg_panel'], fg=theme['fg_label'], font=('Arial', 12)).pack(side=tk.LEFT, padx=(10,0))
        self.edit_value_entry = tk.Entry(edit_controls, width=4, font=('Consolas', 12), bg=theme['entry_bg'], fg=theme['entry_fg'], insertbackground=theme['insert_bg'])
        self.edit_value_entry.pack(side=tk.LEFT, padx=5)
        
        tk.Button(edit_controls, text="Write", command=self.write_memory_byte, bg=theme['btn2_bg'], fg=theme['btn2_fg'], font=('Arial', 11, 'bold')).pack(side=tk.LEFT, padx=5)
        tk.Button(edit_controls, text="Read", command=self.read_memory_byte, bg=theme['btn3_bg'], fg=theme['btn3_fg'], font=('Arial', 11, 'bold')).pack(side=tk.LEFT, padx=5)
        
        # Control buttons
        control_frame = tk.Frame(self.left_panel, bg=theme['bg_panel'])
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        btn_style = {'bg': theme['btn_bg'], 'fg': theme['btn_fg'], 'font': ('Arial', 12, 'bold'), 'relief': tk.RAISED, 'bd': 2}
        
        tk.Button(control_frame, text="Assemble", command=self.assemble_code, **btn_style).pack(side=tk.LEFT, padx=2)
        tk.Button(control_frame, text="Run", command=self.run_program, **btn_style).pack(side=tk.LEFT, padx=2)
        tk.Button(control_frame, text="Step", command=self.step_program, **btn_style).pack(side=tk.LEFT, padx=2)
        tk.Button(control_frame, text="Reset", command=self.reset_cpu, **btn_style).pack(side=tk.LEFT, padx=2)
        tk.Button(control_frame, text="Stop", command=self.stop_program, bg=theme['btn_stop_bg'], fg=theme['btn_stop_fg'], font=('Arial', 12, 'bold')).pack(side=tk.LEFT, padx=2)
        
        # Add Load and Save buttons
        tk.Button(control_frame, text="Load .asm", command=self.load_asm_file, bg=theme['btn2_bg'], fg=theme['btn2_fg'], font=('Arial', 12, 'bold')).pack(side=tk.LEFT, padx=2)
        tk.Button(control_frame, text="Save .asm", command=self.save_asm_file, bg=theme['btn2_bg'], fg=theme['btn2_fg'], font=('Arial', 12, 'bold')).pack(side=tk.LEFT, padx=2)
        
        # Add AI Explain button (quick access)
        tk.Button(control_frame, text="🤖 Explain", command=self.explain_code_with_ai, bg=theme['btn_explain_bg'], fg=theme['btn_explain_fg'], font=('Arial', 12, 'bold')).pack(side=tk.LEFT, padx=2)
        
        # Right panel - CPU state and memory
        right_panel = tk.Frame(self.main_frame, bg=theme['bg_panel'])
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # CPU Registers
        reg_frame = tk.LabelFrame(right_panel, text="CPU Registers", bg=theme['bg_panel'], fg=theme['fg_title'], font=('Arial', 14, 'bold'))
        reg_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.reg_labels = {}
        reg_info = [
            ('A', 'Accumulator'), ('B', 'B Register'), ('C', 'C Register'),
            ('D', 'D Register'), ('E', 'E Register'), ('H', 'H Register'), ('L', 'L Register')
        ]
        
        for i, (reg, desc) in enumerate(reg_info):
            frame = tk.Frame(reg_frame, bg=theme['bg_panel'])
            frame.pack(fill=tk.X, padx=5, pady=2)
            
            tk.Label(frame, text=f"{reg}:", bg=theme['bg_panel'], fg=theme['fg_label'], font=('Consolas', 12, 'bold')).pack(side=tk.LEFT)
            self.reg_labels[reg] = tk.Label(frame, text="00", bg='#181c2f', fg=theme['fg_reg'], font=('Consolas', 14, 'bold'), width=4)
            self.reg_labels[reg].pack(side=tk.LEFT, padx=5)
            tk.Label(frame, text=desc, bg=theme['bg_panel'], fg=theme['fg_desc'], font=('Arial', 11)).pack(side=tk.LEFT, padx=10)
        
        # 16-bit registers
        reg16_frame = tk.LabelFrame(right_panel, text="16-bit Registers", bg=theme['bg_panel'], fg=theme['fg_title'], font=('Arial', 14, 'bold'))
        reg16_frame.pack(fill=tk.X, padx=10, pady=5)
        
        reg16_info = [('PC', 'Program Counter'), ('SP', 'Stack Pointer')]
        
        for reg, desc in reg16_info:
            frame = tk.Frame(reg16_frame, bg=theme['bg_panel'])
            frame.pack(fill=tk.X, padx=5, pady=2)
            
            tk.Label(frame, text=f"{reg}:", bg=theme['bg_panel'], fg=theme['fg_label'], font=('Consolas', 12, 'bold')).pack(side=tk.LEFT)
            self.reg_labels[reg] = tk.Label(frame, text="0000", bg='#181c2f', fg=theme['fg_reg'], font=('Consolas', 14, 'bold'), width=6)
            self.reg_labels[reg].pack(side=tk.LEFT, padx=5)
            tk.Label(frame, text=desc, bg=theme['bg_panel'], fg=theme['fg_desc'], font=('Arial', 11)).pack(side=tk.LEFT, padx=10)
        
        # Flags
        flags_frame = tk.LabelFrame(right_panel, text="Status Flags", bg=theme['bg_panel'], fg=theme['fg_title'], font=('Arial', 14, 'bold'))
        flags_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.flag_labels = {}
        flags_info = [('S', 'Sign'), ('Z', 'Zero'), ('AC', 'Aux Carry'), ('P', 'Parity'), ('C', 'Carry')]
        
        flags_grid = tk.Frame(flags_frame, bg=theme['bg_panel'])
        flags_grid.pack(padx=5, pady=5)
        
        for i, (flag, desc) in enumerate(flags_info):
            frame = tk.Frame(flags_grid, bg=theme['bg_panel'])
            frame.grid(row=i//3, column=i%3, padx=5, pady=2, sticky='w')
            
            tk.Label(frame, text=f"{flag}:", bg=theme['bg_panel'], fg=theme['fg_label'], font=('Consolas', 11, 'bold')).pack(side=tk.LEFT)
            self.flag_labels[flag] = tk.Label(frame, text="0", bg='#181c2f', fg=theme['fg_flag'], font=('Consolas', 12, 'bold'), width=2)
            self.flag_labels[flag].pack(side=tk.LEFT, padx=2)
        
        # Memory viewer
        mem_frame = tk.LabelFrame(right_panel, text="Memory View", bg=theme['bg_panel'], fg=theme['fg_title'], font=('Arial', 14, 'bold'))
        mem_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Memory address input
        addr_frame = tk.Frame(mem_frame, bg=theme['bg_panel'])
        addr_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(addr_frame, text="Address:", bg=theme['bg_panel'], fg=theme['fg_label'], font=('Arial', 12)).pack(side=tk.LEFT)
        self.addr_entry = tk.Entry(addr_frame, width=6, font=('Consolas', 12), bg=theme['entry_bg'], fg=theme['entry_fg'], insertbackground=theme['insert_bg'])
        self.addr_entry.pack(side=tk.LEFT, padx=5)
        self.addr_entry.insert(0, "8000")
        
        tk.Button(addr_frame, text="View", command=self.update_memory_view, bg=theme['btn2_bg'], fg=theme['btn2_fg'], font=('Arial', 11, 'bold')).pack(side=tk.LEFT, padx=5)
        tk.Button(addr_frame, text="Reset Memory", command=self.reset_memory, bg=theme['btn_stop_bg'], fg=theme['btn_stop_fg'], font=('Arial', 11, 'bold')).pack(side=tk.LEFT, padx=5)
        
        # Memory display
        self.memory_text = scrolledtext.ScrolledText(
            mem_frame,
            width=50,  # Matched width with code editor
            height=20,
            bg=theme['mem_bg'],
            fg=theme['mem_fg'],
            font=('Consolas', 18),
            state=tk.DISABLED
        )
        self.memory_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Status bar
        self.status_bar = tk.Label(
            self.root,
            text="Ready",
            bg=theme['status_bg'],
            fg=theme['status_fg'],
            font=('Arial', 12),
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def assemble_code(self):
        """Assemble the code in the editor"""
        try:
            logger.info("Starting code assembly")
            code = self.code_text.get('1.0', tk.END)
            machine_code = self.assembler.assemble(code)
            
            # Load into memory
            self.memory.load_program(machine_code)
            
            logger.info(f"Assembly successful - {len(machine_code)} bytes loaded")
            self.status_bar.config(text=f"Assembly successful - {len(machine_code)} bytes loaded")
            self.update_memory_view()
            
        except Exception as e:
            logger.error(f"Assembly failed: {str(e)}")
            messagebox.showerror("Assembly Error", str(e))
            self.status_bar.config(text="Assembly failed")
    
    def run_program(self):
        """Run the program continuously"""
        if not self.running:
            logger.info("Starting program execution")
            self.running = True
            self.step_mode = False
            self.status_bar.config(text="Running...")
            
            def execute_loop():
                try:
                    while self.running and not self.cpu.halted:
                        self.cpu.execute_instruction()
                        self.root.after(0, self.update_display)
                        time.sleep(0.1)  # Slow down for visualization
                    
                    if self.cpu.halted:
                        logger.info("Program halted")
                        self.status_bar.config(text="Program halted")
                    else:
                        logger.info("Execution stopped by user")
                        self.status_bar.config(text="Execution stopped")
                    
                    self.running = False
                except Exception as e:
                    logger.error(f"Runtime error: {str(e)}")
                    self.root.after(0, lambda: messagebox.showerror("Runtime Error", str(e)))
                    self.running = False
                    self.status_bar.config(text="Runtime error")
            
            threading.Thread(target=execute_loop, daemon=True).start()
    
    def step_program(self):
        """Execute single instruction"""
        try:
            if not self.cpu.halted:
                logger.debug("Executing single step")
                self.cpu.execute_instruction()
                self.update_display()
                self.status_bar.config(text="Step executed")
            else:
                logger.info("Attempted step while CPU halted")
                self.status_bar.config(text="Program halted")
        except Exception as e:
            logger.error(f"Step execution error: {str(e)}")
            messagebox.showerror("Runtime Error", str(e))
            self.status_bar.config(text="Runtime error")
    
    def stop_program(self):
        """Stop program execution"""
        logger.info("Stopping program execution")
        self.running = False
        self.status_bar.config(text="Execution stopped")
    
    def reset_cpu(self):
        """Reset CPU to initial state"""
        logger.info("Resetting CPU")
        self.running = False
        self.cpu = CPU(self.memory)
        self.update_display()
        self.status_bar.config(text="CPU reset")
    
    def update_display(self):
        """Update all display elements"""
        logger.debug("Updating display")
        # Update registers
        for reg in ['A', 'B', 'C', 'D', 'E', 'H', 'L']:
            self.reg_labels[reg].config(text=f"{self.cpu.registers[reg]:02X}")
        
        # Update 16-bit registers
        self.reg_labels['PC'].config(text=f"{self.cpu.PC:04X}")
        self.reg_labels['SP'].config(text=f"{self.cpu.SP:04X}")
        
        # Update flags
        for flag in ['S', 'Z', 'AC', 'P', 'C']:
            self.flag_labels[flag].config(text="1" if self.cpu.flags[flag] else "0")
    
    def update_memory_view(self):
        """Update memory display"""
        try:
            start_addr = int(self.addr_entry.get(), 16)
            logger.debug(f"Updating memory view starting at address {start_addr:04X}")
            self.memory_text.config(state=tk.NORMAL)
            self.memory_text.delete('1.0', tk.END)
            
            # Display 16 rows of 16 bytes each
            for row in range(16):
                addr = start_addr + (row * 16)
                line = f"{addr:04X}: "
                
                # Display bytes
                for col in range(16):
                    if addr + col < 0x10000:
                        byte = self.memory.read(addr + col)
                        line += f"{byte:02X} "
                    else:
                        line += "   "
                
                # Display ASCII representation
                line += "  "
                for col in range(16):
                    if addr + col < 0x10000:
                        byte = self.memory.read(addr + col)
                        # Only show printable ASCII
                        if 32 <= byte <= 126:
                            line += chr(byte)
                        else:
                            line += "."
                    else:
                        line += " "
                
                self.memory_text.insert(tk.END, line + "\n")
            
            self.memory_text.config(state=tk.DISABLED)
            
        except ValueError:
            logger.error(f"Invalid memory address: {self.addr_entry.get()}")
            messagebox.showerror("Error", "Invalid memory address")
    
    def load_asm_file(self):
        """Load assembly code from a .asm file"""
        try:
            file_path = filedialog.askopenfilename(
                title="Load Assembly File",
                filetypes=[("Assembly Files", "*.asm"), ("All Files", "*.*")]
            )
            
            if file_path:
                with open(file_path, 'r') as file:
                    code = file.read()
                    self.code_text.delete('1.0', tk.END)
                    self.code_text.insert('1.0', code)
                logger.info(f"Loaded assembly code from {file_path}")
                self.status_bar.config(text=f"Loaded assembly code from {file_path}")
        except Exception as e:
            logger.error(f"Error loading assembly file: {str(e)}")
            messagebox.showerror("Error", f"Failed to load assembly file: {str(e)}")
    
    def save_asm_file(self):
        """Save assembly code to a .asm file"""
        try:
            file_path = filedialog.asksaveasfilename(
                title="Save Assembly File",
                defaultextension=".asm",
                filetypes=[("Assembly Files", "*.asm"), ("All Files", "*.*")]
            )
            
            if file_path:
                code = self.code_text.get('1.0', tk.END)
                with open(file_path, 'w') as file:
                    file.write(code)
                logger.info(f"Saved assembly code to {file_path}")
                self.status_bar.config(text=f"Saved assembly code to {file_path}")
        except Exception as e:
            logger.error(f"Error saving assembly file: {str(e)}")
            messagebox.showerror("Error", f"Failed to save assembly file: {str(e)}")
    
    def write_memory_byte(self):
        """Write a byte value to the specified memory location"""
        try:
            addr = int(self.edit_addr_entry.get(), 16)
            value = int(self.edit_value_entry.get(), 16)
            
            if 0 <= addr <= 0xFFFF and 0 <= value <= 0xFF:
                self.memory.write(addr, value)
                logger.info(f"Wrote value {value:02X} to address {addr:04X}")
                self.status_bar.config(text=f"Wrote {value:02X} to address {addr:04X}")
                self.update_memory_view()  # Update the memory view to show the change
            else:
                raise ValueError("Address must be between 0000-FFFF and value between 00-FF")
        except ValueError as e:
            logger.error(f"Invalid memory write: {str(e)}")
            messagebox.showerror("Error", f"Invalid input: {str(e)}")
    
    def read_memory_byte(self):
        """Read a byte value from the specified memory location"""
        try:
            addr = int(self.edit_addr_entry.get(), 16)
            
            if 0 <= addr <= 0xFFFF:
                value = self.memory.read(addr)
                self.edit_value_entry.delete(0, tk.END)
                self.edit_value_entry.insert(0, f"{value:02X}")
                logger.info(f"Read value {value:02X} from address {addr:04X}")
                self.status_bar.config(text=f"Read {value:02X} from address {addr:04X}")
            else:
                raise ValueError("Address must be between 0000-FFFF")
        except ValueError as e:
            logger.error(f"Invalid memory read: {str(e)}")
            messagebox.showerror("Error", f"Invalid input: {str(e)}")
    
    def reset_memory(self):
        """Reset all memory locations to zero"""
        try:
            for addr in range(0x10000):  # Reset all 64KB of memory
                self.memory.write(addr, 0)
            logger.info("Memory reset to zero")
            self.status_bar.config(text="Memory reset to zero")
            self.update_memory_view()
        except Exception as e:
            logger.error(f"Error resetting memory: {str(e)}")
            messagebox.showerror("Error", f"Failed to reset memory: {str(e)}")
    
    def on_memory_write(self, address: int, value: int):
        """Callback for memory write operations"""
        # Only update memory view if the written address is visible in the current view
        try:
            start_addr = int(self.addr_entry.get(), 16)
            end_addr = start_addr + (16 * 16)  # 16 rows of 16 bytes
            if start_addr <= address < end_addr:
                self.update_memory_view()
        except ValueError:
            pass  # Ignore invalid address format
    
    def toggle_theme(self):
        self.current_theme = 'light' if self.current_theme == 'dark' else 'dark'
        self.apply_theme()

    def apply_theme(self):
        theme = self.themes[self.current_theme]
        self.root.configure(bg=theme['bg_main'])
        self.main_frame.configure(bg=theme['bg_main'])
        self.top_bar.configure(bg=theme['bg_main'])
        self.title_label.configure(bg=theme['bg_main'], fg=theme['fg_title'])
        self.theme_btn.configure(
            text="🌙 Dark Mode" if self.current_theme=='light' else "☀️ Light Mode",
            bg=theme['btn_bg'], fg=theme['btn_fg']
        )
        self.left_panel.configure(bg=theme['bg_panel'])

        # Update code editor section
        for widget in self.left_panel.winfo_children():
            if isinstance(widget, tk.LabelFrame):
                widget.configure(bg=theme['bg_panel'], fg=theme['fg_title'])
                for sub in widget.winfo_children():
                    if isinstance(sub, tk.Frame):
                        sub.configure(bg=theme['bg_panel'])
                        for subsub in sub.winfo_children():
                            if isinstance(subsub, tk.Label):
                                subsub.configure(bg=theme['bg_panel'], fg=theme['fg_label'])
                            elif isinstance(subsub, tk.Entry):
                                subsub.configure(bg=theme['entry_bg'], fg=theme['entry_fg'], insertbackground=theme['insert_bg'])
                            elif isinstance(subsub, tk.Button):
                                text = subsub.cget('text')
                                if text == 'Write':
                                    subsub.configure(bg=theme['btn2_bg'], fg=theme['btn2_fg'])
                                elif text == 'Read':
                                    subsub.configure(bg=theme['btn3_bg'], fg=theme['btn3_fg'])
                                elif text == '🤖 Explain':
                                    subsub.configure(bg=theme['btn_explain_bg'], fg=theme['btn_explain_fg'])
                                else:
                                    subsub.configure(bg=theme['btn_bg'], fg=theme['btn_fg'])
                    elif isinstance(sub, tk.Label):
                        sub.configure(bg=theme['bg_panel'], fg=theme['fg_title'])
                    elif isinstance(sub, scrolledtext.ScrolledText):
                        sub.configure(bg=theme['bg_code'], fg=theme['fg_main'], insertbackground=theme['insert_bg'])

        # Update control buttons
        for widget in self.left_panel.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.configure(bg=theme['bg_panel'])
                for btn in widget.winfo_children():
                    if isinstance(btn, tk.Button):
                        text = btn.cget('text')
                        if text == 'Stop' or text == 'Reset Memory':
                            btn.configure(bg=theme['btn_stop_bg'], fg=theme['btn_stop_fg'])
                        elif text in ['Write', 'Load .asm', 'Save .asm', 'View']:
                            btn.configure(bg=theme['btn2_bg'], fg=theme['btn2_fg'])
                        elif text == 'Read':
                            btn.configure(bg=theme['btn3_bg'], fg=theme['btn3_fg'])
                        elif text == '🤖 Explain':
                            btn.configure(bg=theme['btn_explain_bg'], fg=theme['btn_explain_fg'])
                        else:
                            btn.configure(bg=theme['btn_bg'], fg=theme['btn_fg'])
                    elif isinstance(btn, tk.Label):
                        btn.configure(bg=theme['bg_panel'], fg=theme['fg_label'])
                    elif isinstance(btn, tk.Entry):
                        btn.configure(bg=theme['entry_bg'], fg=theme['entry_fg'], insertbackground=theme['insert_bg'])

        # Update right panel sections
        for right_panel in self.main_frame.winfo_children():
            if isinstance(right_panel, tk.Frame) and right_panel is not self.left_panel and right_panel is not self.top_bar:
                right_panel.configure(bg=theme['bg_panel'])
                for section in right_panel.winfo_children():
                    if isinstance(section, tk.LabelFrame):
                        section.configure(bg=theme['bg_panel'], fg=theme['fg_title'])
                        for row in section.winfo_children():
                            if isinstance(row, tk.Frame):
                                row.configure(bg=theme['bg_panel'])
                                for item in row.winfo_children():
                                    if isinstance(item, tk.Label):
                                        # Register/flag/desc labels
                                        if item in self.reg_labels.values():
                                            item.configure(bg=theme['bg_code'], fg=theme['fg_reg'])
                                        elif item in self.flag_labels.values():
                                            item.configure(bg=theme['bg_code'], fg=theme['fg_flag'])
                                        else:
                                            item.configure(bg=theme['bg_panel'], fg=theme['fg_label'])
                                    elif isinstance(item, tk.Entry):
                                        item.configure(bg=theme['entry_bg'], fg=theme['entry_fg'], insertbackground=theme['insert_bg'])
                            elif isinstance(row, tk.Label):
                                row.configure(bg=theme['bg_panel'], fg=theme['fg_label'])
                            elif isinstance(row, scrolledtext.ScrolledText):
                                row.configure(bg=theme['mem_bg'], fg=theme['mem_fg'])
                    elif isinstance(section, scrolledtext.ScrolledText):
                        section.configure(bg=theme['mem_bg'], fg=theme['mem_fg'])
                    elif isinstance(section, tk.Frame):
                        section.configure(bg=theme['bg_panel'])
                        for item in section.winfo_children():
                            if isinstance(item, tk.Label):
                                item.configure(bg=theme['bg_panel'], fg=theme['fg_label'])
                            elif isinstance(item, tk.Entry):
                                item.configure(bg=theme['entry_bg'], fg=theme['entry_fg'], insertbackground=theme['insert_bg'])
                            elif isinstance(item, tk.Button):
                                text = item.cget('text')
                                if text == 'Reset Memory':
                                    item.configure(bg=theme['btn_stop_bg'], fg=theme['btn_stop_fg'])
                                elif text == 'View':
                                    item.configure(bg=theme['btn2_bg'], fg=theme['btn2_fg'])
                                else:
                                    item.configure(bg=theme['btn_bg'], fg=theme['btn_fg'])
        # Update all scrolledtext widgets (code and memory)
        self.code_text.configure(bg=theme['bg_code'], fg=theme['fg_main'], insertbackground=theme['insert_bg'])
        self.memory_text.configure(bg=theme['mem_bg'], fg=theme['mem_fg'])
        # Update register and flag value labels directly
        for reg in self.reg_labels:
            if reg in ['PC', 'SP']:
                self.reg_labels[reg].configure(bg=theme['bg_code'], fg=theme['fg_reg'])
            elif reg in ['A', 'B', 'C', 'D', 'E', 'H', 'L']:
                self.reg_labels[reg].configure(bg=theme['bg_code'], fg=theme['fg_reg'])
        for flag in self.flag_labels:
            self.flag_labels[flag].configure(bg=theme['bg_code'], fg=theme['fg_flag'])
        # Update status bar
        self.status_bar.configure(bg=theme['status_bg'], fg=theme['status_fg'])
        self.update_display()
    
    def run(self):
        """Start the GUI main loop"""
        logger.info("Starting GUI main loop")
        self.root.mainloop()
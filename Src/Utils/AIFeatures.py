import os
import requests
import re
import json
from typing import Optional, Dict, Any, List, Tuple
from dotenv import load_dotenv
from Src.Utils.Logger import logger

# Load environment variables
load_dotenv()

class AIFeatures:
    """Main AI features orchestrator for 8085 simulator"""
    
    def __init__(self):
        logger.info("Initializing AI Features")
        self.api_key = os.environ.get("GROQ_API_KEY", "")
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = "mistral-saba-24b"
        
        # Initialize all AI feature modules
        self.explainer = CodeExplainer(self.api_key, self.base_url, self.model)
        self.optimizer = CodeOptimizer(self.api_key, self.base_url, self.model)
        self.debugger = CodeDebugger(self.api_key, self.base_url, self.model)
        self.documenter = CodeDocumenter(self.api_key, self.base_url, self.model)
        self.quiz_generator = QuizGenerator(self.api_key, self.base_url, self.model)
        self.completer = CodeCompleter(self.api_key, self.base_url, self.model)
        self.translator = CodeTranslator(self.api_key, self.base_url, self.model)
        self.analyzer = PerformanceAnalyzer(self.api_key, self.base_url, self.model)
        self.learning_path = LearningPathGenerator(self.api_key, self.base_url, self.model)
        self.reviewer = CodeReviewer(self.api_key, self.base_url, self.model)
        self.visualizer = AlgorithmVisualizer(self.api_key, self.base_url, self.model)
        
        if self.api_key:
            logger.info("API key found for AI features")
        else:
            logger.warning("No API key found for AI features")
    
    def get_available_features(self) -> List[str]:
        """Get list of available AI features"""
        return [
            'explain', 'optimize', 'debug', 'document', 'quiz',
            'complete', 'translate', 'analyze', 'learn', 'review', 'visualize'
        ]
    
    def execute_feature(self, feature: str, **kwargs) -> Dict[str, Any]:
        """Execute any AI feature"""
        feature_map = {
            'explain': self.explainer.explain_code,
            'optimize': self.optimizer.optimize_code,
            'debug': self.debugger.debug_code,
            'document': self.documenter.generate_documentation,
            'quiz': self.quiz_generator.generate_quiz,
            'complete': self.completer.suggest_next_instruction,
            'translate': self.translator.translate_code,
            'analyze': self.analyzer.analyze_performance,
            'learn': self.learning_path.generate_learning_path,
            'review': self.reviewer.review_code,
            'visualize': self.visualizer.visualize_algorithm
        }
        
        if feature in feature_map:
            logger.info(f"Executing AI feature: {feature}")
            return feature_map[feature](**kwargs)
        else:
            logger.error(f"Unknown AI feature: {feature}")
            return {
                'success': False,
                'error': 'UNKNOWN_FEATURE',
                'message': f'Unknown feature: {feature}',
                'data': None
            }

class BaseAIFeature:
    """Base class for all AI features"""
    
    def __init__(self, api_key: str, base_url: str, model: str):
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
    
    def _make_api_call(self, system_prompt: str, user_prompt: str, max_tokens: int = 2000) -> Dict[str, Any]:
        """Make API call to Groq"""
        if not self.api_key:
            return {
                'success': False,
                'error': 'API_KEY_MISSING',
                'message': 'API key not set'
            }
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "max_tokens": max_tokens,
                "temperature": 0.3
            }
            
            response = requests.post(self.base_url, json=data, headers=headers, timeout=30)
            response.raise_for_status()
            
            response_data = response.json()
            choices = response_data.get("choices", [])
            
            if choices:
                return {
                    'success': True,
                    'data': choices[0]["message"]["content"].strip()
                }
            else:
                return {
                    'success': False,
                    'error': 'NO_RESPONSE',
                    'message': 'No response from AI service'
                }
                
        except Exception as e:
            logger.error(f"API call failed: {str(e)}")
            return {
                'success': False,
                'error': 'API_ERROR',
                'message': f'API call failed: {str(e)}'
            }

class CodeExplainer(BaseAIFeature):
    """AI-powered code explanation"""
    
    def explain_code(self, code: str) -> Dict[str, Any]:
        system_prompt = """You are an expert Intel 8085 microprocessor assembly programming instructor. 
Provide clear, educational explanations of 8085 assembly code with this structure:
1. **Program Overview**: Brief description of what the program does
2. **Instruction-by-Instruction Breakdown**: Explain each instruction's purpose and data flow
3. **Key Concepts**: Important 8085 concepts demonstrated
4. **Educational Notes**: Learning insights and tips

Use clear formatting with bold headers, bullet points, and structured explanations."""
        
        user_prompt = f"""Please explain this Intel 8085 assembly code:

```assembly
{code}
```

Provide a comprehensive, educational explanation following the structure outlined."""
        
        result = self._make_api_call(system_prompt, user_prompt)
        if result['success']:
            return {
                'success': True,
                'explanation': result['data'],
                'message': 'Explanation generated successfully'
            }
        return result

class CodeOptimizer(BaseAIFeature):
    """AI-powered code optimization"""
    
    def optimize_code(self, code: str) -> Dict[str, Any]:
        system_prompt = """You are an expert 8085 assembly optimizer. Analyze code and suggest improvements for:
- Performance optimizations
- Memory usage reductions
- Code size optimizations
- Alternative approaches
- Best practices

Provide specific, actionable recommendations with code examples."""
        
        user_prompt = f"""Analyze and optimize this 8085 assembly code:

```assembly
{code}
```

Provide optimization suggestions with explanations and improved code examples."""
        
        result = self._make_api_call(system_prompt, user_prompt)
        if result['success']:
            return {
                'success': True,
                'optimizations': result['data'],
                'message': 'Optimization analysis completed'
            }
        return result

class CodeDebugger(BaseAIFeature):
    """AI-powered debugging assistance"""
    
    def debug_code(self, code: str, error_message: str = "") -> Dict[str, Any]:
        system_prompt = """You are an expert 8085 assembly debugger. Help users identify and fix issues in their code.
Provide:
- Error analysis and common causes
- Step-by-step debugging guide
- Corrected code suggestions
- Prevention tips
- Best practices for avoiding similar issues"""
        
        user_prompt = f"""Debug this 8085 assembly code:

Code:
```assembly
{code}
```

Error: {error_message if error_message else "No specific error provided"}

Provide debugging assistance and solutions."""
        
        result = self._make_api_call(system_prompt, user_prompt)
        if result['success']:
            return {
                'success': True,
                'debug_analysis': result['data'],
                'message': 'Debug analysis completed'
            }
        return result

class CodeDocumenter(BaseAIFeature):
    """AI-powered documentation generation"""
    
    def generate_documentation(self, code: str) -> Dict[str, Any]:
        system_prompt = """You are an expert technical writer for 8085 assembly. Create comprehensive documentation including:
- Function/algorithm description
- Input/Output specifications
- Memory usage analysis
- Execution flow description
- Usage examples
- Performance characteristics
- Important notes and warnings"""
        
        user_prompt = f"""Create detailed documentation for this 8085 assembly code:

```assembly
{code}
```

Provide comprehensive documentation following the structure outlined."""
        
        result = self._make_api_call(system_prompt, user_prompt)
        if result['success']:
            return {
                'success': True,
                'documentation': result['data'],
                'message': 'Documentation generated successfully'
            }
        return result

class QuizGenerator(BaseAIFeature):
    """AI-powered quiz generation"""
    
    def generate_quiz(self, code: str, difficulty: str = "intermediate") -> Dict[str, Any]:
        system_prompt = """You are an expert 8085 assembly instructor. Create educational quizzes with:
- Multiple choice questions
- Fill-in-the-blank questions
- True/False questions
- Step-by-step execution questions
- Difficulty levels (Beginner/Intermediate/Advanced)

Provide questions, correct answers, and explanations."""
        
        user_prompt = f"""Create a quiz based on this 8085 assembly code:

```assembly
{code}
```

Difficulty level: {difficulty}

Generate a comprehensive quiz with various question types, correct answers, and explanations."""
        
        result = self._make_api_call(system_prompt, user_prompt)
        if result['success']:
            return {
                'success': True,
                'quiz': result['data'],
                'message': 'Quiz generated successfully'
            }
        return result

class CodeCompleter(BaseAIFeature):
    """AI-powered code completion"""
    
    def suggest_next_instruction(self, code: str, context: str = "") -> Dict[str, Any]:
        system_prompt = """You are an expert 8085 assembly programmer. Suggest the next logical instruction based on:
- Current code context
- Common programming patterns
- Best practices
- Register state considerations
- Memory usage patterns

Provide multiple suggestions with reasoning."""
        
        user_prompt = f"""Suggest the next instruction for this 8085 assembly code:

Current code:
```assembly
{code}
```

Context: {context if context else "No additional context provided"}

Provide logical next instructions with explanations."""
        
        result = self._make_api_call(system_prompt, user_prompt)
        if result['success']:
            return {
                'success': True,
                'suggestions': result['data'],
                'message': 'Code completion suggestions generated'
            }
        return result

class CodeTranslator(BaseAIFeature):
    """AI-powered code translation"""
    
    def translate_code(self, code: str, target_architecture: str) -> Dict[str, Any]:
        system_prompt = """You are an expert assembly language translator. Translate 8085 assembly code to other architectures.
Provide:
- Equivalent code in target architecture
- Key differences explained
- Optimization opportunities
- Portability considerations
- Architecture-specific notes"""
        
        user_prompt = f"""Translate this 8085 assembly code to {target_architecture}:

```assembly
{code}
```

Provide the translation with explanations of key differences and considerations."""
        
        result = self._make_api_call(system_prompt, user_prompt)
        if result['success']:
            return {
                'success': True,
                'translation': result['data'],
                'message': f'Code translated to {target_architecture}'
            }
        return result

class PerformanceAnalyzer(BaseAIFeature):
    """AI-powered performance analysis"""
    
    def analyze_performance(self, code: str) -> Dict[str, Any]:
        system_prompt = """You are an expert 8085 performance analyst. Analyze code performance including:
- Execution time analysis
- Memory usage breakdown
- Bottleneck identification
- Optimization suggestions
- Performance metrics
- Cycle count estimation
- Resource utilization"""
        
        user_prompt = f"""Analyze the performance of this 8085 assembly code:

```assembly
{code}
```

Provide comprehensive performance analysis with metrics and optimization suggestions."""
        
        result = self._make_api_call(system_prompt, user_prompt)
        if result['success']:
            return {
                'success': True,
                'performance_analysis': result['data'],
                'message': 'Performance analysis completed'
            }
        return result

class LearningPathGenerator(BaseAIFeature):
    """AI-powered learning path generation"""
    
    def generate_learning_path(self, user_level: str, topics: List[str]) -> Dict[str, Any]:
        system_prompt = """You are an expert 8085 assembly instructor. Create personalized learning paths including:
- Structured learning sequence
- Practice exercises
- Progressive difficulty
- Assessment points
- Recommended resources
- Learning milestones
- Time estimates"""
        
        user_prompt = f"""Create a learning path for 8085 assembly:

User Level: {user_level}
Topics: {', '.join(topics)}

Provide a comprehensive, structured learning path with exercises and milestones."""
        
        result = self._make_api_call(system_prompt, user_prompt)
        if result['success']:
            return {
                'success': True,
                'learning_path': result['data'],
                'message': 'Learning path generated successfully'
            }
        return result

class CodeReviewer(BaseAIFeature):
    """AI-powered code review"""
    
    def review_code(self, code: str) -> Dict[str, Any]:
        system_prompt = """You are an expert 8085 assembly code reviewer. Review code for:
- Code quality assessment
- Best practices evaluation
- Security considerations
- Maintainability analysis
- Style and readability
- Efficiency improvements
- Documentation quality"""
        
        user_prompt = f"""Review this 8085 assembly code:

```assembly
{code}
```

Provide comprehensive code review with suggestions for improvement."""
        
        result = self._make_api_call(system_prompt, user_prompt)
        if result['success']:
            return {
                'success': True,
                'review': result['data'],
                'message': 'Code review completed'
            }
        return result

class AlgorithmVisualizer(BaseAIFeature):
    """AI-powered algorithm visualization"""
    
    def visualize_algorithm(self, code: str) -> Dict[str, Any]:
        system_prompt = """You are an expert algorithm visualizer for 8085 assembly. Create visualization descriptions including:
- Step-by-step visualization
- Data flow diagrams
- State transitions
- Memory state changes
- Register value tracking
- Execution flow
- Visual metaphors"""
        
        user_prompt = f"""Create a visualization description for this 8085 algorithm:

```assembly
{code}
```

Provide detailed visualization description with step-by-step breakdown."""
        
        result = self._make_api_call(system_prompt, user_prompt)
        if result['success']:
            return {
                'success': True,
                'visualization': result['data'],
                'message': 'Algorithm visualization generated'
            }
        return result 
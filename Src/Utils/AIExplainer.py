import os
import requests
import re
from typing import Optional, Dict, Any
from dotenv import load_dotenv
from Src.Utils.Logger import logger

# Load environment variables
load_dotenv()

class AIExplainer:
    """AI-powered code explanation service using Groq API"""
    
    def __init__(self):
        logger.info("Initializing AI Explainer")
        self.api_key = os.environ.get("GROQ_API_KEY", "")
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = "mistral-saba-24b"
        
        if self.api_key:
            logger.info("API key found in environment variables")
        else:
            logger.warning("No API key found in environment variables")
    
    def get_api_key(self) -> Optional[str]:
        """Get the API key, return None if not set"""
        return self.api_key if self.api_key else None
    
    def set_api_key(self, api_key: str) -> None:
        """Set the API key"""
        logger.info("Setting new API key")
        self.api_key = api_key
    
    def _create_system_prompt(self) -> str:
        """Create the system prompt for 8085 assembly explanation"""
        return """You are an expert Intel 8085 microprocessor assembly programming instructor. 
Your role is to provide clear, educational explanations of 8085 assembly code.

When explaining code, follow this structure:

1. **Program Overview**: Brief description of what the program does
2. **Instruction-by-Instruction Breakdown**: 
   - Explain each instruction's purpose
   - Show how data flows through registers/memory
   - Highlight important concepts
3. **Key Concepts**: Explain any important 8085 concepts used
4. **Educational Notes**: Provide learning insights and tips

Use clear, structured formatting with:
- Bold headers for sections
- Bullet points for lists
- Code blocks for assembly snippets
- Explanatory text for concepts

Focus on educational value and clarity for students learning 8085 assembly."""
    
    def _create_user_prompt(self, code: str) -> str:
        """Create the user prompt for code explanation"""
        return f"""Please explain this Intel 8085 assembly code:

```assembly
{code}
```

Provide a comprehensive, educational explanation following the structure I outlined. 
Make sure to explain:
- What each instruction does and why it's used
- How data flows through the program
- The overall purpose and logic
- Any important 8085 concepts demonstrated
- Educational insights for learning assembly programming

Format the response with clear sections, bullet points, and structured explanations."""
    
    def _format_explanation(self, raw_explanation: str) -> str:
        """Format and structure the AI explanation"""
        logger.debug("Formatting AI explanation")
        # Clean up the explanation
        explanation = raw_explanation.strip()
        
        # Ensure proper markdown formatting
        explanation = re.sub(r'\*\*(.*?)\*\*', r'**\1**', explanation)  # Fix bold formatting
        explanation = re.sub(r'```assembly\n', '```assembly\n', explanation)  # Fix code blocks
        
        # Add structure if missing
        if not explanation.startswith('**'):
            # Try to add structure based on content
            lines = explanation.split('\n')
            formatted_lines = []
            
            # Add headers if they don't exist
            if not any('Program Overview' in line for line in lines):
                formatted_lines.append('**Program Overview**')
                formatted_lines.append('')
            
            formatted_lines.extend(lines)
            explanation = '\n'.join(formatted_lines)
        
        logger.debug(f"Formatted explanation length: {len(explanation)} characters")
        return explanation
    
    def explain_code(self, code: str) -> Dict[str, Any]:
        """
        Explain 8085 assembly code using AI
        
        Args:
            code (str): The assembly code to explain
            
        Returns:
            Dict[str, Any]: Result containing success status, explanation, and error info
        """
        logger.info("Starting AI code explanation")
        logger.debug(f"Code length: {len(code)} characters")
        
        if not self.api_key:
            logger.error("API key missing for AI explanation")
            return {
                'success': False,
                'error': 'API_KEY_MISSING',
                'message': 'GROQ_API_KEY not found in environment variables. Please set GROQ_API_KEY in your .env file or environment variables.',
                'explanation': None
            }
        
        if not code.strip():
            logger.warning("No code provided for AI explanation")
            return {
                'success': False,
                'error': 'NO_CODE',
                'message': 'No assembly code provided to explain.',
                'explanation': None
            }
        
        try:
            logger.info("Preparing API request to Groq")
            # Prepare the API request
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": self._create_system_prompt()},
                    {"role": "user", "content": self._create_user_prompt(code)}
                ],
                "max_tokens": 2000,
                "temperature": 0.3
            }
            
            logger.debug(f"Making API request to {self.base_url}")
            # Make the API call
            response = requests.post(
                self.base_url, 
                json=data, 
                headers=headers, 
                timeout=30
            )
            
            logger.debug(f"API response status: {response.status_code}")
            # Handle HTTP errors
            response.raise_for_status()
            
            # Parse the response
            response_data = response.json()
            choices = response_data.get("choices", [])
            
            if not choices:
                logger.error("No choices received from AI API")
                return {
                    'success': False,
                    'error': 'NO_RESPONSE',
                    'message': 'No explanation received from AI service.',
                    'explanation': None
                }
            
            # Extract and format the explanation
            raw_explanation = choices[0]["message"]["content"].strip()
            logger.debug(f"Raw explanation length: {len(raw_explanation)} characters")
            
            formatted_explanation = self._format_explanation(raw_explanation)
            
            logger.info("AI explanation completed successfully")
            return {
                'success': True,
                'error': None,
                'message': 'Explanation generated successfully',
                'explanation': formatted_explanation
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {str(e)}")
            return {
                'success': False,
                'error': 'API_ERROR',
                'message': f'Failed to connect to Groq API: {str(e)}',
                'explanation': None
            }
        except Exception as e:
            logger.error(f"Unexpected error in AI explanation: {str(e)}")
            return {
                'success': False,
                'error': 'UNEXPECTED_ERROR',
                'message': f'Unexpected error: {str(e)}',
                'explanation': None
            }
    
    def test_connection(self) -> Dict[str, Any]:
        """
        Test the API connection
        
        Returns:
            Dict[str, Any]: Result of connection test
        """
        logger.info("Testing AI API connection")
        
        if not self.api_key:
            logger.error("No API key available for connection test")
            return {
                'success': False,
                'error': 'API_KEY_MISSING',
                'message': 'API key not set'
            }
        
        try:
            logger.debug("Preparing connection test request")
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": self.model,
                "messages": [
                    {"role": "user", "content": "Hello"}
                ],
                "max_tokens": 10
            }
            
            logger.debug(f"Making test request to {self.base_url}")
            response = requests.post(
                self.base_url, 
                json=data, 
                headers=headers, 
                timeout=10
            )
            
            response.raise_for_status()
            logger.info("API connection test successful")
            
            return {
                'success': True,
                'error': None,
                'message': 'API connection successful'
            }
            
        except Exception as e:
            logger.error(f"API connection test failed: {str(e)}")
            return {
                'success': False,
                'error': 'CONNECTION_FAILED',
                'message': f'Connection test failed: {str(e)}'
            } 
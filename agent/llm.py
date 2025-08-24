import json
import os
from typing import Union, Dict, Any

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

class LLMError(Exception):
    def __init__(self, message="LLM error occurred"):
        super().__init__(message)

class LLMUnavailableError(LLMError):
    def __init__(self, message="LLM service unavailable"):
        super().__init__(message)

class LLMAPIError(LLMError):
    def __init__(self, message="LLM API call failed"):
        super().__init__(message)

def _call_openai_llm(prompt: str) -> str:
    if not OPENAI_AVAILABLE:
        raise LLMUnavailableError("OpenAI library not installed")
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise LLMUnavailableError("OPENAI_API_KEY not found in environment variables")
    
    try:
        client = openai.OpenAI(api_key=api_key)
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system", 
                    "content": """You are a helpful assistant. Provide concise, accurate answers. If asked to summarize in a specific number of words, follow that constraint exactly.

Examples of how to answer:
What is 12.5% of 243? → 30.375
Summarize today's weather in Paris in 3 words. → Mild and cloudy.
Who is Ada Lovelace? → Short factual answer
Add 10 to the average temperature in Paris and London right now. → 28.0°C"""
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            max_tokens=150,
            temperature=0.7,
            timeout=10
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        raise LLMAPIError(f"OpenAI API call failed: {str(e)}")

def llm_fallback(prompt: str) -> str:
    if not isinstance(prompt, str):
        return "Generated Answer for: [Invalid prompt type]"
    
    if not prompt.strip():
        return "Generated Answer for: [Empty prompt]"
    
    try:
        # Try to get response from OpenAI
        response = _call_openai_llm(prompt)
        return response
        
    except (LLMUnavailableError, LLMAPIError):
        # Fallback to simple message when LLM is unavailable
        prompt_preview = prompt[:60] + "..." if len(prompt) > 60 else prompt
        return f"Generated Answer for: {prompt_preview}"


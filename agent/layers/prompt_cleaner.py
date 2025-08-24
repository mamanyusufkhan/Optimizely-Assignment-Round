import re
from typing import Dict, List, Any, Optional
from .base import BaseLayer, LayerResult

class PromptCleaningError(Exception):
    def __init__(self, message="Prompt cleaning failed"):
        super().__init__(message)

class ExtensiblePromptCleaner(BaseLayer):
    def __init__(self, config: Optional[Dict[str, Any]] = None):
       
        super().__init__("prompt_cleaner", config)
        

        self.spelling_corrections = {
            "wether": "weather",
            "wheather": "weather", 
            "temprature": "temperature",
            "tempurature": "temperature",
            "calcualte": "calculate",
            "convertion": "conversion",
            "currancy": "currency",
            "curreny": "currency",
            "dollers": "dollars",
            "euros": "EUR",
            "whats": "what is",
            "wat is": "what is",
            "wht is": "what is",
            "ada lovelace": "Ada Lovelace",
            "albert einstein": "Albert Einstein",
            "marie curie": "Marie Curie"
        }
        
        self.abbreviations = {
            "avg": "average",
            "temp": "temperature",
            "calc": "calculate",
            "curr": "currency",
            "conv": "convert",
            "%": "percent"
        }
        
        self.math_patterns = [
            (r'(\d+)\s*x\s*(\d+)', r'\1 * \2'),
            (r'(\d+)\s*÷\s*(\d+)', r'\1 / \2'), 
            (r'(\d+)\s*−\s*(\d+)', r'\1 - \2'), 
        ]
        
        self.enable_spelling = True
        self.enable_abbreviations = True
        self.enable_math_normalization = True
        self.enable_case_normalization = True
    
    def initialize(self) -> None:
        super().initialize()
        
        if self.config:
            if "spelling_corrections" in self.config:
                self.spelling_corrections.update(self.config["spelling_corrections"])
            
            if "abbreviations" in self.config:
                self.abbreviations.update(self.config["abbreviations"])
            
            if "math_patterns" in self.config:
                self.math_patterns.extend(self.config["math_patterns"])
            
            for flag in ["enable_spelling", "enable_abbreviations", "enable_math_normalization", "enable_case_normalization"]:
                if flag in self.config:
                    setattr(self, flag, self.config[flag])
    
    def process(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> LayerResult:
        if not isinstance(input_data, str):
            return LayerResult(
                data=None,
                success=False,
                error_message=f"Expected string input, got {type(input_data)}"
            )
        
        if not input_data.strip():
            return LayerResult(
                data=None,
                success=False,
                error_message="Empty prompt provided"
            )
        
        try:
            cleaned_prompt = input_data.strip()
            metadata = {
                "original_prompt": input_data,
                "transformations": []
            }
            
            if self.enable_spelling:
                cleaned_prompt, spell_changes = self._apply_spelling_corrections(cleaned_prompt)
                if spell_changes:
                    metadata["transformations"].append({"type": "spelling", "changes": spell_changes})
            
            if self.enable_abbreviations:
                cleaned_prompt, abbrev_changes = self._apply_abbreviations(cleaned_prompt)
                if abbrev_changes:
                    metadata["transformations"].append({"type": "abbreviations", "changes": abbrev_changes})
            
            if self.enable_math_normalization:
                cleaned_prompt, math_changes = self._apply_math_normalization(cleaned_prompt)
                if math_changes:
                    metadata["transformations"].append({"type": "math", "changes": math_changes})
            
            if self.enable_case_normalization:
                cleaned_prompt = self._apply_case_normalization(cleaned_prompt)
            
            return LayerResult(
                data=cleaned_prompt,
                metadata=metadata,
                success=True
            )
            
        except Exception as e:
            return LayerResult(
                data=None,
                success=False,
                error_message=f"Prompt cleaning failed: {str(e)}"
            )
    
    def _apply_spelling_corrections(self, text: str) -> tuple[str, List[Dict[str, str]]]:
        corrected_text = text
        changes = []
        
        for wrong, correct in self.spelling_corrections.items():
            if wrong in corrected_text.lower():
                old_text = corrected_text
                corrected_text = re.sub(re.escape(wrong), correct, corrected_text, flags=re.IGNORECASE)
                if old_text != corrected_text:
                    changes.append({"from": wrong, "to": correct})
        
        return corrected_text, changes
    
    def _apply_abbreviations(self, text: str) -> tuple[str, List[Dict[str, str]]]:
        expanded_text = text
        changes = []
        
        for abbrev, expansion in self.abbreviations.items():
            pattern = r'\b' + re.escape(abbrev) + r'\b'
            if re.search(pattern, expanded_text, re.IGNORECASE):
                old_text = expanded_text
                expanded_text = re.sub(pattern, expansion, expanded_text, flags=re.IGNORECASE)
                if old_text != expanded_text:
                    changes.append({"from": abbrev, "to": expansion})
        
        return expanded_text, changes
    
    def _apply_math_normalization(self, text: str) -> tuple[str, List[Dict[str, str]]]:
        normalized_text = text
        changes = []
        
        for pattern, replacement in self.math_patterns:
            old_text = normalized_text
            normalized_text = re.sub(pattern, replacement, normalized_text)
            if old_text != normalized_text:
                changes.append({"pattern": pattern, "replacement": replacement})
        
        return normalized_text, changes
    
    def _apply_case_normalization(self, text: str) -> str:
        sentences = text.split('. ')
        normalized_sentences = []
        
        for sentence in sentences:
            if sentence:
                sentence = sentence[0].upper() + sentence[1:] if len(sentence) > 1 else sentence.upper()
                normalized_sentences.append(sentence)
        
        return '. '.join(normalized_sentences)

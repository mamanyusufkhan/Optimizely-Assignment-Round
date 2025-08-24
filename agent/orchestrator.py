from typing import Dict, Any, Optional, List
from .layers.base import LayerPipeline, LayerResult
from .layers.prompt_cleaner import ExtensiblePromptCleaner
from .layers.query_parser import ExtensibleQueryParser  
from .layers.execution_engine import ExtensibleExecutionEngine
from .logging_system import get_logger

class Orchestrator:
   
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.pipeline = LayerPipeline(self.config.get("pipeline_name", "agent_pipeline"))
        self.logger = get_logger()
        self._build_pipeline()
    
    def _build_pipeline(self) -> None:
        
        cleaner_config = self.config.get("prompt_cleaner", {})
        prompt_cleaner = ExtensiblePromptCleaner(cleaner_config)
        self.pipeline.add_layer(prompt_cleaner)
        
    
        parser_config = self.config.get("query_parser", {})
        query_parser = ExtensibleQueryParser(parser_config)
        self.pipeline.add_layer(query_parser)
        
        
        engine_config = self.config.get("execution_engine", {})
        execution_engine = ExtensibleExecutionEngine(engine_config)
        self.pipeline.add_layer(execution_engine)
        
        if "custom_layers" in self.config:
            for layer_config in self.config["custom_layers"]:
                layer_class = layer_config["class"]
                layer_params = layer_config.get("params", {})
                custom_layer = layer_class(layer_params)
                self.pipeline.add_layer(custom_layer)
    
    def process_query(self, raw_query: str, context: Optional[Dict[str, Any]] = None) -> str:
        self.logger.start_query(raw_query)
        
        try:
            result = self.pipeline.process(raw_query, context)
            
            if result.success:
                self.logger.complete_query(result.data, success=True)
                return str(result.data)
            else:
                
                self.logger.log_error(Exception(result.error_message or "Pipeline failed"), "during pipeline execution")
                
                try:
                    from .llm import llm_fallback
                    self.logger.log_fallback("pipeline execution failed")
                    fallback_result = llm_fallback(raw_query)
                    self.logger.complete_query(fallback_result, success=True)
                    return fallback_result
                except Exception as fallback_error:
                    self.logger.log_error(fallback_error, "during LLM fallback")
                    default_result = f"Generated Answer for: {raw_query}"
                    self.logger.complete_query(default_result, success=False)
                    return default_result
                    
        except Exception as e:
            self.logger.log_error(e, "during main pipeline execution")
            
            try:
                from .llm import llm_fallback
                self.logger.log_fallback("main execution failed")
                fallback_result = llm_fallback(raw_query)
                self.logger.complete_query(fallback_result, success=True)
                return fallback_result
            except Exception as fallback_error:
                self.logger.log_error(fallback_error, "during ultimate fallback")
                default_result = f"Generated Answer for: {raw_query}"
                self.logger.complete_query(default_result, success=False)
                return default_result
                return llm_fallback(raw_query)
            except Exception:
                return f"Generated Answer for: {raw_query}"
    
    def get_pipeline_info(self) -> Dict[str, Any]:
        return {
            "pipeline_name": self.pipeline.name,
            "layers": [str(layer) for layer in self.pipeline.layers],
            "layer_count": len(self.pipeline.layers),
            "config": self.config
        }
    
    def add_custom_layer(self, layer, position: Optional[int] = None) -> None:
        if position is not None:
            self.pipeline.layers.insert(position, layer)
        else:
            self.pipeline.add_layer(layer)


def create_orchestrator(preset: str = "default", custom_config: Optional[Dict[str, Any]] = None) -> Orchestrator:
    presets = {
        "default": {
            "pipeline_name": "default_agent",
            "prompt_cleaner": {
                "enable_spelling": True,
                "enable_abbreviations": True,
                "enable_math_normalization": True
            },
            "query_parser": {
                "fallback_strategy": "llm"
            },
            "execution_engine": {
                "enable_fallback": True
            }
        },
        
        "minimal": {
            "pipeline_name": "minimal_agent",
            "prompt_cleaner": {
                "enable_spelling": False,
                "enable_abbreviations": False,
                "enable_math_normalization": True
            },
            "query_parser": {
                "patterns": [] 
            }
        },
        
        "enhanced": {
            "pipeline_name": "enhanced_agent",
            "prompt_cleaner": {
                "enable_spelling": True,
                "enable_abbreviations": True,
                "enable_math_normalization": True,
                "enable_case_normalization": True,
                "spelling_corrections": {
                    "wat": "what",
                    "wth": "what"
                }
            },
            "query_parser": {
                "enable_advanced_patterns": True
            },
            "execution_engine": {
                "enable_detailed_logging": True
            }
        }
    }
    
    config = presets.get(preset, presets["default"]).copy()
    
    
    if custom_config:
        config.update(custom_config)
    
    return Orchestrator(config)

# Example usage and extension patterns
class CustomLoggingLayer:
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.name = "logger"
        self.config = config or {}
        self.initialized = False
    
    def initialize(self) -> None:
        
        self.initialized = True
        print(f"[Logger] Initialized with config: {self.config}")
    
    def process(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> LayerResult:
    
        print(f"[Logger] Processing: {input_data}")
        return LayerResult(data=input_data, success=True)
    
    def cleanup(self) -> None:
        print("[Logger] Cleaned up")

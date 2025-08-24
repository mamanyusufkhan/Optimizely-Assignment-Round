"""
Base layer interface for the agent system.

This module defines the abstract base classes and interfaces that all layers must implement.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from dataclasses import dataclass

@dataclass
class LayerResult:
    data: Any
    metadata: Optional[Dict[str, Any]] = None
    success: bool = True
    error_message: Optional[str] = None

class BaseLayer(ABC):
    def __init__(self, name: str, config: Optional[Dict[str, Any]] = None):
        self.name = name
        self.config = config or {}
        self.initialized = False
    
    def initialize(self) -> None:
        self.initialized = True
    
    @abstractmethod
    def process(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> LayerResult:
        pass
    
    def cleanup(self) -> None:
        pass
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}')"

class LayerPipeline:
    
    def __init__(self, name: str = "default"):
        self.name = name
        self.layers = []
        self.context = {}
    
    def add_layer(self, layer: BaseLayer) -> 'LayerPipeline':
        
        if not isinstance(layer, BaseLayer):
            raise TypeError(f"Layer must be instance of BaseLayer, got {type(layer)}")
        
        self.layers.append(layer)
        return self
    
    def process(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> LayerResult:
        
        for layer in self.layers:
            if not layer.initialized:
                layer.initialize()
        
        processing_context = {**self.context}
        if context:
            processing_context.update(context)
        
        current_data = input_data
        
        for layer in self.layers:
            try:
                result = layer.process(current_data, processing_context)
                
                if not result.success:
                    return LayerResult(
                        data=None,
                        success=False,
                        error_message=f"Layer {layer.name} failed: {result.error_message}"
                    )
                
                current_data = result.data
                
                if result.metadata:
                    processing_context[f"{layer.name}_metadata"] = result.metadata
                    
            except Exception as e:
                return LayerResult(
                    data=None,
                    success=False,
                    error_message=f"Layer {layer.name} error: {str(e)}"
                )
        
        return LayerResult(
            data=current_data,
            metadata=processing_context,
            success=True
        )
    
    def cleanup(self) -> None:
        for layer in self.layers:
            try:
                layer.cleanup()
            except Exception:
                pass 

"""
Logging system for the extensible agent.
Provides structured logging for debugging and monitoring.
"""

import logging
import time
import json
from typing import Any, Dict, Optional
from datetime import datetime


class AgentLogger:

    
    def __init__(self, log_level: str = "INFO"):
        self.logger = logging.getLogger("ExtensibleAgent")
        self.logger.setLevel(getattr(logging, log_level.upper()))
        
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        
        self.query_start_time = None
        self.current_query = None
    
    def start_query(self, query: str) -> None:
        self.current_query = query
        self.query_start_time = time.time()
        self.logger.info(f"Starting query: '{query}'")
    
    def log_parsing(self, query_type: str, steps: int, pattern: str) -> None:
    
        self.logger.info(f"Parsed as {query_type} with {steps} steps (pattern: {pattern})")
    
    def log_execution_step(self, step_num: int, tool: str, operation: str, params: Dict[str, Any]) -> None:
        safe_params = {k: str(v)[:100] for k, v in params.items()}
        self.logger.info(f"Step {step_num}: {tool}.{operation}({safe_params})")
    
    def log_step_result(self, step_num: int, result: Any, execution_time: float) -> None:
        result_str = str(result)[:200] if result else "None"
        self.logger.info(f"Step {step_num} completed in {execution_time:.3f}s: {result_str}")
    
    def log_variable_storage(self, var_name: str, value: Any) -> None:
        value_str = str(value)[:100] if value else "None"
        self.logger.debug(f"Stored variable '{var_name}': {value_str}")
    
    def log_error(self, error: Exception, context: str = "") -> None:
        self.logger.error(f"Error {context}: {type(error).__name__}: {str(error)}")
    
    def log_fallback(self, reason: str) -> None:
        self.logger.warning(f"Falling back to LLM: {reason}")
    
    def complete_query(self, result: Any, success: bool = True) -> None:
        if self.query_start_time:
            total_time = time.time() - self.query_start_time
            result_str = str(result)[:200] if result else "None"
            
            if success:
                self.logger.info(f"Query completed in {total_time:.3f}s: {result_str}")
            else:
                self.logger.error(f"Query failed after {total_time:.3f}s: {result_str}")
        
        self.query_start_time = None
        self.current_query = None
    
    def log_performance_metrics(self, metrics: Dict[str, Any]) -> None:
        self.logger.info(f"Metrics: {json.dumps(metrics, indent=2)}")


# Global logger instance
agent_logger = AgentLogger()


def get_logger() -> AgentLogger:
    return agent_logger


def set_log_level(level: str) -> None:
    agent_logger.logger.setLevel(getattr(logging, level.upper()))

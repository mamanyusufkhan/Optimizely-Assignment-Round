from dataclasses import dataclass
from enum import Enum
from typing import List, Any, Dict, Optional


class QueryType(Enum):
    SINGLE_TOOL = "single_tool"
    MULTI_STEP = "multi_step"
    LLM_REQUIRED = "llm_required"
    UNKNOWN = "unknown"


@dataclass
class ExecutionStep:
    tool: str
    operation: str
    parameters: Dict[str, Any]
    description: str = ""
    variables: Optional[Dict[str, str]] = None
    
    def __post_init__(self):
        if self.variables is None:
            self.variables = {}


@dataclass
class ExecutionPlan:
    type: QueryType
    steps: List[ExecutionStep]
    description: str = ""
    confidence: float = 1.0
    
    def __post_init__(self):
        if not self.steps:
            self.steps = []

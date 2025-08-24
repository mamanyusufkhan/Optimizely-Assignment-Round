
import time
from typing import Dict, Any, Optional, Callable, List
from abc import ABC, abstractmethod
from .base import BaseLayer, LayerResult
from .data_structures import ExecutionPlan, ExecutionStep, QueryType
from ..logging_system import get_logger

class ExecutionError(Exception):
    def __init__(self, message="Execution error occurred"):
        super().__init__(message)

class ToolNotFoundError(ExecutionError):
    def __init__(self, tool_name: str):
        super().__init__(f"Tool not found: {tool_name}")

class VariableSubstitutionError(ExecutionError):
    def __init__(self, message="Variable substitution failed"):
        super().__init__(message)

class ToolAdapter(ABC):
    def __init__(self, name: str, operations: Dict[str, Callable]):
        self.name = name
        self.operations = operations
    
    @abstractmethod
    def execute_operation(self, operation: str, params: Dict[str, Any]) -> Any:
        pass
    
    def has_operation(self, operation: str) -> bool:
        return operation in self.operations

class StandardToolAdapter(ToolAdapter):
    
    def execute_operation(self, operation: str, params: Dict[str, Any]) -> Any:
        if operation not in self.operations:
            raise ExecutionError(f"Operation '{operation}' not found in tool '{self.name}'")
        
        function = self.operations[operation]
        return function(**params)

class WeatherToolAdapter(ToolAdapter):
    def execute_operation(self, operation: str, params: Dict[str, Any]) -> Any:
        """Execute weather operation with special handling."""
        if operation not in self.operations:
            raise ExecutionError(f"Operation '{operation}' not found in tool '{self.name}'")
        
        function = self.operations[operation]
        result = function(**params)
       
        if isinstance(result, str) and "°C" in result:
            numeric_value = float(result.replace("°C", ""))
            return {
                "display": result,  # "18°C" 
                "numeric": numeric_value,  # 18.0
                "value": numeric_value  # Alternative numeric access
            }
        
        return result

class CalculatorToolAdapter(ToolAdapter):
    def execute_operation(self, operation: str, params: Dict[str, Any]) -> Any:
        """Execute calculator operation with special handling."""
        if operation not in self.operations:
            raise ExecutionError(f"Operation '{operation}' not found in tool '{self.name}'")
        
        function = self.operations[operation]
        
        if operation == "calculate":
            return function(**params)
        else:
            return function(**params)

class LLMToolAdapter(ToolAdapter):
    
    def execute_operation(self, operation: str, params: Dict[str, Any]) -> Any:
        if operation not in self.operations:
            raise ExecutionError(f"Operation '{operation}' not found in tool '{self.name}'")
        
        function = self.operations[operation]
        
        if operation == "llm_fallback":
            prompt = params.get("prompt", "")
            return function(prompt)
        else:
            return function(**params)

class ExecutionStrategy(ABC):
    
    @abstractmethod
    def can_handle(self, plan: ExecutionPlan) -> bool:
        pass
    
    @abstractmethod
    def execute(self, plan: ExecutionPlan, engine: 'ExtensibleExecutionEngine') -> Any:
        pass

class SingleToolStrategy(ExecutionStrategy):
    
    def can_handle(self, plan: ExecutionPlan) -> bool:
        return plan.type == QueryType.SINGLE_TOOL
    
    def execute(self, plan: ExecutionPlan, engine: 'ExtensibleExecutionEngine') -> Any:
        if not plan.steps:
            raise ExecutionError("No steps in execution plan")
        
        step = plan.steps[0]
        result = engine._execute_step(step)
        
        return engine._format_result(result, step.tool, step.operation)

class MultiStepStrategy(ExecutionStrategy):
    """Strategy for executing multi-step plans."""
    
    def can_handle(self, plan: ExecutionPlan) -> bool:
        return plan.type == QueryType.MULTI_STEP
    
    def execute(self, plan: ExecutionPlan, engine: 'ExtensibleExecutionEngine') -> Any:
        if not plan.steps:
            raise ExecutionError("No steps in execution plan")
        
        engine.variables = {}
        last_result = None
        is_temperature_calculation = False
        
        plan_description = plan.description.lower()
        if "temperature" in plan_description or any("weather" in step.description.lower() for step in plan.steps):
            is_temperature_calculation = True
            engine.logger.logger.debug("🌡️ Detected temperature calculation context")
        
        for i, step in enumerate(plan.steps, 1):
            step_start_time = time.time()

            engine.logger.log_execution_step(
                step_num=i,
                tool=step.tool,
                operation=step.operation,
                params=step.parameters
            )
            
            substituted_params = engine._substitute_variables(step.parameters)
            
            execution_step = ExecutionStep(
                tool=step.tool,
                operation=step.operation,
                parameters=substituted_params,
                description=step.description,
                variables=step.variables
            )
            
            result = engine._execute_step(execution_step)
            
            step_time = time.time() - step_start_time
            engine.logger.log_step_result(i, result, step_time)
            
            if step.variables and "result_var" in step.variables:
                var_name = step.variables["result_var"]
                engine.variables[var_name] = result
                engine.logger.log_variable_storage(var_name, result)
            
            last_result = result
        
        if is_temperature_calculation and isinstance(last_result, (int, float)):
            final_result = f"{last_result}°C"
            engine.logger.logger.debug(f"🌡️ Applied temperature unit: {final_result}")
            return final_result
        
        return last_result

class LLMStrategy(ExecutionStrategy):
    
    def can_handle(self, plan: ExecutionPlan) -> bool:
        return plan.type == QueryType.LLM_REQUIRED
    
    def execute(self, plan: ExecutionPlan, engine: 'ExtensibleExecutionEngine') -> Any:
        if not plan.steps:
            from ..llm import llm_fallback
            return llm_fallback(plan.original_query)
        
        step = plan.steps[0]
        return engine._execute_step(step)

class ExtensibleExecutionEngine(BaseLayer):
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__("execution_engine", config)
        self.tool_adapters: Dict[str, ToolAdapter] = {}
        self.execution_strategies: List[ExecutionStrategy] = []
        self.variables: Dict[str, Any] = {}
        self.logger = get_logger()
    
    def initialize(self) -> None:
        super().initialize()
        
        self._register_default_tools()
        
        self._register_default_strategies()
        
        if self.config:
            if "custom_tools" in self.config:
                for tool_name, tool_config in self.config["custom_tools"].items():
                    self.register_tool_adapter(tool_name, tool_config["adapter"])
            
            if "custom_strategies" in self.config:
                for strategy in self.config["custom_strategies"]:
                    self.register_execution_strategy(strategy)
    
    def _register_default_tools(self) -> None:
        from ..tools import calculator, weather, knowledge_base, currency
        from ..llm import llm_fallback
        
        calc_adapter = CalculatorToolAdapter("calculator", {
            "calculate": calculator.calculate,
            "add": calculator.add,
            "subtract": calculator.subtract,
            "multiply": calculator.multiply,
            "divide": calculator.divide,
            "percent_of": calculator.percent_of,
            "average": calculator.average,
            "power": calculator.power
        })
        self.register_tool_adapter("calculator", calc_adapter)
        
        weather_adapter = WeatherToolAdapter("weather", {
            "get_weather": weather.get_weather
        })
        self.register_tool_adapter("weather", weather_adapter)
        
        kb_adapter = StandardToolAdapter("knowledge_base", {
            "kb_lookup": knowledge_base.kb_lookup
        })
        self.register_tool_adapter("knowledge_base", kb_adapter)
        
        currency_adapter = StandardToolAdapter("currency", {
            "currency_convert": currency.currency_convert
        })
        self.register_tool_adapter("currency", currency_adapter)
        
        llm_adapter = LLMToolAdapter("llm", {
            "llm_fallback": llm_fallback,
            "generate": llm_fallback
        })
        self.register_tool_adapter("llm", llm_adapter)
    
    def _register_default_strategies(self) -> None:
        self.register_execution_strategy(SingleToolStrategy())
        self.register_execution_strategy(MultiStepStrategy())
        self.register_execution_strategy(LLMStrategy())
    
    def register_tool_adapter(self, name: str, adapter: ToolAdapter) -> None:
        self.tool_adapters[name] = adapter
    
    def register_execution_strategy(self, strategy: ExecutionStrategy) -> None:
        self.execution_strategies.append(strategy)
    
    def process(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> LayerResult:
        if not isinstance(input_data, ExecutionPlan):
            return LayerResult(
                data=None,
                success=False,
                error_message=f"Expected ExecutionPlan input, got {type(input_data)}"
            )
        
        plan = input_data
        
        try:
            metadata = {
                "plan_type": plan.type.value,
                "steps_count": len(plan.steps),
                "strategy_used": None
            }
            
            for strategy in self.execution_strategies:
                if strategy.can_handle(plan):
                    result = strategy.execute(plan, self)
                    metadata["strategy_used"] = strategy.__class__.__name__
                    
                    return LayerResult(
                        data=result,
                        metadata=metadata,
                        success=True
                    )
            
            return LayerResult(
                data=None,
                success=False,
                error_message=f"No execution strategy found for plan type: {plan.type}"
            )
            
        except Exception as e:
            try:
                from ..llm import llm_fallback
                result = llm_fallback(plan.original_query)
                metadata["strategy_used"] = "fallback"
                
                return LayerResult(
                    data=result,
                    metadata=metadata,
                    success=True
                )
            except Exception:
                return LayerResult(
                    data=None,
                    success=False,
                    error_message=f"Execution failed: {str(e)}"
                )
    
    def _execute_step(self, step: ExecutionStep) -> Any:
        if step.tool not in self.tool_adapters:
            raise ToolNotFoundError(step.tool)
        
        adapter = self.tool_adapters[step.tool]
        
        if not adapter.has_operation(step.operation):
            raise ExecutionError(f"Operation '{step.operation}' not found in tool '{step.tool}'")
        
        try:
            return adapter.execute_operation(step.operation, step.parameters)
        except Exception as e:
            raise ExecutionError(f"Error executing {step.tool}.{step.operation}: {str(e)}")
    
    def _substitute_variables(self, params: Dict[str, Any]) -> Dict[str, Any]:
        substituted = {}
        
        for key, value in params.items():
            if isinstance(value, str):
                if value.startswith("${") and value.endswith("}"):
                    var_name = value[2:-1]
                    if var_name in self.variables:
                        var_value = self.variables[var_name]
                        if isinstance(var_value, dict) and "numeric" in var_value and "display" in var_value:
                            if key in ["numbers", "first_number", "second_number", "amount"]:
                                substituted[key] = var_value["numeric"]
                            else:
                                substituted[key] = var_value["display"]
                        else:
                            substituted[key] = var_value
                    else:
                        raise VariableSubstitutionError(f"Variable '{var_name}' not found")
                elif "${" in value and "}" in value:
                    substituted_text = value
                    import re
                    variable_pattern = r'\$\{([^}]+)\}'
                    matches = re.findall(variable_pattern, value)
                    
                    for var_name in matches:
                        if var_name in self.variables:
                            var_value = self.variables[var_name]
                            if isinstance(var_value, dict) and "display" in var_value:
                                replacement = var_value["display"]
                            else:
                                replacement = str(var_value)
                            substituted_text = substituted_text.replace(f"${{{var_name}}}", replacement)
                        else:
                            raise VariableSubstitutionError(f"Variable '{var_name}' not found")
                    
                    substituted[key] = substituted_text
                else:
                    substituted[key] = value
            elif isinstance(value, list):
                substituted_list = []
                for item in value:
                    if isinstance(item, str) and item.startswith("${") and item.endswith("}"):
                        var_name = item[2:-1]
                        if var_name in self.variables:
                            var_value = self.variables[var_name]
                            if isinstance(var_value, dict) and "numeric" in var_value:
                                substituted_list.append(var_value["numeric"])
                            else:
                                substituted_list.append(var_value)
                        else:
                            raise VariableSubstitutionError(f"Variable '{var_name}' not found")
                    else:
                        substituted_list.append(item)
                substituted[key] = substituted_list
            else:
                substituted[key] = value
        
        return substituted
    
    def _format_result(self, result: Any, tool: str, operation: str) -> str:
        if tool == "calculator":
            return str(result)
        elif tool == "weather":
            if isinstance(result, dict) and 'display' in result:
                return result['display']
            else:
                return f"{result}°C"
        elif tool == "currency":
            return str(result)
        elif tool == "knowledge_base":
            return str(result)
        elif tool == "llm":
            return str(result)
        else:
            return str(result)
    
    def _format_final_result(self, result: Any, output_format: str = None) -> str:
        """Format the final result of a multi-step execution."""
        if output_format == "temperature":
            return f"{result}°C"
        elif output_format == "currency":
            return str(result)
        else:
            return str(result)

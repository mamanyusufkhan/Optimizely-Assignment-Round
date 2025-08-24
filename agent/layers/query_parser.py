import re
from typing import Dict, List, Any, Optional, Callable, Type
from abc import ABC, abstractmethod
from dataclasses import dataclass
from .base import BaseLayer, LayerResult
from .data_structures import ExecutionPlan, ExecutionStep, QueryType

class QueryParsingError(Exception):
    def __init__(self, message="Query parsing failed"):
        super().__init__(message)

class QueryPattern(ABC):    
    def __init__(self, name: str, priority: int = 0):
        self.name = name
        self.priority = priority
    
    @abstractmethod
    def matches(self, query: str) -> bool:
        pass
    
    @abstractmethod
    def parse(self, query: str) -> ExecutionPlan:
        pass

class CalculatorPattern(QueryPattern):
    
    def __init__(self):
        super().__init__("calculator", priority=10)
        self.patterns = {
            'percentage': r'(?:what\s+is\s+|calculate\s+)?(\d+(?:\.\d+)?)\s*%\s+of\s+(\d+(?:\.\d+)?)',
            'percent_of': r'(\d+(?:\.\d+)?)\s+percent\s+of\s+(\d+(?:\.\d+)?)',
            'addition': r'(?:add|plus|sum)\s+(\d+(?:\.\d+)?)\s+(?:and|to|\+|with)\s+(\d+(?:\.\d+)?)',
            'subtraction': r'(?:subtract|minus)\s+(\d+(?:\.\d+)?)\s+(?:from|-)\s+(\d+(?:\.\d+)?)',
            'multiplication': r'(?:multiply|times)\s+(\d+(?:\.\d+)?)\s+(?:by|\*|times)\s+(\d+(?:\.\d+)?)',
            'division': r'(?:divide)\s+(\d+(?:\.\d+)?)\s+(?:by|/)\s+(\d+(?:\.\d+)?)',
            'average': r'(?:average|avg)\s+(?:of\s+)?(\d+(?:\.\d+)?)(?:\s+and\s+(\d+(?:\.\d+)?))+',
            'simple_math': r'(\d+(?:\.\d+)?)\s*([+\-*/])\s*(\d+(?:\.\d+)?)'
        }
    
    def matches(self, query: str) -> bool:
        query_lower = query.lower()
        return any(re.search(pattern, query_lower) for pattern in self.patterns.values())
    
    def parse(self, query: str) -> ExecutionPlan:
        query_lower = query.lower()
        
        match = re.search(self.patterns['percentage'], query_lower)
        if not match:
            match = re.search(self.patterns['percent_of'], query_lower)
        
        if match:
            percentage = float(match.group(1))
            number = float(match.group(2))
            
            step = ExecutionStep(
                tool="calculator",
                operation="percent_of",
                parameters={"percentage": percentage, "number": number},
                description=f"Calculate {percentage}% of {number}"
            )
            
            return ExecutionPlan(
                type=QueryType.SINGLE_TOOL,
                steps=[step],
                description=f"Calculate {percentage}% of {number}"
            )
        
        match = re.search(self.patterns['addition'], query_lower)
        if match:
            num1 = float(match.group(1))
            num2 = float(match.group(2))
            
            step = ExecutionStep(
                tool="calculator",
                operation="add",
                parameters={"first_number": num1, "second_number": num2},
                description=f"Add {num1} and {num2}"
            )
            
            return ExecutionPlan(
                type=QueryType.SINGLE_TOOL,
                steps=[step],
                description=f"Add {num1} and {num2}"
            )
        
        match = re.search(self.patterns['subtraction'], query_lower)
        if match:
            num1 = float(match.group(1))
            num2 = float(match.group(2))
            
            step = ExecutionStep(
                tool="calculator",
                operation="subtract",
                parameters={"first_number": num2, "second_number": num1},
                description=f"Subtract {num1} from {num2}"
            )
            
            return ExecutionPlan(
                type=QueryType.SINGLE_TOOL,
                steps=[step],
                description=f"Subtract {num1} from {num2}"
            )
        
        match = re.search(self.patterns['multiplication'], query_lower)
        if match:
            num1 = float(match.group(1))
            num2 = float(match.group(2))
            
            step = ExecutionStep(
                tool="calculator",
                operation="multiply",
                parameters={"first_number": num1, "second_number": num2},
                description=f"Multiply {num1} by {num2}"
            )
            
            return ExecutionPlan(
                type=QueryType.SINGLE_TOOL,
                steps=[step],
                description=f"Multiply {num1} by {num2}"
            )
        
        match = re.search(self.patterns['division'], query_lower)
        if match:
            num1 = float(match.group(1))
            num2 = float(match.group(2))
            
            step = ExecutionStep(
                tool="calculator",
                operation="divide",
                parameters={"first_number": num1, "second_number": num2},
                description=f"Divide {num1} by {num2}"
            )
            
            return ExecutionPlan(
                type=QueryType.SINGLE_TOOL,
                steps=[step],
                description=f"Divide {num1} by {num2}"
            )
        
        match = re.search(self.patterns['simple_math'], query_lower)
        if match:
            num1 = float(match.group(1))
            operator = match.group(2)
            num2 = float(match.group(3))
            
            operation_map = {'+': 'add', '-': 'subtract', '*': 'multiply', '/': 'divide'}
            operation = operation_map.get(operator)
            
            if operation:
                step = ExecutionStep(
                    tool="calculator",
                    operation=operation,
                    parameters={"first_number": num1, "second_number": num2},
                    description=f"Calculate {num1} {operator} {num2}"
                )
                
                return ExecutionPlan(
                    type=QueryType.SINGLE_TOOL,
                    steps=[step],
                    description=f"Calculate {num1} {operator} {num2}"
                )
        
        raise QueryParsingError(f"No matching calculator pattern for: {query}")

class WeatherPattern(QueryPattern):
    
    def __init__(self):
        super().__init__("weather", priority=8)
        self.patterns = {
            'simple_weather': r'(?:weather|temperature)\s+(?:in|for)\s+([a-zA-Z\s]+)',
            'get_weather': r'(?:get|show|check)\s+(?:weather|temperature)\s+(?:in|for)\s+([a-zA-Z\s]+)',
            'weather_summarize': r'summarize\s+(?:today\'s\s+)?weather\s+in\s+([a-zA-Z\s]+?)\s+in\s+(\d+)\s+words?'
        }
    
    def matches(self, query: str) -> bool:
        query_lower = query.lower()
        return any(re.search(pattern, query_lower) for pattern in self.patterns.values())
    
    def parse(self, query: str) -> ExecutionPlan:
        query_lower = query.lower()
        
        
        match = re.search(self.patterns['weather_summarize'], query_lower)
        if match:
            city = match.group(1).strip()
            word_count = int(match.group(2))
            
            step = ExecutionStep(
                tool="weather",
                operation="get_weather",
                parameters={"city": city},
                description=f"Get weather for {city}"
            )
            
            return ExecutionPlan(
                type=QueryType.SINGLE_TOOL,
                steps=[step],
                description=f"Get weather for {city}"
            )
        
        match = re.search(self.patterns['get_weather'], query_lower)
        if match:
            city = match.group(1).strip()
            
            step = ExecutionStep(
                tool="weather",
                operation="get_weather",
                parameters={"city": city},
                description=f"Get weather for {city}"
            )
            
            return ExecutionPlan(
                type=QueryType.SINGLE_TOOL,
                steps=[step],
                description=f"Get weather for {city}"
            )
            
        match = re.search(self.patterns['simple_weather'], query_lower)
        if match:
            city = match.group(1).strip()
            
            step = ExecutionStep(
                tool="weather",
                operation="get_weather",
                parameters={"city": city},
                description=f"Get weather for {city}"
            )
            
            return ExecutionPlan(
                type=QueryType.SINGLE_TOOL,
                steps=[step],
                description=f"Get weather for {city}"
            )
        
        raise QueryParsingError(f"No matching weather pattern for: {query}")

class KnowledgeBasePattern(QueryPattern):
    
    def __init__(self):
        super().__init__("knowledge_base", priority=6)
        self.patterns = {
            'who_is': r'who\s+is\s+([a-zA-Z\s]+)\??',
            'what_is': r'what\s+is\s+([a-zA-Z\s]+)\??',
            'tell_me_about': r'tell\s+me\s+about\s+([a-zA-Z\s]+)\??'
        }
    
    def matches(self, query: str) -> bool:
        query_lower = query.lower()
        return any(re.search(pattern, query_lower) for pattern in self.patterns.values())
    
    def parse(self, query: str) -> ExecutionPlan:
        query_lower = query.lower()
        
        for pattern_name, pattern in self.patterns.items():
            match = re.search(pattern, query_lower)
            if match:
                subject = match.group(1).strip()
                
                step = ExecutionStep(
                    tool="knowledge_base",
                    operation="kb_lookup",
                    parameters={"query": subject},
                    description=f"Look up information about {subject}"
                )
                
                return ExecutionPlan(
                    type=QueryType.SINGLE_TOOL,
                    steps=[step],
                    description=f"Look up information about {subject}"
                )
        
        raise QueryParsingError(f"No matching knowledge base pattern for: {query}")

class CurrencyPattern(QueryPattern):
    
    def __init__(self):
        super().__init__("currency", priority=40)
        self.patterns = {
            'convert_amount': r'convert\s+(\d+(?:\.\d+)?)\s+([a-z]{3})\s+(?:to|into)\s+([a-z]{3})',
            'convert_result': r'convert\s+(?:the\s+)?(.+?)\s+(?:usd|eur|gbp|jpy|cad|aud|chf|cny)\s+(?:to|into)\s+([a-z]{3})'
        }
    
    def matches(self, query: str) -> bool:
        query_lower = query.lower()
        return any(re.search(pattern, query_lower) for pattern in self.patterns.values())
    
    def parse(self, query: str) -> ExecutionPlan:
        query_lower = query.lower()
        
        match = re.search(self.patterns['convert_amount'], query_lower)
        if match:
            amount = float(match.group(1))
            from_currency = match.group(2).upper()
            to_currency = match.group(3).upper()
            
            step = ExecutionStep(
                tool="currency",
                operation="currency_convert",
                parameters={
                    "amount": amount,
                    "from_currency": from_currency,
                    "to_currency": to_currency
                },
                description=f"Convert {amount} {from_currency} to {to_currency}"
            )
            
            return ExecutionPlan(
                type=QueryType.SINGLE_TOOL,
                steps=[step],
                description=f"Convert {amount} {from_currency} to {to_currency}"
            )
        
        
        raise QueryParsingError(f"No matching currency pattern for: {query}")

class ComponentBasedQueryParser(QueryPattern):
    
    def __init__(self):
        super().__init__("component_based", priority=60)
        
        self.math_patterns = {
            'percentage': r'(\d+(?:\.\d+)?)\s*%\s*of\s+(\d+(?:\.\d+)?)',
            'average': r'average\s+of\s+(\d+(?:\.\d+)?)\s+and\s+(\d+(?:\.\d+)?)',
            'add_to': r'add\s+(\d+(?:\.\d+)?)\s+to\s+(.+)',
            'basic_math': r'(\d+(?:\.\d+)?)\s*([+\-*/])\s*(\d+(?:\.\d+)?)'
        }
        
        self.weather_patterns = {
            'temperature': r'temperature\s+in\s+([a-zA-Z\s]+?)(?:\s+and\s+([a-zA-Z\s]+?))?',
            'weather': r'weather\s+in\s+([a-zA-Z\s]+)',
            'avg_temp': r'average\s+temperature\s+in\s+([a-zA-Z\s]+?)\s+and\s+([a-zA-Z\s]+?)(?:\s+right\s+now)?$'
        }
        
        self.knowledge_patterns = {
            'who_is': r'who\s+is\s+([a-zA-Z\s]+)\??',
            'what_is': r'what\s+is\s+([a-zA-Z\s]+)\??'
        }
        
        self.currency_patterns = {
            'convert': r'convert\s+(.+?)\s+([a-z]{3})\s+(?:to|into)\s+([a-z]{3})',
            'direct_convert': r'convert\s+(\d+(?:\.\d+)?)\s+([a-z]{3})\s+(?:to|into)\s+([a-z]{3})'
        }
        
        self.processing_patterns = {
            'summarize': r'summarize\s+(.+?)\s+in\s+(\d+)\s+words?'
        }
    
    def matches(self, query: str) -> bool:
        query_lower = query.lower()
        
        all_patterns = {**self.math_patterns, **self.weather_patterns, 
                       **self.knowledge_patterns, **self.currency_patterns,
                       **self.processing_patterns}
        
        return any(re.search(pattern, query_lower) for pattern in all_patterns.values())
    
    def parse(self, query: str) -> ExecutionPlan:
        query_lower = query.lower()
        
        if match := re.search(self.math_patterns['percentage'], query_lower):
            percentage, number = float(match.group(1)), float(match.group(2))
            step = ExecutionStep(
                tool="calculator",
                operation="percent_of",
                parameters={"percentage": percentage, "number": number},
                description=f"Calculate {percentage}% of {number}"
            )
            return ExecutionPlan(
                type=QueryType.SINGLE_TOOL,
                steps=[step],
                description=f"Calculate {percentage}% of {number}"
            )
        
        if match := re.search(self.knowledge_patterns['who_is'], query_lower):
            subject = match.group(1).strip()
            step = ExecutionStep(
                tool="knowledge_base",
                operation="kb_lookup",
                parameters={"query": subject},
                description=f"Look up information about {subject}"
            )
            return ExecutionPlan(
                type=QueryType.SINGLE_TOOL,
                steps=[step],
                description=f"Look up information about {subject}"
            )
        
        if match := re.search(self.processing_patterns['summarize'], query_lower):
            content = match.group(1).strip()
            word_count = int(match.group(2))
            
            if "weather" in content and re.search(r'in\s+([a-zA-Z\s]+)', content):
                city_match = re.search(r'in\s+([a-zA-Z\s]+)', content)
                city = city_match.group(1).strip()
                
                steps = [
                    ExecutionStep(
                        tool="weather",
                        operation="get_weather", 
                        parameters={"city": city},
                        description=f"Get weather data for {city}",
                        variables={"result_var": "weather_data"}
                    ),
                    ExecutionStep(
                        tool="llm",
                        operation="generate",
                        parameters={
                            "prompt": f"Summarize " + "${weather_data}" + f" in exactly {word_count} words"
                        },
                        description=f"Summarize weather in {word_count} words",
                        variables={}
                    )
                ]
                
                return ExecutionPlan(
                    type=QueryType.MULTI_STEP,
                    steps=steps,
                    description=f"Summarize weather in {city} in {word_count} words"
                )
        
        if "add" in query_lower and "average temperature" in query_lower:
            add_match = re.search(r'add\s+(\d+(?:\.\d+)?)', query_lower)
            cities_match = re.search(r'average\s+temperature\s+in\s+([a-zA-Z\s]+?)\s+and\s+([a-zA-Z\s]+?)(?:\s+right\s+now)?\.?$', query_lower)
            
            if add_match and cities_match:
                add_value = float(add_match.group(1))
                city1 = cities_match.group(1).strip()
                city2 = cities_match.group(2).strip()
                
                steps = [
                    ExecutionStep(
                        tool="weather",
                        operation="get_weather",
                        parameters={"city": city1},
                        description=f"Get temperature in {city1}",
                        variables={"result_var": "temp1"}
                    ),
                    ExecutionStep(
                        tool="weather",
                        operation="get_weather", 
                        parameters={"city": city2},
                        description=f"Get temperature in {city2}",
                        variables={"result_var": "temp2"}
                    ),
                    ExecutionStep(
                        tool="calculator",
                        operation="average",
                        parameters={"numbers": ["${temp1}", "${temp2}"]},
                        description=f"Calculate average of temperatures",
                        variables={"result_var": "avg_temp"}
                    ),
                    ExecutionStep(
                        tool="calculator",
                        operation="add",
                        parameters={"first_number": "${avg_temp}", "second_number": add_value},
                        description=f"Add {add_value} to average temperature",
                        variables={}
                    )
                ]
                
                return ExecutionPlan(
                    type=QueryType.MULTI_STEP,
                    steps=steps,
                    description=f"Add {add_value} to average temperature in {city1} and {city2}"
                )
        
        if "convert" in query_lower and "average" in query_lower:
            convert_avg_match = re.search(r'convert\s+(?:the\s+)?average\s+of\s+(\d+(?:\.\d+)?)\s+and\s+(\d+(?:\.\d+)?)\s+([a-z]{3})\s+(?:to|into)\s+([a-z]{3})', query_lower)
            
            if convert_avg_match:
                num1 = float(convert_avg_match.group(1))
                num2 = float(convert_avg_match.group(2))
                from_currency = convert_avg_match.group(3).upper()
                to_currency = convert_avg_match.group(4).upper()
                
                steps = [
                    ExecutionStep(
                        tool="calculator",
                        operation="average",
                        parameters={"numbers": [num1, num2]},
                        description=f"Calculate average of {num1} and {num2}",
                        variables={"result_var": "avg_amount"}
                    ),
                    ExecutionStep(
                        tool="currency",
                        operation="currency_convert",
                        parameters={
                            "amount": "${avg_amount}",
                            "from_currency": from_currency,
                            "to_currency": to_currency
                        },
                        description=f"Convert average to {to_currency}",
                        variables={}
                    )
                ]
                
                return ExecutionPlan(
                    type=QueryType.MULTI_STEP,
                    steps=steps,
                    description=f"Convert average of {num1} and {num2} {from_currency} to {to_currency}"
                )
        
        if match := re.search(self.currency_patterns['direct_convert'], query_lower):
            amount = float(match.group(1))
            from_currency = match.group(2).upper()
            to_currency = match.group(3).upper()
            
            step = ExecutionStep(
                tool="currency",
                operation="currency_convert",
                parameters={
                    "amount": amount,
                    "from_currency": from_currency,
                    "to_currency": to_currency
                },
                description=f"Convert {amount} {from_currency} to {to_currency}"
            )
            return ExecutionPlan(
                type=QueryType.SINGLE_TOOL,
                steps=[step],
                description=f"Convert {amount} {from_currency} to {to_currency}"
            )
        
        raise QueryParsingError(f"No matching component pattern for: {query}")

class MultiStepPattern(QueryPattern):
    
    def __init__(self):
        super().__init__("multi_step", priority=50)
        self.patterns = {
            'math_avg_temp': r'(add|subtract|plus|minus|multiply|divide|times)\s+(\d+(?:\.\d+)?)\s+(?:to|from|by|with)\s+(?:the\s+)?average\s+(?:temperature|weather)\s+(?:of\s+|in\s+)(\w+(?:\s+\w+)*?)\s+and\s+(\w+(?:\s+\w+)*?)(?:\s+(?:right\s+now|now|today|currently))?',
            'math_specific_temp': r'(add|subtract|plus|minus|multiply|divide)\s+(\d+(?:\.\d+)?)\s+(?:to|from|by)\s+(?:the\s+)?(?:temperature|weather)\s+(?:of\s+|in\s+)(\w+(?:\s+\w+)*?)(?:\s+(?:right\s+now|now|today|currently))?',
            'if_temp_math': r'if\s+(?:the\s+)?(?:temperature|weather)\s+in\s+([a-zA-Z]+(?:\s+[a-zA-Z]+)*?)\s+is\s+(\d+(?:\.\d+)?)\s*°?c?\s*(?:degrees?)?\s+and\s+(?:i\s+)?(add|subtract|plus|minus|multiply|divide)\s+(\d+(?:\.\d+)?)\s*(?:degrees?|°c?)?',
            'multi_city_temp': r'(average|sum|total|combine)\s+(?:the\s+)?(?:temperatures?|weather)\s+(?:of\s+|in\s+)(\w+(?:\s+\w+)*?)(?:\s*,\s*(\w+(?:\s+\w+)*?))*\s+and\s+(\w+(?:\s+\w+)*?)(?:\s+(?:right\s+now|now|today|currently))?',
            'math_avg_currency': r'(add|subtract|plus|minus|multiply|divide)\s+(\d+(?:\.\d+)?)\s+(?:to|from|by)\s+(?:the\s+)?average\s+of\s+(\d+(?:\.\d+)?)\s+and\s+(\d+(?:\.\d+)?)\s+([a-z]{3})',
            'convert_avg_currency': r'convert\s+(?:the\s+)?average\s+of\s+(\d+(?:\.\d+)?)\s+and\s+(\d+(?:\.\d+)?)\s+([a-z]{3})\s+(?:to|into)\s+([a-z]{3})',
            'summarize_weather': r'summarize\s+(?:today.s\s+|the\s+)?(?:weather|temperature)\s+(?:of\s+|in\s+)([a-zA-Z\s]+?)\s+(?:in\s+|using\s+|with\s+)(\d+)\s+words?',
            'compare_temps': r'(compare|difference|diff)\s+(?:the\s+)?(?:temperatures?|weather)\s+(?:between\s+|of\s+)(\w+(?:\s+\w+)*?)\s+and\s+(\w+(?:\s+\w+)*?)(?:\s+(?:right\s+now|now|today|currently))?',
            'temp_range': r'(?:what.s\s+the\s+)?(highest|lowest|maximum|minimum|max|min)\s+(?:temperature|weather)\s+(?:between\s+|among\s+)(\w+(?:\s+\w+)*?)(?:\s*,\s*(\w+(?:\s+\w+)*?))*\s+and\s+(\w+(?:\s+\w+)*?)(?:\s+(?:right\s+now|now|today|currently))?'
        }
    
    def matches(self, query: str) -> bool:
        query_lower = query.lower()
        return any(re.search(pattern, query_lower) for pattern in self.patterns.values())
    
    def parse(self, query: str) -> ExecutionPlan:
        query_lower = query.lower()
        
        match = re.search(self.patterns['math_avg_temp'], query_lower)
        if match:
            operation_word = match.group(1).strip()
            value = float(match.group(2))
            city1 = match.group(3).strip()
            city2 = match.group(4).strip()
            
            operation_map = {
                'add': 'add', 'plus': 'add',
                'subtract': 'subtract', 'minus': 'subtract',
                'multiply': 'multiply', 'times': 'multiply',
                'divide': 'divide'
            }
            
            calc_operation = operation_map.get(operation_word, 'add')
            
            steps = [
                ExecutionStep(
                    tool="weather",
                    operation="get_weather",
                    parameters={"city": city1},
                    description=f"Get temperature in {city1}",
                    variables={"result_var": "temp1"}
                ),
                ExecutionStep(
                    tool="weather", 
                    operation="get_weather",
                    parameters={"city": city2},
                    description=f"Get temperature in {city2}",
                    variables={"result_var": "temp2"}
                ),
                ExecutionStep(
                    tool="calculator",
                    operation="average",
                    parameters={"numbers": ["${temp1}", "${temp2}"]},
                    description=f"Calculate average of temperatures",
                    variables={"result_var": "avg"}
                ),
                ExecutionStep(
                    tool="calculator",
                    operation=calc_operation,
                    parameters={"first_number": "${avg}", "second_number": value},
                    description=f"{operation_word.capitalize()} {value} {'to' if calc_operation == 'add' else 'from' if calc_operation == 'subtract' else 'by'} average temperature"
                )
            ]
            
            return ExecutionPlan(
                type=QueryType.MULTI_STEP,
                steps=steps,
                description=f"{operation_word.capitalize()} {value} {'to' if calc_operation == 'add' else 'from' if calc_operation == 'subtract' else 'by'} average temperature in {city1} and {city2}"
            )
        
        match = re.search(self.patterns['math_specific_temp'], query_lower)
        if match:
            operation_word = match.group(1).strip()
            value = float(match.group(2))
            city = match.group(3).strip()
            
            operation_map = {
                'add': 'add', 'plus': 'add',
                'subtract': 'subtract', 'minus': 'subtract',
                'multiply': 'multiply', 'divide': 'divide'
            }
            
            calc_operation = operation_map.get(operation_word, 'add')
            
            steps = [
                ExecutionStep(
                    tool="weather",
                    operation="get_weather",
                    parameters={"city": city},
                    description=f"Get temperature in {city}",
                    variables={"result_var": "temp"}
                ),
                ExecutionStep(
                    tool="calculator",
                    operation=calc_operation,
                    parameters={"first_number": "${temp}", "second_number": value},
                    description=f"{operation_word.capitalize()} {value} {'to' if calc_operation == 'add' else 'from' if calc_operation == 'subtract' else 'by'} temperature in {city}"
                )
            ]
            
            return ExecutionPlan(
                type=QueryType.MULTI_STEP,
                steps=steps,
                description=f"{operation_word.capitalize()} {value} {'to' if calc_operation == 'add' else 'from' if calc_operation == 'subtract' else 'by'} temperature in {city}"
            )
        
        match = re.search(self.patterns['if_temp_math'], query_lower)
        if match:
            city = match.group(1).strip()
            temp_value = float(match.group(2))
            operation_word = match.group(3).strip()
            math_value = float(match.group(4))
            
            operation_map = {
                'add': 'add', 'plus': 'add',
                'subtract': 'subtract', 'minus': 'subtract',
                'multiply': 'multiply', 'divide': 'divide'
            }
            
            calc_operation = operation_map.get(operation_word, 'add')
            
            steps = [
                ExecutionStep(
                    tool="calculator",
                    operation=calc_operation,
                    parameters={"first_number": temp_value, "second_number": math_value},
                    description=f"{operation_word.capitalize()} {math_value} {'to' if calc_operation == 'add' else 'from' if calc_operation == 'subtract' else 'by'} {temp_value}°C"
                )
            ]
            
            return ExecutionPlan(
                type=QueryType.MULTI_STEP,
                steps=steps,
                description=f"{operation_word.capitalize()} {math_value} {'to' if calc_operation == 'add' else 'from' if calc_operation == 'subtract' else 'by'} {temp_value}°C temperature in {city}"
            )
        
        match = re.search(self.patterns['multi_city_temp'], query_lower)
        if match:
            operation_word = match.group(1).strip()
            city1 = match.group(2).strip()
            city2 = match.group(4).strip()  # Skip group 3 as it's the optional middle city
            
            steps = [
                ExecutionStep(
                    tool="weather",
                    operation="get_weather",
                    parameters={"city": city1},
                    description=f"Get temperature in {city1}",
                    variables={"result_var": "temp1"}
                ),
                ExecutionStep(
                    tool="weather",
                    operation="get_weather",
                    parameters={"city": city2},
                    description=f"Get temperature in {city2}",
                    variables={"result_var": "temp2"}
                ),
                ExecutionStep(
                    tool="calculator",
                    operation="average" if operation_word == "average" else "add",
                    parameters={"numbers": ["${temp1}", "${temp2}"]},
                    description=f"{operation_word.capitalize()} temperatures in {city1} and {city2}"
                )
            ]
            
            return ExecutionPlan(
                type=QueryType.MULTI_STEP,
                steps=steps,
                description=f"{operation_word.capitalize()} temperatures in {city1} and {city2}"
            )
        
        match = re.search(self.patterns['compare_temps'], query_lower)
        if match:
            comparison_type = match.group(1).strip()
            city1 = match.group(2).strip()
            city2 = match.group(3).strip()
            
            steps = [
                ExecutionStep(
                    tool="weather",
                    operation="get_weather",
                    parameters={"city": city1},
                    description=f"Get temperature in {city1}",
                    variables={"result_var": "temp1"}
                ),
                ExecutionStep(
                    tool="weather",
                    operation="get_weather",
                    parameters={"city": city2},
                    description=f"Get temperature in {city2}",
                    variables={"result_var": "temp2"}
                ),
                ExecutionStep(
                    tool="calculator",
                    operation="subtract",
                    parameters={"first_number": "${temp1}", "second_number": "${temp2}"},
                    description=f"Calculate temperature difference between {city1} and {city2}"
                )
            ]
            
            return ExecutionPlan(
                type=QueryType.MULTI_STEP,
                steps=steps,
                description=f"Compare temperatures between {city1} and {city2}"
            )
        
        match = re.search(self.patterns['convert_avg_currency'], query_lower)
        if match:
            num1 = float(match.group(1))
            num2 = float(match.group(2))
            from_currency = match.group(3).upper()
            to_currency = match.group(4).upper()
            
            steps = [
                ExecutionStep(
                    tool="calculator",
                    operation="average",
                    parameters={"numbers": [num1, num2]},
                    description=f"Calculate average of {num1} and {num2}",
                    variables={"result_var": "avg"}
                ),
                ExecutionStep(
                    tool="currency",
                    operation="currency_convert",
                    parameters={
                        "amount": "${avg}",
                        "from_currency": from_currency,
                        "to_currency": to_currency
                    },
                    description=f"Convert average to {to_currency}"
                )
            ]
            
            return ExecutionPlan(
                type=QueryType.MULTI_STEP,
                steps=steps,
                description=f"Convert average of {num1} and {num2} {from_currency} to {to_currency}"
            )
        
        match = re.search(self.patterns['summarize_weather'], query_lower)
        if match:
            city = match.group(1).strip()
            word_count = int(match.group(2))
            
            steps = [
                ExecutionStep(
                    tool="weather",
                    operation="get_weather",
                    parameters={"city": city},
                    description=f"Get weather data for {city}",
                    variables={"result_var": "weather_data"}
                ),
                ExecutionStep(
                    tool="llm",
                    operation="llm_fallback",
                    parameters={
                        "prompt": f"Summarize the weather temperature ${{weather_data}} in {city} in exactly {word_count} words"
                    },
                    description=f"Summarize weather in {word_count} words"
                )
            ]
            
            return ExecutionPlan(
                type=QueryType.MULTI_STEP,
                steps=steps,
                description=f"Summarize weather in {city} in {word_count} words"
            )
        
        raise QueryParsingError(f"No matching multi-step pattern for: {query}")

class ExtensibleQueryParser(BaseLayer):
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__("query_parser", config)
        self.patterns: List[QueryPattern] = []
        self.fallback_strategy = "llm" 
    
    def initialize(self) -> None:
        super().initialize()
        
        self._register_default_patterns()
        if self.config and "patterns" in self.config:
            for pattern_class in self.config["patterns"]:
                if isinstance(pattern_class, type) and issubclass(pattern_class, QueryPattern):
                    self.register_pattern(pattern_class())
        
        self.patterns.sort(key=lambda p: p.priority, reverse=True)
    
    def _register_default_patterns(self) -> None:
        self.register_pattern(ComponentBasedQueryParser())
        self.register_pattern(CalculatorPattern())
        self.register_pattern(WeatherPattern())
        self.register_pattern(KnowledgeBasePattern())
        self.register_pattern(CurrencyPattern())
        self.register_pattern(MultiStepPattern())
    
    def register_pattern(self, pattern: QueryPattern) -> None:
        if not isinstance(pattern, QueryPattern):
            raise TypeError(f"Pattern must be instance of QueryPattern, got {type(pattern)}")
        
        self.patterns.append(pattern)
        self.patterns.sort(key=lambda p: p.priority, reverse=True)
    
    def process(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> LayerResult:
        if not isinstance(input_data, str):
            return LayerResult(
                data=None,
                success=False,
                error_message=f"Expected string input, got {type(input_data)}"
            )
        
        query = input_data.strip()
        if not query:
            return LayerResult(
                data=None,
                success=False,
                error_message="Empty query provided"
            )
        
        try:
            metadata = {
                "original_query": query,
                "patterns_tried": []
            }
            
            for pattern in self.patterns:
                try:
                    if pattern.matches(query):
                        execution_plan = pattern.parse(query)
                        metadata["matched_pattern"] = pattern.name
                        metadata["patterns_tried"].append(pattern.name)
                        
                        return LayerResult(
                            data=execution_plan,
                            metadata=metadata,
                            success=True
                        )
                except Exception as e:
                    metadata["patterns_tried"].append(f"{pattern.name} (failed: {str(e)})")
                    continue
            
            fallback_plan = self._create_fallback_plan(query)
            metadata["matched_pattern"] = "fallback"
            
            return LayerResult(
                data=fallback_plan,
                metadata=metadata,
                success=True
            )
            
        except Exception as e:
            return LayerResult(
                data=None,
                success=False,
                error_message=f"Query parsing failed: {str(e)}"
            )
    
    def _create_fallback_plan(self, query: str) -> ExecutionPlan:
        step = ExecutionStep(
            tool="llm",
            operation="llm_fallback",
            parameters={"prompt": query},
            description="Process with LLM fallback"
        )
        
        return ExecutionPlan(
            type=QueryType.LLM_REQUIRED,
            steps=[step],
            description=f"LLM fallback for: {query}"
        )

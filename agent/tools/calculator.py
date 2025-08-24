from typing import List, Union

# Custom exceptions for calculator errors
class CalculatorError(Exception):
    
    def __init__(self, message="Calculator error occurred"):
        super().__init__(message)

class InvalidOperationError(CalculatorError):
   
    def __init__(self, operation):
        super().__init__(f"Unsupported operation: '{operation}'")

class DivisionByZeroError(CalculatorError):
    
    def __init__(self):
        super().__init__("Cannot divide by zero")

class InvalidInputError(CalculatorError):
    
    def __init__(self, message="Invalid input provided"):
        super().__init__(message)

def add(first_number: float, second_number: float) -> float:
   
    return first_number + second_number

def subtract(first_number: float, second_number: float) -> float:
    return first_number - second_number

def multiply(first_number: float, second_number: float) -> float:
    return first_number * second_number

def divide(first_number: float, second_number: float) -> float:
    if second_number == 0:
        raise DivisionByZeroError()
    return first_number / second_number

def percent_of(percentage: float, number: float) -> float:
    return (percentage / 100.0) * number

def average(numbers: List[float]) -> float:
    if not numbers:
        raise InvalidInputError("Cannot calculate average of empty list")
    return sum(numbers) / len(numbers)

def power(base: float, exponent: float) -> float:
    return base ** exponent

def calculate(operation: str, first_number: float, second_number: float = None, numbers: List[float] = None) -> float:
    if not isinstance(operation, str):
        raise InvalidInputError("Operation must be a string")
    
    operation = operation.lower().strip()
    
    if first_number is not None and not isinstance(first_number, (int, float)):
        raise InvalidInputError("First number must be a number")
    
    if second_number is not None and not isinstance(second_number, (int, float)):
        raise InvalidInputError("Second number must be a number")
    
    if operation == "add":
        if second_number is None:
            raise InvalidInputError("Addition requires two numbers")
        return add(first_number, second_number)
    
    elif operation == "subtract":
        if second_number is None:
            raise InvalidInputError("Subtraction requires two numbers")
        return subtract(first_number, second_number)
    
    elif operation == "multiply":
        if second_number is None:
            raise InvalidInputError("Multiplication requires two numbers")
        return multiply(first_number, second_number)
    
    elif operation == "divide":
        if second_number is None:
            raise InvalidInputError("Division requires two numbers")
        return divide(first_number, second_number)
    
    elif operation == "percent_of":
        if second_number is None:
            raise InvalidInputError("Percent calculation requires two numbers (percentage and number)")
        return percent_of(first_number, second_number)
    
    elif operation == "power":
        if second_number is None:
            raise InvalidInputError("Power calculation requires two numbers (base and exponent)")
        return power(first_number, second_number)
    
    elif operation == "average":
        if numbers is None or not numbers:
            raise InvalidInputError("Average calculation requires a list of numbers")
        return average(numbers)
    
    else:
        raise InvalidOperationError(operation)

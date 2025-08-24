# Architecture Documentation

## System Overview

The extensible agent system employs a **layered pipeline architecture** that transforms natural language queries into structured execution plans and tool operations. The design emphasizes modularity, extensibility, and fault tolerance through well-defined interfaces and comprehensive error handling.

## Architectural Principles

### **1. Separation of Concerns**
Each layer has a single, well-defined responsibility:
- **Orchestration**: Query lifecycle management
- **Parsing**: Natural language to structured data transformation
- **Execution**: Tool orchestration and result composition

### **2. Interface-Driven Design**
All components implement abstract interfaces enabling:
- **Pluggability**: Easy component replacement
- **Testability**: Isolated unit testing
- **Extensibility**: New functionality without core changes

### **3. Pipeline Processing**
Linear data flow with context preservation:
```
Input → Clean → Parse → Execute → Format → Output
```

## System Architecture

### **High-Level Structure**

```
┌─────────────────────────────────────────┐
│                Entry Point              │  ← main.py
│            answer(query: str)           │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│             Orchestrator                │  ← Coordination & Lifecycle
│   • Pipeline Management                 │
│   • Error Handling & Fallbacks         │
│   • Logging & Monitoring               │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│            Layer Pipeline               │  ← Sequential Processing
│   • Context Management                  │
│   • Layer Coordination                  │
│   • Failure Recovery                    │
└─────────────────┬───────────────────────┘
                  │
     ┌────────────┼────────────┐
     │            │            │
┌────▼────┐  ┌────▼────┐  ┌────▼────┐
│ Prompt  │  │  Query  │  │Execution│  ← Processing Layers
│ Cleaner │  │ Parser  │  │ Engine  │
└─────────┘  └─────────┘  └─────────┘
                  │            │
                  │       ┌────▼────┐
                  │       │  Tool   │  ← Tool Adapters
                  │       │Adapters │
                  │       └─────────┘
                  │            │
┌─────────────────▼────────────▼─────────┐
│              Tool Layer                │  ← Domain-Specific Tools
│  Calculator | Weather | Currency      │
│  Knowledge Base | LLM Fallback        │
└───────────────────────────────────────┘
```

## Core Components

### **1. Orchestrator Layer**

**Purpose**: Central coordination hub for query processing

**Design Pattern**: **Facade Pattern** + **Chain of Responsibility**

**Key Responsibilities**:
- Pipeline assembly and configuration
- Query lifecycle management (start → process → complete)
- Error handling and fallback strategies
- Logging and performance monitoring

**Architecture**:
```python
class Orchestrator:
    def __init__(self, config: Dict[str, Any])
    def process_query(self, query: str, context: Dict[str, Any]) -> str
    def _build_pipeline(self) -> None
    def _handle_error(self, error: Exception, query: str) -> str
```

**Configuration-Driven Assembly**:
```python
config = {
    "prompt_cleaner": {...},
    "query_parser": {...}, 
    "execution_engine": {...},
    "custom_layers": [...]  # Extensibility point
}
```

### **2. Layer Pipeline System**

**Purpose**: Manages sequential processing with context preservation

**Design Pattern**: **Pipeline Pattern** + **Strategy Pattern**

**Core Interface**:
```python
@dataclass
class LayerResult:
    data: Any
    metadata: Optional[Dict[str, Any]]
    success: bool
    error_message: Optional[str]

class BaseLayer(ABC):
    def process(self, input_data: Any, context: Dict[str, Any]) -> LayerResult
```

**Processing Flow**:
1. **Input Validation**: Type and format checking
2. **Layer Execution**: Sequential processing with error handling
3. **Context Propagation**: Metadata and state passing
4. **Result Composition**: Success/failure aggregation

### **3. Query Processing Layers**

#### **Prompt Cleaner Layer**
**Purpose**: Input normalization and validation

**Transformations**:
- Whitespace normalization
- Case standardization
- Special character handling
- Input validation

#### **Query Parser Layer**
**Purpose**: Natural language to structured execution plan transformation

**Design Pattern**: **Strategy Pattern** + **Priority Queue**

**Pattern System**:
```python
class QueryPattern(ABC):
    priority: int
    def matches(self, query: str) -> bool
    def parse(self, query: str) -> ExecutionPlan
```

**Pattern Hierarchy** (by priority):
1. **ComponentBasedQueryParser** (Priority 60)
2. **MultiStepPattern** (Priority 50) 
3. **CurrencyPattern** (Priority 40)
4. **CalculatorPattern** (Priority 10)
5. **WeatherPattern** (Priority 8)
6. **KnowledgeBasePattern** (Priority 6)

**Execution Plan Structure**:
```python
@dataclass
class ExecutionPlan:
    type: QueryType
    steps: List[ExecutionStep]
    description: str

@dataclass
class ExecutionStep:
    tool: str
    operation: str
    parameters: Dict[str, Any]
    description: str
    variables: Dict[str, str]
```

#### **Execution Engine Layer**
**Purpose**: Structured plan execution with tool orchestration

**Design Pattern**: **Strategy Pattern** + **Adapter Pattern**

**Execution Strategies**:
```python
class SingleToolStrategy:
    def can_handle(self, plan: ExecutionPlan) -> bool
    def execute(self, plan: ExecutionPlan, engine: ExecutionEngine) -> Any

class MultiStepStrategy:
    def can_handle(self, plan: ExecutionPlan) -> bool
    def execute(self, plan: ExecutionPlan, engine: ExecutionEngine) -> Any
```

**Variable Management System**:
- **Variable Storage**: `${variable_name}` placeholder system
- **Substitution Engine**: Dynamic parameter replacement
- **Scope Isolation**: Per-query variable namespaces

## Data Flow Architecture

### **Single-Step Query Flow**

```
"What is 25% of 100?" 
    │
    ▼ [Prompt Cleaner]
"what is 25% of 100?"
    │
    ▼ [Query Parser → CalculatorPattern]
ExecutionPlan {
    type: SINGLE_TOOL,
    steps: [
        ExecutionStep {
            tool: "calculator",
            operation: "percent_of",
            parameters: {percentage: 25, number: 100}
        }
    ]
}
    │
    ▼ [Execution Engine → SingleToolStrategy]
calculator.percent_of(25, 100) → 25.0
    │
    ▼ [Result Formatting]
"25.0"
```

### **Multi-Step Query Flow**

```
"Add 10 to the average temperature in Paris and London"
    │
    ▼ [Prompt Cleaner]
"add 10 to the average temperature in paris and london"
    │
    ▼ [Query Parser → MultiStepPattern]
ExecutionPlan {
    type: MULTI_STEP,
    steps: [
        Step 1: weather.get_weather(city="paris") → var: temp1
        Step 2: weather.get_weather(city="london") → var: temp2  
        Step 3: calculator.average(numbers=[${temp1}, ${temp2}]) → var: avg
        Step 4: calculator.add(first_number=${avg}, second_number=10)
    ]
}
    │
    ▼ [Execution Engine → MultiStepStrategy]
Variables: {}
Step 1: weather.get_weather("paris") → 18.0 → Variables: {temp1: 18.0}
Step 2: weather.get_weather("london") → 17.0 → Variables: {temp1: 18.0, temp2: 17.0}
Step 3: calculator.average([18.0, 17.0]) → 17.5 → Variables: {..., avg: 17.5}
Step 4: calculator.add(17.5, 10) → 27.5
    │
    ▼ [Result Formatting]
## Tool Adapter Architecture

### **Design Pattern**: **Adapter Pattern**

**Purpose**: Standardizes tool interfaces and handles result formatting

**Adapter Types**:

#### **StandardToolAdapter**
- **Use Case**: Direct function mapping (Calculator, Currency, Knowledge Base)
- **Interface**: Direct parameter passing and result return

#### **WeatherToolAdapter** 
- **Use Case**: Special temperature data handling
- **Features**: 
  - Extracts numeric values from formatted strings ("18°C" → 18.0)
  - Dual format support (display + numeric)
  - Enables mathematical operations on temperature data

#### **LLMToolAdapter**
- **Use Case**: Language model integration
- **Features**: Prompt handling and response processing

**Registration Pattern**:
```python
class ExtensibleExecutionEngine:
    def initialize(self):
        self.register_tool_adapter("calculator", calculator_adapter)
        self.register_tool_adapter("weather", weather_adapter)
        self.register_tool_adapter("currency", currency_adapter)
        # ... additional tools
```

## Error Handling Architecture

### **Multi-Level Error Strategy**

**1. Layer-Level Error Handling**:
```python
class BaseLayer:
    def process(self, input_data: Any) -> LayerResult:
        try:
            # Layer processing logic
            return LayerResult(data=result, success=True)
        except Exception as e:
            return LayerResult(
                data=None, 
                success=False, 
                error_message=str(e)
            )
```

**2. Pipeline-Level Error Recovery**:
```python
class LayerPipeline:
    def process(self, input_data: Any) -> LayerResult:
        for layer in self.layers:
            result = layer.process(current_data)
            if not result.success:
                return LayerResult(
                    data=None,
                    success=False,
                    error_message=f"Layer {layer.name} failed: {result.error_message}"
                )
```

**3. Orchestrator-Level Fallbacks**:
```python
class Orchestrator:
    def process_query(self, query: str) -> str:
        try:
            result = self.pipeline.process(query)
            if result.success:
                return str(result.data)
            else:
                # LLM fallback strategy
                return self._llm_fallback(query)
        except Exception:
            # Ultimate fallback
            return f"Generated Answer for: {query}"
```

## Configuration System

### **Hierarchical Configuration**

**1. Orchestrator Configuration**:
```python
orchestrator_config = {
    "pipeline_name": "agent_pipeline",
    "prompt_cleaner": {...},
    "query_parser": {...},
    "execution_engine": {...},
    "custom_layers": [...]
}
```

**2. Layer-Specific Configuration**:
```python
parser_config = {
    "patterns": [CalculatorPattern, WeatherPattern, ...],
    "fallback_strategy": "llm",
    "enable_advanced_patterns": True
}
```

**3. Preset Configurations**:
```python
presets = {
    "default": {...},     
    "minimal": {...},      
    "enhanced": {...}     
}
```

## Extensibility Points

### **1. Adding New Tools**

**Step 1**: Create tool module
```python
# agent/tools/new_tool.py
def new_operation(param: str) -> str:
    return f"Processed: {param}"
```

**Step 2**: Create tool adapter
```python
new_adapter = StandardToolAdapter("new_tool", {
    "new_operation": new_tool.new_operation
})
```

**Step 3**: Register in execution engine
```python
execution_engine.register_tool_adapter("new_tool", new_adapter)
```

### **2. Adding New Query Patterns**

```python
class NewPattern(QueryPattern):
    def __init__(self):
        super().__init__("new_pattern", priority=15)
    
    def matches(self, query: str) -> bool:
        # Pattern matching logic
        
    def parse(self, query: str) -> ExecutionPlan:
        # Execution plan creation
```

### **3. Adding Custom Layers**

```python
class CustomLayer(BaseLayer):
    def process(self, input_data: Any, context: Dict[str, Any]) -> LayerResult:
        # Custom processing logic
        return LayerResult(data=processed_data, success=True)
```

## Performance Considerations

### **1. Pattern Matching Optimization**
- **Priority-based ordering**: Higher priority patterns checked first
- **Short-circuit evaluation**: Stop on first match
- **Regex compilation**: Pre-compiled regex patterns

### **2. Variable Management**
- **Lazy evaluation**: Variables substituted only when needed
- **Memory isolation**: Per-query variable scopes
- **Garbage collection**: Variables cleared after query completion

### **3. Tool Adapter Caching**
- **Adapter reuse**: Single adapter instances across queries
- **Connection pooling**: Ready for external API integration
- **Result formatting**: Efficient string formatting

## Security Considerations

### **1. Input Validation**
- **Type checking**: Strict input type validation
- **Sanitization**: Query cleaning and normalization
- **Length limits**: Protection against extremely long inputs

### **2. Error Information Disclosure**
- **Error masking**: Internal errors not exposed to users
- **Safe fallbacks**: Controlled error messages
- **Logging isolation**: Sensitive data not logged

### **3. Tool Isolation**
- **Sandboxed execution**: Tools cannot access system resources
- **Parameter validation**: All tool inputs validated
- **Exception handling**: Tools cannot crash the system

## Monitoring and Observability

### **1. Logging Architecture**
```python
class LoggingSystem:
    def start_query(self, query: str) -> None
    def log_execution_step(self, step_num: int, tool: str, operation: str) -> None
    def complete_query(self, result: str, success: bool) -> None
    def log_error(self, error: Exception, context: str) -> None
    def log_fallback(self, reason: str) -> None
```

### **2. Performance Metrics**
- **Query processing time**: End-to-end timing
- **Step execution time**: Individual operation timing
- **Success rates**: Query completion statistics
- **Error patterns**: Failure analysis

### **3. System Health**
- **Layer status**: Individual layer health checks
- **Tool availability**: Tool adapter status monitoring
- **Memory usage**: Resource consumption tracking



### 4. Query Parser Layer (agent/layers/query_parser.py)

**Purpose**: Converts natural language queries into structured execution plans

#### Pattern-Based Architecture

**Query Patterns**:
- **ComponentBasedQueryParser**: Handles component-based queries
- **CalculatorPattern**: Mathematical operations
- **WeatherPattern**: Weather-related queries
- **KnowledgeBasePattern**: Knowledge lookup queries
- **CurrencyPattern**: Currency conversion operations
- **MultiStepPattern**: Complex multi-step operations

**Pattern Interface**:
```python
class QueryPattern:
    priority: int
    def matches(query: str) -> bool
    def parse(query: str) -> ExecutionPlan
```

#### Multi-Step Pattern System

**Supported Patterns**:
- **math_avg_temp**: Math operations on temperature averages
- **math_specific_temp**: Math operations on specific temperatures
- **if_temp_math**: Conditional temperature mathematics
- **multi_city_temp**: Multi-city temperature aggregation
- **compare_temps**: Temperature comparisons
- **temp_range**: Temperature range operations (min/max)
- **summarize_weather**: Weather summarization
- **math_avg_currency**: Math operations on currency averages
- **convert_avg_currency**: Currency conversion with averaging

**Execution Plan Structure**:
```python
class ExecutionPlan:
    type: QueryType
    steps: List[ExecutionStep]
    description: str

class ExecutionStep:
    tool: str
    operation: str
    parameters: Dict[str, Any]
    description: str
    variables: Optional[Dict[str, str]]
```

### 5. Execution Engine Layer (agent/layers/execution_engine.py)

**Purpose**: Executes structured execution plans using appropriate tools

#### Tool Adapter System

**Tool Adapters**:
- **CalculatorToolAdapter**: Mathematical operations
- **WeatherToolAdapter**: Weather data retrieval
- **KnowledgeBaseToolAdapter**: Knowledge lookup
- **CurrencyToolAdapter**: Currency conversion

**Adapter Interface**:
```python
class ToolAdapter:
    def execute(operation: str, parameters: Dict[str, Any]) -> Any
    def _format_result(result: Any) -> str
```

#### Variable Substitution System

**Purpose**: Manages variable storage and substitution in multi-step operations

**Features**:
- **Variable Storage**: Stores intermediate results
- **Pattern Substitution**: Replaces ${variable_name} patterns
- **Type Conversion**: Handles different data types
- **Context Management**: Maintains variable scope

**Variable Substitution Flow**:
```python
def _substitute_variables(parameters: Dict[str, Any]) -> Dict[str, Any]:
    # Replace ${variable_name} with stored values
    # Handle nested substitutions
    # Type conversion and validation
```

#### Execution Strategies

**Single Tool Strategy**: Direct tool execution for simple queries
**Multi-Step Strategy**: Sequential execution with variable management
**Conditional Strategy**: Conditional execution based on intermediate results

### 6. Tool Layer

#### Calculator Tool (agent/tools/calculator.py)

**Operations**:
- **Basic Arithmetic**: add, subtract, multiply, divide
- **Percentage**: percent_of calculations
- **Aggregation**: average, sum
- **Advanced**: power, modulus

**Interface**:
```python
def evaluate(expression: str) -> float
def add(first_number: float, second_number: float) -> float
def subtract(first_number: float, second_number: float) -> float
def multiply(first_number: float, second_number: float) -> float
def divide(first_number: float, second_number: float) -> float
def percent_of(percentage: float, number: float) -> float
def average(numbers: List[float]) -> float
```

#### Weather Tool (agent/tools/weather.py)

**Purpose**: Provides weather data for global cities

**Data Structure**:
```python
_WEATHER_DATA = {
    "city_name": {
        "temperature": float,
        "description": str,
        "humidity": int,
        "wind_speed": float
    }
}
```

**Interface**:
```python
def get_weather(city: str) -> Dict[str, Any]
def temp(city: str) -> Union[str, float]
```

**Supported Cities**: 20+ major global cities with mock weather data

#### Knowledge Base Tool (agent/tools/knowledge_base.py)

**Purpose**: Provides factual information lookup

**Data Categories**:
- **Historical Figures**: Biographical information
- **Scientific Concepts**: Scientific definitions and explanations
- **General Knowledge**: Various factual information

**Interface**:
```python
def kb_lookup(query: str) -> str
def search_knowledge_base(query: str) -> Optional[str]
```

#### Currency Tool (agent/tools/currency.py)

**Purpose**: Currency conversion between major currencies

**Supported Currencies**: USD, EUR, GBP with configurable exchange rates

**Interface**:
```python
def convert_currency(amount: float, from_currency: str, to_currency: str) -> float
def get_exchange_rate(from_currency: str, to_currency: str) -> float
```

## Data Flow Architecture

### Query Processing Flow

```
User Query
    │
    ▼
┌─────────────┐
│ Entry Point │
└─────────────┘
    │
    ▼
┌─────────────┐
│Orchestrator │
└─────────────┘
    │
    ▼
┌─────────────┐
│Layer Pipeline│
└─────────────┘
    │
    ▼
┌─────────────┐
│Query Parser │ ← Pattern Matching
└─────────────┘   Execution Plan
    │
    ▼
┌─────────────┐
│Execution    │ ← Tool Execution
│Engine       │   Variable Management
└─────────────┘
    │
    ▼
┌─────────────┐
│Tool Layer   │ ← Specific Operations
└─────────────┘
    │
    ▼
┌─────────────┐
│Formatted    │
│Result       │
└─────────────┘
```

### Multi-Step Execution Flow

```
Step 1: Parse Query
    │
    ▼
Step 2: Generate Execution Plan
    │
    ▼
Step 3: Execute First Tool
    │
    ▼
Step 4: Store Result in Variables
    │
    ▼
Step 5: Substitute Variables in Next Step
    │
    ▼
Step 6: Execute Next Tool
    │
    ▼
Step 7: Repeat Until All Steps Complete
    │
    ▼
Step 8: Format Final Result
```

## Configuration System

### Layer Configuration

**Structure**:
```python
{
    "layer_name": {
        "enabled": bool,
        "config": {
            "specific_settings": Any
        }
    }
}
```

### Tool Configuration

**Exchange Rates**:
```python
EXCHANGE_RATES = {
    "USD_EUR": 0.85,
    "USD_GBP": 0.73,
    "EUR_USD": 1.18,
    "EUR_GBP": 0.86,
    "GBP_USD": 1.37,
    "GBP_EUR": 1.16
}
```

## Error Handling Architecture

### Layered Error Handling

1. **Tool Level**: Individual tool error handling
2. **Adapter Level**: Tool adapter error management
3. **Engine Level**: Execution engine error handling
4. **Pipeline Level**: Layer pipeline error management
5. **Orchestrator Level**: Top-level error handling and fallbacks

### Fallback Strategy

**LLM Fallback**: When structured processing fails, system falls back to a simple LLM-style response

```python
def _handle_fallback(query: str) -> str:
    return f"Generated Answer for: {query}"
```

## Extensibility Points

### Adding New Layers

1. Inherit from `BaseLayer`
2. Implement required methods
3. Register with orchestrator
4. Configure in pipeline

### Adding New Patterns

1. Inherit from `QueryPattern`
2. Implement pattern matching logic
3. Define execution plan generation
4. Register with query parser

### Adding New Tools

1. Create tool module
2. Implement tool interface
3. Create corresponding tool adapter
4. Register with execution engine

### Adding New Tool Adapters

1. Inherit from base adapter pattern
2. Implement execution logic
3. Add result formatting
4. Register with execution engine



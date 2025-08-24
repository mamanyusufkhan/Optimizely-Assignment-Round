# Test Documentation

## Overview

The test suite consists of 71 comprehensive test cases organized into 13 test classes, covering all aspects of the extensible agent system's functionality.

## Test Structure

### TestBasicFunctionality (5 tests)
Tests core functionality across all major tools:

- **test_percentage_calculation**: Validates calculator percentage operations (`12.5% of 243`)
- **test_knowledge_base_query**: Tests knowledge base lookups for historical figures
- **test_simple_arithmetic**: Tests basic arithmetic operations (`15 + 25`)
- **test_weather_query**: Validates weather data retrieval for cities
- **test_currency_conversion**: Tests currency conversion between major currencies

### TestTemperatureAndWeatherInterchangeability (5 tests)
Ensures "temperature" and "weather" terms work identically:

- **test_weather_vs_temperature_basic_query**: Basic city weather/temperature queries
- **test_weather_vs_temperature_averaging**: Averaging operations with both terms
- **test_weather_vs_temperature_math_operations**: Mathematical operations on both terms
- **test_weather_vs_temperature_comparison**: Comparison operations between cities
- **test_weather_vs_temperature_summarization**: Summarization with both terminologies

### TestMultiStepOperations (8 tests)
Complex multi-step operation validation:

- **test_temperature_averaging_with_addition**: 4-step: get temp1 → get temp2 → average → add
- **test_temperature_averaging_with_subtraction**: 4-step: get temp1 → get temp2 → average → subtract
- **test_temperature_averaging_with_multiplication**: 4-step: get temp1 → get temp2 → average → multiply
- **test_temperature_averaging_with_division**: 2-step: division operations with proper patterns
- **test_currency_with_averaging**: 3-step: average → currency conversion
- **test_weather_summarization**: Multi-step weather summarization with word limits
- **test_multi_city_temperature_operations**: Aggregation across multiple cities
- **test_conditional_temperature_math**: If-then conditional mathematical operations

### TestAdvancedMathOperations (3 tests)
Mathematical operation validation:

- **test_complex_percentage_calculations**: Various percentage calculations with edge cases
- **test_arithmetic_operations_comprehensive**: Addition, subtraction, multiplication, division
- **test_decimal_operations**: Decimal number arithmetic operations

### TestWeatherOperations (4 tests)
Weather-specific functionality:

- **test_single_city_weather_queries**: Individual city weather retrieval
- **test_temperature_comparison_operations**: Temperature comparisons between cities
- **test_temperature_range_operations**: Min/max temperature operations
- **test_multi_city_aggregation**: Aggregation operations across multiple cities

### TestCurrencyOperations (3 tests)
Currency conversion and calculations:

- **test_basic_currency_conversions**: USD↔EUR, USD↔GBP, EUR↔USD, GBP↔EUR conversions
- **test_currency_with_calculations**: Currency operations combined with mathematical calculations
- **test_decimal_currency_conversions**: Currency conversions with decimal amounts

### TestKnowledgeBaseOperations (3 tests)
Knowledge base functionality:

- **test_historical_figures**: Queries about historical personalities
- **test_scientific_concepts**: Queries about scientific topics
- **test_case_insensitive_knowledge_queries**: Case-insensitive knowledge retrieval

### TestErrorHandling (8 tests)
Error handling and edge cases:

- **test_empty_query**: Empty string input handling
- **test_invalid_city**: Non-existent city name handling
- **test_invalid_calculation**: Malformed mathematical expressions
- **test_nonsense_query**: Completely nonsensical input handling
- **test_malformed_math_queries**: Incomplete mathematical expressions
- **test_invalid_currency_codes**: Invalid currency code handling
- **test_extremely_long_queries**: Very long input string handling
- **test_special_characters_in_queries**: Special character handling in queries

### TestParsingSystem (4 tests)
Query parsing system validation:

- **test_parser_initialization**: Parser component initialization
- **test_percentage_pattern_recognition**: Percentage pattern matching validation
- **test_multi_step_pattern_recognition**: Multi-step pattern identification
- **test_pattern_priority**: Pattern priority and matching order validation
- **test_all_pattern_types**: Comprehensive pattern type recognition

### TestExecutionEngine (3 tests)
Execution engine functionality:

- **test_engine_initialization**: Execution engine component initialization
- **test_variable_substitution**: Variable substitution in multi-step operations
- **test_complex_variable_substitution**: Complex variable substitution scenarios

### TestRobustness (4 tests)
System reliability and performance:

- **test_concurrent_queries**: Multiple query handling without interference
- **test_memory_isolation**: Query isolation and state management
- **test_stress_testing**: 20 consecutive queries for performance validation
- **test_mixed_query_types**: Rapid switching between different query types

### TestTools (4 tests)
Individual tool validation:

- **test_calculator_operations**: All calculator operations (add, subtract, multiply, divide, percentage)
- **test_weather_tool_consistency**: Weather tool result consistency
- **test_currency_tool_accuracy**: Currency conversion accuracy validation
- **test_tool_error_handling**: Individual tool error handling

### TestIntegrationScenarios (2 tests)
Integration and workflow testing:

- **test_chained_operations**: Complex chained multi-step operations
- **test_mixed_language_patterns**: Alternative expressions for same operations

### TestMultiStepRegexCombinations (12 tests)
Comprehensive regex pattern validation with 200+ individual patterns:

#### test_two_step_weather_operations (25+ patterns)
Temperature retrieval + mathematical operations:
- **Addition patterns**: "Add 5 to the temperature in Paris", "Plus 3 to the weather in London"
- **Subtraction patterns**: "Subtract 4 from the temperature in Madrid", "Minus 6 from the weather in Sydney"
- **Multiplication patterns**: "Multiply the temperature in Paris by 2", "Double the temperature in Berlin"
- **Division patterns**: "Divide the temperature in Madrid by 2", "Halve the temperature in Mumbai"
- **Preposition variations**: "Add 10 with the temperature in Paris", "Combine 5 and the weather in London"
- **Time qualifiers**: "Add 5 to the temperature in Paris right now", "Subtract 3 from the weather in London currently"

#### test_three_step_temperature_averaging_math (30+ patterns)
Get temp1 + Get temp2 + Average + Math operation:
- **Addition to averages**: "Add 10 to the average temperature in Paris and London"
- **Subtraction from averages**: "Subtract 12 from the average temperature in Paris and London"
- **Multiplication with averages**: "Multiply the average temperature in Paris and London by 2"
- **Division with averages**: "Divide the average temperature in Paris and London by 2"
- **Alternative operation words**: "Increase", "Boost", "Reduce", "Decrease", "Sum", "Remove"
- **Global city combinations**: Paris/London, Berlin/Madrid, Tokyo/Sydney, Mumbai/Chicago, etc.
- **Time qualifiers**: "right now", "currently", "today", "now"

#### test_three_step_currency_averaging_conversion (15+ patterns)
Average numbers + Convert currency:
- **Basic patterns**: "Convert the average of 100 and 200 USD to EUR"
- **Alternative verbs**: "Change", "Transform", "Exchange"
- **Currency pairs**: USD↔EUR, USD↔GBP, EUR↔USD, GBP↔EUR
- **Decimal numbers**: "Convert the average of 99.99 and 100.01 USD to EUR"
- **Large numbers**: "Convert the average of 1000 and 2000 USD to EUR"

#### test_four_step_temperature_averaging_with_math (20+ patterns)
Most complex operations with explicit time qualifiers:
- **Addition patterns**: "Add 15 to the average temperature in Paris and London right now"
- **Subtraction patterns**: "Subtract 8 from the average temperature in Amsterdam and Rome right now"
- **Multiplication patterns**: "Multiply the average temperature in New York and Los Angeles by 3 right now"
- **Division patterns**: "Divide the average temperature in Tokyo and Sydney by 2 right now"
- **Operation variations**: "Sum", "Combine", "Join", "Merge"

#### test_conditional_temperature_patterns (15+ patterns)
If-then temperature mathematical operations:
- **Basic patterns**: "If the temperature in Paris is 18 and add 5"
- **Degree formats**: "If the temperature in Tokyo is 22°C and add 8"
- **Alternative formats**: "If the weather in Sydney is 28 degrees and subtract 6"
- **Operation words**: "plus", "minus", "times", with and without "I" prefix
- **Celsius variations**: "degrees celsius", "°c", "degrees"

#### test_temperature_comparison_patterns (15+ patterns)
Temperature comparison between cities:
- **Basic comparisons**: "Compare the temperatures between Paris and London"
- **Difference patterns**: "What's the difference in temperature between Paris and London"
- **Abbreviations**: "Diff the temperatures between Amsterdam and Rome"
- **Multiple cities**: "Compare temperatures among Paris, London and Berlin"
- **Time qualifiers**: "Compare the temperatures between Paris and London right now"

#### test_temperature_range_patterns (20+ patterns)
Temperature range operations (min/max):
- **Highest patterns**: "What's the highest temperature between Paris and London"
- **Lowest patterns**: "What's the lowest temperature between Paris and London"
- **Alternative words**: "maximum", "minimum", "max", "min"
- **Multiple cities**: "What's the highest temperature among Paris, London and Berlin"
- **Time qualifiers**: "What's the highest temperature between Paris and London right now"

#### test_multi_city_aggregation_patterns (20+ patterns)
Aggregation operations across cities:
- **Average patterns**: "Average the temperatures in Paris and London"
- **Sum patterns**: "Sum the temperatures in Paris and London"
- **Total patterns**: "Total the temperatures in Amsterdam and Rome"
- **Combine patterns**: "Combine the temperatures in New York and Los Angeles"
- **Multiple cities**: "Average the temperatures in Paris, London and Berlin"
- **Time qualifiers**: "Average the temperatures in Paris and London right now"

#### test_weather_summarization_patterns (15+ patterns)
Weather summarization with word count variations:
- **Word count variations**: 1-5 words with different cities
- **Temperature vs weather**: Both terminologies tested
- **Time qualifiers**: "today's weather", "today's temperature"
- **Preposition variations**: "of", "in", "using", "with"
- **Singular/plural**: "1 word" vs "2 words"

#### test_currency_math_combinations (15+ patterns)
Currency with mathematical operations:
- **Addition**: "Add 50 to the average of 100 and 200 USD"
- **Subtraction**: "Subtract 20 from the average of 100 and 200 USD"
- **Multiplication**: "Multiply the average of 50 and 100 USD by 2"
- **Division**: "Divide the average of 100 and 200 USD by 2"
- **Alternative words**: "Increase", "Reduce", "Double", "Halve"

#### test_complex_nested_operations (10+ patterns)
Complex nested operations:
- **Nested temperature**: "Add 10 to the result of averaging temperature in Paris and London"
- **Nested currency**: "Convert to EUR the result of adding 50 to average of 100 and 150 USD"
- **Mixed operations**: "Add the temperature in Paris to the average of 10 and 20"

#### test_edge_case_regex_patterns (15+ patterns)
Edge cases and variations:
- **Whitespace variations**: Extra spaces between words
- **Case variations**: UPPERCASE, lowercase, MiXeD cAsE
- **Punctuation**: Periods, exclamation marks, question marks
- **City name formats**: "New York City", "Los Angeles", "San Francisco"
- **Decimal numbers**: 5.5, 3.25, 2.5, 1.5
- **Alternative time expressions**: "at this moment", "as of now", "at present"



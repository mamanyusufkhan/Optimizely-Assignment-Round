import pytest
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from main import answer
from agent.layers.query_parser import ExtensibleQueryParser
from agent.layers.execution_engine import ExtensibleExecutionEngine
from agent.orchestrator import Orchestrator


class TestBasicFunctionality:
    
    def test_percentage_calculation(self):
        result = answer("What is 12.5% of 243?")
        assert result == "30.375"
    
    def test_knowledge_base_query(self):
        result = answer("Who is Ada Lovelace?")
        assert "mathematician" in result.lower()
        assert "computing" in result.lower() or "analytical engine" in result.lower()
    
    def test_simple_arithmetic(self):
        result = answer("What is 15 + 25?")
        assert result == "40.0"
    
    def test_weather_query(self):
        result = answer("What is the weather in Paris?")
        assert "°C" in result
    
    def test_currency_conversion(self):
        result = answer("Convert 100 USD to EUR")
        assert isinstance(result, str)
        assert result != ""


class TestTemperatureAndWeatherInterchangeability:

    def test_weather_vs_temperature_basic_query(self):

        temp_result = answer("What is the temperature in London?")
        weather_result = answer("What is the weather in London?")
        assert "°C" in temp_result
        assert "°C" in weather_result
    
    def test_weather_vs_temperature_averaging(self):
        temp_avg = answer("Average the temperature in Paris and London right now")
        weather_avg = answer("Average the weather in Paris and London right now")
        assert "°C" in temp_avg
        assert "°C" in weather_avg
    
    def test_weather_vs_temperature_math_operations(self):
        temp_math = answer("Add 5 to the average temperature in Paris and London")
        weather_math = answer("Add 5 to the average weather in Paris and London")
        assert "°C" in temp_math
        assert "°C" in weather_math
    
    def test_weather_vs_temperature_comparison(self):
        temp_compare = answer("Compare the temperatures between Paris and London")
        weather_compare = answer("Compare the weather between Paris and London")
        assert isinstance(temp_compare, str)
        assert isinstance(weather_compare, str)
    
    def test_weather_vs_temperature_summarization(self):
        temp_summary = answer("Summarize the temperature in Paris in 3 words")
        weather_summary = answer("Summarize the weather in Paris in 3 words")
        assert isinstance(temp_summary, str)
        assert isinstance(weather_summary, str)


class TestMultiStepOperations:
    def test_temperature_averaging_with_addition(self):
        result = answer("Add 10 to the average temperature in Paris and London right now.")
        assert result == "27.5°C"
    
    def test_temperature_averaging_with_subtraction(self):
        result = answer("Subtract 5 from the average temperature in Paris and London right now.")
        assert result == "12.5°C"
    
    def test_temperature_averaging_with_multiplication(self):
        result = answer("Multiply 2 with the average temperature in Paris and London right now.")
        assert result == "35.0°C"
    
    def test_temperature_averaging_with_division(self):
        result = answer("Divide 2 by the average temperature in Paris and London right now.")
        assert isinstance(result, str)
    
    def test_currency_with_averaging(self):
        result = answer("Convert the average of 10 and 20 USD into EUR")
        assert result == "12.75"
    
    def test_weather_summarization(self):
        result = answer("Summarize today's weather in Paris in 3 words.")
        assert "Summarize 18°C in exactly 3 words" in result
    
    def test_multi_city_temperature_operations(self):
        result = answer("Sum the temperatures in Paris, London and Berlin")
        assert isinstance(result, str)
        
    def test_conditional_temperature_math(self):
        result = answer("If the temperature in Paris is 18 and add 5")
        assert isinstance(result, str)


class TestAdvancedMathOperations:
    
    def test_complex_percentage_calculations(self):
        test_cases = [
            ("What is 25% of 80?", "20.0"),
            ("What is 33.5% of 200?", "67.0"),
            ("What is 0.5% of 1000?", "5.0"),
            ("What is 150% of 60?", "90.0")
        ]
        
        for query, expected in test_cases:
            result = answer(query)
            assert result == expected, f"Failed for query: {query}"
    
    def test_arithmetic_operations_comprehensive(self):
        test_cases = [
            ("What is 123 + 456?", "579.0"),
            ("What is 1000 - 234?", "766.0"),
            ("What is 25 * 8?", "200.0"),
            ("What is 144 / 12?", "12.0"),
            ("What is 17 + 28?", "45.0")  # Two number addition works
        ]
        
        for query, expected in test_cases:
            result = answer(query)
            assert result == expected, f"Failed for query: {query}"
    
    def test_decimal_operations(self):
        test_cases = [
            ("What is 12.5 + 7.3?", "19.8"),
            ("What is 100.0 - 25.75?", "74.25"),
            ("What is 3.14 * 2?", "6.28"),
            ("What is 50.5 / 5?", "10.1")
        ]
        
        for query, expected in test_cases:
            result = answer(query)
            assert result == expected, f"Failed for query: {query}"


class TestWeatherOperations:
    
    def test_single_city_weather_queries(self):
        cities = ["Paris", "London", "Tokyo", "New York", "Berlin"]
        
        for city in cities:
            result = answer(f"What is the weather in {city}?")
            assert "°C" in result, f"Failed for city: {city}"
            assert isinstance(result, str)
    
    def test_temperature_comparison_operations(self):
        test_cases = [
            "Compare the temperatures between Paris and London",
            "What's the difference in temperature between Tokyo and Berlin",
            "Compare weather of New York and Paris"
        ]
        
        for query in test_cases:
            result = answer(query)
            assert isinstance(result, str)
            assert result != ""
    
    def test_temperature_range_operations(self):
        test_cases = [
            "What's the highest temperature between Paris and London",
            "What's the lowest temperature among Paris, London and Berlin",
            "Find the maximum weather between Tokyo and New York",
            "Find the minimum temperature between Berlin and Paris"
        ]
        
        for query in test_cases:
            result = answer(query)
            assert isinstance(result, str)
            assert result != ""
    
    def test_multi_city_aggregation(self):
        test_cases = [
            "Average the temperatures in Paris and London",
            "Sum the weather in Tokyo, Berlin and Paris",
            "Total the temperatures in London, New York and Tokyo",
            "Combine the weather in Paris, London, Berlin and Tokyo"
        ]
        
        for query in test_cases:
            result = answer(query)
            assert isinstance(result, str)
            assert result != ""


class TestCurrencyOperations:
    def test_basic_currency_conversions(self):
        test_cases = [
            ("Convert 100 USD to EUR", "85.0"),
            ("Convert 50 EUR to USD", "58.82"),
            ("Convert 200 USD to GBP", "146.0"), 
            ("Convert 75 GBP to EUR", "87.33") 
        ]
        
        for query, expected in test_cases:
            result = answer(query)
            assert result == expected, f"Failed for query: {query}"
    
    def test_currency_with_calculations(self):
        test_cases = [
            "Convert the average of 50 and 100 USD into EUR",
            "Convert the sum of 25 and 75 USD into GBP", 
            "Add 20 to the average of 30 and 40 USD"
        ]
        
        for query in test_cases:
            result = answer(query)
            assert isinstance(result, str)
            assert result != ""
    
    def test_decimal_currency_conversions(self):
        test_cases = [
            "Convert 99.99 USD to EUR",
            "Convert 123.45 EUR to GBP",
            "Convert 250.50 GBP to USD"
        ]
        
        for query in test_cases:
            result = answer(query)
            assert isinstance(result, str)
            assert result != ""


class TestKnowledgeBaseOperations:

    
    def test_historical_figures(self):
        queries = [
            "Who is Ada Lovelace?",
            "Who is Marie Curie?", 
            "Who is Albert Einstein?",
            "Who is Isaac Newton?",
            "Who is Leonardo da Vinci?"
        ]
        
        for query in queries:
            result = answer(query)
            assert isinstance(result, str)
            assert len(result) > 10  
    
    def test_scientific_concepts(self):
        queries = [
            "What is photosynthesis?",
            "What is gravity?",
            "What is DNA?",
            "What is evolution?",
            "What is the periodic table?"
        ]
        
        for query in queries:
            result = answer(query)
            assert isinstance(result, str)
            assert len(result) > 10
    
    def test_case_insensitive_knowledge_queries(self):
        test_cases = [
            ("Who is ada lovelace?", "Who is Ada Lovelace?"),
            ("WHO IS MARIE CURIE?", "Who is Marie Curie?"),
            ("who is Albert Einstein?", "Who is Albert Einstein?")
        ]
        
        for lower_query, proper_query in test_cases:
            result1 = answer(lower_query)
            result2 = answer(proper_query)
            assert isinstance(result1, str)
            assert isinstance(result2, str)


class TestErrorHandling:
    
    def test_empty_query(self):
        result = answer("")
        assert isinstance(result, str)
        assert result != ""
    
    def test_invalid_city(self):
        result = answer("What is the weather in XyzInvalidCity123?")
        assert isinstance(result, str)
    
    def test_invalid_calculation(self):
        result = answer("What is abc% of xyz?")
        assert isinstance(result, str)
    
    def test_nonsense_query(self):
        result = answer("Blahblahblah random words xyz 123")
        assert isinstance(result, str)
        assert "Generated Answer" in result 
    
    def test_malformed_math_queries(self):

        malformed_queries = [
            "What is + 5?",
            "Calculate * 10",
            "What is 5 + + 3?",
            "Divide by zero",
            "What is % of 100?"
        ]
        
        for query in malformed_queries:
            result = answer(query)
            assert isinstance(result, str)
    
    def test_invalid_currency_codes(self):
        invalid_queries = [
            "Convert 100 XYZ to EUR",
            "Convert 50 USD to ABC", 
            "Convert 75 INVALID to FAKE"
        ]
        
        for query in invalid_queries:
            result = answer(query)
            assert isinstance(result, str)
    
    def test_extremely_long_queries(self):
        long_query = "What is the weather in " + "very " * 100 + "long city name?"
        result = answer(long_query)
        assert isinstance(result, str)
    
    def test_special_characters_in_queries(self):
        special_queries = [
            "What is 5 + 3 @#$%?",
            "Weather in Paris!!! ??? ###",
            "Convert 100 USD to EUR & GBP",
            "Who is Marie Curie??? !!! @@@"
        ]
        
        for query in special_queries:
            result = answer(query)
            assert isinstance(result, str)


class TestParsingSystem:
    
    def test_parser_initialization(self):
        parser = ExtensibleQueryParser()
        parser.initialize()
        assert len(parser.patterns) > 0
    
    def test_percentage_pattern_recognition(self):
        parser = ExtensibleQueryParser()
        parser.initialize()
        
        result = parser.process("What is 25% of 100?")
        plan = result.data
        
        assert plan.type.value == "single_tool"
        assert len(plan.steps) == 1
        assert plan.steps[0].tool == "calculator"
        assert plan.steps[0].operation == "percent_of"
    
    def test_multi_step_pattern_recognition(self):
        parser = ExtensibleQueryParser()
        parser.initialize()
        
        result = parser.process("Add 5 to the average temperature in New York and Chicago right now.")
        plan = result.data
        
        assert plan.type.value == "multi_step"
        assert len(plan.steps) == 4
    
    def test_pattern_priority(self):
        parser = ExtensibleQueryParser()
        parser.initialize()
        
        result = parser.process("Add 10 to the average temperature in Paris and London")
        plan = result.data
        
        assert plan.type.value == "multi_step"
        assert len(plan.steps) > 1
    
    def test_all_pattern_types(self):
        parser = ExtensibleQueryParser()
        parser.initialize()
        
        test_patterns = [
            ("What is 25% of 100?", "single_tool"),
            ("Add 5 to the average temperature in Paris and London", "multi_step"),
            ("What is the weather in Tokyo?", "single_tool"),
            ("Convert 100 USD to EUR", "single_tool"),
            ("Who is Ada Lovelace?", "single_tool")
        ]
        
        for query, expected_type in test_patterns:
            result = parser.process(query)
            plan = result.data
            assert plan.type.value == expected_type, f"Failed for query: {query}"


class TestExecutionEngine:
    def test_engine_initialization(self):
        engine = ExtensibleExecutionEngine()
        engine.initialize()
        assert "calculator" in engine.tool_adapters
        assert "weather" in engine.tool_adapters
        assert "knowledge_base" in engine.tool_adapters
        assert "currency" in engine.tool_adapters
    
    def test_variable_substitution(self):
        engine = ExtensibleExecutionEngine()
        engine.initialize()
        
        engine.variables = {"temp1": 20.0, "temp2": 25.0}
        
        params = {"numbers": ["${temp1}", "${temp2}"]}
        result = engine._substitute_variables(params)
        
        assert result["numbers"] == [20.0, 25.0]
    
    def test_complex_variable_substitution(self):
        engine = ExtensibleExecutionEngine()
        engine.initialize()
        
        engine.variables = {
            "temp1": 20.0,
            "temp2": 25.0, 
            "currency_amount": 100.0,
            "percentage": 15.5
        }
        
        test_cases = [
            ({"numbers": ["${temp1}", "${temp2}"]}, {"numbers": [20.0, 25.0]}),
            ({"first_number": "${currency_amount}", "second_number": "${percentage}"}, 
             {"first_number": 100.0, "second_number": 15.5}),
            ({"amount": "${currency_amount}"}, {"amount": 100.0})
        ]
        
        for input_params, expected in test_cases:
            result = engine._substitute_variables(input_params)
            assert result == expected


class TestRobustness:
    
    def test_concurrent_queries(self):
        queries = [
            "What is 10% of 50?",
            "Who is Marie Curie?",
            "Convert 50 USD to EUR",
            "What is the weather in London?",
            "Add 5 to the average temperature in Paris and Berlin",
            "What is 25 * 8?",
            "Compare temperatures between Tokyo and New York",
            "Summarize weather in London in 2 words"
        ]
        
        results = []
        for query in queries:
            result = answer(query)
            results.append(result)
            assert isinstance(result, str)
            assert result != ""
        

        assert all(len(result) > 0 for result in results)
    
    def test_memory_isolation(self):

 
        answer("Add 10 to the average temperature in Paris and London right now.")
        result = answer("What is 5 + 5?")
        assert result == "10.0"
        
        
        answer("Convert the average of 50 and 100 USD to EUR")
        result = answer("What is 3 * 7?")
        assert result == "21.0"
    
    def test_stress_testing(self):
        for i in range(20):
            query = f"What is {i} + {i*2}?"
            result = answer(query)
            expected = str(float(i + i*2))
            assert result == expected
    
    def test_mixed_query_types(self):
        query_sequence = [
            ("What is 10 + 5?", "15.0"),
            ("What is the weather in Paris?", None),  
            ("Who is Ada Lovelace?", None),  # 
            ("Convert 100 USD to EUR", "85.0"),
            ("What is 25% of 80?", "20.0"),
            ("Add 3 to the average temperature in London and Berlin", None) 
        ]
        
        for query, expected in query_sequence:
            result = answer(query)
            if expected:
                assert result == expected
            else:
                assert isinstance(result, str)
                assert len(result) > 0


class TestTools:
    
    def test_calculator_operations(self):
        operations = [
            ("What is 10 + 5?", "15.0"),
            ("What is 20 - 8?", "12.0"),
            ("What is 6 * 7?", "42.0"),
            ("What is 50 / 10?", "5.0"),
            ("What is 20% of 150?", "30.0")
        ]
        
        for query, expected in operations:
            result = answer(query)
            assert result == expected
    
    def test_weather_tool_consistency(self):
        result1 = answer("What is the weather in Paris?")
        result2 = answer("What is the weather in Paris?")
        assert result1 == result2
    
    def test_currency_tool_accuracy(self):
        result = answer("Convert 100 USD to EUR")
        assert result == "85.0"
    
    def test_tool_error_handling(self):
        test_cases = [
            "What is the weather in NonExistentCity12345?",
            "Convert 0 USD to EUR",
            "What is 0% of 100?",
            "Who is SomeRandomPersonWhoDoesntExist?"
        ]
        
        for query in test_cases:
            result = answer(query)
            assert isinstance(result, str)


class TestIntegrationScenarios:
    
    def test_chained_operations(self):
        result1 = answer("Add 5 to the average temperature in Paris and London")
        assert "°C" in result1
        
        result2 = answer("Convert the average of 75 and 125 USD to EUR") 
        assert isinstance(result2, str)
        
        result3 = answer("What is 15% of the result from 200 + 300?")
        assert isinstance(result3, str)
    
    def test_mixed_language_patterns(self):
        equivalent_queries = [
            ["Add 10 to the average temperature in Paris and London",
             "Plus 10 to the average temperature in Paris and London"],
            ["What is 25% of 100?", "Calculate 25 percent of 100"],
            ["Convert 100 USD to EUR", "Change 100 USD into EUR"]
        ]
        
        for query_group in equivalent_queries:
            results = [answer(query) for query in query_group]
            for result in results:
                assert isinstance(result, str)
                assert len(result) > 0


class TestMultiStepRegexCombinations:
    
    def test_two_step_weather_operations(self):
        two_step_patterns = [
            "Add 5 to the temperature in Paris",
            "Plus 3 to the weather in London", 
            "Increase the temperature in Berlin by 7",
            "Boost the weather in Tokyo by 2",
            

            "Subtract 4 from the temperature in Madrid",
            "Minus 6 from the weather in Sydney",
            "Reduce the temperature in Mumbai by 8",
            "Decrease the weather in Chicago by 1",
            
            "Multiply the temperature in Paris by 2",
            "Times the weather in London by 3",
            "Double the temperature in Berlin",
            "Triple the weather in Tokyo",
            
            "Divide the temperature in Madrid by 2",
            "Split the weather in Sydney by 4",
            "Halve the temperature in Mumbai",
            
            "Add 10 with the temperature in Paris",
            "Combine 5 and the weather in London",
            "Sum 3 plus the temperature in Berlin",
            

            "Add 5 to the temperature in Paris right now",
            "Subtract 3 from the weather in London currently",
            "Multiply the temperature in Berlin by 2 today",
            "Divide the weather in Tokyo by 4 now",
        ]
        
        for pattern in two_step_patterns:
            result = answer(pattern)
            assert isinstance(result, str)
            assert len(result) > 0
            print(f"✓ {pattern} -> {result}")
    
    def test_three_step_temperature_averaging_math(self):
        three_step_avg_patterns = [

            "Add 10 to the average temperature in Paris and London",
            "Plus 5 to the average weather in Berlin and Madrid",
            "Increase the average temperature in Tokyo and Sydney by 15",
            "Boost the average weather in Mumbai and Chicago by 8",
            "Sum 7 with the average temperature in Amsterdam and Rome",
            
            "Subtract 12 from the average temperature in Paris and London",
            "Minus 8 from the average weather in Berlin and Madrid",
            "Reduce the average temperature in Tokyo and Sydney by 6",
            "Decrease the average weather in Mumbai and Chicago by 4",
            "Remove 3 from the average temperature in Amsterdam and Rome",
            
            "Multiply the average temperature in Paris and London by 2",
            "Times the average weather in Berlin and Madrid by 3",
            "Double the average temperature in Tokyo and Sydney",
            "Triple the average weather in Mumbai and Chicago",
            "Scale the average temperature in Amsterdam and Rome by 1.5",
            
            "Divide the average temperature in Paris and London by 2",
            "Split the average weather in Berlin and Madrid by 4",
            "Halve the average temperature in Tokyo and Sydney",
            "Quarter the average weather in Mumbai and Chicago",
            
            "Add 5 to the average temperature in New York and Los Angeles",
            "Subtract 7 from the average weather in Beijing and Shanghai",
            "Multiply the average temperature in Delhi and Dhaka by 2",
            "Divide the average weather in Singapore and Dubai by 3",
            
            "Add 10 to the average temperature in Paris and London right now",
            "Subtract 5 from the average weather in Berlin and Madrid currently", 
            "Multiply the average temperature in Tokyo and Sydney by 2 today",
            "Divide the average weather in Mumbai and Chicago by 4 now",
        ]
        
        for pattern in three_step_avg_patterns:
            result = answer(pattern)
            assert isinstance(result, str)
            assert len(result) > 0
            print(f"✓ {pattern} -> {result}")
    
    def test_three_step_currency_averaging_conversion(self):
        currency_avg_patterns = [
            "Convert the average of 100 and 200 USD to EUR",
            "Change the average of 50 and 150 USD into GBP", 
            "Transform the average of 75 and 125 EUR to USD",
            "Exchange the average of 60 and 140 GBP into EUR",
            
            "Convert the average of 25 and 75 USD to EUR",
            "Change the average of 300 and 500 USD into GBP",
            "Transform the average of 80 and 120 EUR to USD", 
            "Exchange the average of 90 and 110 GBP into EUR",
            
            "Convert the average of 99.99 and 100.01 USD to EUR",
            "Change the average of 50.5 and 49.5 EUR into USD",
            "Transform the average of 75.25 and 74.75 GBP to EUR",
            
            "Convert the average of 1000 and 2000 USD to EUR",
            "Change the average of 5000 and 10000 EUR into GBP",
            "Transform the average of 250 and 750 GBP to USD",
        ]
        
        for pattern in currency_avg_patterns:
            result = answer(pattern)
            assert isinstance(result, str)
            assert len(result) > 0
            print(f"✓ {pattern} -> {result}")
    
    def test_four_step_temperature_averaging_with_math(self):
    
        four_step_patterns = [
            "Add 15 to the average temperature in Paris and London right now",
            "Plus 20 to the average weather in Berlin and Madrid currently",
            "Increase the average temperature in Tokyo and Sydney by 25 today",
            "Boost the average weather in Mumbai and Chicago by 10 now",
            
            "Subtract 8 from the average temperature in Amsterdam and Rome right now",
            "Minus 12 from the average weather in Delhi and Dhaka currently",
            "Reduce the average temperature in Beijing and Shanghai by 6 today",
            "Decrease the average weather in Singapore and Dubai by 4 now",
             
            "Multiply the average temperature in New York and Los Angeles by 3 right now",
            "Times the average weather in Moscow and Toronto by 2 currently",
            "Double the average temperature in Paris and London today",
            "Triple the average weather in Berlin and Madrid now",
            
            "Divide the average temperature in Tokyo and Sydney by 2 right now", 
            "Split the average weather in Mumbai and Chicago by 3 currently",
            "Halve the average temperature in Amsterdam and Rome today",
            "Quarter the average weather in Delhi and Dhaka now",
            
            "Sum 5 with the average temperature in Paris and London right now",
            "Combine 7 and the average weather in Berlin and Madrid currently",
            "Join 3 to the average temperature in Tokyo and Sydney today",
            "Merge 9 with the average weather in Mumbai and Chicago now",
        ]
        
        for pattern in four_step_patterns:
            result = answer(pattern)
            assert isinstance(result, str)
            assert len(result) > 0
            print(f"✓ {pattern} -> {result}")
    
    def test_conditional_temperature_patterns(self):
        conditional_patterns = [
            "If the temperature in Paris is 18 and add 5",
            "If the weather in London is 17 and subtract 3", 
            "If the temperature in Berlin is 20 and multiply 2",
            "If the weather in Madrid is 25 and divide 5",
            
            "If the temperature in Tokyo is 22°C and add 8",
            "If the weather in Sydney is 28 degrees and subtract 6",
            "If the temperature in Mumbai is 35°c and multiply 1.5",
            "If the weather in Chicago is 15 degrees celsius and divide 3",
            

            "If the temperature in Amsterdam is 19 and plus 4",
            "If the weather in Rome is 24 and minus 7",
            "If the temperature in Delhi is 32 and times 2",
            
            "If the temperature in Paris is 18 and I add 5",
            "If the weather in London is 17 and I subtract 3",
            "If the temperature in Berlin is 20 and I multiply 2", 
            "If the weather in Madrid is 25 and I divide 5",
            
        ]
        
        for pattern in conditional_patterns:
            result = answer(pattern)
            assert isinstance(result, str)
            assert len(result) > 0
            print(f"✓ {pattern} -> {result}")
    
    def test_temperature_comparison_patterns(self):
    
        comparison_patterns = [
            "Compare the temperatures between Paris and London",
            "Compare the weather between Berlin and Madrid", 
            "Compare temperatures of Tokyo and Sydney",
            "Compare weather of Mumbai and Chicago",
            
            "What's the difference in temperature between Paris and London",
            "What's the difference in weather between Berlin and Madrid",
            "Find the difference between temperatures in Tokyo and Sydney",
            "Calculate the difference between weather in Mumbai and Chicago",
            
            "Diff the temperatures between Amsterdam and Rome",
            "Diff the weather between Delhi and Dhaka",
            "Diff temperatures of Beijing and Shanghai", 
            "Diff weather of Singapore and Dubai",
            
            "Compare the temperatures between Paris and London right now",
            "Compare the weather between Berlin and Madrid currently",
            "Compare temperatures of Tokyo and Sydney today",
            "Compare weather of Mumbai and Chicago now",
            
            "Compare temperatures among Paris, London and Berlin",
            "Compare weather among Tokyo, Sydney and Mumbai",
            "Compare the temperatures across Paris and London",
            "Compare the weather across Berlin and Madrid",
        ]
        
        for pattern in comparison_patterns:
            result = answer(pattern)
            assert isinstance(result, str)
            assert len(result) > 0
            print(f"✓ {pattern} -> {result}")
    
    def test_temperature_range_patterns(self):
        range_patterns = [
            
            "What's the highest temperature between Paris and London",
            "Find the highest weather between Berlin and Madrid",
            "Get the maximum temperature between Tokyo and Sydney", 
            "Show the maximum weather between Mumbai and Chicago",
            "Identify the max temperature between Amsterdam and Rome",
            "Display the max weather between Delhi and Dhaka",
            
            "What's the lowest temperature between Paris and London",
            "Find the lowest weather between Berlin and Madrid",
            "Get the minimum temperature between Tokyo and Sydney",
            "Show the minimum weather between Mumbai and Chicago", 
            "Identify the min temperature between Amsterdam and Rome",
            "Display the min weather between Delhi and Dhaka",
            
            "What's the highest temperature among Paris, London and Berlin",
            "Find the lowest weather among Tokyo, Sydney and Mumbai",
            "Get the maximum temperature among Amsterdam, Rome and Madrid",
            "Show the minimum weather among Delhi, Dhaka and Chicago",
            
            "What's the highest temperature between Paris and London right now",
            "Find the lowest weather between Berlin and Madrid currently",
            "Get the maximum temperature between Tokyo and Sydney today",
            "Show the minimum weather between Mumbai and Chicago now",
        ]
        
        for pattern in range_patterns:
            result = answer(pattern)
            assert isinstance(result, str)
            assert len(result) > 0
            print(f"✓ {pattern} -> {result}")
    
    def test_multi_city_aggregation_patterns(self):
        aggregation_patterns = [
            "Average the temperatures in Paris and London",
            "Average the weather in Berlin and Madrid",
            "Calculate the average temperature in Tokyo and Sydney",
            "Find the average weather in Mumbai and Chicago",
 
            "Sum the temperatures in Paris and London", 
            "Sum the weather in Berlin and Madrid",
            "Total the temperatures in Tokyo and Sydney",
            "Add up the weather in Mumbai and Chicago",

            "Total the temperatures in Amsterdam and Rome",
            "Total the weather in Delhi and Dhaka", 
            "Sum up the temperatures in Beijing and Shanghai",
            "Add the weather in Singapore and Dubai",

            "Combine the temperatures in New York and Los Angeles",
            "Combine the weather in Moscow and Toronto",
            "Merge the temperatures in Paris and London",
            "Join the weather in Berlin and Madrid",

            "Average the temperatures in Paris, London and Berlin",
            "Sum the weather in Tokyo, Sydney and Mumbai", 
            "Total the temperatures in Amsterdam, Rome and Madrid",
            "Combine the weather in Delhi, Dhaka and Chicago",
            
            "Average the temperatures in Paris and London right now",
            "Sum the weather in Berlin and Madrid currently",
            "Total the temperatures in Tokyo and Sydney today", 
            "Combine the weather in Mumbai and Chicago now",
        ]
        
        for pattern in aggregation_patterns:
            result = answer(pattern)
            assert isinstance(result, str)
            assert len(result) > 0
            print(f"✓ {pattern} -> {result}")
    
    def test_weather_summarization_patterns(self):
        summarization_patterns = [
            "Summarize the weather in Paris in 1 word",
            "Summarize the weather in London in 2 words",
            "Summarize the weather in Berlin in 3 words", 
            "Summarize the weather in Madrid in 4 words",
            "Summarize the weather in Tokyo in 5 words",
            
            "Summarize the temperature in Paris in 1 word",
            "Summarize the temperature in London in 2 words",
            "Summarize the temperature in Berlin in 3 words",
            "Summarize the temperature in Madrid in 4 words",

            "Summarize today's weather in Paris in 2 words",
            "Summarize today's temperature in London in 3 words",
            "Summarize today's weather in Berlin in 4 words",
            "Summarize today's temperature in Madrid in 5 words",

            "Summarize weather of Paris in 3 words",
            "Summarize temperature of London in 2 words", 
            "Summarize the weather of Berlin using 4 words",
            "Summarize the temperature of Madrid with 5 words",

            "Summarize the weather in Tokyo in 1 word",
            "Summarize the temperature in Sydney using 1 word",
            "Summarize weather in Mumbai with 1 word",
        ]
        
        for pattern in summarization_patterns:
            result = answer(pattern)
            assert isinstance(result, str)
            assert len(result) > 0
            print(f"✓ {pattern} -> {result}")
    
    def test_currency_math_combinations(self):
        currency_math_patterns = [

            "Add 50 to the average of 100 and 200 USD",
            "Plus 25 to the average of 75 and 125 EUR",
            "Increase the average of 80 and 120 GBP by 30",
            "Boost the average of 90 and 110 USD by 40", 

            "Subtract 20 from the average of 100 and 200 USD",
            "Minus 15 from the average of 75 and 125 EUR",
            "Reduce the average of 80 and 120 GBP by 10",
            "Decrease the average of 90 and 110 USD by 5",
            
            "Multiply the average of 50 and 100 USD by 2",
            "Times the average of 60 and 140 EUR by 3",
            "Double the average of 75 and 125 GBP",
            "Triple the average of 40 and 80 USD",
            
            "Divide the average of 100 and 200 USD by 2",
            "Split the average of 150 and 250 EUR by 4", 
            "Halve the average of 80 and 120 GBP",
            "Quarter the average of 100 and 300 USD",
        ]
        
        for pattern in currency_math_patterns:
            result = answer(pattern)
            assert isinstance(result, str)
            assert len(result) > 0
            print(f"✓ {pattern} -> {result}")
    
    def test_complex_nested_operations(self):
        complex_patterns = [
            "Add 10 to the result of averaging temperature in Paris and London",
            "Multiply by 2 the sum of weather in Berlin and Madrid",
            "Subtract 5 from the total of temperatures in Tokyo and Sydney",
            "Divide by 3 the combination of weather in Mumbai and Chicago",
            
            "Convert to EUR the result of adding 50 to average of 100 and 150 USD",
            "Change to GBP the result of multiplying average of 75 and 125 USD by 2",
            "Transform to USD the result of subtracting 25 from average of 200 and 300 EUR",
            
            "Add the temperature in Paris to the average of 10 and 20",
            "Multiply the weather in London by the result of 5 plus 3",
            "Subtract the temperature in Berlin from the sum of 15 and 25",
            "Divide the weather in Madrid by the average of 2 and 4",
        ]
        
        for pattern in complex_patterns:
            result = answer(pattern)
            assert isinstance(result, str)
            assert len(result) > 0
            print(f"✓ {pattern} -> {result}")
    
    def test_edge_case_regex_patterns(self):
        edge_case_patterns = [

            "Add  5  to  the  temperature  in  Paris",
            "Subtract   3   from   weather   in   London",
            "Multiply    the    average    temperature    in    Berlin    and    Madrid    by    2",
            
            "ADD 5 TO THE TEMPERATURE IN PARIS",
            "subtract 3 from weather in london", 
            "MuLtIpLy ThE aVeRaGe TeMs In BeRlIn AnD mAdRiD bY 2",
            

            "Add 5 to the temperature in Paris.",
            "Subtract 3 from weather in London!",
            "Multiply the average temps in Berlin and Madrid by 2?",
            "Divide the weather in Tokyo by 4...",
            

            "Add 5 to temperature in New York City",
            "Subtract 3 from weather in Los Angeles", 
            "Multiply average temps in San Francisco and Las Vegas by 2",

            "Add 5.5 to the temperature in Paris",
            "Subtract 3.25 from weather in London",
            "Multiply the average temps in Berlin and Madrid by 2.5",
            "Divide the weather in Tokyo by 1.5",
            
            "Add 5 to temperature in Paris at this moment",
            "Subtract 3 from weather in London as of now",
            "Multiply average temps in Berlin and Madrid by 2 at present",
        ]
        
        for pattern in edge_case_patterns:
            result = answer(pattern)
            assert isinstance(result, str)
            assert len(result) > 0
            print(f"✓ {pattern} -> {result}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

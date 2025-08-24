
import requests
import os
from typing import Optional, Dict

class CurrencyError(Exception):
    
    def __init__(self, message="Currency conversion error occurred"):
        super().__init__(message)

class InvalidAmountError(CurrencyError):

    def __init__(self, message="Invalid amount provided"):
        super().__init__(message)

class InvalidCurrencyCodeError(CurrencyError):

    def __init__(self, message="Invalid currency code format"):
        super().__init__(message)

class UnsupportedCurrencyError(CurrencyError):
    def __init__(self, message="Currency not supported"):
        super().__init__(message)

class CurrencyCalculationError(CurrencyError):
    def __init__(self, message="Currency calculation failed"):
        super().__init__(message)

# Exchange rates relative to USD (to represent an API)
_EXCHANGE_RATES = {
    "USD": 1.0,      
    "EUR": 0.85,     
    "GBP": 0.73,     
    "JPY": 110.0,   
    "CAD": 1.25,    
    "AUD": 1.35,     
    "CHF": 0.92,     
    "CNY": 6.45,     
}

def _validate_amount(amount): 
    if not isinstance(amount, (int, float)):
        raise InvalidAmountError("Amount must be a number")
    
    if amount < 0:
        raise InvalidAmountError("Amount cannot be negative")


def _validate_currency_codes(from_currency, to_currency):
    
    if not isinstance(from_currency, str) or not isinstance(to_currency, str):
        raise InvalidCurrencyCodeError("Currency codes must be strings")


def _validate_currency_format(currency_code):

    if len(currency_code) != 3: 
        raise InvalidCurrencyCodeError("Currency codes must be 3 letters (e.g., USD, EUR)")
    
    if not currency_code.isalpha():
        raise InvalidCurrencyCodeError("Currency codes must contain only letters")

def _validate_currency_support(currency_code):
    if currency_code not in _EXCHANGE_RATES:
        available_currencies = ", ".join(sorted(_EXCHANGE_RATES.keys()))
        raise UnsupportedCurrencyError(
            f"Unsupported currency: {currency_code}. "
            f"Supported currencies: {available_currencies}"
        )

def _get_exchange_rate_from_api(from_currency: str, to_currency: str) -> Optional[float]:
    api_key = os.getenv('EXCHANGE_RATE_API_KEY')
    if not api_key:
        return None
    
    try:
        # Using exchangerate-api.com as an example (you can use any exchange rate API)
        base_url = f"https://v6.exchangerate-api.com/v6/{api_key}/pair/{from_currency}/{to_currency}"
        
        response = requests.get(base_url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('result') == 'success':
                return data.get('conversion_rate')
        
        return None
        
    except (requests.RequestException, KeyError, ValueError):
      
        return None

def _get_exchange_rate_from_fallback(from_currency: str, to_currency: str) -> float:
   
    if from_currency == to_currency:
        return 1.0
    
    if from_currency not in _EXCHANGE_RATES:
        raise UnsupportedCurrencyError(f"Currency {from_currency} not supported in fallback data")
    if to_currency not in _EXCHANGE_RATES:
        raise UnsupportedCurrencyError(f"Currency {to_currency} not supported in fallback data")
    
    
    usd_rate_from = 1.0 / _EXCHANGE_RATES[from_currency]
    rate_to_target = _EXCHANGE_RATES[to_currency]
    
    return usd_rate_from * rate_to_target

def currency_convert(amount: float, from_currency: str, to_currency: str) -> float:
   
    try:
        _validate_amount(amount)
        _validate_currency_codes(from_currency, to_currency)
        
        
        from_curr = from_currency.strip().upper()
        to_curr = to_currency.strip().upper()
        
        _validate_currency_format(from_curr)
        _validate_currency_format(to_curr)
        
    
        if from_curr == to_curr:
            return round(float(amount), 2)
        
        
        exchange_rate = _get_exchange_rate_from_api(from_curr, to_curr)
        
        if exchange_rate is not None:
            result = amount * exchange_rate
            return round(result, 2)
        
    
        _validate_currency_support(from_curr)
        _validate_currency_support(to_curr)
        
        exchange_rate = _get_exchange_rate_from_fallback(from_curr, to_curr)
        result = amount * exchange_rate
        
        return round(result, 2)
        
    except (InvalidAmountError, InvalidCurrencyCodeError, UnsupportedCurrencyError) as e:
        raise e
    except (ZeroDivisionError, OverflowError) as e:
        raise CurrencyCalculationError(f"Currency conversion calculation error: {e}")
    except Exception as e:
        raise CurrencyError(f"Unexpected currency conversion error: {e}")

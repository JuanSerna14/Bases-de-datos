import decimal
from datetime import datetime

def format_currency(value):
    """Formatea un valor decimal como moneda"""
    if isinstance(value, (decimal.Decimal, float, int)):
        return f"${value:,.2f}"
    return value

def format_date(date_value, format_str='%Y-%m-%d %H:%M:%S'):
    """Formatea una fecha a string"""
    if isinstance(date_value, datetime):
        return date_value.strftime(format_str)
    return date_value

def validate_decimal(value):
    """Valida y convierte un valor a Decimal"""
    try:
        return decimal.Decimal(str(value))
    except (decimal.InvalidOperation, ValueError):
        return None
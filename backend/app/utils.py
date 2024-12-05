from datetime import datetime

def parse_date(date_str):
    """Convierte una cadena de texto a un objeto de fecha"""
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise ValueError(f"Fecha inválida: {date_str}. Formato esperado: YYYY-MM-DD")

def calculate_total(items, key):
    """Calcula el total de un campo en una lista de diccionarios"""
    return sum(item[key] for item in items)


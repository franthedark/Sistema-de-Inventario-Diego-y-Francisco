from datetime import datetime

# Función para calcular las ganancias (precio de venta menos IVA y costo de producto)
def calculate_profit(price: float, cost: float, iva: float):
    price_without_iva = price / (1 + iva)
    profit = price_without_iva - cost
    return profit

# Función para formatear fechas
def format_date(date: datetime):
    return date.strftime('%Y-%m-%d %H:%M:%S')

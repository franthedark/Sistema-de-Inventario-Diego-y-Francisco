from litestar import post, get
from app.database import SessionLocal
from app.models import Product, Purchase, PurchaseItem, Sale, SaleItem
from app.auth import verify_token, create_access_token
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from app.utils import calculate_profit
from datetime import datetime

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Ruta para crear una compra
@post("/purchase")
def create_purchase(supplier: str, items: list, db: Session = Depends(get_db)):
    total_purchase = 0.0
    purchase = Purchase(supplier=supplier)
    db.add(purchase)
    db.commit()
    db.refresh(purchase)

    for item in items:
        product = db.query(Product).filter(Product.id == item['product_id']).first()
        if not product:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        total_purchase += item['quantity'] * item['price']
        purchase_item = PurchaseItem(product_id=item['product_id'], quantity=item['quantity'], price=item['price'], purchase_id=purchase.id)
        db.add(purchase_item)
        product.stock += item['quantity']  # Actualizar stock de producto
        db.add(product)

    purchase.total = total_purchase
    db.commit()
    return {"message": "Compra registrada exitosamente", "purchase_id": purchase.id}

# Ruta para crear una venta
@post("/sale")
def create_sale(items: list, db: Session = Depends(get_db)):
    total_sale = 0.0
    total_iva = 0.0
    sale = Sale()
    db.add(sale)
    db.commit()
    db.refresh(sale)

    for item in items:
        product = db.query(Product).filter(Product.id == item['product_id']).first()
        if not product:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        if product.stock < item['quantity']:
            raise HTTPException(status_code=400, detail="Stock insuficiente")
        total_sale += item['quantity'] * item['price']
        total_iva += (item['quantity'] * item['price']) * 0.19  # IVA del 19%

        sale_item = SaleItem(product_id=item['product_id'], quantity=item['quantity'], price=item['price'], sale_id=sale.id)
        db.add(sale_item)
        product.stock -= item['quantity']  # Reducir stock de producto
        db.add(product)

    sale.total = total_sale
    sale.iva = total_iva
    db.commit()
    return {"message": "Venta registrada exitosamente", "sale_id": sale.id}

# Ruta para generar reporte de ventas
@get("/report")
def generate_report(start_date: datetime, end_date: datetime, db: Session = Depends(get_db)):
    sales = db.query(Sale).filter(Sale.date >= start_date, Sale.date <= end_date).all()
    report = []
    total_sales = 0.0
    total_profit = 0.0

    for sale in sales:
        for item in sale.products:
            product = db.query(Product).filter(Product.id == item.product_id).first()
            profit = calculate_profit(item.price, product.price, 0.19)  # IVA 19%
            total_sales += item.quantity * item.price
            total_profit += profit * item.quantity
            report.append({
                "product": product.name,
                "quantity": item.quantity,
                "price": item.price,
                "profit": profit,
            })

    return {"report": report, "total_sales": total_sales, "total_profit": total_profit}

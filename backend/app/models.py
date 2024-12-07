from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, ForeignKey, DateTime, Text
from datetime import datetime
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    compras = relationship("Compra", back_populates="user")
    ventas = relationship("Venta", back_populates="user")

class Producto(Base):
    __tablename__ = 'productos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)
    precio = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False, default=0)
    imagen = Column(String(255), nullable=True)
    estado = Column(Boolean, default=True)

class Compra(Base):
    __tablename__ = 'compras'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))  # Relación con el usuario
    fecha = Column(DateTime, default=datetime.utcnow)
    proveedor = Column(String(100), nullable=False)
    detalles = relationship("DetalleCompra", back_populates="compra")
    user = relationship("User", back_populates="compras")
    total = Column(Float, nullable=False, default=0.0)

class DetalleCompra(Base):
    __tablename__ = 'detalles_compra'
    id = Column(Integer, primary_key=True, autoincrement=True)
    compra_id = Column(Integer, ForeignKey('compras.id'))
    producto_id = Column(Integer, ForeignKey('productos.id'))
    cantidad = Column(Integer, nullable=False)
    precio = Column(Float, nullable=False)
    compra = relationship("Compra", back_populates="detalles")
    producto = relationship("Producto")

class Venta(Base):
    __tablename__ = 'ventas'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))  # Relación con el usuario
    fecha = Column(DateTime, default=datetime.utcnow)
    detalles = relationship("DetalleVenta", back_populates="venta")
    user = relationship("User", back_populates="ventas")
    total = Column(Float, nullable=False, default=0)

    total_productos_vendidos = Column(Integer, default=0)  # Para contar productos vendidos
    total_costo_productos = Column(Float, default=0.0)     # Para contar el costo de los productos
    ganancias = Column(Float, default=0.0) 

class DetalleVenta(Base):
    __tablename__ = 'detalles_venta'
    id = Column(Integer, primary_key=True, autoincrement=True)
    venta_id = Column(Integer, ForeignKey('ventas.id'))
    producto_id = Column(Integer, ForeignKey('productos.id'))
    cantidad = Column(Integer, nullable=False)
    precio = Column(Float, nullable=False)
    venta = relationship("Venta", back_populates="detalles")
    producto = relationship("Producto")

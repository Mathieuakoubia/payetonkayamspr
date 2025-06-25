from sqlalchemy.orm import relationship
from .Databases import Base
import datetime
from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, ForeignKey, Boolean, Text, Date, TIMESTAMP, Numeric


class Reseller(Base):
    __tablename__ = "resellers"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    address = Column(Text)
    email = Column(String(100), unique=True, nullable=False)
    api_key = Column(String(100), unique=True, index=True)
    created_at = Column(TIMESTAMP)
    is_active = Column(Boolean, default=True)

    

    products = relationship("Product", back_populates="reseller")


class Customer(Base):
    __tablename__ = "customers"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    address = Column(Text)
    birthdate = Column(Date)
    email = Column(String(100))  # <-- ajout ici

    orders = relationship("Order", back_populates="customer")



class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    description = Column(Text)
    category = Column(String(50))
    price = Column(Numeric(10,2))
    image = Column(Text)
    reseller_id = Column(Integer, ForeignKey("resellers.id"), nullable=True)

    reseller = relationship("Reseller", back_populates="products")
    stock = relationship("Stock", back_populates="product", uselist=False)
    order_items = relationship("OrderItem", back_populates="product")

class Stock(Base):
    __tablename__ = "stock"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))
    quantity = Column(Integer)
    last_updated = Column(TIMESTAMP)

    product = relationship("Product", back_populates="stock")


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(50), nullable=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    created_at = Column(TIMESTAMP)

    customer = relationship("Customer", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    price = Column(Numeric(10,2))

    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")
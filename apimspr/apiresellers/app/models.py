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
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP)

    # Reseller
    api_keys = relationship("ApiKey", back_populates="reseller")



class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    address = Column(Text)
    birthdate = Column(Date)
    email = Column(Text)
    is_active = Column(Boolean, default=True)

    orders = relationship("Order", back_populates="customer")





class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    description = Column(Text)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"))
    price = Column(Numeric(10, 2))
    image = Column(Text)

    stock = relationship("Stock", back_populates="product", uselist=False)
    order_items = relationship("OrderItem", back_populates="product")

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True)

class ApiKey(Base):
    __tablename__ = "api_keys"
    id = Column(Integer, primary_key=True, index=True)
    key_hash = Column(String(255), nullable=False, unique=True)
    type = Column(String(20), nullable=False)
    reseller_id = Column(Integer, ForeignKey("resellers.id", ondelete="CASCADE"), nullable=True)
    revoked = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP)

    # ApiKey
    reseller = relationship("Reseller", back_populates="api_keys")


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

class Prospect(Base):
    __tablename__ = "prospects"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    address = Column(Text)
    birthdate = Column(Date)
    email = Column(Text)

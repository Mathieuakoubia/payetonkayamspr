from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime


class ResellerBase(BaseModel):
    first_name: str
    last_name: str
    address: str
    email: str

class ResellerCreate(ResellerBase):
    pass

class ResellerOut(ResellerBase):
    id: int
    api_key: str
    created_at: datetime

    class Config:
        from_attributes = True




from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str
    description: str
    category: str
    price: float
    image: str

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True



class StockBase(BaseModel):
    quantity: int

class StockCreate(StockBase):
    product_id: int

class StockUpdate(BaseModel):
    quantity: int

class StockOut(StockBase):
    id: int
    product_id: int
    last_updated: datetime

    class Config:
        from_attributes = True


class CustomerBase(BaseModel):
    first_name: str
    last_name: str
    address: str
    birthdate: date
    email: str

class CustomerCreate(CustomerBase):
    pass

class CustomerOut(CustomerBase):
    id: int

    class Config:
        from_attributes = True

# ---------------------- Order ----------------------
class OrderBase(BaseModel):
    order_number:  Optional[str] = None
    customer_id: int

class OrderCreate(OrderBase):
    pass

class OrderOut(OrderBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# ---------------------- Order Item ----------------------
class OrderItemBase(BaseModel):
    order_id: int
    product_id: int
    quantity: int
    price: float

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemOut(OrderItemBase):
    id: int

    class Config:
        from_attributes = True

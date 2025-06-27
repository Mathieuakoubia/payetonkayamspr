from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime

# ---------------------- Reseller ----------------------
class ResellerBase(BaseModel):
    first_name: str
    last_name: str
    address: str
    email: str

class ResellerCreate(ResellerBase):
    pass

class ResellerOut(ResellerBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ---------------------- Api Key ----------------------
class ApiKeyBase(BaseModel):
    key_hash: str
    type: str  # 'reseller' ou 'webshop'
    reseller_id: Optional[int] = None

class ApiKeyCreate(ApiKeyBase):
    pass

class ApiKeyOut(ApiKeyBase):
    id: int
    revoked: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ---------------------- Category ----------------------
class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryOut(CategoryBase):
    id: int

    class Config:
        from_attributes = True


# ---------------------- Product ----------------------
class ProductBase(BaseModel):
    name: str
    description: str
    category_id: int
    price: float
    image: str

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True


# ---------------------- Stock ----------------------
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


# ---------------------- Customer ----------------------
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
    is_active: bool

    class Config:
        from_attributes = True


# ---------------------- Order ----------------------
class OrderBase(BaseModel):
    order_number: Optional[str] = None
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


# ---------------------- Prospect ----------------------
class ProspectBase(BaseModel):
    first_name: str
    last_name: str
    address: str
    birthdate: date
    email: str

class ProspectCreate(ProspectBase):
    pass

class ProspectOut(ProspectBase):
    id: int

    class Config:
        from_attributes = True

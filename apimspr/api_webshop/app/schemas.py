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

class CategoryUpdate(BaseModel):
    name: Optional[str] = None

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

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None
    price: Optional[float] = None
    image: Optional[str] = None

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

class CustomerUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    address: Optional[str] = None
    birthdate: Optional[date] = None
    email: Optional[str] = None

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

class OrderUpdate(BaseModel):
    order_number: Optional[str] = None
    customer_id: Optional[int] = None

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

class OrderItemUpdate(BaseModel):
    order_id: Optional[int] = None
    product_id: Optional[int] = None
    quantity: Optional[int] = None
    price: Optional[float] = None

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

class ProspectUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    address: Optional[str] = None
    birthdate: Optional[date] = None
    email: Optional[str] = None

class ProspectOut(ProspectBase):
    id: int

    class Config:
        from_attributes = True

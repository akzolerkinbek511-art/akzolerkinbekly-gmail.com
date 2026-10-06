"""
ОН 7.2 — 30-тапсырма: Dataclass / DTO / Pydantic модельдері
FoodExpress деректер модельдері
"""

from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, field_validator, EmailStr, ConfigDict


class OrderStatus(str, Enum):
    NEW = "new"
    PAID = "paid"
    PREPARING = "preparing"
    DELIVERING = "delivering"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    RETURNED = "returned"


class PaymentMethod(str, Enum):
    KASPI = "kaspi"
    HALYK = "halyk"
    CARD = "card"
    CASH = "cash"


# ---------- Pydantic (API / валидация) ----------

class UserCreate(BaseModel):
    phone: str = Field(..., pattern=r"^\+7\d{10}$", examples=["+77001234567"])
    full_name: str = Field(..., min_length=2, max_length=150)
    password: str = Field(..., min_length=8)

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if not any(c.isupper() for c in v):
            raise ValueError("Құпиясөзде кемінде 1 бас әріп болуы керек")
        if not any(c.isdigit() for c in v):
            raise ValueError("Құпиясөзде кемінде 1 цифр болуы керек")
        return v


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    phone: str
    full_name: str
    is_active: bool
    created_at: datetime


class AddressCreate(BaseModel):
    title: Optional[str] = Field(None, max_length=50)
    full_address: str = Field(..., min_length=5, max_length=300)
    latitude: Optional[Decimal] = None
    longitude: Optional[Decimal] = None
    is_default: bool = False


class DishOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: Optional[str] = None
    price: Decimal
    is_available: bool
    restaurant_id: int
    category_id: Optional[int] = None


class OrderItemIn(BaseModel):
    dish_id: int
    quantity: int = Field(..., ge=1, le=99)


class CreateOrderDTO(BaseModel):
    restaurant_id: int
    address_id: int
    items: list[OrderItemIn] = Field(..., min_length=1)
    promo_code: Optional[str] = Field(None, max_length=50)


class OrderOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    restaurant_id: int
    status: OrderStatus
    total_amount: Decimal
    delivery_fee: Decimal
    discount_amount: Decimal
    promo_code: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class PaymentIn(BaseModel):
    method: PaymentMethod
    amount: Decimal = Field(..., gt=0)


class PaymentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    order_id: int
    amount: Decimal
    method: PaymentMethod
    status: str
    transaction_id: Optional[str] = None
    paid_at: Optional[datetime] = None


class ReviewCreate(BaseModel):
    order_id: int
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = Field(None, max_length=1000)

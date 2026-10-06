"""
ОН 7.2 — 29-тапсырма: Функция сигнатуралары
10 талаптан skeleton код (type hints + docstring).
Жүйе: FoodExpress
"""

from typing import Optional
from datetime import datetime
from decimal import Decimal
from enum import Enum


class OrderStatus(str, Enum):
    NEW = "new"
    PAID = "paid"
    PREPARING = "preparing"
    DELIVERING = "delivering"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    RETURNED = "returned"


def register_user(phone: str, full_name: str, password: str) -> dict:
    """
    Пайдаланушыны телефон нөмірімен тіркейді.

    Args:
        phone: +7XXXXXXXXXX форматындағы телефон
        full_name: Толық аты-жөні
        password: Құпиясөз (минимум 8 таңба)

    Returns:
        dict: {"id": int, "phone": str, "full_name": str}

    Raises:
        ValueError: Телефон форматы немесе құпиясөз талаптары орындалмаса
        ConflictError: Телефон әлдеқашан тіркелген болса
    """
    ...


def login_with_otp(phone: str, otp: str) -> dict:
    """
    OTP арқылы кіру.

    Args:
        phone: Тіркелген телефон
        otp: 6 таңбалы код

    Returns:
        dict: {"access_token": str, "refresh_token": str, "expires_in": int}

    Raises:
        AuthenticationError: OTP қате немесе мерзімі өткен
    """
    ...


def search_dishes(
    query: str,
    category_id: Optional[int] = None,
    restaurant_id: Optional[int] = None,
    limit: int = 20,
    offset: int = 0,
) -> list[dict]:
    """
    Тағамдарды іздеу және сүзу.

    Args:
        query: Іздеу мәтіні
        category_id: Категория ID (опционал)
        restaurant_id: Мейрамхана ID (опционал)
        limit: Нәтижелер саны
        offset: Өткізілетін жазбалар

    Returns:
        list[dict]: Тағамдар тізімі
    """
    ...


def add_to_cart(user_id: int, dish_id: int, quantity: int = 1) -> dict:
    """
    Себетке тағам қосу.

    Args:
        user_id: Пайдаланушы ID
        dish_id: Тағам ID
        quantity: Саны (≥ 1)

    Returns:
        dict: Жаңартылған себет

    Raises:
        NotFoundError: Тағам немесе пайдаланушы табылмаса
        ValidationError: quantity < 1
    """
    ...


def create_order(
    user_id: int,
    restaurant_id: int,
    address_id: int,
    items: list[dict],
    promo_code: Optional[str] = None,
) -> dict:
    """
    Тапсырыс құру.

    Args:
        user_id: Пайдаланушы ID
        restaurant_id: Мейрамхана ID
        address_id: Мекенжай ID
        items: [{"dish_id": int, "quantity": int}, ...]
        promo_code: Промокод (опционал)

    Returns:
        dict: {"id": int, "status": "new", "total_amount": Decimal, ...}

    Raises:
        ValidationError: Себет бос немесе мекенжай жарамсыз
        BusinessError: Мейрамхана жабық немесе қор жеткіліксіз
    """
    ...


def process_payment(
    order_id: int,
    method: str,
    amount: Decimal,
) -> dict:
    """
    Төлемді өңдеу.

    Args:
        order_id: Тапсырыс ID
        method: "kaspi" | "halyk" | "card"
        amount: Төленетін сома

    Returns:
        dict: {"transaction_id": str, "status": "success" | "failed"}

    Raises:
        PaymentError: Төлем қабылданбаса
        NotFoundError: Тапсырыс табылмаса
    """
    ...


def update_order_status(
    order_id: int,
    new_status: OrderStatus,
    actor_id: int,
) -> dict:
    """
    Тапсырыс статусын өзгерту (рұқсат етілген ауысулар ғана).

    Args:
        order_id: Тапсырыс ID
        new_status: Жаңа статус
        actor_id: Әрекетті жасаушы (user/courier/admin)

    Returns:
        dict: Жаңартылған тапсырыс

    Raises:
        InvalidTransitionError: Рұқсат етілмеген ауысу
        PermissionError: Құқық жеткіліксіз
    """
    ...


def calculate_discount(
    subtotal: Decimal,
    user_id: int,
    promo_code: Optional[str] = None,
) -> Decimal:
    """
    Жеңілдік есептеу (студент, промокод, бонустар).

    Args:
        subtotal: Бастапқы сома
        user_id: Пайдаланушы ID (студент статусын тексеру үшін)
        promo_code: Промокод

    Returns:
        Decimal: Жеңілдік сомасы (≥ 0)
    """
    ...


def assign_courier(order_id: int, courier_id: int) -> dict:
    """
    Курьерді тапсырысқа тағайындау.

    Args:
        order_id: Тапсырыс ID
        courier_id: Курьер ID

    Returns:
        dict: Delivery жазбасы

    Raises:
        ConflictError: Курьер бос емес
        NotFoundError: Тапсырыс/курьер табылмаса
    """
    ...


def get_order_tracking(order_id: int, user_id: int) -> dict:
    """
    Тапсырыс трекингін алу.

    Args:
        order_id: Тапсырыс ID
        user_id: Сұраушы пайдаланушы (құқық тексеру)

    Returns:
        dict: {"status": str, "courier_location": dict | None, "eta_minutes": int}

    Raises:
        PermissionError: Басқаның тапсырысын көруге тырысса
        NotFoundError: Тапсырыс жоқ
    """
    ...

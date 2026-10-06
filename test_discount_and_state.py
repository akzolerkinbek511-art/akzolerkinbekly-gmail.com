"""
ОН 7.2 — 44-тапсырма: Unit-тесттер
DiscountService + OrderStateMachine үшін 20+ тест
pytest, coverage ≥ 80% мақсаты
"""

import pytest
from decimal import Decimal
from unittest.mock import MagicMock

# ---------- жеңілдетілген класс көшірмелері (тест үшін) ----------
from enum import Enum
from typing import Set, Optional


class OrderStatus(str, Enum):
    NEW = "new"
    PAID = "paid"
    PREPARING = "preparing"
    DELIVERING = "delivering"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    RETURNED = "returned"


ALLOWED = {
    OrderStatus.NEW: {OrderStatus.PAID, OrderStatus.CANCELLED},
    OrderStatus.PAID: {OrderStatus.PREPARING, OrderStatus.CANCELLED},
    OrderStatus.PREPARING: {OrderStatus.DELIVERING, OrderStatus.CANCELLED},
    OrderStatus.DELIVERING: {OrderStatus.DELIVERED, OrderStatus.RETURNED},
    OrderStatus.DELIVERED: {OrderStatus.RETURNED},
    OrderStatus.CANCELLED: set(),
    OrderStatus.RETURNED: set(),
}


class InvalidTransitionError(Exception):
    pass


class OrderStateMachine:
    def __init__(self, initial=OrderStatus.NEW):
        self._status = initial

    @property
    def status(self):
        return self._status

    def can_transition(self, target):
        return target in ALLOWED.get(self._status, set())

    def transition_to(self, target):
        if not self.can_transition(target):
            raise InvalidTransitionError(f"{self._status} -> {target}")
        self._status = target
        return self._status


class DiscountService:
    STUDENT = Decimal("0.20")

    def __init__(self, user_repo, promo_repo):
        self.user_repo = user_repo
        self.promo_repo = promo_repo

    def calculate(self, subtotal: Decimal, user_id: int, promo_code: Optional[str] = None) -> Decimal:
        discount = Decimal("0")
        user = self.user_repo.get(user_id)
        if user and getattr(user, "is_student", False):
            discount += subtotal * self.STUDENT
        if promo_code:
            promo = self.promo_repo.get_active(promo_code)
            if promo:
                if promo.type == "percent":
                    discount += subtotal * (promo.value / Decimal("100"))
                else:
                    discount += promo.value
        bonus = min(getattr(user, "bonus_balance", Decimal("0")) if user else Decimal("0"),
                    subtotal * Decimal("0.10"))
        discount += bonus
        return min(discount, subtotal)


# ---------- State Machine тесттері ----------
def test_initial_status_is_new():
    sm = OrderStateMachine()
    assert sm.status == OrderStatus.NEW


def test_new_to_paid():
    sm = OrderStateMachine()
    sm.transition_to(OrderStatus.PAID)
    assert sm.status == OrderStatus.PAID


def test_new_to_cancelled():
    sm = OrderStateMachine()
    sm.transition_to(OrderStatus.CANCELLED)
    assert sm.status == OrderStatus.CANCELLED


def test_full_happy_path():
    sm = OrderStateMachine()
    sm.transition_to(OrderStatus.PAID)
    sm.transition_to(OrderStatus.PREPARING)
    sm.transition_to(OrderStatus.DELIVERING)
    sm.transition_to(OrderStatus.DELIVERED)
    assert sm.status == OrderStatus.DELIVERED


def test_invalid_new_to_delivered_raises():
    sm = OrderStateMachine()
    with pytest.raises(InvalidTransitionError):
        sm.transition_to(OrderStatus.DELIVERED)


def test_cancelled_is_terminal():
    sm = OrderStateMachine()
    sm.transition_to(OrderStatus.CANCELLED)
    with pytest.raises(InvalidTransitionError):
        sm.transition_to(OrderStatus.PAID)


def test_returned_is_terminal():
    sm = OrderStateMachine(OrderStatus.DELIVERED)
    sm.transition_to(OrderStatus.RETURNED)
    with pytest.raises(InvalidTransitionError):
        sm.transition_to(OrderStatus.DELIVERED)


def test_can_transition_true():
    sm = OrderStateMachine()
    assert sm.can_transition(OrderStatus.PAID) is True


def test_can_transition_false():
    sm = OrderStateMachine()
    assert sm.can_transition(OrderStatus.DELIVERED) is False


def test_delivering_to_returned():
    sm = OrderStateMachine(OrderStatus.DELIVERING)
    sm.transition_to(OrderStatus.RETURNED)
    assert sm.status == OrderStatus.RETURNED


# ---------- DiscountService тесттері ----------
@pytest.fixture
def mock_repos():
    user_repo = MagicMock()
    promo_repo = MagicMock()
    return user_repo, promo_repo


def test_no_discount(mock_repos):
    user_repo, promo_repo = mock_repos
    user_repo.get.return_value = MagicMock(is_student=False, bonus_balance=Decimal("0"))
    promo_repo.get_active.return_value = None
    svc = DiscountService(user_repo, promo_repo)
    assert svc.calculate(Decimal("1000"), 1) == Decimal("0")


def test_student_discount(mock_repos):
    user_repo, promo_repo = mock_repos
    user_repo.get.return_value = MagicMock(is_student=True, bonus_balance=Decimal("0"))
    promo_repo.get_active.return_value = None
    svc = DiscountService(user_repo, promo_repo)
    assert svc.calculate(Decimal("1000"), 1) == Decimal("200")


def test_percent_promo(mock_repos):
    user_repo, promo_repo = mock_repos
    user_repo.get.return_value = MagicMock(is_student=False, bonus_balance=Decimal("0"))
    promo_repo.get_active.return_value = MagicMock(type="percent", value=Decimal("10"))
    svc = DiscountService(user_repo, promo_repo)
    assert svc.calculate(Decimal("1000"), 1, "SAVE10") == Decimal("100")


def test_fixed_promo(mock_repos):
    user_repo, promo_repo = mock_repos
    user_repo.get.return_value = MagicMock(is_student=False, bonus_balance=Decimal("0"))
    promo_repo.get_active.return_value = MagicMock(type="fixed", value=Decimal("150"))
    svc = DiscountService(user_repo, promo_repo)
    assert svc.calculate(Decimal("1000"), 1, "MINUS150") == Decimal("150")


def test_bonus_capped_at_10_percent(mock_repos):
    user_repo, promo_repo = mock_repos
    user_repo.get.return_value = MagicMock(is_student=False, bonus_balance=Decimal("500"))
    promo_repo.get_active.return_value = None
    svc = DiscountService(user_repo, promo_repo)
    # 10% of 1000 = 100
    assert svc.calculate(Decimal("1000"), 1) == Decimal("100")


def test_combined_student_and_promo(mock_repos):
    user_repo, promo_repo = mock_repos
    user_repo.get.return_value = MagicMock(is_student=True, bonus_balance=Decimal("0"))
    promo_repo.get_active.return_value = MagicMock(type="percent", value=Decimal("10"))
    svc = DiscountService(user_repo, promo_repo)
    # 20% + 10% = 300
    assert svc.calculate(Decimal("1000"), 1, "SAVE10") == Decimal("300")


def test_discount_never_exceeds_subtotal(mock_repos):
    user_repo, promo_repo = mock_repos
    user_repo.get.return_value = MagicMock(is_student=True, bonus_balance=Decimal("9999"))
    promo_repo.get_active.return_value = MagicMock(type="fixed", value=Decimal("5000"))
    svc = DiscountService(user_repo, promo_repo)
    assert svc.calculate(Decimal("100"), 1, "BIG") == Decimal("100")


def test_zero_subtotal(mock_repos):
    user_repo, promo_repo = mock_repos
    user_repo.get.return_value = MagicMock(is_student=True, bonus_balance=Decimal("0"))
    promo_repo.get_active.return_value = None
    svc = DiscountService(user_repo, promo_repo)
    assert svc.calculate(Decimal("0"), 1) == Decimal("0")


def test_user_not_found(mock_repos):
    user_repo, promo_repo = mock_repos
    user_repo.get.return_value = None
    promo_repo.get_active.return_value = None
    svc = DiscountService(user_repo, promo_repo)
    assert svc.calculate(Decimal("500"), 999) == Decimal("0")


def test_invalid_promo_ignored(mock_repos):
    user_repo, promo_repo = mock_repos
    user_repo.get.return_value = MagicMock(is_student=False, bonus_balance=Decimal("0"))
    promo_repo.get_active.return_value = None
    svc = DiscountService(user_repo, promo_repo)
    assert svc.calculate(Decimal("500"), 1, "INVALID") == Decimal("0")


# Іске қосу: pytest test_discount_and_state.py -v --cov=. --cov-report=term-missing
# Күтілетін: 20+ тест, coverage ≥ 80%

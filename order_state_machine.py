"""
ОН 7.2 — 34-тапсырма: Тапсырыс күйлері — State Machine
Жаңа → Төленді → Жіберілді → Жеткізілді → Қайтарылды
Рұқсат етілмеген ауысуларды бұғаттау.
"""

from enum import Enum
from typing import Set


class OrderStatus(str, Enum):
    NEW = "new"
    PAID = "paid"
    PREPARING = "preparing"      # мейрамхана дайындауда
    DELIVERING = "delivering"    # жіберілді / жолда
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    RETURNED = "returned"


# Рұқсат етілген ауысулар (from → {to, ...})
ALLOWED_TRANSITIONS: dict[OrderStatus, Set[OrderStatus]] = {
    OrderStatus.NEW: {OrderStatus.PAID, OrderStatus.CANCELLED},
    OrderStatus.PAID: {OrderStatus.PREPARING, OrderStatus.CANCELLED},
    OrderStatus.PREPARING: {OrderStatus.DELIVERING, OrderStatus.CANCELLED},
    OrderStatus.DELIVERING: {OrderStatus.DELIVERED, OrderStatus.RETURNED},
    OrderStatus.DELIVERED: {OrderStatus.RETURNED},
    OrderStatus.CANCELLED: set(),   # терминал
    OrderStatus.RETURNED: set(),    # терминал
}


class InvalidTransitionError(Exception):
    def __init__(self, current: OrderStatus, target: OrderStatus):
        self.current = current
        self.target = target
        super().__init__(
            f"Рұқсат етілмеген ауысу: {current.value} → {target.value}"
        )


class OrderStateMachine:
    def __init__(self, initial: OrderStatus = OrderStatus.NEW):
        self._status = initial

    @property
    def status(self) -> OrderStatus:
        return self._status

    def can_transition(self, target: OrderStatus) -> bool:
        return target in ALLOWED_TRANSITIONS.get(self._status, set())

    def transition_to(self, target: OrderStatus) -> OrderStatus:
        if not self.can_transition(target):
            raise InvalidTransitionError(self._status, target)
        self._status = target
        return self._status

    def available_transitions(self) -> Set[OrderStatus]:
        return ALLOWED_TRANSITIONS.get(self._status, set()).copy()


# --- Диаграмма (Mermaid) ---
# stateDiagram-v2
#     [*] --> NEW
#     NEW --> PAID
#     NEW --> CANCELLED
#     PAID --> PREPARING
#     PAID --> CANCELLED
#     PREPARING --> DELIVERING
#     PREPARING --> CANCELLED
#     DELIVERING --> DELIVERED
#     DELIVERING --> RETURNED
#     DELIVERED --> RETURNED
#     CANCELLED --> [*]
#     RETURNED --> [*]
#     DELIVERED --> [*]


if __name__ == "__main__":
    sm = OrderStateMachine()
    print("Бастапқы:", sm.status)
    print("Қолжетімді:", [s.value for s in sm.available_transitions()])

    sm.transition_to(OrderStatus.PAID)
    print("Төленді:", sm.status)

    sm.transition_to(OrderStatus.PREPARING)
    sm.transition_to(OrderStatus.DELIVERING)
    sm.transition_to(OrderStatus.DELIVERED)
    print("Жеткізілді:", sm.status)

    try:
        sm.transition_to(OrderStatus.NEW)  # рұқсат етілмеген
    except InvalidTransitionError as e:
        print("Бұғатталды:", e)

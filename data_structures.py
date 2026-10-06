"""
ОН 7.2 — 31-тапсырма: Деректер құрылымын таңдау
5 есеп үшін дұрыс құрылым + негіздеме + код мысалы
"""

from collections import deque
from heapq import heappush, heappop
from typing import Any


# 1. Кезек (Queue) — тапсырыстарды өңдеу кезегі
# Негіздеме: FIFO — алғашқы келген тапсырыс алғашқы өңделеді.
order_queue: deque[int] = deque()

def enqueue_order(order_id: int) -> None:
    order_queue.append(order_id)

def dequeue_order() -> int | None:
    if order_queue:
        return order_queue.popleft()
    return None


# 2. Кэш (Cache) — мәзір / сессия кэші
# Негіздеме: dict — O(1) қатынау, кілт-мән жұбы.
menu_cache: dict[int, dict[str, Any]] = {}

def get_cached_menu(restaurant_id: int) -> dict | None:
    return menu_cache.get(restaurant_id)

def set_cached_menu(restaurant_id: int, menu: dict) -> None:
    menu_cache[restaurant_id] = menu


# 3. Рейтинг (Top-N) — ең жоғары рейтингті мейрамханалар
# Негіздеме: heap (min-heap теріс мәнмен) — top-k тиімді.
# (rating, restaurant_id) — ranking үшін
rating_heap: list[tuple[float, int]] = []

def add_rating(restaurant_id: int, rating: float) -> None:
    # max-heap эмуляциясы: теріс рейтинг
    heappush(rating_heap, (-rating, restaurant_id))

def get_top_restaurants(k: int = 10) -> list[tuple[int, float]]:
    # көшірме жасап, top-k алу
    temp = list(rating_heap)
    result = []
    for _ in range(min(k, len(temp))):
        neg_r, rid = heappop(temp)
        result.append((rid, -neg_r))
    return result


# 4. Іздеу (Search index) — жылдам іздеу үшін set / inverted index
# Негіздеме: set — membership O(1); inverted index — токен → id-лер.
search_index: dict[str, set[int]] = {}

def index_dish(dish_id: int, tokens: list[str]) -> None:
    for token in tokens:
        token = token.lower()
        if token not in search_index:
            search_index[token] = set()
        search_index[token].add(dish_id)

def search_dishes_by_tokens(tokens: list[str]) -> set[int]:
    if not tokens:
        return set()
    result = search_index.get(tokens[0].lower(), set()).copy()
    for t in tokens[1:]:
        result &= search_index.get(t.lower(), set())
    return result


# 5. Тарих (History) — пайдаланушы тапсырыс тарихы
# Негіздеме: list — реттілік сақталады, соңғы N-ді оңай алуға болады.
# (үлкен көлемде — deque maxlen немесе БД)
order_history: dict[int, list[int]] = {}  # user_id → [order_id, ...]

def add_to_history(user_id: int, order_id: int) -> None:
    if user_id not in order_history:
        order_history[user_id] = []
    order_history[user_id].append(order_id)

def get_recent_orders(user_id: int, limit: int = 20) -> list[int]:
    history = order_history.get(user_id, [])
    return history[-limit:][::-1]  # соңғылары алдымен

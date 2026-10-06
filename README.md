# ОН 7.2 — 50 практикалық жұмыс (4 курс)

**Пән:** Бағдарламалық қамтамасыз етуге қойылған дайын талаптар спецификациялары бойынша код әзірлеу

**Мақсаты:** Талаптарды талдау → архитектураны жобалау → код әзірлеу → тестілеу және валидация кезеңдерін толық орындау.

**Мысал жүйе:** FoodExpress (онлайн тамақ жеткізу қосымшасы)

**Қолданылған құралдар:** Word, Excel, VS Code, Mermaid, Python, FastAPI, Pydantic, pytest, Docker, GitHub Actions, Ruff, Black

---

## Жоба құрылымы

```
artifacts/
├── 1_tarau/                  # 1-тарау (тапсырмалар 1–13)
├── 1_tarau_толық.zip
├── 2_tarau/                  # 2-тарау (тапсырмалар 14–26)
├── 2_tarau_толық.zip
├── 3_tarau/                  # 3-тарау (тапсырмалар 27–42)
├── 3_tarau_толық.zip
├── 4_tarau/                  # 4-тарау (тапсырмалар 43–50)
├── 4_tarau_толық.zip
├── 24_26_VSCode.zip          # 24 және 26-тапсырмалар (VS Code)
└── README.md                 # Осы файл
```

---

## 1-тарау. Талаптар спецификациясын талдау негіздері (1–13)

| № | Тапсырма | Формат | Нәтиже |
|---|----------|--------|--------|
| 1 | SRS құрылым картасы | Excel | FoodExpress SRS бөлімдері кестесі |
| 2 | IEEE 29148 салыстыру | Excel | Сәйкестік чек-парағы |
| 3 | Талап сапасы | Word | 20 талаптың түзетілген тізімі |
| 4 | FR / NFR жіктеу | Excel | 30 талап категориялау кестесі |
| 5 | Өлшенетін NFR | Word | 5 өлшенетін NFR |
| 6 | Толықтық тексеру | Word | Банк SRS ақаулар журналы (12) |
| 7 | User Stories + backlog | Word | 12 User Story + Given-When-Then |
| 8 | Use Case сипаттау | Word | Кітапхана жүйесі диаграмма түсіндірмесі |
| 9 | Traceability Matrix | Excel | 15 талап ↔ Use Case RTM |
| 10 | Mermaid диаграммалар | Word | Use Case + Activity + Sequence |
| 11 | DFD талдау | Word | Онлайн-дүкен 0/1 деңгей DFD |
| 12 | ERD → SQL | Word | PostgreSQL schema.sql |
| 13 | AI арқылы тексеру | Word | Сыни талдау есебі |

---

## 2-тарау. Бағдарламалық архитектураны жобалау (14–26)

| № | Тапсырма | Формат | Нәтиже |
|---|----------|--------|--------|
| 14 | ТЗ құрылымын талдау | Word + Excel | ГОСТ 34 сәйкестік кестесі |
| 15 | Функционалдық блоктар | Word | 8 блок + Mermaid схема |
| 16 | Сервер ресурстарын есептеу | Word + Excel | Есептеу парағы |
| 17 | Архитектуралық стиль + ADR | Word | 3 ADR (блог, банк, такси) |
| 18 | C4 моделі | Word | Context + Container (Mermaid) |
| 19 | Архитектура ↔ NFR | Word + Excel | Сәйкестік кестесі |
| 20 | OpenAPI келісімі | Word | openapi.yaml (5 эндпоинт) |
| 21 | Монолит → микросервис | Word | 3 сервис + схема |
| 22 | Модульдік бөліну | Word | 10 модуль картасы |
| 23 | Репозиторий құрылымы | Word | Папка + GitHub Flow |
| 24 | Code Style (линтер) | VS Code | pyproject.toml + before/after код |
| 25 | Naming Conventions | Word + Excel | 40 before/after |
| 26 | CI lint workflow | VS Code | .github/workflows/lint.yml |

---

## 3-тарау. Талаптар негізінде код әзірлеу (27–42)

| № | Тапсырма | Формат | Нәтиже |
|---|----------|--------|--------|
| 27 | Кластар + UML | Word | Class диаграммасы (Mermaid) |
| 28 | Интерфейстер (төлем) | Word | PaymentProcessor + 3 іске асыру |
| 29 | Функция сигнатуралары | VS Code | signatures.py (10 функция) |
| 30 | Pydantic модельдері | VS Code | models.py |
| 31 | Деректер құрылымдары | VS Code | data_structures.py (5 құрылым) |
| 32 | ORM + миграция | Word | SQLAlchemy модельдері |
| 33 | Жеңілдік есептеу | Word | DiscountService |
| 34 | State Machine | VS Code | order_state_machine.py |
| 35 | REST API | Word | FastAPI skeleton |
| 36 | Сценарий ↔ код | Word | Трассировка кестесі |
| 37 | Валидация | Word | Pydantic + 15 тест идеясы |
| 38 | Error handling | VS Code | error_handler.py + хабарламалар |
| 39 | Логтау | Word | Structured JSON logging |
| 40 | AI code review | Word | Review чек-парағы |
| 41 | Docker | Word | Dockerfile + docker-compose |
| 42 | Конфигурация / құпиялар | Word | .env + Settings + gitleaks |

---

## 4-тарау. Тестілеу, оңтайландыру және финалдық валидация (43–50)

| № | Тапсырма | Формат | Нәтиже |
|---|----------|--------|--------|
| 43 | Тест-кейстер | Word | 20 тест-кейс кестесі |
| 44 | Unit-тесттер | VS Code | 20+ pytest (coverage ≥ 80%) |
| 45 | API тестілеу | VS Code | pytest + httpx |
| 46 | CI тест | VS Code | ci.yml (test + coverage + Docker) |
| 47 | Баг-репорттар | Word | 9 баг-репорт |
| 48 | Күрделілік / өнімділік | Word | Big-O + timeit before/after |
| 49 | Рефакторинг | Word | Code smell → кіші функциялар |
| 50 | Финалдық валидация | Word | RTM + құжаттама пакеті |

---

## Word құжаттарына қойылған талаптар

- Шрифт: Times New Roman
- Кегль: 14
- Барлық шеттер: 2 см
- Абзац алдында/кейін: 0 пт
- Жол аралығы: бірлік (single)

---

## VS Code тапсырмалары

Келесі тапсырмалар код файлдары ретінде берілген (тікелей VS Code-та ашуға болады):

- **24** — pyproject.toml, bad_code.py, fixed_code.py
- **26** — .github/workflows/lint.yml
- **29** — signatures.py
- **30** — models.py
- **31** — data_structures.py
- **34** — order_state_machine.py
- **38** — error_handler.py
- **44** — test_discount_and_state.py
- **45** — test_api.py
- **46** — .github/workflows/ci.yml

---

## Figma интерактивті демолар (ұсынылған)

Кейін жасалатын интерактивті демолар:

| № | Тапсырма | Демо мазмұны |
|---|----------|--------------|
| 7 | User Stories | Kanban backlog + Given-When-Then |
| 8 | Use Case | Актерлер мен сценарийлер |
| 10 | Activity | Тапсырыс беру ағыны |
| 15 | Functional Blocks | Блоктар схемасы |
| 18 | C4 | Context + Container |
| 21 | Microservices | Монолит → 3 сервис |
| 27 | UML Class | Класс диаграммасы |
| 34 | State Machine | Статус ауысулары |

---

## Қалай пайдалану керек

1. Қажетті тараудың ZIP файлын жүктеңіз.
2. Word/Excel файлдарын ашыңыз.
3. VS Code тапсырмаларын сәйкес папкадан ашыңыз.
4. Python тапсырмалары үшін:
   ```bash
   pip install pytest pytest-cov httpx fastapi pydantic ruff black
   pytest -v
   ```
5. Figma демоларын жоғарыдағы тізім бойынша жасаңыз.

---

## Қорытынды

Барлық **50 тапсырма** толық орындалды.  
Талаптарды талдаудан бастап тестілеу мен финалдық валидацияға дейінгі толық цикл қамтылған.

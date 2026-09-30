# API Testing (Otus QA-Python)

Домашнее задание по тестированию REST API на основе их документации.

## Тестируемые сервисы

| Сервис | Документация | Модуль тестов |
| --- | --- | --- |
| Dog CEO | <https://dog.ceo/dog-api/> | `tests/test_dog_api.py` |
| Open Brewery DB | <https://www.openbrewerydb.org/> | `tests/test_brewery_api.py` |
| JSONPlaceholder | <https://jsonplaceholder.typicode.com/> | `tests/test_jsonplaceholder_api.py` |

Для каждого сервиса написано не менее 5 тестов, минимум 2 из них используют
параметризацию (`@pytest.mark.parametrize`).

## Часть 2. Проверка статус-кода по URL

Тест `tests/test_url_status.py` принимает два параметра через `pytest.addoption`:

- `--url` — проверяемый адрес, по умолчанию `https://ya.ru`;
- `--status_code` — ожидаемый код ответа, по умолчанию `200`.

Опции регистрируются в `conftest.py`, фикстуры и тестовая функция — в модуле
`tests/test_url_status.py`.

Примеры запуска:

```bash
pytest tests/test_url_status.py --url=https://mail.ru --status_code=200
pytest tests/test_url_status.py --url=https://ya.ru/sfhfh --status_code=404
```

## Установка и запуск

```bash
pip install -r requirements.txt
pytest
```

Запуск только одного сервиса:

```bash
pytest tests/test_dog_api.py
```

## Структура проекта

```
.
├── conftest.py                      # регистрация --url и --status_code
├── pytest.ini                       # конфигурация pytest
├── requirements.txt                 # зависимости
└── tests
    ├── test_dog_api.py              # тесты Dog CEO API
    ├── test_brewery_api.py          # тесты Open Brewery DB API
    ├── test_jsonplaceholder_api.py  # тесты JSONPlaceholder API
    └── test_url_status.py           # Часть 2: проверка статуса по URL
```

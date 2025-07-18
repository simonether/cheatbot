# 🚀 CheatBot API: Асинхронная Python-библиотека

![PyPI - Version](https://img.shields.io/pypi/v/cheatbot)
[![CI/CD Pipeline](https://github.com/simonether/cheatbot/actions/workflows/ci.yml/badge.svg)](https://github.com/simonether/cheatbot/actions/workflows/ci.yml)
![License](https://img.shields.io/github/license/simonether/cheatbot)

**`cheatbot`** — это мощная и интуитивно понятная асинхронная Python-библиотека, разработанная для бесшовного взаимодействия с API сервиса CheatBot. Она предоставляет удобный интерфейс для управления задачами, получения информации о сервисах и профиле, а также автоматизации рутинных операций.

## ✨ Особенности

*   **Полностью асинхронная**: Построена на `asyncio` для высокопроизводительных и неблокирующих операций.
*   **Типобезопасность**: Использует `pydantic` для строгой валидации данных и автодополнения.
*   **Простота использования**: Чистый и понятный API, который легко интегрировать в ваши проекты.
*   **Надежность**: Встроенная обработка ошибок и исключений для стабильной работы.
*   **Гибкость**: Поддержка всех основных функций CheatBot API.

## 🚀 Начало работы

Эти инструкции помогут вам быстро запустить проект на вашем локальном компьютере.

### 📋 Предварительные требования

Для работы с проектом вам понадобится [uv](https://github.com/astral-sh/uv) — чрезвычайно быстрый установщик и распознаватель пакетов Python.



## ▶️ Быстрый старт

Чтобы использовать библиотеку в своем проекте, вам понадобится API-ключ от сервиса [CheatBot](https://cheatbot.ru/). Вы можете получить его в [личном кабинете](https://cheatbot.ru/lk/settings) после регистрации.

**Установка из PyPI (рекомендуется):**

```bash
pip install cheatbot
```

**Установка из GitHub (для последней версии):**

```bash
pip install git+https://github.com/simonether/cheatbot.git
```

Вот простой пример использования клиента для получения информации о профиле и сервисах:

```python
import asyncio
import os

from cheatbot import CheatBotClient

async def main():
    # Получите ваш API-ключ из переменной окружения
    api_key = os.getenv("CHEATBOT_API_KEY")
    if not api_key:
        raise ValueError("Переменная окружения CHEATBOT_API_KEY не установлена.")

    # Инициализация клиента. Используйте async with для автоматического закрытия сессии.
    async with CheatBotClient(api_key) as client:
        print("--- Информация о профиле ---")
        profile = await client.get_profile_info()
        print(f"Баланс: {profile.balance} RUB")
        print(f"ID пользователя: {profile.user_id}")

        print("\n--- Доступные сервисы ---")
        # Получение всех сервисов
        all_services = client.services.get_all()
        print(f"Всего доступных сервисов: {len(all_services)}")

        # Пример поиска конкретного сервиса по ID (например, ID 40)
        service_id_to_find = 40
        service = client.services.get_by_id(service_id_to_find)
        if service:
            print(f"Найден сервис (ID: {service_id_to_find}): {service.name} (Категория: {service.category_name})")
        else:
            print(f"Сервис с ID {service_id_to_find} не найден.")

if __name__ == "__main__":
    asyncio.run(main())
```

## 🧪 Запуск тестов

Для запуска тестов используйте `pytest`:

```bash
uv run pytest
```

## 🤝 Участие

Мы приветствуем любой вклад в развитие проекта! Пожалуйста, ознакомьтесь с нашим [руководством по участию](CONTRIBUTING.md) и [кодексом поведения](CODE_OF_CONDUCT.md).

## 📄 Лицензия

Этот проект распространяется под лицензией MIT. Подробности смотрите в файле [LICENSE](LICENSE).

## ❓ Поддержка

Если у вас есть вопросы, предложения или вы столкнулись с проблемой, пожалуйста, создайте [Issue на GitHub](https://github.com/simonether/cheatbot/issues). Мы постараемся ответить как можно скорее.

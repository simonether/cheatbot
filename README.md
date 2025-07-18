# 🤖 Библиотека для API CheatBot

Асинхронная Python-библиотека для взаимодействия с API сервиса CheatBot.

## 🚀 Начало работы

Эти инструкции помогут вам запустить проект на вашем локальном компьютере для разработки и тестирования.

### 📋 Предварительные требования

Для работы с проектом вам понадобится [uv](https://github.com/astral-sh/uv). `uv` — это чрезвычайно быстрый установщик и распознаватель пакетов Python.

### 🔧 Установка

1.  **Клонируйте репозиторий:**
    ```bash
    git clone https://github.com/simonether/cheatbot.git
    cd cheatbot
    ```

2.  **Создайте виртуальное окружение и установите зависимости с помощью `uv`:**
    ```bash
    uv sync
    ```
    Эта команда создаст `.venv` в каталоге вашего проекта и установит все зависимости из `pyproject.toml`.

## ▶️ Использование

Чтобы использовать библиотеку в своем проекте, вы можете установить ее прямо из GitHub:

```bash
pip install git+https://github.com/simonether/cheatbot.git
```

Вот пример использования клиента:

```python
import asyncio
import os

from cheatbot import CheatBotClient

async def main():
    api_key = os.getenv("CHEATBOT_API_KEY")
    if not api_key:
        raise ValueError("Переменная окружения CHEATBOT_API_KEY не установлена.")

    async with CheatBotClient(api_key) as client:
        # Получение информации о профиле
        profile = await client.get_profile_info()
        print(f"Баланс: {profile.balance}")

        # Получение всех сервисов
        services = client.services.get_all()
        print(f"Всего сервисов: {len(services)}")

        # Поиск определенного сервиса
        service = client.services.get_by_id(40)
        if service:
            print(f"Найден сервис: {service.name}")

if __name__ == "__main__":
    asyncio.run(main())
```

## 🧪 Запуск тестов

Для запуска тестов используйте `pytest`:

```bash
uv run pytest
```
# Pulse — Telegram-бот для продуктивности

## Бот для управления заметками, напоминаниями и показывающий курсы валют и погоду прямо в Telegram.

### Требования — Python 3.10+, pip, Telegram Bot Token

#### Установка
git clone https://git.quillon.ru/student/pulse.git
cd pulse
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

#### Запуск — python bot.py

#### Лицензия — MIT
python main.py

### Список доступных команд бота:
/start — приветствие
/note текст — добавить заметку
/notes — показать все заметки
/weather город — погода
/rate USD RUB — курс валюты
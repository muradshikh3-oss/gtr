import json
from telegram import Update
from telegram.ext import ContextTypes, Application, CommandHandler
from api import get_weather, get_rate
from config import TOKEN


data = {"notes": [], "expenses": []}
def save_data():
    with open("data.json", "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


async def note_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Использование: /note текст")
        return
    text = " ".join(context.args)
    data["notes"].append(text)
    save_data(data)
    await update.message.reply_text(f"Заметка добавлена: {text}")
data = {"notes": ["Купить молоко", "Учить Python"], "expenses": []}

async def notes_cmd(update, context):
  if data["notes"] == " ":
    await update.message.reply_text("Заметок пока нет.")
  else:
    lines = [f"{i}. {note}" for i, note in enumerate(data["notes"], 1)]
    text = "\n".join(lines)
    await update.message.reply_text(text)
DATA_FILE = "data.json"

async def notes_cmd(update, context):
    notes = data["notes"]

    if not notes:
        await update.message.reply_text("Заметок пока нет.")
        return

    lines = []

    for i, note in enumerate(notes, 1):
        lines.append(f"{i}. {note}")

    await update.message.reply_text("\n".join(lines))

def load_data() -> dict:
    """Загрузить данные из JSON. Если файла нет — вернуть шаблон."""
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        return {"notes": [], "expenses": []}
def save_data(data: dict) -> None:
    """Сохранить данные в JSON."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

data = load_data()
print("Загружено:", data)
data["notes"].append("Тестовая заметка")
save_data(data)
print("Сохранено!")
data2 = load_data()
print("После перезагрузки:", data2)
async def weather_cmd(update, context):
    city = " ".join(context.args)

    if city == "":
        await update.message.reply_text("Использование: /weather город")
        return

    try:
        result = get_weather(city)
        await update.message.reply_text(result)
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {e}")


data = {"notes": [], "expenses": [
    {"amount": 150.0, "category": "еда"},
    {"amount": 2500.0, "category": "транспорт"}
]}


async def rate_cmd(update, context):
    if len(context.args) != 2:
        await update.message.reply_text("Использование: /rate USD RUB")
        return
    base = context.args[0].upper()
    target = context.args[1].upper()
    try:
        result = get_rate(base, target)
        await update.message.reply_text(result)
    except Exception as e:
        await update.message.reply_text(f"Ошибка курса: {e}")

async def expenses_cmd(update, context):
    items = data["expenses"]
    if not items:
        await update.message.reply_text("Расходов нет.")
        return
    lines = [f"{i}. {e['amount']} руб — {e['category']}" for i, e in enumerate(items, 1)]
    total = sum(e["amount"] for e in items)
    lines.append(f"\nИтого: {total} руб")
    await update.message.reply_text("\n".join(lines))
def main():
    global data
    data = load_data()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("note", note_cmd))
    app.add_handler(CommandHandler("notes", notes_cmd))
    app.add_handler(CommandHandler("weather", weather_cmd))
    app.add_handler(CommandHandler("rate", rate_cmd))
    app.add_handler(CommandHandler("expenses", expenses_cmd))
    app.run_polling()


if __name__ == "__main__":
    main()
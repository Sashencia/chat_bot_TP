# main.py
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from memory.memory_manager import MemoryManager
from agent.agent import create_simple_chain
from agent.tools import explain_style_sync, summarize_history
from prompts.prompt_templates import get_system_prompt
from utils.logger import logger
from utils.validators import is_empty, sanitize_input
from langchain_core.runnables.history import RunnableWithMessageHistory
import asyncio

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TELEGRAM_TOKEN:
    raise ValueError("❌ Пропущен TELEGRAM_TOKEN в .env")

memory_manager = MemoryManager()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    memory_manager.get_history(user.id)
    await update.message.reply_text(
        f"Привет, {user.first_name}! 👋\n"
        "🔹 `/style_formal` — строго\n🔹 `/style_casual` — дружелюбно\n"
        "🔹 `/summary` — итог диалога\n🔹 `/help_style` — что такое стили?"
    )

async def set_formal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    memory_manager.set_style(update.effective_user.id, "formal")
    await update.message.reply_text("✅ Стиль: **формальный**.", parse_mode="Markdown")

async def set_casual(update: Update, context: ContextTypes.DEFAULT_TYPE):
    memory_manager.set_style(update.effective_user.id, "casual")
    await update.message.reply_text("✅ Стиль: **неформальный**! 😊")

async def summary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    history = memory_manager.get_history(update.effective_user.id)
    await update.message.reply_text(summarize_history(history))

async def help_style(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📘 Гайд по стилям:\n\n" + explain_style_sync())

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text
    if is_empty(text):
        await update.message.reply_text("Вы ничего не написали… 😊")
        return

    style = memory_manager.get_style(user_id)
    system_msg = get_system_prompt(style)
    chain = create_simple_chain()

    chain_with_history = RunnableWithMessageHistory(
        chain,
        lambda sid: memory_manager.get_history(int(sid)),
        input_messages_key="input",
        history_messages_key="chat_history",
    )

    # ✅ Показываем "печатает"
    await update.message.chat.send_chat_action("typing")

    try:
        # Добавим таймаут 30 сек (чтобы не висело бесконечно)
        response = await asyncio.wait_for(
            chain_with_history.ainvoke(
                {"system_message": system_msg, "input": text},
                config={"configurable": {"session_id": str(user_id)}}
            ),
            timeout=30.0
        )
        await update.message.reply_text(str(response).replace("**", ""), parse_mode=None)
    except asyncio.TimeoutError:
        fallback = "🤔 Думаю… попробуй чуть короче?" if style == "casual" else "Обработка запроса занимает больше времени. Повторите позже."
        await update.message.reply_text(fallback)
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        msg = "Извините, временная ошибка 🌟" if style == "casual" else "Произошла ошибка. Повторите позже."
        await update.message.reply_text(msg)

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("style_formal", set_formal))
    app.add_handler(CommandHandler("style_casual", set_casual))
    app.add_handler(CommandHandler("summary", summary))
    app.add_handler(CommandHandler("help_style", help_style))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    logger.info("✅ Бот запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()
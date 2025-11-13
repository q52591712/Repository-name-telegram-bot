# bot.py
import os
import logging
from datetime import datetime
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "你好！我是双向机器人\n"
        "发任何消息我都会回复你！\n"
        "试试说：你好"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start - 开始\n"
        "/help - 帮助\n"
        "其他消息我会回显 + 时间"
    )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    await update.message.reply_text(f"你说：{text}\n\n回复时间：{now}")

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error("Error:", exc_info=context.error)

def main():
    TOKEN = os.getenv("BOT_TOKEN")
    if not TOKEN:
        raise ValueError("请设置 BOT_TOKEN 环境变量")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    app.add_error_handler(error_handler)

    mode = os.getenv("DEPLOY_MODE", "polling").lower()

    if mode == "webhook":
        webhook_url = os.getenv("WEBHOOK_URL")
        port = int(os.getenv("PORT", 10000))
        if not webhook_url:
            raise ValueError("WEBHOOK_URL 未设置")
        print(f"Webhook 启动: {webhook_url}")
        app.run_webhook(
            listen="0.0.0.0",
            port=port,
            url_path=TOKEN,
            webhook_url=f"{webhook_url}/{TOKEN}"
        )
    else:
        print("Polling 模式启动（本地调试）")
        app.run_polling()

if name == "__main__":
    main()

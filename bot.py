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

# 配置日志
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# /start 命令
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "你好！我是双向机器人\n"
        "发任何消息我都会回复你！\n"
        "试试说：你好"
    )

# /help 命令
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start - 开始\n"
        "/help - 帮助\n"
        "其他消息我会回显 + 时间"
    )

# 回音处理
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    await update.message.reply_text(f"你说：{text}\n\n回复时间：{now}")

# 错误处理
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error("处理更新时出错:", exc_info=context.error)

# 主函数
def main():
    # 必须设置 BOT_TOKEN
    TOKEN = os.getenv("BOT_TOKEN")
    if not TOKEN:
        raise ValueError("错误：请在环境变量中设置 BOT_TOKEN")

    # 创建 Application
    app = Application.builder().token(TOKEN).build()

    # 注册处理器
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    app.add_error_handler(error_handler)

    # 部署模式
    mode = os.getenv("DEPLOY_MODE", "polling").lower()

    if mode == "webhook":
        webhook_url = os.getenv("WEBHOOK_URL")
        port = int(os.getenv("PORT", "10000"))

        if not webhook_url:
            raise ValueError("WEBHOOK 模式需要设置 WEBHOOK_URL")

        # 关键：url_path 必须是 TOKEN 本身
        print(f"启动 Webhook: {webhook_url}/{TOKEN}")
        app.run_webhook(
            listen="0.0.0.0",
            port=port,
            url_path=TOKEN,                    # 正确：使用 TOKEN
            webhook_url=f"{webhook_url}/{TOKEN}"
        )
    else:
        print("启动 Polling 模式（本地调试）")
        app.run_polling()

if __name__ == "__main__":
    main()

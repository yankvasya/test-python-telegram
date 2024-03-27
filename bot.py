import logging
import random
import os

from telegram import Update,ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from dotenv import load_dotenv

load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

reply_keyboard = [["🟥", "⬛️"]]

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


async def start(update: Update,ContextTypes) -> None:
    """Send a message when the command /start is issued."""

    user = update.effective_user
    await update.message.reply_html(
        f"Hi {user.mention_html()}!\n\nWhat is color card: 🟥 or ⬛️?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="What is color card?"
        ),
    )


async def take_random_card():
    """Get a random card"""
    types = ['♦', '♥', '♠', '♣']
    values = ['6', '7', '8', '9', 'V', 'D', 'K']
    return f'{random.choice(types)}{random.choice(values)}'


async def random_card(update: Update,ContextTypes) -> None:
    types = {
        '♦': '🟥',
        '♥': '🟥',
        '♠': '⬛️',
        '♣': '⬛️',
    }
    current_card = await take_random_card()
    type_current_card = current_card[0]
    is_valid = types[type_current_card] == update.message.text
    response_text = "Correct" if is_valid else "Incorrect"
    await update.message.reply_text(f'{response_text}. Card was {current_card}\n\nWhat is color card: 🟥 or ⬛️?',
                                    reply_markup=ReplyKeyboardMarkup(
                                        reply_keyboard, one_time_keyboard=True,
                                        input_field_placeholder=f"{response_text}. What is color card?"
                                    ),
                                    )


def main() -> None:
    """Start the bot."""
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, random_card))
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()

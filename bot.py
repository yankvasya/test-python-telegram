import logging
import random

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

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
    await update.message.reply_text(f'{"Correct" if is_valid else "Incorrect"}. Card was {current_card}\n\nWhat is color card: 🟥 or ⬛️?')


def main() -> None:
    """Start the bot."""
    application = Application.builder().token("7167409761:AAGZ-gigq4_B-NVT730GS2tOPOHzGKxt6H8").build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, random_card))
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()

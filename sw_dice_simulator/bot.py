import os
import gettext
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from sw_dice_simulator.dice import roll_from_string

# Load translations
localedir = os.path.join(os.path.dirname(__file__), "locales")
def get_translation(language):
    return gettext.translation("bot", localedir, languages=[language], fallback=True)

# Variable to store user language preferences
user_languages = {}

# Whitelist file path
WHITELIST_FILE = "whitelist.txt"

def load_whitelist():
    """Loads the whitelist from a file."""
    try:
        with open(WHITELIST_FILE, "r") as file:
            return set(line.strip() for line in file if line.strip())
    except FileNotFoundError:
        print(f"Whitelist file {WHITELIST_FILE} not found. Creating an empty whitelist.")
        return set()

WHITELIST = load_whitelist()

def is_user_allowed(update: Update, translator) -> bool:
    """Checks if the user is in the whitelist."""
    username = update.effective_user.username
    if username not in WHITELIST:
        _ = translator.gettext
        update.message.reply_text(
            _( "I'm sorry, you're not subscribed. Go to swdicebot.matesncode.com to subscribe.")
        )
        return False
    return True


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a welcome message when the bot is started."""
    translator = get_translation("en")
    if not is_user_allowed(update, translator):
        return

    user_id = update.effective_user.id
    user_languages[user_id] = "en"  # Default language is English
    _ = translator.gettext
    await update.message.reply_text(
        _("")
        + "Welcome to the Star Wars Dice Roller bot!\n"
        + "Use /roll <dice_input> to roll your dice.\n"
        + "Use /language <en|es> to set your language.\n"
        + "Use /list_dice to see available dice options.\n"
        + "Example: /roll 2ca,2pe,3di,1be,2co"
    )


async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sets the user's preferred language."""
    translator = get_translation("en")
    if not is_user_allowed(update, translator):
        return

    if not context.args:
        await update.message.reply_text("Usage: /language <en|es>")
        return

    language = context.args[0].lower()
    if language not in ["en", "es"]:
        await update.message.reply_text("Invalid language. Use 'en' or 'es'.")
        return

    user_id = update.effective_user.id
    user_languages[user_id] = language
    translator = get_translation(language)
    _ = translator.gettext
    await update.message.reply_text(_("Language set successfully."))


async def list_dice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Lists the possible dice options in the user's selected language."""
    user_id = update.effective_user.id
    language = user_languages.get(user_id, "en")
    translator = get_translation(language)
    if not is_user_allowed(update, translator):
        return

    _ = translator.gettext
    dice_list = {
        "ability": _( "Ability (ca)"),
        "proficiency": _( "Proficiency (pe)"),
        "difficulty": _( "Difficulty (di)"),
        "challenge": _( "Challenge (de)"),
        "boost": _( "Boost (be)"),
        "setback": _( "Setback (co)"),
        "force": _( "Force (fu)")
    }

    response = _( "Available dice options:\n")
    for name in dice_list.values():
        response += f"- {name}\n"

    await update.message.reply_text(response)


async def roll(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles dice rolling and sends the results."""
    user_id = update.effective_user.id
    language = user_languages.get(user_id, "en")
    translator = get_translation(language)
    if not is_user_allowed(update, translator):
        return

    if not context.args:
        await update.message.reply_text("Usage: /roll <dice_input>")
        return

    dice_input = " ".join(context.args)
    try:
        results, individual_rolls = roll_from_string(dice_input)
        _ = translator.gettext

        # Prepare the response
        response = _( "🎲 **Individual Rolls:**\n")
        for roll in individual_rolls:
            response += f"- {roll['dice_type']}: {roll['result']}\n"

        response += _( "\n**Final Results:**\n")
        for symbol, count in results.items():
            response += f"- {symbol}: {count}\n"

        await update.message.reply_text(response)
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")


def main():
    """Run the bot."""
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    if not TOKEN:
        raise ValueError("The TELEGRAM_BOT_TOKEN environment variable is missing!")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("roll", roll))
    app.add_handler(CommandHandler("language", set_language))
    app.add_handler(CommandHandler("list_dice", list_dice))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()

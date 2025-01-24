import os
import gettext
import random
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dice import roll_from_string

# Load translations
localedir = os.path.join(os.path.dirname(__file__), "locales")


def get_translation(language):
    return gettext.translation("bot", localedir, languages=[language], fallback=True)


# Variable to store user language preferences and bot mode
user_languages = {}
bot_mode = "text"  # Default mode is text

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
    # username = update.effective_user.username
    # if username not in WHITELIST:
    #     _ = translator.gettext
    #     update.message.reply_text(
    #         _("I'm sorry, you're not subscribed. Go to swdicebot.matesncode.com to subscribe.")
    #     )
    #     return False
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
        _("Welcome to the Star Wars Dice Roller bot!\n"
          "Use /roll <dice_input> to roll your dice.\n"
          "Use /language <en|es> to set your language.\n"
          "Use /list_dice to see available dice options.\n"
          "Example: /roll 2ca,2pe,3di,1be,2co")
    )


async def set_mode(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sets the bot mode (text or picture)."""
    global bot_mode
    translator = get_translation("en")
    if not is_user_allowed(update, translator):
        return

    if not context.args or context.args[0].lower() not in ["text", "picture"]:
        await update.message.reply_text("Usage: /mode <text|picture>")
        return

    bot_mode = context.args[0].lower()
    await update.message.reply_text(f"Bot mode set to {bot_mode}.")


async def list_dice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Lists the possible dice options in the user's selected language."""
    user_id = update.effective_user.id
    language = user_languages.get(user_id, "en")
    translator = get_translation(language)
    if not is_user_allowed(update, translator):
        return

    _ = translator.gettext
    dice_list = {
        "ability": _("Ability (ca)"),
        "proficiency": _("Proficiency (pe)"),
        "difficulty": _("Difficulty (di)"),
        "challenge": _("Challenge (de)"),
        "boost": _("Boost (be)"),
        "setback": _("Setback (co)"),
        "force": _("Force (fu)")
    }

    response = _("Available dice options:\n")
    for name in dice_list.values():
        response += f"- {name}\n"

    await update.message.reply_text(response)


async def roll(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles dice rolling and sends the results."""
    global bot_mode
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

        if bot_mode == "text":
            # Prepare the response in text mode
            response = _("🎲 **Individual Rolls:**\n")
            for roll in individual_rolls:
                response += f"- {roll['dice_type']}: {roll['result']}\n"

        elif bot_mode == "picture":
            # Send pictures for each individual roll
            for roll in individual_rolls:
                dice_type = roll['dice_type']
                result = roll['result']

                # Find the corresponding folder and images
                BASE_DIR = os.path.dirname(os.path.abspath(__file__))
                folder_path = os.path.join(BASE_DIR, "dices", dice_type, result)
                if os.path.exists(folder_path):
                    images = os.listdir(folder_path)
                    if images:
                        # Pick a random image
                        image_path = os.path.join(folder_path, random.choice(images))
                        with open(image_path, "rb") as image_file:
                            await update.message.reply_photo(InputFile(image_file))
                else:
                    await update.message.reply_text(f"No image found for {dice_type} - {result}")

        response += _("\n**Final Results:**\n")
        for symbol, count in results.items():
            response += f"- {symbol}: {count}\n"

        await update.message.reply_text(response)

    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")


async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sets the user's preferred language."""
    translator = get_translation("en")
    if not is_user_allowed(update, translator):
        return

    if not context.args or context.args[0].lower() not in ["en", "es"]:
        await update.message.reply_text(
            _("Usage: /language <en|es>")
        )
        return

    language = context.args[0].lower()
    user_id = update.effective_user.id
    user_languages[user_id] = language

    translator = get_translation(language)
    _ = translator.gettext
    await update.message.reply_text(
        _("Language set successfully.")
    )


def main():
    """Run the bot."""
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    if not TOKEN:
        raise ValueError("The TELEGRAM_BOT_TOKEN environment variable is missing!")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("roll", roll))
    app.add_handler(CommandHandler("mode", set_mode))
    app.add_handler(CommandHandler("language", set_language))
    app.add_handler(CommandHandler("list_dice", list_dice))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()

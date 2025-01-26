
# Star Wars Dice Roller Bot

A Telegram bot that simulates dice rolls for the **Star Wars: Edge of the Empire** role-playing game, including support for text and image-based outputs. The bot allows players to roll dice pools, set their language, and view detailed results of their rolls.

## Features

- Roll dice pools using RPG-specific dice:
  - **Ability (ca)**, **Proficiency (pe)**, **Difficulty (di)**, **Challenge (de)**, **Boost (be)**, **Setback (co)**, and **Force (fu)**
- Multi-language support: English (`en`) and Spanish (`es`)
- Choose between text or image-based results
- Configurable user access using a whitelist

---

## Installation

### Prerequisites
- Python 3.8 or higher
- `pip` and `virtualenv` installed

### Step 1: Clone the Repository
```bash
git clone https://github.com/your-username/star-wars-dice-roller-bot.git
cd star-wars-dice-roller-bot
```

### Step 2: Set Up the Environment
1. Create and activate a virtual environment:
   ```bash
   python3.8 -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Configuration

### Telegram Bot Token
1. Create a bot using [BotFather](https://core.telegram.org/bots#botfather).
2. Copy the token and set it as an environment variable:
   ```bash
   export TELEGRAM_BOT_TOKEN=your_token_here
   ```

### Language Configuration
The bot uses `.po` and `.mo` files for translations. To update translations:
1. Extract translatable strings:
   ```bash
   xgettext -o locales/bot.pot --language=Python --keyword=_ bot.py
   ```
2. Create `.po` files for your desired languages:
   ```bash
   msginit -l en -i locales/bot.pot -o locales/en/LC_MESSAGES/bot.po
   msginit -l es -i locales/bot.pot -o locales/es/LC_MESSAGES/bot.po
   ```
3. Compile translations:
   ```bash
   msgfmt locales/en/LC_MESSAGES/bot.po -o locales/en/LC_MESSAGES/bot.mo
   msgfmt locales/es/LC_MESSAGES/bot.po -o locales/es/LC_MESSAGES/bot.mo
   ```

### Whitelist Configuration
To restrict access to specific users, add their Telegram usernames to the `whitelist.txt` file (one username per line).

---

## Usage

### Start the Bot
1. Run the bot:
   ```bash
   python bot.py
   ```

2. Use `screen` to run the bot in the background:
   - Start a new `screen` session:
     ```bash
     screen -S bot_session
     ```
   - Run your bot inside the `screen` session:
     ```bash
     python bot.py
     ```
   - Detach from the session:
     Press `Ctrl+A` followed by `D`.

3. Reattach to the `screen` session when needed:
   ```bash
   screen -r bot_session
   ```

4. List all active `screen` sessions:
   ```bash
   screen -ls
   ```

5. To stop the bot and close the session, reattach and type:
   ```bash
   exit
   ```

### Commands
| Command            | Description                                                                 |
|--------------------|-----------------------------------------------------------------------------|
| `/start`           | Displays a welcome message and instructions.                              |
| `/roll <dice>`     | Rolls the specified dice pool (e.g., `/roll 2ca,1pe,1di`).                 |
| `/language <lang>` | Sets the language (`en` or `es`).                                          |
| `/list_dice`       | Lists the available dice and their shorthand codes.                       |

### Text and Image Modes
- **Text Mode**: Displays roll results in plain text.
- **Image Mode**: Displays dice rolls as images. Images are stored in the `dices/` directory, with a folder for each dice type and its results. I'm sorry but, due to copyright considerations, dice images are not included in the repository. Please add your own images for the dice results.

---

## Directory Structure

```
.
├── bot.py                # Main bot logic
├── dice.py               # Dice rolling logic
├── locales/              # Translation files
│   ├── en/LC_MESSAGES/
│   │   ├── bot.po
│   │   └── bot.mo
│   └── es/LC_MESSAGES/
│       ├── bot.po
│       └── bot.mo
├── dices/                # Dice images directory
│   ├── ability/
│   ├── proficiency/
│   ├── difficulty/
│   ├── ...
├── requirements.txt      # Python dependencies
└── whitelist.txt         # User whitelist for bot access
```

---

## License

This project is licensed under the [GNU General Public License v3.0](LICENSE).

---

## Contributors

- **Gabriel La Torre** - Developer

For contributions, feel free to open issues or submit pull requests.

---

## Support

If you encounter issues or have questions, please reach out to [hola@latorregabriel.com](mailto:hola@latorregabriel.com).

# EtuUTT-Bot

A project of redoing the Discord bot made in JavaScript used at my school.  
Be sure to have Python 3.8 or higher installed as it is required by discord.py.

Clone the projet and install the requirements (in a venv preferably):

```
git clone https://github.com/Zalk0/EtuUTT-Bot.git
cd EtuUTT-Bot
pip install -r requirements.txt
```

---
Before launching the bot, you need to fill in a **`.env`** file (using
the [example](https://github.com/Zalk0/EtuUTT-Bot/blob/main/.env.example)
I provide in the repo).  
You need a Discord bot token, to have one go to
the [Discord Developer Portal](https://discord.com/developers) and create a new
application.  
Go to the Bot section and click the Reset Token button, you can now claim the token.  
You also have to enable all the Privileged Gateway Intents as I assume they're enabled in the code.

---
After having done all this you can launch the bot:

```
python main.py
```

## Contributing

Use [ruff](https://github.com/astral-sh/ruff) to lint and format the code before making a pull
request.

## Acknowledgments

Thanks to Ivann which did the original Discord bot.

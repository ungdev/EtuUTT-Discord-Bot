# EtuUTT-Discord-Bot

A project of redoing the Discord bot made in JavaScript used at my school.  
Be sure to have Python 3.8 or higher installed as it is required by discord.py.

Clone the projet and install the requirements (in a
[venv](https://docs.python.org/library/venv.html) preferably):

```
git clone https://github.com/ungdev/EtuUTT-Discord-Bot.git
cd EtuUTT-Discord-Bot
pip install -r requirements.txt
```

Note: replace `requirements.txt` by `requirements-dev.txt` if you wish to install the dev
requirements to contribute to the bot.

---
Before launching the bot, you need to fill in a **`.env`** file (using
the [example](https://github.com/ungdev/EtuUTT-Discord-Bot/blob/main/.env.example)
I provide in the repo).  
You need a Discord bot token, to have one go to
the [Discord Developer Portal](https://discord.com/developers) and create a new
application.  
Go to the Bot section and click the Reset Token button, you can now claim the token.  
You also have to enable all the Privileged Gateway Intents as I assume they're enabled in the code.

---
After having done all this you can launch the bot:

```
python -m etuutt_bot
```

## Contributing

Use [ruff](https://github.com/astral-sh/ruff) to lint and format the code before making a pull request.  
I also use [pre-commit](https://github.com/pre-commit/pre-commit) to run ruff before each commit.

## Acknowledgments

Thanks to Ivann who did the original Discord bot.  
It can be found [here](https://github.com/ungdev/discord_bot_firewall).

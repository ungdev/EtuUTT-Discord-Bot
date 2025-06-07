# EtuUTT-Discord-Bot

A project of redoing the Discord bot made in JavaScript used at my school.  
Be sure to have Python 3.10 or higher installed.

Clone the projet and install [uv](https://docs.astral.sh/uv/getting-started/installation/):

```bash
git clone https://github.com/ungdev/EtuUTT-Discord-Bot.git
cd EtuUTT-Discord-Bot/
uv sync
```

> [!TIP]
> The `uv sync` command creates a virtual environment and installs the dependencies inside.
> By default, it installs the project dependencies and the dependencies of the dev group.
> To install the dependencies of the other groups (like the docs), you can add the `--all-groups`
> flag to the command.

---
Before launching the bot, you need to fill in the two configuration files (**`.env`** and
**`discord.toml`**) (using the [.env.example](.env.example) and
the [discord.example.toml](data/discord.example.toml) I provide in the repo).  
You can copy them like this and edit the copied files:

```bash
cp .env.example .env
cp data/discord.example.toml data/discord.toml
```

You need a Discord bot token, to have one go to
the [Discord Developer Portal](https://discord.com/developers) and create a new
application.  
Go to the Bot section and click the Reset Token button, you can now claim the token.  
You also have to enable all the Privileged Gateway Intents as I assume they're enabled in the code.

---
After having done all this you can launch the bot:

```bash
python -m etuutt_bot
```

## Contributing

Use [ruff](https://github.com/astral-sh/ruff) to lint and format the code before making a pull
request.  
I also use [pre-commit](https://github.com/pre-commit/pre-commit) to run ruff before each commit.

## Acknowledgments

Thanks to Ivann who did the original Discord bot.  
It can be found [here](https://github.com/ungdev/discord_bot_firewall).

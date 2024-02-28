import logging
from os import getenv

import discord
from discord.ext import commands

from etuutt_bot.commands_list import commands_list
from etuutt_bot.web import start_server


# Create a class of the bot
class EtuUTTBot(commands.Bot):
    # Initialization when class is called
    def __init__(self):
        # Define the bot debug log level, defaults to INFO if undefined or invalid
        self.logger = logging.getLogger("bot")
        log_level = logging.getLevelName(getenv("LOG_LEVEL", logging.INFO))
        self.log_level = log_level if isinstance(log_level, int) else logging.INFO
        self.logger.setLevel(self.log_level)

        # Set intents for the bot
        intents = discord.Intents.all()

        # Set activity of the bot
        activity_type = {
            "playing": 0,
            "streaming": 1,
            "listening": 2,
            "watching": 3,
            "custom": 4,
            "competing": 5,
        }
        activity = discord.Activity(
            type=activity_type.get(getenv("BOT_ACTIVITY_TYPE")),
            name=getenv("BOT_ACTIVITY_NAME"),
            state=getenv("BOT_ACTIVITY_STATE"),
        )

        # Apply intents, activity and status to the bot
        super().__init__(
            command_prefix=commands.when_mentioned,
            intents=intents,
            activity=activity,
            status=getenv("BOT_STATUS"),
        )

        # Variable for storing owners id
        # If set manually, it will not fetch from the bot's application info
        self.owners = []

    async def setup_hook(self):
        # Populate the command tree
        await commands_list(self)

        # Starts the web server
        await start_server(self)

    # When the bot is ready
    async def on_ready(self):
        # Waits until internal cache is ready
        await self.wait_until_ready()

        # Log in the console that the bot is ready
        self.logger.info(f"{self.user} is now online and ready!")

        await self.get_channel(int(getenv("CHANNEL_ADMIN_ID"))).send(
            "Je suis en ligne. Je viens d'être (re)démarré. Cela signifie qu'il y a soit eu "
            "un bug, soit que j'ai été mis à jour, soit qu'on m'a redémarré manuellement."
        )

    # Event when someone joins a guild the bot is in
    async def on_member_join(self, member: discord.Member):
        # Ignore join of bots
        if member.bot:
            return

        # If member joined the guild the bot is watching
        if member.guild.id == getenv("GUILD_ID"):
            await member.send(
                "Bienvenue sur le serveur Discord des étudiants de l'UTT.\n"
                "Ceci n'étant pas une zone de non droit, vous **devez** vous identifier "
                f"en cliquant ici (**que vous soyez étudiant ou prof**) : {getenv('BOT_URL')}"
                "Vous devez également lire les règles dans le channel `accueil`\n\n"
                "En cas de problème, contactez l'un des administrateurs, "
                "visibles en haut à droite.\n"
                "Tapez `/` dans un channel texte pour voir la liste des commandes."
            )

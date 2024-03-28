import logging
from os import getenv
from pathlib import Path

import aiohttp
import discord
import tomlkit as toml
from discord.ext import commands
from tomlkit.exceptions import TOMLKitError

from etuutt_bot.commands_list import commands_list
from etuutt_bot.web import start_server


# Create a class of the bot
class EtuUTTBot(commands.Bot):
    # Initialization when class is called
    def __init__(self) -> None:
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

        # Initialize watched guild with only ID
        self.watched_guild = discord.Object(id=int(getenv("GUILD_ID")))

    async def setup_hook(self) -> None:
        # Start aiohttp client session
        self.session = aiohttp.ClientSession()
        # Load data in the bot
        try:
            self.data = toml.parse(Path("data", "discord.toml").read_text())
        except FileNotFoundError:
            self.logger.warning("Discord Data file not found")
        except TOMLKitError as e:
            self.logger.warning(f"Unable to parse Discord Data: {e}")
        # Load commands
        await commands_list(self)
        # Start the web server
        self.runner = await start_server(self)

    # When the bot is ready
    async def on_ready(self) -> None:
        # Waits until internal cache is ready
        await self.wait_until_ready()

        # Get watched guild with additional information
        self.watched_guild = self.get_guild(int(getenv("GUILD_ID")))

        # Log in the console and the admin channel that the bot is ready
        self.logger.info(f"{self.user} is now online and ready!")
        await self.get_channel(int(getenv("CHANNEL_ADMIN_ID"))).send(
            "Je suis en ligne. Je viens d'être (re)démarré. Cela signifie qu'il y a soit eu "
            "un bug, soit que j'ai été mis à jour, soit qu'on m'a redémarré manuellement."
        )

    # Event when someone joins a guild the bot is in
    async def on_member_join(self, member: discord.Member) -> None:
        # Ignore join of bots
        if member.bot:
            return

        # If member joined the guild the bot is watching
        if member.guild.id == self.watched_guild.id:
            await member.send(
                "Bienvenue sur le serveur Discord des étudiants de l'UTT.\n"
                "Ceci n'étant pas une zone de non droit, vous **devez** vous identifier "
                f"en cliquant ici (**que vous soyez étudiant ou prof**) : {getenv('BOT_URL')}"
                "Vous devez également lire les règles dans le channel `accueil`\n\n"
                "En cas de problème, contactez l'un des administrateurs, "
                "visibles en haut à droite.\n"
                "Tapez `/` dans un channel texte pour voir la liste des commandes."
            )

    # React to messages sent in channels bot has access to
    async def on_message(self, message: discord.Message) -> None:
        # Ignore messages from bots including self
        if message.author.bot:
            return

        # Do something on message from a user

        # Process declared commands
        await self.process_commands(message)

    async def close(self) -> None:
        # Write Discord Data back to file (save the modifs)
        Path("data", "discord.toml").write_text(toml.dumps(self.data))

        # Close web server and http session cleanly
        await self.runner.cleanup()
        await self.session.close()

        # Do normal action when stopped (do last because it might throw an error)
        # Error fix: https://github.com/Rapptz/discord.py/pull/9769
        # We can't perform async operation after the super call as it may be stopped midway
        await super().close()
        self.logger.info("Bot stopped gracefully")

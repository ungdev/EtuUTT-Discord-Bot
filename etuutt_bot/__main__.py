import asyncio
import os
import signal
from logging import handlers
from pathlib import Path

import sentry_sdk
from discord.utils import setup_logging
from sentry_sdk.integrations.aiohttp import AioHttpIntegration

from etuutt_bot.bot import EtuUTTBot


# Class taken from the d.py server
# It's to run the bot.close() method which is async as the (sync) signal handler
class StopSignalHandler:
    def __init__(self, bot):
        self.bot = bot
        self._task = None

    def __call__(self):
        if self._task:
            raise KeyboardInterrupt
        self._task = asyncio.create_task(self.bot.close())


async def main():
    """Fonction principale appelée au démarrage du bot."""
    # Automatically reads SENTRY_DSN environment var
    sentry_sdk.init(
        # Enable performance monitoring
        enable_tracing=True,
        # Choose integrations
        # TODO: fine tuning integrations and settings (maybe use logging instead)
        integrations=[AioHttpIntegration(transaction_style="method_and_path_pattern")],
    )

    # Create an instance of the Discord Bot
    bot = EtuUTTBot()

    # Setup the logging (stream handler and file handler)
    setup_logging()
    Path("data", "logs").mkdir(exist_ok=True)
    handler = handlers.RotatingFileHandler(
        filename=Path("data", "logs", "log"),
        maxBytes=10485760,  # 10Mo
        backupCount=5,
        encoding="utf-8",
    )
    setup_logging(handler=handler)

    # Run the bot with token and handle stop signals to stop gracefully
    async with bot:
        # Check for Windows because Windows isn't able to handle signals like UNIX systems
        # There's no implementation of add_signal_handlers() on Windows
        # Consequence: the bot won't be able to stop gracefully on Windows
        # Doesn't really matter as the prod runs on Linux/in Docker
        if os.name != "nt":
            for s in (signal.SIGHUP, signal.SIGINT, signal.SIGTERM):
                bot.loop.add_signal_handler(s, StopSignalHandler(bot))
        token = bot.settings.bot.token.get_secret_value()
        await bot.start(token, reconnect=True)


if __name__ == "__main__":
    asyncio.run(main())

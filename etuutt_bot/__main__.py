import asyncio
import signal
from logging import handlers
from os import getenv
from pathlib import Path

import sentry_sdk
from discord.utils import setup_logging
from dotenv import load_dotenv
from sentry_sdk.integrations.aiohttp import AioHttpIntegration

from etuutt_bot.bot import EtuUTTBot


class StopSignalHandler:
    def __init__(self, bot):
        self.bot = bot
        self._task = None

    def __call__(self):
        if self._task:
            raise KeyboardInterrupt
        self._task = asyncio.create_task(self.bot.close())


async def main():
    # Load the environment variables from the .env file if it exists
    if Path(".env").is_file():
        load_dotenv()

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

    # Setup the logging
    Path("logs").mkdir(exist_ok=True)
    handler = handlers.RotatingFileHandler(
        filename=Path("logs", "log"),
        maxBytes=10485760,  # 10Mo
        backupCount=5,
        encoding="utf-8",
    )
    setup_logging(handler=handler)

    # Run the bot with token and handle stop signals to stop gracefully
    async with bot:
        for s in (signal.SIGHUP, signal.SIGTERM, signal.SIGINT):
            bot.loop.add_signal_handler(s, StopSignalHandler(bot))
        await bot.start(getenv("BOT_TOKEN"), reconnect=True)


if __name__ == "__main__":
    asyncio.run(main())

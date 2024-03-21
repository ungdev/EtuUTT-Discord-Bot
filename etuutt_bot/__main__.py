import logging.handlers as handlers
from os import getenv
from pathlib import Path

import sentry_sdk
from dotenv import load_dotenv
from sentry_sdk.integrations.aiohttp import AioHttpIntegration

from etuutt_bot.bot import EtuUTTBot


def main():
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
    client = EtuUTTBot()

    # Setup the logging
    Path("logs").mkdir(exist_ok=True)
    handler = handlers.RotatingFileHandler(
        filename=Path("logs", "log"),
        maxBytes=10485760,  # 10Mo
        backupCount=5,
        encoding="utf-8",
    )

    # Run the client with the token
    client.run(getenv("BOT_TOKEN"), reconnect=True, log_handler=handler, root_logger=True)


if __name__ == "__main__":
    main()

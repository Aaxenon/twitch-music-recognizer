from modules.bot import Bot
from modules.config import config
from modules.logger import logger


if __name__ == '__main__':
    if config.bot_token and config.twitch_channel:
        bot = Bot()
    else:
        logger.error('Empty bot token or channel name')

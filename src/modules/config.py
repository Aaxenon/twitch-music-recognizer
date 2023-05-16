import os
from modules.logger import logger

DEFAULT_COOLDOWN = 90
DEFAULT_RECORD_LENGTH = 7
MIN_COOLDOWN = 45


class Config:
    def __init__(self):
        self.bot_token = os.getenv('TWITCH_BOT_OAUTH_TOKEN')
        self.command_aliases = os.getenv('TWITCH_COMMAND_ALIASES')
        self.command_name = os.getenv('TWITCH_COMMAND_NAME') or 'song'
        self.command_prefix = os.getenv('TWITCH_CHAT_PREFIX') or '!'
        self.messages = {
            'LISTENING': os.getenv('MESSAGE_LISTENING') or 'Listening to the stream...',
            'NO_SONG': os.getenv('MESSAGE_NO_SONG') or 'Song is not recognized.',
            'NO_STREAM': os.getenv('MESSAGE_NO_STREAM') or 'No stream available.',
            'RETRY': os.getenv('MESSAGE_RETRY') or 'One more try...',
            'SONG_NAME': os.getenv('MESSAGE_SONG_NAME') or '{}',
        }
        self.twitch_channel = os.getenv('TWITCH_CHANNEL_NAME')
        self.should_retry = False if os.getenv(
            'TWITCH_SHOULD_RETRY') == '0' else True
        self.set_cooldown()
        self.set_record_length()

    def set_cooldown(self):
        cooldown = DEFAULT_COOLDOWN
        env_cooldown = os.getenv('TWITCH_COMMAND_COOLDOWN')

        if env_cooldown:
            try:
                env_cooldown = int(env_cooldown)
            except ValueError:
                logger.error('Invalid cooldown number, using default value')
            else:
                if env_cooldown >= MIN_COOLDOWN:
                    cooldown = env_cooldown
                else:
                    logger.error('Invalid cooldown time, using default value')

        setattr(type(self), 'command_cooldown', cooldown)

    def set_record_length(self):
        record_length = DEFAULT_RECORD_LENGTH
        env_record_length = os.getenv('TWITCH_RECORD_LENGTH')

        if env_record_length:
            try:
                env_record_length = int(env_record_length)
            except ValueError:
                logger.error('Invalid record length number, using default value')
            else:
                if env_record_length >= 0:
                    record_length = env_record_length
                else:
                    logger.error('Invalid record length time, using default value')

        setattr(type(self), 'record_length', record_length)


config = Config()

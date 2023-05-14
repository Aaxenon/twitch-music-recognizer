import asyncio
import time
from twitchio.ext import commands
from modules.config import config
from modules.logger import logger
from modules.recognizer import Recognizer


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            token=config.bot_token,
            prefix=config.command_prefix,
            initial_channels=[config.twitch_channel]
        )
        self.recognizer = Recognizer()
        self.last_run_time = 0
        self.run()

    async def event_ready(self):
        logger.info('Bot is running')

    async def event_error(self, error):
        logger.error(error)

    @commands.command(
        name=config.command_name,
        aliases=[alias.strip() for alias in config.command_aliases.split(',')],
    )
    async def get_song(self, ctx: commands.Context):
        # Check if command is on cooldown
        if int(time.time()) - self.last_run_time < config.command_cooldown:
            return

        self.last_run_time = int(time.time())
        await ctx.reply(config.messages['LISTENING'])

        response = await self.recognizer.execute()

        # There is no delay between replies if stream is offline
        # Following replies don't go through if they are too frequent 
        if response == config.messages['NO_STREAM']:
            await asyncio.sleep(5)

        # Do one retry if retrying is enabled and song is not recognized
        if config.should_retry and response == config.messages['NO_SONG']:
            await ctx.reply(config.messages["RETRY"])
            response = await self.recognizer.execute()

        await ctx.reply(response)

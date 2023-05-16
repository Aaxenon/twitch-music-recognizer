import asyncio
import streamlink
import subprocess
from shazamio import Shazam
from modules.config import config
from modules.logger import logger

CONVERT_COMMAND = 'ffmpeg -ss 3 -i /output/clip_1.mp4 ' \
    '-loglevel error -vn -acodec libvorbis -y /output/audio.ogg'


class Recognizer:
    def __init__(self):
        self.shazam = Shazam()
        self.twitch_channel = config.twitch_channel
        # Add ad time to record length
        self.record_length = config.record_length + 13

    def convert_mp4_to_ogg(self):
        subprocess.call(CONVERT_COMMAND, shell=True)

    async def execute(self):
        is_stream_recorded = await self.record_stream()

        if not is_stream_recorded:
            return config.messages['NO_STREAM']

        self.convert_mp4_to_ogg()

        response = await self.recognize_song()
        return response

    async def get_stream_url(self):
        streams = streamlink.streams(
            f'https://www.twitch.tv/{self.twitch_channel}')

        if 'audio_only' in streams:
            m3u8_url = streams['audio_only'].url
            return True, m3u8_url
        else:
            return False, None

    async def recognize_song(self):
        response = await self.shazam.recognize_song('/output/audio.ogg')

        if response and len(response['matches']) > 0:
            return config.messages['SONG_NAME']\
                .format(response['track']['share']['subject'])
        else:
            return config.messages['NO_SONG']

    async def record_stream(self):
        is_stream_available, m3u8_url = await self.get_stream_url()

        if not is_stream_available or not m3u8_url:
            return False

        ffmpeg_cmd = ['ffmpeg', '-i', m3u8_url, '-c', 'copy',
                      '-f', 'segment', '-segment_wrap', '3',
                      '-segment_time', '12', '-loglevel', 'error',
                      '-bsf:a', 'aac_adtstoasc', '/output/clip_%d.mp4']
        process = await asyncio.create_subprocess_exec(*ffmpeg_cmd)
        await asyncio.sleep(self.record_length)
        process.terminate()
        await process.communicate()
        return True

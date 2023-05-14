
# Twitch Livestream Music Recognizer Bot

This is a Twich Bot that is based on [TwitchIO](https://github.com/TwitchIO/TwitchIO) and uses [ShazamIO](https://github.com/dotX12/ShazamIO) to recognize music on a livestream in real-time and output the song name in the chat when recognized.

## How it works

When a viewer uses a command in the Twitch chat, the bot will start recording the stream’s audio for 22 seconds. It will then remove the first 13 seconds, which contains an embedded Twitch ad. The remaining audio will be sent to ShazamIO to recognize the song. If ShazamIO can detect the song, the bot will output the song name in the chat.

## Deployment

- Clone the project to your desired location
- Copy and rename .env.default file using the command:

```bash
  cp .env.default .env
```

- Set your environment variables in .env file (explained below)
- Build and run the Docker container using:

```bash
  docker compose up master
```

Alternatively, you can run the container in the background using the ```--detach``` flag with the ```docker compose up``` command.

You can find the logs in the ```logs``` folder.

## Environment variables

Before running the service, ensure that you’ve set the following environment variables in your ```.env``` file:

```
TWITCH_BOT_OAUTH_TOKEN=<token>
TWITCH_CHANNEL_NAME=<username>
```

Where ```<token>``` and ```<username>``` are your respective Twitch Bot OAuth Token and your Twitch Channel Name. You can generate your Twitch Bot OAuth Token by following the instructions on the official Twitch Developer site. You can find an example of token generation at [Twitch Token Generation website](https://twitchapps.com/tmi/). Note that you need to be logged in as your bot account.

The following variables are optional and will use default values if left blank:

```
# Aliases for command. No default values. Accepts one or multiple values separated by a comma
TWITCH_COMMAND_ALIASES=
# Cooldown for command, value in seconds. Minimum value is 45. Default value: 90
TWITCH_COMMAND_COOLDOWN=
# Command name. Default value: song
TWITCH_COMMAND_NAME=
# Prefix for command. Default value: !
TWITCH_CHAT_PREFIX=
# If the bot should automatically retry after the first failure. 
# Takes 1 or 0 as values for true or false values accordingly. Default value: 1
TWITCH_SHOULD_RETRY=

# Localization
# Message at the start of recognition. Default value: Listening to the stream...
MESSAGE_LISTENING=
# Message if the song is not recognized. Default value: Song is not recognized.
MESSAGE_NO_SONG=
# Message if the stream is not available. Default value: No stream available.
MESSAGE_NO_STREAM=
 Message for retry if the song is not recognized. Default value: Song is not recognized.
MESSAGE_RETRY=
# Message for song name output.
# Takes a string with '{}' characters that will be replaced with 'Title - Artist'.
# Example: Track is: {}. Enjoy!
# Output: Track is: Title - Artist. Enjoy!
# Default value: {}
MESSAGE_SONG_NAME=
```

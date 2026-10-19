import os

from dotenv import load_dotenv

import logging

# noinspection PyPackageRequirements
import discord
# noinspection PyPackageRequirements
from discord.ext import commands

load_dotenv()

DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
DISCORD_GUILD_ID = os.getenv('DISCORD_GUILD_ID')
DISCORD_WELCOME_CHANNEL_ID = os.getenv('DISCORD_WELCOME_CHANNEL_ID')
DISCORD_ROLE_MESSAGE_ID = os.getenv('DISCORD_ROLE_MESSAGE_ID')
DISCORD_GENERAL_CHANNEL_ID = os.getenv('DISCORD_GENERAL_CHANNEL_ID')
MEMBER_ROLE_ID = os.getenv('MEMBER_ROLE_ID')

ALLOWED_WELCOME_MESSAGES = [
    "hi",
    "hii",
    "hiii",
    "hai",
    "haii",
    "haiii"
]

# Intents
_intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=_intents)

# logger
logger = logging.getLogger()
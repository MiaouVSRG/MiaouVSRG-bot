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

# Intents
_intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=_intents)

# logger
logger = logging.getLogger()
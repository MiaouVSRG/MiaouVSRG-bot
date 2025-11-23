import random

from globals import *

from discord.ext import tasks
from discord.utils import get

import datetime

import requests

IS_SERVER_OK = True
IS_WEBSITE_OK = True

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.CustomActivity(
            name="Miaou" # TODO "Miaou | # of online members"
        )
    )
    random_gay_ping.start()
    check_server_status.start()
    await bot.tree.sync()

@bot.hybrid_command(
    name="miaou",
    description="Miaou (ping test)"
)
async def miaou(ctx):
    await ctx.send("Miaou")

@bot.hybrid_command(
    name="gay",
    description="gay"
)
async def gay(ctx: commands.Context, user:discord.User):
    await ctx.send(f"{user.mention if user is not None else '@<1331679752221622345>'} is gay")

def get_url_status_code(url: str):
    try:
        rep = requests.get(url)
        return rep.status_code
    except Exception:
        return None

@tasks.loop(minutes=1)
async def check_server_status():
    global IS_SERVER_OK
    global IS_WEBSITE_OK

    health_check_status_code = get_url_status_code("https://api.miaouvsrg.com/health")
    website_check_status_code = get_url_status_code("https://www.miaouvsrg.com")

    # Because the bot will only run on the MiaouVSRG server, and not on other ones, we know that the first guild is the MiaouVSRG server
    server_ping_role = get(bot.guilds[0].roles, name="server ping")

    if health_check_status_code == 200:
        await bot.get_channel(1441836398494617701).edit(name="Game server : UP")
        if not IS_SERVER_OK:
            await bot.get_channel(1425933813950976229).send(f"{server_ping_role.mention} Game server is now up !")
    elif IS_SERVER_OK and not health_check_status_code:
        await bot.get_channel(1441836398494617701).edit(name="Game server : DOWN")
        await bot.get_channel(1425933813950976229).send(f"{server_ping_role.mention} Game server is down. Skill issue, they say.")

    if website_check_status_code == 200:
        await bot.get_channel(1441836903140954253).edit(name="Website : UP")
        if not IS_WEBSITE_OK:
            await bot.get_channel(1425933813950976229).send(f"{server_ping_role.mention} Website is now up !")
    elif IS_WEBSITE_OK and not website_check_status_code:
        await bot.get_channel(1441836903140954253).edit(name="Website : DOWN")
        await bot.get_channel(1425933813950976229).send(f"{server_ping_role.mention} Website is down. Skill issue, they say.")
    return

@tasks.loop(time=datetime.time(hour=10))
async def random_gay_ping():
    members = bot.guilds[0].members

    random_member = random.choice(members)
    while random_member.global_name.casefold() == "percyqaz".casefold():
        random_member = random.choice(members)

    await bot.get_channel(1359150025988640981).send(f"{random_member.mention} is today's gay cat")
    return


bot.run(DISCORD_BOT_TOKEN)

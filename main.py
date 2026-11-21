import asyncio

from globals import *
import random as r


def has_allowed_role():

  async def predicate(ctx: commands.Context):
    if not ctx.guild:
      return False

                    # DEV ROLE
    allowed_roles = [1459662773767377044]

    role_check = any(role.id in allowed_roles for role in ctx.author.roles)
    return role_check

  return commands.check(predicate)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.CustomActivity(
            name="Miaou"  # TODO "Miaou | # of online members"
        )
    )
    await bot.tree.sync()
    await change_status()


async def change_status():
    guild = bot.get_guild(int(DISCORD_GUILD_ID))

    if guild is None:
        return

    member_count = guild.member_count
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.CustomActivity(
            name=f"Miaou | {member_count} members"  # TODO "Miaou | # of online members"
        )
    )

@bot.event
async def on_member_join(member: discord.Member):
    channel = bot.get_channel(DISCORD_WELCOME_CHANNEL_ID)

    if not channel:
        try:
            channel = await bot.fetch_channel(DISCORD_WELCOME_CHANNEL_ID)
        except discord.HTTPException:
            channel = None

    if channel is not None:
        async with channel.typing():
            await asyncio.sleep(2)
        await channel.send(f"Welcome to Ctrl+Meow Studios {member.mention} ! **Please say 'hi' to get the member role (bot verification)**")

    await change_status()


@bot.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    await change_status()
    if payload.user_id == bot.user.id:
        return

    if payload.message_id == int(DISCORD_ROLE_MESSAGE_ID):

        guild = bot.get_guild(payload.guild_id)
        if guild is None:
            return

        if payload.member is None:
            return

        SNEAK_PEAK_ROLE_ID = 1560787700922191924
        SNEAK_PEAK_REACTION = "👀"

        STATUS_PING_ROLE_ID = 1435294325553500190
        STATUS_PING_REACTION = "💥"

        if payload.emoji.name == SNEAK_PEAK_REACTION:
            role = guild.get_role(SNEAK_PEAK_ROLE_ID)
            if role:
                await payload.member.add_roles(role)

        if payload.emoji.name == STATUS_PING_REACTION:
            role = guild.get_role(STATUS_PING_ROLE_ID)
            if role:
                await payload.member.add_roles(role)


@bot.event
async def on_raw_reaction_remove(payload: discord.RawReactionActionEvent):
    if payload.user_id == bot.user.id:
        return

    if payload.message_id == int(DISCORD_ROLE_MESSAGE_ID):

        guild = bot.get_guild(payload.guild_id)
        if guild is None:
            return

        member = guild.get_member(payload.user_id)
        if member is None:
            return

        SNEAK_PEAK_ROLE_ID = 1560787700922191924
        SNEAK_PEAK_REACTION = "👀"

        STATUS_PING_ROLE_ID = 1435294325553500190
        STATUS_PING_REACTION = "💥"

        if payload.emoji.name == SNEAK_PEAK_REACTION:
            role = guild.get_role(SNEAK_PEAK_ROLE_ID)
            if role:
                await member.remove_roles(role)

        if payload.emoji.name == STATUS_PING_REACTION:
            role = guild.get_role(STATUS_PING_ROLE_ID)
            if role:
                await member.remove_roles(role)


@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return

    if message.guild is None:
        return

    if message.channel.id == int(DISCORD_WELCOME_CHANNEL_ID) and message.content.lower() in ALLOWED_WELCOME_MESSAGES:
        role = message.guild.get_role(MEMBER_ROLE_ID)

        if not role:
            roles = await message.guild.fetch_roles()
            role = discord.utils.get(roles, id=int(MEMBER_ROLE_ID))

        author = message.author
        if author is None:
            return

        if role:
            await message.delete()
            if role not in author.roles:
                await author.add_roles(role)
            await send_welcome_message(author)

    if "<@1358886070108029068>" in message.content:
        RANDOM_EMOTES = {
            "<:chewinggumstare:1543226533458616440>":4.18,
            "<:crevette:1542568392790376639>":3.5,
            "<:crevetteaerodynamic:1542570374586306660>":3.5,
            "<:crevettestare:1542573325908181092>":3.5,
            "<:goobert:1542561406287745124>":4.18,
            "<:horus:1542569595133493338>":4.18,
            "<:horusstare:1542570114128412673>":4.18,
            "<:hubertgamerpro:1542570250737029240>":4.18,
            "<:hubertstare:1542573603885813830>":4.18,
            "<:luffysmug:1542569809949106317>":4.18,
            "<:tetecoussin:1542569344033095680>":3.5,
            "<:wth:1554639064064335963>":0.5,
            "<:moccha:1572669707625168896>":4.18,
            "<:bliksem:1572669756606259256>":4.18,
            "<:angryhorus:1566059318770540604>":4.18,
            "<:bruhhorus:1566888888948232312>":4.18,
            "<:copycatphat:1570655712949043381>":4.18,
            "<:crevettehunt:1568060055968948265>":3.5,
            "<:crevettelaugh:1568060785698021496>":3.5,
            "<:crevettephone:1568060621516443749>":3.5,
            "<:crevettesleepy:1568060977075851304>":3.5,
            "<:crevettesmile:1568059988662947951>":3.5,
            "<:goofypopo:1572670753076412546>":4.18,
            "<:loading:1566887589930074254>":4.18,
            "<:lucifer:1572669640642007121>":4.18,
            "<a:o2mo:1570658748979216445>":0.5,
            "<:boboxcat:1570657005524488232>":0.5,
            "<:wollekeZzz:1572669795122413578>":4.18,
            "<:what:1570656541030228088>":0.5
        }

        emotes=list(RANDOM_EMOTES.keys())
        probabilities=list(RANDOM_EMOTES.values())




        emote = r.choices(emotes, weights=probabilities, k=1)[0]
        await message.channel.send(emote)

    await bot.process_commands(message)


async def send_welcome_message(author: discord.Member):
    RANDOM_EMOTES = {
            "<:chewinggumstare:1543226533458616440>":4.18,
            "<:crevette:1542568392790376639>":3.5,
            "<:crevetteaerodynamic:1542570374586306660>":3.5,
            "<:crevettestare:1542573325908181092>":3.5,
            "<:goobert:1542561406287745124>":4.18,
            "<:horus:1542569595133493338>":4.18,
            "<:horusstare:1542570114128412673>":4.18,
            "<:hubertgamerpro:1542570250737029240>":4.18,
            "<:hubertstare:1542573603885813830>":4.18,
            "<:luffysmug:1542569809949106317>":4.18,
            "<:tetecoussin:1542569344033095680>":3.5,
            "<:wth:1554639064064335963>":0.5,
            "<:moccha:1572669707625168896>":4.18,
            "<:bliksem:1572669756606259256>":4.18,
            "<:angryhorus:1566059318770540604>":4.18,
            "<:bruhhorus:1566888888948232312>":4.18,
            "<:copycatphat:1570655712949043381>":4.18,
            "<:crevettehunt:1568060055968948265>":3.5,
            "<:crevettelaugh:1568060785698021496>":3.5,
            "<:crevettephone:1568060621516443749>":3.5,
            "<:crevettesleepy:1568060977075851304>":3.5,
            "<:crevettesmile:1568059988662947951>":3.5,
            "<:goofypopo:1572670753076412546>":4.18,
            "<:loading:1566887589930074254>":4.18,
            "<:lucifer:1572669640642007121>":4.18,
            "<a:o2mo:1570658748979216445>":0.5,
            "<:boboxcat:1570657005524488232>":0.5,
            "<:wollekeZzz:1572669795122413578>":4.18,
            "<:what:1570656541030228088>":0.5
        }

    emotes = list(RANDOM_EMOTES.keys())
    probabilities = list(RANDOM_EMOTES.values())

    emote = r.choices(emotes, weights=probabilities, k=1)[0]

    channel = bot.get_channel(DISCORD_GENERAL_CHANNEL_ID)
    if not channel:
        try:
            channel = await bot.fetch_channel(DISCORD_GENERAL_CHANNEL_ID)
        except discord.HTTPException:
            channel = None

    if channel:
        await channel.send(f"Welcome {author.mention} !\n"
                       f"The game is currently in active development, and will soon have a playtest : https://discord.com/channels/1359150025363554497/1359151600052207757/1555536674883371039\n"
                       f"Do not hesitate to get your roles in <#1560779411010228224> ! {emote} ")


@bot.hybrid_command(
    name="test_member_join",
    description="Tests member join"
)
@has_allowed_role()
async def test_member_join(ctx, member: discord.Member):
    await ctx.defer(ephemeral=True)
    await on_member_join(member)
    await ctx.send("Test started.")


@bot.hybrid_command(
    name="playtest",
    description="Please read peep's welcome message"
)
async def playtest(ctx):
    await ctx.defer(ephemeral=False)
    await ctx.send("hi, we will release playtest applications when the game will be polished enough. Please check https://discord.com/channels/1359150025363554497/1359151600052207757/1555536674883371039")


@bot.hybrid_command(
    name="miaou",
    description="Miaou (ping test)"
)
async def miaou(ctx):
    await ctx.send("Miaou")


@bot.hybrid_command(
    name="sync",
    description="Syncs guild commands"
)
@has_allowed_role()
async def sync(ctx):
    await ctx.defer(ephemeral=True)
    await bot.tree.sync()
    await ctx.send("Synced")


bot.run(DISCORD_BOT_TOKEN)
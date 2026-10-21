from globals import *
import random as r


def has_allowed_role():

  async def predicate(ctx: commands.Context):
    if not ctx.guild:
      return False

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

    if message.channel.id == int(DISCORD_WELCOME_CHANNEL_ID) and message.content in ALLOWED_WELCOME_MESSAGES:
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
        RANDOM_EMOTES = [
            "<:chewinggumstare:1543226533458616440>",
            "<:crevette:1542568392790376639>",
            "<:crevetteaerodynamic:1542570374586306660>",
            "<:crevettestare:1542573325908181092>",
            "<:goobert:1542561406287745124>",
            "<:horus:1542569595133493338>",
            "<:horusstare:1542570114128412673>",
            "<:hubertgamerpro:1542570250737029240>",
            "<:hubertstare:1542573603885813830>",
            "<:luffysmug:1542569809949106317>",
            "<:tetecoussin:1542569344033095680>",
            "<:wth:1554639064064335963>"
        ]
        emote = r.choice(RANDOM_EMOTES)
        await message.channel.send(emote)

    await bot.process_commands(message)


async def send_welcome_message(author: discord.Member):
    RANDOM_EMOTES = [
        "<:chewinggumstare:1543226533458616440>",
        "<:crevette:1542568392790376639>",
        "<:crevetteaerodynamic:1542570374586306660>",
        "<:crevettestare:1542573325908181092>",
        "<:goobert:1542561406287745124>",
        "<:horus:1542569595133493338>",
        "<:horusstare:1542570114128412673>",
        "<:hubertgamerpro:1542570250737029240>",
        "<:hubertstare:1542573603885813830>",
        "<:luffysmug:1542569809949106317>",
        "<:tetecoussin:1542569344033095680>",
        "<:wth:1554639064064335963>"
    ]
    emote = r.choice(RANDOM_EMOTES)
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
@has_allowed_role()
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

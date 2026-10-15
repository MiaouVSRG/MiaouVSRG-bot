from globals import *


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

        if role:
            await message.delete()
            if role not in author.roles:
                await author.add_roles(role)

    await bot.process_commands(message)


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

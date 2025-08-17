from globals import *

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.CustomActivity(
            name="Miaou" # TODO "Miaou | # of online members"
        )
    )

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
    await ctx.send(f"{user.mention if user is not None else "@<1331679752221622345>"} is gay")


bot.run(DISCORD_BOT_TOKEN)

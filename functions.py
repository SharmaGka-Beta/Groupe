import discord
from discord.ext import commands
import database

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix = "sin ", intents = intents)

@bot.event
async def on_ready():
    print("Bot is ready")

@bot.command()
async def init(ctx):
    
    channel_exists = discord.utils.get(ctx.guild.channels, name = 'sin-city')

    if channel_exists:
        await ctx.send("Already Initialized")
        return
    
    await ctx.guild.create_text_channel("Sin City")

    database.create_tables()

    await ctx.send("Initialized")

@bot.command()
async def profile(ctx):
    info = db.get_user(ctx.author.id)
    embed = discord.Embed(title="Welcome to Sin City!", color= discord.Color.brand_red())

    embed.set_thumbnail(url=ctx.author.avatar.url)
    embed.add_field(name="\u200b", value="PLAYER INFO", inline=True)
    embed.add_field(name="\u200b", value=f"👤 Player Name: {ctx.author.name}", inline=False)
    embed.add_field(name="\u200b", value=f"🪙 Balance: {info["coins"]}", inline=False)
    embed.add_field(name="\u200b", value=f"🆙 Level: {info["level"]}", inline=False)


    embed.add_field(name="\ub200", value=f"🔥 WANTED METER: {info["wanted"]}", inline=False)
    embed.add_field(name="\ub200", value=f"📈 RESPECT METER: {info["respect"]}", inline=True)
    embed.add_field(name="\ub200", value=f"🪪 ROLE: {info["user_role"]}", inline=True)

    await ctx.send(embed=embed)

    
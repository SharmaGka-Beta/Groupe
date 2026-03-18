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
async def inventory(ctx):
    

    uid = ctx.authour.id
    inventory = database.get_inventory(uid)
    
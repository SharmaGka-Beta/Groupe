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
    info = database.get_user(ctx.author.id)
    embed = discord.Embed(title="Welcome to Sin City!", color= discord.Color.brand_red())

    embed.set_thumbnail(url=ctx.author.display_avatar.url)
    embed.add_field(name="\u200b", value="PLAYER INFO", inline=True)
    embed.add_field(name="\u200b", value=f"👤 Player Name: {ctx.author.name}", inline=False)
    embed.add_field(name="\u200b", value=f"🪙 Balance: {info["money"]}", inline=False)
    # embed.add_field(name="\u200b", value=f"🆙 Level: {info["level"]}", inline=False)


    embed.add_field(name="\ub200", value=f"🔥 WANTED METER: {info["wanted"]}", inline=False)
    embed.add_field(name="\ub200", value=f"📈 RESPECT METER: {info["integrity"]}", inline=False)
    embed.add_field(name="\ub200", value=f"🪪 ROLE: {info["user_role"]}", inline=False)

    await ctx.send(embed=embed)

    
@bot.command()
async def inventory(ctx):

    database.add_user(ctx.author.id)
    inven = database.get_inventory(ctx.author.id)
    embed = discord.Embed(title = "Inventory", color = discord.Color.brand_red())

    embed.set_thumbnail(url = ctx.author.display_avatar.url)
    value_g = '\n'.join(f"{m[0]}: {m[1]}" for m in inven[0])
    value_d = '\n'.join(f"{m[0]}: {m[1]}" for m in inven[1])
    value_i = '\n'.join(f"{m[0]}: {m[1]}" for m in inven[2])

    embed.add_field(name = "Guns", value = value_g or "You currently own no guns", inline = False)
    embed.add_field(name = "Drugs", value = value_d or "You currently own no drugs", inline = False)
    embed.add_field(name = "Items", value = value_i or "You currently own no items", inline = False)

    await ctx.send(embed = embed)
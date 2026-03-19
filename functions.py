import discord
from discord.ext import commands
import database
import random

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

# RED_NUMBERS = {1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36}
# BLACK_NUMBERS = {2,4,6,8,10,11,13,15,17,20,22,24,26,28,29,31,33,35}

@bot.command()
async def roulette(ctx, amount: int , bet_type:str):
    bet_type=bet_type.lower()
    # user_id=ctx.author.id
    
    if amount<=0:
        await ctx.send("Bet must be greater than zero")
        return

    valid_colours=["red","black"]
    valid_numbers=[str(i) for i in range(1,37)]

    if bet_type not in valid_colours and bet_type not in valid_numbers:
        await ctx.send("Invalid bet!: Enter a colour (red/black) or number (1 to 36)")
        return 
    
    
    
    if bet_type in valid_numbers:
        result=random.randint(1,36)
        if result==bet_type:
            await ctx.send("Congratulation! You won ")
            # profit=amount*35
        else:
            await ctx.send("You lost")
            # profit=-amount
        

    else:
        result=random.choice(valid_colours)
        if result==bet_type:
            await ctx.send("Congratulation! You won")
            # profit=amount*2
        else:
            await ctx.send("You lost")
            # profit=-amount
    
    


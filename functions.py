import discord
from discord.ext import commands
import database
import random
import messages

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


    embed.add_field(name="\u200b", value=f"🔥 WANTED METER: {info["wanted"]}", inline=False)
    embed.add_field(name="\u200b", value=f"📈 RESPECT METER: {info["integrity"]}", inline=False)
    embed.add_field(name="\u200b", value=f"🪪 ROLE: {info["user_role"]}", inline=False)

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

@bot.command()
async def shop(ctx):
    info = database.get_user(ctx.author.id)
    pages = [
        {
            "title": "GUNS",
            "items": [
                ("🔫 Pistol", "100", "A basic handgun"),
                ("⚔️ Assault Rifle", "500", "Fully automatic rifle"),
                ("🔱 Machine Gun", "1200", "Sprays bullets fast"),
                ("🎯 Sniper", "2000", "One shot, one kill"),
            ]
        },
        {
            "title": "DRUGS",
            "items": [
                ("🌿 Weed", "50", "Mild and cheap"),
                ("💊 Meth", "300", "High risk high reward"),
                ("💉 Heroin", "400", "Dangerous stuff"),
                ("❄️ Cocaine", "600", "The classic"),
                ("🔵 LSD", "250", "Trippy"),
                ("🥶 Blue Meth", "1000", "Say my name"),
            ]
        }
    ]

    embed = discord.Embed(title = "SHOP", color = discord.Color.brand_red())
    
    embed.add_field(name="Welcome to Sin City Shop! Buy any item with 'sin buy'", value = "\u200b" ,inline=False)

    for dic in pages:
        for name, price, desc in dic["items"]:
            embed.add_field(name = f"__{name}__ | 🪙 {price}" , value=desc, inline=False)

    await ctx.send(embed = embed)
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
    
@bot.command()
async def work(ctx):
    info = database.add_user(ctx.author.id)
    a = random.randint(1, 100)
    money = random.randint(50, 150)
    if 1 <= a <= 89:
        mes = random.choice(messages.workp)
        await ctx.send(f"{mes} You gained {money} coins.")
        database.add_money(ctx.author.id, money)

    elif 90 <= a <= 100:
        mes = random.choice(messages.workn)
        await ctx.send(f"{mes} You lost {money} coins.")
        database.remove_money(ctx.author.id, money)




class view(discord.ui.View):
    
    @discord.ui.button(label="Hit", style = discord.ButtonStyle.primary)
    async def button_callback(self, interaction: discord.Interaction, button: discord.ui.Button,):
        await interaction.response.send_message("Hit")

    @discord.ui.button(label="Stand", style = discord.ButtonStyle.primary)
    async def button_callback(self, interaction: discord.Interaction, button: discord.ui.Button,):
        await interaction.response.send_message("Stand")

    
        
        
@bot.command()
async def blackjack(ctx, arg: int):

    info = database.get_user(ctx.author.id)
    if (arg <= 0):
        await ctx.send("Bet must be greater than zero")
        return

    if (arg > info["money"]):
        await ctx.send("Insufficient Balance")

    round_deck = messages.deck[:]
    random.shuffle(round_deck)
    database.remove_money(ctx.author.id, arg)

    print(round_deck.pop())
    
    embed = discord.Embed()
    a = round_deck.pop()
    embed.add_field(name = "Dealer Cards", value = f'{a[0]}{a[1]}  ??')
    b, c = round_deck.pop(), round_deck.pop()
    embed.add_field(name="Your Cards", value=f'{b[0]}{b[1]}  {c[0]}{c[1]}')

    await ctx.send(embed=embed, view=view())



    


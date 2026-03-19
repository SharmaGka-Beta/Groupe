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
    database.create_tables()


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


@bot.command()
async def roulette(ctx, amount: int , bet_type:str):
    user_id=ctx.author.id
    d=database.get_user(user_id)
    bet_type=bet_type.lower()
    
    if amount<=0:
        await ctx.send("Bet must be greater than zero")
        return
    
    if(d["money"]<amount):
        await ctx.send("Insufficient balance")
        return
    

    valid_colours=["red","black"]
    valid_numbers=[str(i) for i in range(1,37)]

    if bet_type not in valid_colours and bet_type not in valid_numbers:
        await ctx.send("Invalid bet!: Enter a colour (red/black) or number (1 to 36)")
        return 
    
    
    
    if bet_type in valid_numbers:
        result=random.randint(1,36)
        if result==int(bet_type):
            await ctx.send(f'Congratulation! It is {result} You won {35*amount} on your current balance')
            database.remove_money(user_id,amount)
            database.add_money(user_id,35*amount)
        else:
            await ctx.send(f'Alas! It is {result} You lost {amount} on your current balance')
            database.remove_money(user_id,amount)
        

    else:
        result=random.choice(valid_colours)
        if result==bet_type:
            await ctx.send(f'Congratulation! It is {result} You won {2*amount} on your current balance')
            database.remove_money(user_id,amount)
            database.add_money(user_id,2*amount)
        else:
            await ctx.send(f'Alas! It is {result} You lost {amount} on your current balance')
            database.remove_money(user_id,amount)



@bot.command()
async def transfer(ctx, amount:int , member:discord.Member):
    payer=ctx.author.id
    receiver=member.id
    database.add_money(receiver,amount)
    database.remove_money(payer,amount)

    await ctx.send(f'{amount} has been sent to {member.display_name}')




    
    


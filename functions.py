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
    database.create_tables()

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("I don't recognize that command. Type 'sin help' to view all commands")
    elif isinstance(error, commands.UserInputError):
        await ctx.send("Your command format is incorrect. Type 'sin help' to view the command formats.")


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


class shop_view(discord.ui.View):
    

    @discord.ui.button(label="Guns", style = discord.ButtonStyle.primary)
    async def gun_callback(self, interaction: discord.Interaction, button: discord.ui.Button,):

        embed = discord.Embed(title = "GUN SHOP", color = discord.Color.brand_red())
    
        embed.add_field(name="Welcome to Sin City Gun Shop! Buy any item with 'sin buy'", value = "\u200b" ,inline=False)

        for item in messages.items_gun:
            embed.add_field(name = f"__{item[0]}__ | 🪙 {item[1]}" , value=item[2], inline=False)

        await interaction.response.edit_message(embed = embed, view = shop_view())

        

    @discord.ui.button(label="Drugs", style = discord.ButtonStyle.primary)
    async def drugs_callback(self, interaction: discord.Interaction, button: discord.ui.Button,):

        embed = discord.Embed(title = "DRUG SHOP", color = discord.Color.brand_red())
    
        embed.add_field(name="Welcome to Sin City Drug Shop! Buy any item with 'sin buy'", value = "\u200b" ,inline=False)

        for item in messages.items_drugs:
            embed.add_field(name = f"__{item[0]}__ | 🪙 {item[1]}" , value=item[2], inline=False)

        await interaction.response.edit_message(embed = embed, view = shop_view())

    @discord.ui.button(label="Items", style = discord.ButtonStyle.primary)
    async def items_callback(self, interaction: discord.Interaction, button: discord.ui.Button,):

        embed = discord.Embed(title = "ITEM SHOP", color = discord.Color.brand_red())
    
        embed.add_field(name="Welcome to Sin City Item Shop! Buy any item with 'sin buy'", value = "\u200b" ,inline=False)

        for item in messages.items_items:
            embed.add_field(name = f"__{item[0]}__ | 🪙 {item[1]}" , value=item[2], inline=False)

        await interaction.response.edit_message(embed = embed, view = shop_view())


@bot.command()
async def shop(ctx):
    database.add_user(ctx.author.id)
    
    embed = discord.Embed(title = "GUN SHOP", color = discord.Color.brand_red())
    
    embed.add_field(name="Welcome to Sin City Gun Shop! Buy any item with 'sin buy'", value = "\u200b" ,inline=False)

    for item in messages.items_gun:
        embed.add_field(name = f"__{item[0]}__ | 🪙 {item[1]}" , value=item[2], inline=False)

    await ctx.send(embed = embed, view = shop_view())


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
    info = database.get_user(ctx.author.id)
    if info["money"] < amount:
        await ctx.send("You don't have the required funds")

    payer=ctx.author.id
    receiver=member.id
    database.add_money(receiver,amount)
    database.remove_money(payer,amount)

    await ctx.send(f'{amount} has been sent to {member.display_name}')
    
@bot.command()
async def work(ctx):
    info = database.get_user(ctx.author.id)

    if info["user_role"] != 'civilian':
        await ctx.send("Why would you still want to go to your puny day job")
        return

    
    a = random.randint(1, 100)
    money = random.randint(20, 50)
    if 1 <= a <= 89:
        mes = random.choice(messages.workp)
        await ctx.send(mes)
        await ctx.send(f" You gained {money} coins.")
        database.add_money(ctx.author.id, money)

    elif 90 <= a <= 100:
        mes = random.choice(messages.workn)
        await ctx.send(mes)
        await ctx.send(f"You lost {money} coins.")
        database.remove_money(ctx.author.id, money)

@bot.command()
async def buy(ctx, item, qty:int = 1):
    info = database.get_user(ctx.author.id)

    item = item.lower()

    if(qty <= 0):
        await ctx.send("Enter a valid quantity of items!")
        return
    for it in messages.items:
        if(item == it[0][2:].lower()):
            if(qty*int(it[1]) > info["money"]):
                await ctx.send("Balance Insufficient!")
                return
            database.update_inventory(ctx.author.id, it[0][2:], it[3], qty)
            database.remove_money(ctx.author.id, qty*int(it[1]))
            if qty == 1:
                await ctx.send(f"{qty} {item} bough successfully!")
            elif qty > 1:
                await ctx.send(f"{qty} {item} bough successfully!")
            return

    await ctx.send("Enter a valid item name!")
def blackjack_value(cards):

    value = 0
    aces = 0
    for i in cards:
        if i[0] == 1:
            aces += 1
            continue
        if i[0] >= 10:
            value += 10
            continue
        value += i[0]
    
    for i in range(aces):
        if (value+11) <= 21:
            value += 11
            continue
        value+=1

    return value



class view(discord.ui.View):

    def __init__(self, ctx, arg):
        super().__init__()
        self.ctx = ctx
        self.arg = arg
    
    @discord.ui.button(label="Hit", style = discord.ButtonStyle.primary)
    async def hit_callback(self, interaction: discord.Interaction, button: discord.ui.Button,):
        
        await interaction.response.defer()

        if blackjack_value(blackjack_cards[self.ctx.author.id]["player"]) == 21:
            await self.ctx.send("The total is already 21.")
            return
        
        round_deck = messages.deck[:]
        random.shuffle(round_deck)

        a = round_deck.pop()
        while a in blackjack_cards[self.ctx.author.id]["player"] and a in blackjack_cards[self.ctx.author.id]["dealer"]:
            a = round_deck.pop()

        blackjack_cards[self.ctx.author.id]["player"].append(a)

        embed = discord.Embed()

        embed.add_field(name = "Dealer Cards", value = f'{messages.special_cards[blackjack_cards[self.ctx.author.id]["dealer"][0][0]]}{blackjack_cards[self.ctx.author.id]["dealer"][0][1]}  ??')
        embed.add_field(name="Your Cards", value=" ".join(f'{messages.special_cards[b[0]]}{b[1]}  ' for b in blackjack_cards[self.ctx.author.id]["player"]))
        embed.add_field(name="\u200b", value="\u200b")
        embed.add_field(name = "Dealer Total", value = blackjack_value(blackjack_cards[self.ctx.author.id]["dealer"]))
        embed.add_field(name = "Your Total", value = blackjack_value(blackjack_cards[self.ctx.author.id]["player"]))
        embed.add_field(name="\u200b", value="\u200b")
        

        if blackjack_value(blackjack_cards[self.ctx.author.id]["player"]) > 21:
            await self.ctx.send(embed = embed)
            await self.ctx.send("BUST!!")
            blackjack_cards.pop(self.ctx.author.id)
            return
        
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view=self)
        
        await self.ctx.send(embed=embed, view=view(self.ctx, self.arg))

        


    @discord.ui.button(label="Stand", style = discord.ButtonStyle.primary)
    async def stand_callback(self, interaction: discord.Interaction, button: discord.ui.Button,):
        await interaction.response.defer()

        round_deck = messages.deck[:]
        random.shuffle(round_deck)

        while True:
            d = round_deck.pop()
            while d in blackjack_cards[self.ctx.author.id]["player"] and d in blackjack_cards[self.ctx.author.id]["dealer"]:
                d = round_deck.pop()

            blackjack_cards[self.ctx.author.id]["dealer"].append(d)
            if blackjack_value(blackjack_cards[self.ctx.author.id]["dealer"]) >= 17:
                break

        embed = discord.Embed()

        embed.add_field(name = "Dealer Cards", value = " ".join(f'{messages.special_cards[b[0]]}{b[1]}  ' for b in blackjack_cards[self.ctx.author.id]["dealer"]))
        embed.add_field(name="Your Cards", value=" ".join(f'{messages.special_cards[b[0]]}{b[1]}  ' for b in blackjack_cards[self.ctx.author.id]["player"]))
        embed.add_field(name="\u200b", value="\u200b")
        embed.add_field(name = "Dealer Total", value = blackjack_value(blackjack_cards[self.ctx.author.id]["dealer"]))
        embed.add_field(name = "Your Total", value = blackjack_value(blackjack_cards[self.ctx.author.id]["player"]))
        embed.add_field(name="\u200b", value="\u200b")

        await self.ctx.send(embed=embed)

        dealer_total = blackjack_value(blackjack_cards[self.ctx.author.id]["dealer"])
        player_total = blackjack_value(blackjack_cards[self.ctx.author.id]["player"])

        if dealer_total > 21:
            await self.ctx.send(f"Dealer Busted!! You won {2*self.arg} coins")
            database.add_money(self.ctx.author.id, 2*self.arg)
            return
        
        elif player_total > dealer_total:
            await self.ctx.send(f"WIN!! You won {2*self.arg} coins")
            database.add_money(self.ctx.author.id, 2*self.arg)
        
        elif dealer_total == player_total:
            await self.ctx.send(f"Tie. You evened out winning {self.arg} coins")
            database.add_money(self.ctx.author.id, self.arg)
            
        
        elif dealer_total > player_total:
            await self.ctx.send("You Lost!!")
            
        
        blackjack_cards.pop(self.ctx.author.id)

    
blackjack_cards = {}      
# {userid: {player: [], dealer: []}}  

        
@bot.command()
async def blackjack(ctx, arg: int):

    if ctx.author.id in blackjack_cards.keys():
        await ctx.send("You have an ongoing game!")
        return

    info = database.get_user(ctx.author.id)
    if (arg <= 0):
        await ctx.send("Bet must be greater than zero")
        return

    if (arg > info["money"]):
        await ctx.send("Insufficient Balance")
        return

    round_deck = messages.deck[:]
    random.shuffle(round_deck)
    database.remove_money(ctx.author.id, arg)
    await ctx.send(f"-{arg} coins")

    
    embed = discord.Embed()
    a = round_deck.pop()
    b, c = round_deck.pop(), round_deck.pop()
    blackjack_cards[ctx.author.id] = {"player": [b, c], "dealer": [a]}

    embed.add_field(name = "Dealer Cards", value = f'{messages.special_cards[a[0]]}{a[1]}  ??')
    embed.add_field(name="Your Cards", value=f'{messages.special_cards[b[0]]}{b[1]}  {messages.special_cards[c[0]]}{c[1]}')
    embed.add_field(name="\u200b", value="\u200b")
    embed.add_field(name = "Dealer Total", value = blackjack_value(blackjack_cards[ctx.author.id]["dealer"]))
    embed.add_field(name = "Your Total", value = blackjack_value(blackjack_cards[ctx.author.id]["player"]))
    embed.add_field(name="\u200b", value="\u200b")

    if blackjack_value(blackjack_cards[ctx.author.id]["player"]) == 21:
        await ctx.send(embed = embed)
        await ctx.send(f"BLACKJACK!!! You won {int(2.5*arg)} coins")
        database.add_money(ctx.author.id, int(2.5*arg))
        blackjack_cards.pop(ctx.author.id)
        return


    await ctx.send(embed=embed, view=view(ctx, arg))



    


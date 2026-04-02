import discord
from functions import bot
import database
import random
import messages

@bot.command()
async def roulette(ctx, amount: int , bet_type:str):
    user_id=ctx.author.id
    d=database.get_user(user_id)

    if d["jail"] == 1:
        await ctx.send("You are a convict! Get out of jail first!!")
        return
    
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
    
    database.remove_money(user_id,amount)
    if bet_type in valid_numbers:
        result=random.randint(1,36)
        if result==int(bet_type):
            await ctx.send(f'Congratulation! It is {result}! You won!!')
            await ctx.send(f'+{36*amount} coins')
            database.add_money(user_id,36*amount)
        else:
            await ctx.send(f'Alas! It is {result}. You lost.')
        

    else:
        result=random.choice(valid_colours)
        if result==bet_type:
            await ctx.send(f'Congratulation! It is {result}! You won!!')
            await ctx.send(f'+{2*amount} coins')
            database.add_money(user_id,2*amount)
        else:
            await ctx.send(f'Alas! It is {result}. You lost.')


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

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("Not your game!", ephemeral = True)
            return False
        return True
    
    @discord.ui.button(label="Hit", style = discord.ButtonStyle.primary)
    async def hit_callback(self, interaction: discord.Interaction, button: discord.ui.Button,):
        
        await interaction.response.defer()

        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view=self)

        if blackjack_value(blackjack_cards[self.ctx.author.id]["player"]) == 21:
            await self.ctx.send("The total is already 21.")
            return
        
        round_deck = messages.deck[:]
        random.shuffle(round_deck)

        a = round_deck.pop()
        while a in blackjack_cards[self.ctx.author.id]["player"] or a in blackjack_cards[self.ctx.author.id]["dealer"]:
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
        
        
        await self.ctx.send(embed=embed, view=view(self.ctx, self.arg))

        


    @discord.ui.button(label="Stand", style = discord.ButtonStyle.primary)
    async def stand_callback(self, interaction: discord.Interaction, button: discord.ui.Button,):
        await interaction.response.defer()

        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view=self)

        round_deck = messages.deck[:]
        random.shuffle(round_deck)

        while True:
            d = round_deck.pop()
            while d in blackjack_cards[self.ctx.author.id]["player"] or d in blackjack_cards[self.ctx.author.id]["dealer"]:
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

    info = database.get_user(ctx.author.id)
    if info["jail"] == 1:
        await ctx.send("You are a convict! Get out of jail first!!")
        return
    

    if ctx.author.id in blackjack_cards.keys():
        await ctx.send("You have an ongoing game!")
        return

    if (arg <= 0):
        await ctx.send("Bet must be greater than zero")
        return

    if (arg > info["money"]):
        await ctx.send("Insufficient Balance")
        return

    round_deck = messages.deck[:]
    random.shuffle(round_deck)
    
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

@bot.command()
async def slots(ctx, arg: int):
    info = database.get_user(ctx.author.id)
    money = info["money"]
    if(info["jail"]):
        await ctx.send("You are a convict! Get out of jail first!!")
        return
    if(arg > money):
        await ctx.send("Can't bet more than you have buddy.")
        return
    if(arg <= 0):
        await ctx.send("Good try, how about you put this energy into a job")
        return

    symbols = messages.slots_symbols
    weights = messages.slots_weights
    payouts = messages.slots_payouts

    reel = random.choices(symbols, weights, k=3)
    
    response = ""
    if(reel[0] == reel[1] == reel[2]):
        response = f"**JACKPOT!!! YOU WON {arg*payouts[reel[0]]} COINS!**"
        database.add_money(ctx.author.id, arg*payouts[reel[0]])

    elif(reel[0] == reel[1] or reel[1] == reel[2]):
        response = f"Close.... You won {arg} coins"
        database.add_money(ctx.author.id, arg)

    else:
        response = f"You lost {arg} coins"
        database.remove_money(ctx.author.id, arg)
    
    embed = discord.Embed(
    description=(
        f"◖{reel[0]}{reel[1]}{reel[2]}◗\n"
        f"{response}"
    ),
    color=discord.Color.gold()
)

    embed.set_author(name=f"{ctx.author.name}'s slots", icon_url=ctx.author.avatar.url)
    #embed.add_field(name="\u200b", value=f"\n◖{reel[0]}{reel[1]}{reel[2]}◗\n{response}")
    await ctx.send(embed=embed)
    
    


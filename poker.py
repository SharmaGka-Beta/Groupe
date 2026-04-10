from functions import bot
import messages
import random
import discord

game = {"all": [], "current": []}

small_p = 0
pot = 0

@bot.command()
async def poker(ctx):
    game["all"].append(ctx.author)
    await ctx.send(f"Added {ctx.author} to the game")

@bot.command()
async def run_r(ctx):

    for i in game["all"]:
        if i not in game["current"]:
            game["current"].append(i)

    if (len(game["current"]) < 2):
        await ctx.send("Need atleast 2 players!")
        game["current"].clear()
        return
    
    await round(ctx)

class pokerView(discord.ui.View):

    def __init__(self, ctx):
        super().__init__(timeout=20)
        self.ctx = ctx
    
    @discord.ui.button(label="Call", style = discord.ButtonStyle.primary,)
    async def accept_callback(self, interaction: discord.Interaction, button: discord.ui.Button,):
        pass



async def bet_round():

    players = game["current"][:]
    for i in game["current"]:

        embed = discord.Embed()
        embed.add_field(name = "Current Pot", value = pot)
        



async def round(ctx):

    round_deck = messages.deck[:]
    random.shuffle(round_deck)

    for i in game["current"]:
        card1 = round_deck.pop()
        card2 = round_deck.pop()

        embed = discord.Embed()

        embed.add_field(name = "Your Hand: ", value = f'{messages.special_cards[card1[0]]}{card1[1]}  {messages.special_cards[card2[0]]}{card2[1]}')

        try:
            await i.send(embed = embed)
        except:
            await ctx.send(f"Couldn't DM {i}")

    

from functions import bot
import messages
import random
import discord
import database

game = {}
#uid : {all = [], current = [], small, start, bet, pot}

class startView(discord.ui.View):

    def __init__(self, host, ctx):
        super().__init__()
        self.host = host
        self.ctx = ctx

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.host.id:
            await interaction.response.send_message("Not your game!", ephemeral = True)
            return False
        return True
    
    @discord.ui.button(label="Start", style = discord.ButtonStyle.primary)
    async def start_callback(self, interaction: discord.Interaction, button: discord.ui.Button,):

        await interaction.response.defer()

        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view=self)

        await self.ctx.send(f"{self.host.mention} has started the game")
        game["start"] = True
        await runr(self.ctx, self.host)
    
    @discord.ui.button(label="Wait", style = discord.ButtonStyle.primary)
    async def wait_callback(self, interaction: discord.Interaction, button: discord.ui.Button,):

        await interaction.response.defer()

        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view=self)

        await self.host.send("Waiting for more players")


@bot.command()
async def poker(ctx, member: discord.Member, s: int = None):

    if (member == ctx.author):
        if ctx.author.id not in game:
            if (s == None):
                await ctx.send("Please give a small blind amount")
                return
            
            try:
                await member.send("Test message")
            except discord.Forbidden:
                await ctx.send("Turn on your DMs to play poker!")
                return
            
            game[ctx.author.id] = {"all": [], "current": [], "small": s, "start": False, "bet": 0, "pot": 0}
            game[ctx.author.id]["all"].append(ctx.author)
            await ctx.send("Game Created!")
        else:
            await ctx.send("Your game already exists!")
        return

    if (member.id not in game):
        await ctx.send("This game doesn't exist!")
        return
    
    if (ctx.author not in game[member.id]["all"]):

        try:
            await ctx.author.send("Test message")
        except discord.Forbidden:
            await ctx.send("Turn on your DMs to play poker!")
            return
        
        game[member.id]["all"].append(ctx.author)
        await ctx.send(f"{ctx.author.mention} joined {member.mention}'s game")
        if (game["start"]):
            await ctx.author.send("There is an ongoing game. You can join from the next round.")
        
        num = len(game[member.id]["all"])
        if (num >= 2 and (not game["start"])):
            embed = discord.Embed()
            embed.add_field(name = f"There are {num} players in the lobby. Start Game?", value = "\u200b")
            await ctx.author.send(embed = embed, view = startView(member, ctx))

    else:
        await ctx.send("You are already in the game!")


async def runr(ctx, host):

    for i in game[host.id]["all"]:
        if i not in game[host.id]["current"]:
            game[host.id]["current"].append(i)

    if (len(game[host.id]["current"]) < 2):
        await ctx.send("Need atleast 2 players!")
        game[host.id]["current"].clear()
        return
    
    await round(ctx, host)


async def round(ctx, host):

    round_deck = messages.deck[:]
    random.shuffle(round_deck)

    for i in range(len(game[host.id]["current"])):
        card1 = round_deck.pop()
        card2 = round_deck.pop()

        embed = discord.Embed()

        embed.add_field(name = "Your Hand: ", value = f'{messages.special_cards[card1[0]]}{card1[1]}  {messages.special_cards[card2[0]]}{card2[1]}')

        await game[host.id]["current"][i].send(embed = embed)
        if (i == 0):
            game[host.id]["current"][i].send("You are the small blind.")
        elif (i == 0):
            game[host.id]["current"][i].send("You are the big blind.")


async def pre_flop(ctx, host, players):

    for i in range(players):

        player = game[host.id]["current"][i]
        if i == 0:
            await ctx.send(f"{player.mention} has bet {game["small"]} coins.")
            database.remove_money(player.id, game["small"])
            continue

        elif i == 1:
            await ctx.send(f"{player.mention} has bet {2*game["small"]} coins.")
            game["bet"] = game["small"]*2
            database.remove_money(player.id, 2*game["small"])
            continue

        
async def bet(host):

    embed = discord.Embed()
    embed.add_field(name = f"Pot - {game[host.id]["pot"]}", value = "\u200b", inline = False)
    embed.add_field(name = f"Bet - {game[host.id]["bet"]}", value = "\u200b", inline = False)

class betView(discord.ui.View):

    pass

            


    

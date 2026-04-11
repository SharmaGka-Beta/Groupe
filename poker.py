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
        game[self.host.id]["start"] = True
        await runr(self.ctx, self.host)
    
    @discord.ui.button(label="Wait", style = discord.ButtonStyle.primary)
    async def wait_callback(self, interaction: discord.Interaction, button: discord.ui.Button,):

        await interaction.response.defer()

        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view=self)

        await self.host.send("Waiting for more players")

class inviteView(discord.ui.View):

    def __init__(self, ctx):
        super().__init__()
        self.ctx = ctx
        

@bot.command()
async def poker(ctx, s: int, *members: discord.Member):

    if (ctx.author in game):
        await ctx.send("You have an ongoing game!")

    for member in members:

        embed = discord.embed()

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
            #current will store a list of [player name, bet, folded/not folded]
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
        if (game[member.id]["start"]):
            await ctx.author.send("There is an ongoing game. You can join from the next round.")
        
        num = len(game[member.id]["all"])
        if (num >= 2 and (not game[member.id]["start"])):
            embed = discord.Embed()
            embed.add_field(name = f"There are {num} players in the lobby. Start Game?", value = "\u200b")
            await member.send(embed = embed, view = startView(member, ctx))

    else:
        await ctx.send("You are already in the game!")


async def runr(ctx, host):

    for i in game[host.id]["all"]:
        if not any(c[0] == i for c in game[host.id]["current"]):
            game[host.id]["current"].append([i, 0, False])


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

        game[host.id]["current"][i].append([card1, card2])

        embed = discord.Embed()

        embed.add_field(name = "Your Hand: ", value = f'{messages.special_cards[card1[0]]}{card1[1]}  {messages.special_cards[card2[0]]}{card2[1]}')

        await game[host.id]["current"][i][0].send(embed = embed)
        if (i == 0):
            await game[host.id]["current"][i][0].send("You are the small blind.")
        elif (i == 1):
            await game[host.id]["current"][i][0].send("You are the big blind.")

    await pre_flop(ctx, host)


async def pre_flop(ctx, host):

    players = game[host.id]["current"]

    await ctx.send(f"{players[0][0].mention} has bet {game[host.id]["small"]} coins.")
    game[host.id]["pot"] += game[host.id]["small"]
    players[0][1] = game[host.id]["small"]
    database.remove_money(players[0][0].id, game[host.id]["small"])

    await ctx.send(f"{players[1][0].mention} has bet {2*game[host.id]["small"]} coins.")
    game[host.id]["pot"] += 2*game[host.id]["small"]
    game[host.id]["bet"] = game[host.id]["small"]*2
    players[1][1] = 2 * game[host.id]["small"]
    database.remove_money(players[1][0].id, 2*game[host.id]["small"])

    t = 2
    total = len(players)
    while True:

        if (sum(i[2] for i in players) == total - 1):
            break

        if (game[host.id]["current"][t%total][2]):
            t = t + 1
            continue

        if (players[t%total][1] == game[host.id]["bet"]):
            break
        player = players[t%total][0]
        await bet(host, player, ctx, t%total)
        t = t + 1

        
async def bet(host, player, ctx, index):

    view = betView(player, ctx, host, index)
    embed = discord.Embed()
    embed.add_field(name = f"Pot - {game[host.id]["pot"]}", value = "\u200b", inline = False)
    embed.add_field(name = f"Bet - {game[host.id]["bet"]}", value = "\u200b", inline = False)

    view.message = await player.send(embed = embed, view = view)

    await view.wait()

    if view.timed_out:
        await ctx.send(f"{player.mention} took too long! Auto folding")
        game[host.id]["current"][index][2] = True


class betView(discord.ui.View):

    def __init__(self, player, ctx, host, index):
        super().__init__(timeout = 30)
        self.player = player
        self.ctx = ctx
        self.host = host
        self.timed_out = True
        self.index = index
    
    @discord.ui.button(label="Call/Check", style = discord.ButtonStyle.primary)
    async def call_callback(self, interaction: discord.Interaction, button: discord.ui.Button,):

        await interaction.response.defer()

        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view=self)

        bet = game[self.host.id]["bet"] - game[self.host.id]["current"][self.index][1]

        self.timed_out = False
        if (bet == 0):
            await self.ctx.send(f"{self.player.mention} has checked!")
        else:
            await self.ctx.send(f"{self.player.mention} has called {bet} coins!")

        game[self.host.id]["pot"] += bet
        game[self.host.id]["current"][self.index][1] = game[self.host.id]["bet"]
        database.remove_money(self.player.id, bet)

        self.stop()

    @discord.ui.button(label="Fold", style = discord.ButtonStyle.primary)
    async def fold_callback(self, interaction: discord.Interaction, button: discord.ui.Button,):
        
        await interaction.response.defer()

        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view=self)

        self.timed_out = False

        await self.ctx.send(f"{self.player.mention} folded!")
        game[self.host.id]["current"][self.index][2] = True

        self.stop()

    @discord.ui.button(label="Raise", style = discord.ButtonStyle.primary)
    async def raise_callback(self, interaction: discord.Interaction, button: discord.ui.Button,):

        await interaction.response.send_modal(raiseModal(self.player, self.host, self.index, self.ctx, self))

        
class raiseModal(discord.ui.Modal, title = "Raise"):

    amt = discord.ui.TextInput(label = "Raise", placeholder = "Enter Amount", min_length = 1, max_length = 15)

    def __init__(self, player, host, index, ctx, betView):
        super().__init__()
        self.player = player
        self.host = host
        self.index = index
        self.ctx = ctx
        self.betView = betView

    async def on_submit(self, interaction: discord.Interaction):

        try:
            amt = int(self.amt.value)
        except ValueError:
            await interaction.response.send_message("Please enter a valid number")
            return
        
        if amt <= game[self.host.id]["bet"]:
            await interaction.response.send_message("Bet must be greater than current bet!")
            return
        
        await interaction.response.defer()
        
        bet = amt - game[self.host.id]["current"][self.index][1]

        game[self.host.id]["bet"] = amt
        game[self.host.id]["current"][self.index][1] = amt

        game[self.host.id]["pot"] += bet

        database.remove_money(self.player.id, bet)

        await self.ctx.send(f"{self.player.mention} raised to {amt}")

        for child in self.betView.children:
            child.disabled = True
        await self.betView.message.edit(view=self.betView)

        self.betView.timed_out = False
        self.betView.stop()






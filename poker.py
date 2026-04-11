from functions import bot
import messages
import random
import discord
import database
from best_hand import calculate_hand, rank, convert

game = {}
#uid : {all = [], current = [], small, start, bet, pot, start_message, deck, cards}

class over(Exception):
    pass


def balance_low(player, bet):
    
    info = database.get_user(player.id, player.name)
    if (info["money"] < bet):
        return 1
    return 0


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

    def __init__(self, ctx, member):
        super().__init__()
        self.ctx = ctx
        self.member = member

    @discord.ui.button(label="Join", style = discord.ButtonStyle.primary)
    async def join_callback(self, interaction: discord.Interaction, button: discord.ui.Button,):

        await interaction.response.defer()

        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view=self)

        if (game[self.ctx.author.id]["start"]):
            await self.ctx.send(f"{self.member.mention} will join next round.")
        else:
            await self.ctx.send(f"{self.member.mention} has joined {self.ctx.author.mention}'s game")

        if (self.member not in game[self.ctx.author.id]["all"]):
            game[self.ctx.author.id]["all"].append(self.member)

        num = len(game[self.ctx.author.id]["all"])
        if (num >= 2):
            if ("start_message" not in game[self.ctx.author.id]):
                embed = discord.Embed()
                embed.add_field(name = f"There are {num} players in the lobby. Start Game?", value = "\u200b")
                start_msg = await self.ctx.author.send(embed = embed, view = startView(self.ctx.author, self.ctx))
                game[self.ctx.author.id]["start_message"] = start_msg
            else:
                embed = discord.Embed()
                embed.add_field(name = f"There are {num} players in the lobby. Start Game?", value = "\u200b")
                await game[self.ctx.author.id]["start_message"].edit(embed=embed)


    @discord.ui.button(label="Reject", style = discord.ButtonStyle.primary)
    async def reject_callback(self, interaction: discord.Interaction, button: discord.ui.Button,):
        
        await interaction.response.defer()

        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view=self)

        if (self.member in game[self.ctx.author.id]["all"]):
            game[self.ctx.author.id]["all"].remove(self.member)

        await self.ctx.send(f"{self.member.mention} has rejected {self.ctx.author.mention}'s invite")

@bot.command()
async def poker(ctx, s: int, *members: discord.Member):

    if (ctx.author.id in game):
        game.pop(ctx.author.id)

    game[ctx.author.id] = {"all": [ctx.author], "current": [], "small": s, "start": False, "bet": 0, "pot": 0, "cards": []}

    for member in members:

        try:
            await member.send("Test message")
        except discord.Forbidden:
            await ctx.send(f"{member} does not have their DMs on!")
            continue

        embed = discord.Embed()
        embed.add_field(name = f"{ctx.author} is inviting you to a poker game.", value = "\u200b")
        await member.send(embed = embed, view = inviteView(ctx, member))



async def runr(ctx, host):

    for i in game[host.id]["all"]:
        if not any(c[0] == i for c in game[host.id]["current"]):
            game[host.id]["current"].append([i, 0, False])


    if (len(game[host.id]["current"]) < 2):
        await ctx.send("Need atleast 2 players!")
        game[host.id]["current"].clear()
        return
    
    try:
        await round(ctx, host)
    except over:
        return


async def round(ctx, host):

    round_deck = messages.deck[:]
    random.shuffle(round_deck)
    game[host.id]["deck"] = round_deck

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
    
    for player in game[host.id]["current"]:
        player[1] = None
    game[host.id]["bet"] = 0
    
    await flop(ctx, host)
    
    for player in game[host.id]["current"]:
        player[1] = None
    game[host.id]["bet"] = 0

    await turn(ctx, host)

    for player in game[host.id]["current"]:
        player[1] = None
    game[host.id]["bet"] = 0

    await river(ctx, host)

    players = game[host.id]["current"]
    temp = []
    for i in players:
        if i[2] == True:
            continue
        temp.append(i)

    await find_hand(ctx, host, temp)

async def find_hand(ctx, host, players):

    hand = {}

    for i in players:
        hole_cards = i[3]
        community_cards = game[host.id]["cards"]
        seven = hole_cards + community_cards
        hand[i[0]] = calculate_hand(seven)
    
    winner = []
    for i in rank:
        if any(a[0] == i for a in hand.values()):
            winner = [(key, value) for key, value in hand.items() if value[0] == i]
            break
    
    if len(winner) > 1:
        best_val = max(winner, key = lambda x: x[1][1])
        winner = [i for i in winner if i[1][1] == best_val[1][1]]

    card1 = game[host.id]["cards"][0]
    card2 = game[host.id]["cards"][1]
    card3 = game[host.id]["cards"][2]
    card4 = game[host.id]["cards"][3]
    card5 = game[host.id]["cards"][4]
    

    embed = discord.Embed()
    # embed.add_field(name = "\u200b", value = "\u200b")
    # embed.add_field(name = "\u200b", value = f"{messages.special_cards[card1[0]]}{card1[1]}  {messages.special_cards[card2[0]]}{card2[1]}  {messages.special_cards[card3[0]]}{card3[1]}  {messages.special_cards[card4[0]]}{card4[1]}  {messages.special_cards[card5[0]]}{card5[1]}")
    # embed.add_field(name = "\u200b", value = "\u200b")
    
    embed.add_field(name = "Name", value = "\u200b")
    embed.add_field(name = "Cards", value = "\u200b")
    embed.add_field(name = "Best Hand", value = "\u200b")

    for i in players:
        card1 = i[3][0]
        card2 = i[3][1]
        embed.add_field(name = i[0].name, value = "\u200b")
        embed.add_field(name = f"{messages.special_cards[card1[0]]}{card1[1]}  {messages.special_cards[card2[0]]}{card2[1]}", value = "\u200b")
        embed.add_field(name = convert[hand[i[0]][0]], value = "\u200b")

    await ctx.send(embed = embed)
    await end_round(ctx, winner, host)
    raise over()
            


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

    await bet_logic(ctx, host, 2)

async def flop(ctx, host):

    card1 = game[host.id]["deck"].pop()
    card2 = game[host.id]["deck"].pop()
    card3 = game[host.id]["deck"].pop()

    game[host.id]["cards"].append(card1)
    game[host.id]["cards"].append(card2)
    game[host.id]["cards"].append(card3)

    embed = discord.Embed()
    embed.add_field(name = "THE FLOP", value = f"{messages.special_cards[card1[0]]}{card1[1]}  {messages.special_cards[card2[0]]}{card2[1]}  {messages.special_cards[card3[0]]}{card3[1]}")
    await ctx.send(embed = embed)

    await bet_logic(ctx, host, 0)

async def turn(ctx, host):

    card = game[host.id]["deck"].pop()
    game[host.id]["cards"].append(card)
    embed = discord.Embed()

    card1 = game[host.id]["cards"][0]
    card2 = game[host.id]["cards"][1]
    card3 = game[host.id]["cards"][2]


    embed.add_field(name = "THE TURN", value = f"{messages.special_cards[card1[0]]}{card1[1]}  {messages.special_cards[card2[0]]}{card2[1]}  {messages.special_cards[card3[0]]}{card3[1]}  {messages.special_cards[card[0]]}{card[1]}")
    await ctx.send(embed = embed)

    await bet_logic(ctx, host, 0)

async def river(ctx, host):

    card = game[host.id]["deck"].pop()
    game[host.id]["cards"].append(card)
    embed = discord.Embed()

    card1 = game[host.id]["cards"][0]
    card2 = game[host.id]["cards"][1]
    card3 = game[host.id]["cards"][2]
    card4 = game[host.id]["cards"][3]

    embed.add_field(name = "THE RIVER", value = f"{messages.special_cards[card1[0]]}{card1[1]}  {messages.special_cards[card2[0]]}{card2[1]}  {messages.special_cards[card3[0]]}{card3[1]}  {messages.special_cards[card4[0]]}{card4[1]}  {messages.special_cards[card[0]]}{card[1]}")
    await ctx.send(embed = embed)

    await bet_logic(ctx, host, 0)



async def bet_logic(ctx, host, t):

    players = game[host.id]["current"]
    total = len(players)
    while True:

        if (sum(i[2] for i in players) == total - 1):
            winner = None
            for i in players:
                if (i[2] == False):
                    winner = i[0]
            await end_round(ctx, [[winner]], host)
            raise over()

        if (game[host.id]["current"][t%total][2]):
            t = t + 1
            continue

        if (players[t%total][1] == game[host.id]["bet"]):
            break
        player = players[t%total][0]
        await bet_send(host, player, ctx, t%total)
        t = t + 1

async def bet_send(host, player, ctx, index):

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
        super().__init__(timeout = 60)
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

        bet = game[self.host.id]["bet"] - (game[self.host.id]["current"][self.index][1] or 0)
        self.timed_out = False

        if (balance_low(self.player, bet)):
            await self.player.send("Balance Low. Auto Folding")
            await self.ctx.send(f"{self.player.mention} folded!")
            game[self.host.id]["current"][self.index][2] = True
            self.stop()
            return


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
        
        if (balance_low(self.player, amt)):
            await interaction.response.send_message("Balance Low!")
            return
        
        await interaction.response.defer()
        
        bet = amt - (game[self.host.id]["current"][self.index][1] or 0)

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


class anotherViewHost(discord.ui.View):

    def __init__(self, ctx, host):
        super().__init__()
        self.ctx = ctx
        self.host = host

    @discord.ui.button(label="Let's Go", style = discord.ButtonStyle.primary)
    async def again_callback(self, interaction: discord.Interaction, button: discord.ui.Button,):
        
        await interaction.response.defer()

        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view=self)

        members = game[self.host.id]["all"][:]

        game[self.host.id]["all"] = [self.host] 
        for member in members:
            if (member == self.host):
                continue

            embed = discord.Embed()
            embed.add_field(name = f"{self.host} is inviting you to a poker game.", value = "\u200b")
            await member.send(embed = embed, view = inviteView(self.ctx, member))

    @discord.ui.button(label="Maybe Later", style = discord.ButtonStyle.primary)
    async def later_callback(self, interaction: discord.Interaction, button: discord.ui.Button,):

        await interaction.response.defer()

        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view=self)

        game.pop(self.host.id)
        await self.ctx.send(f"{self.host.mention}'s game has ended.")

async def end_round(ctx, winner, host):

    for i in winner:
        await ctx.send(f"{i[0].mention} wins!")
        database.add_money(i[0].id, int(game[host.id]["pot"]/len(winner)))

    game[host.id]["current"].clear()
    game[host.id]["start"] = False
    game[host.id]["bet"] = 0
    game[host.id]["pot"] = 0
    game[host.id]["cards"].clear()
    game[host.id].pop("deck", None)
    game[host.id].pop("start_message", None)
    sb = game[host.id]["all"].pop(0)
    game[host.id]["all"].append(sb)

    embed = discord.Embed()
    embed.add_field(name = "Another Game?", value = "\u200b")
    await host.send(embed = embed, view = anotherViewHost(ctx, host))







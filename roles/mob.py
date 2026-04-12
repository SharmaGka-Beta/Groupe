from functions import bot
import discord
from discord.ext import commands
import messages
import random
import database
import events
import asyncio

class ExtortAndDrugView(discord.ui.View):
    
    def __init__(self, ctx, target, money, type):
        super().__init__()
        self.ctx = ctx
        self.target = target
        self.money = money
        self.type = type


    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("Not for you!", ephemeral = True)
            return False
        return True
    
    @discord.ui.button(label="Accept", style = discord.ButtonStyle.primary,)
    async def accept_callback(self, interaction: discord.Interaction, button: discord.ui.Button,):
    
        await interaction.response.defer()

        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view=self)

        inv = database.get_inventory(self.ctx.author.id)
        info = database.get_user(self.ctx.author.id)
        if (len(inv[0]) == 0 and self.type == "extort"):
            await self.ctx.send("You don't have a weapon!")
            return
        
        if (events.police_catch(self.ctx, 5)):
            await self.ctx.send(f"You were caught by the cops!")
            return

        xp = random.randint(10, 25)*info["lvl"]
        rng = random.randint(1, 5)

        (lvlcnt, bonus, newrole) = database.add_xp(self.ctx.author.id, xp)
        if(lvlcnt):
            await self.ctx.send(f"{self.ctx.author.name} leveled up! +{bonus} coins -{5*lvlcnt} Wanted +{5*lvlcnt} Integrity +{xp} XP")
        if newrole is not None:
            await self.ctx.send(f"Congratulations **{self.ctx.author.name}**! You have been promoted to {newrole}!")
        
        database.remove_integrity(self.ctx.author.id, rng)
        database.add_wanted(self.ctx.author.id, rng)
        database.add_b_money(self.ctx.author.id, self.money)
        await self.ctx.send(f"+{self.money} black money +{rng} Wanted -{rng} Integrity")
    
    @discord.ui.button(label="Deny", style = discord.ButtonStyle.primary,)
    async def deny_callback(self, interaction: discord.Interaction, button: discord.ui.Button,):
        await interaction.response.defer()

        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view=self)

        await self.ctx.send("Coward")
        
@commands.cooldown(1, 2*60, commands.BucketType.user)
@bot.command()
async def extort(ctx):

    info = database.get_user(ctx.author.id, ctx.author.name)

    role = info["user_role"]

    if (role != "associate" and role != "underboss" and role != "godfather"):
        await ctx.send("You're not in the mob!")
        return

    if info["jail"] == 1:
        await ctx.send("You are a convict! Get out of jail first!!")
        return

    target = random.choice(messages.extort_targets)
    money = int(random.randint(50, 100)*database.money_multiplier(info["lvl"]))
    embed = discord.Embed()

    embed.add_field(name = "\u200b", value = f"{target} - {money} coins")

    await ctx.send(embed = embed, view = ExtortAndDrugView(ctx, target, money, "extort"))


@commands.cooldown(1, 2*60, commands.BucketType.user)
@bot.command()
async def deal(ctx):

    info = database.get_user(ctx.author.id, ctx.author.name)

    role = info["user_role"]

    if (role != "associate" and role != "underboss" and role != "godfather"):
        await ctx.send("You're not in the mob!")
        return

    if info["jail"] == 1:
        await ctx.send("You are a convict! Get out of jail first!!")
        return
    
    drug = random.choice(messages.items_drugs)[0]
    money = int(random.randint(50, 100)*database.money_multiplier(info["lvl"]))

    embed = discord.Embed()

    embed.add_field(name = "\u200b", value = f"{drug} - {money:,} coins")

    await ctx.send(embed = embed, view = ExtortAndDrugView(ctx, drug, money, "drug"))
    


    


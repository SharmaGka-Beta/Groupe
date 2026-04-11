from functions import bot
import discord
from discord.ext import commands
import messages
import random
import database
import events
import asyncio

class bribeView(discord.ui.View):
    def __init__(self, ctx, money):
        super().__init__()
        self.ctx = ctx
        self.money = money

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("Not for you!", ephemeral = True)
            return False
        return True
    
    @discord.ui.button(label="Accept", style=discord.ButtonStyle.primary,)
    async def accept_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()

        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view=self)

        info = database.get_user(self.ctx.author.id)
        true = random.randint(0, 10)
        xp = random.randint(5, 15)*info["lvl"]

        await self.ctx.send("You accept the offer...")
        await asyncio.sleep(1)
        if(true >= 9):
   
            await self.ctx.send(f"-5 Integrity +{self.money*2} coins +{xp} XP")
            database.remove_integrity(self.ctx.author.id, 5)
            database.add_money(self.ctx.author.id, self.money*2)

            (lvlcnt, bonus, newrole) = database.add_xp(self.ctx.author.id, xp)
            if(lvlcnt):
                await self.ctx.send(f"{self.ctx.author.name} leveled up! +{bonus} coins -{5*lvlcnt} Wanted +{5*lvlcnt} Integrity")
            if(newrole != None):
                await self.ctx.send(f"Congratulations **{self.ctx.author.name}**! You have been promoted to {newrole}!")

        else:
            await self.ctx.send(f"It was a setup!, You got caught by your precinct\nThey fined you {self.money} coins\n -10 Integrity -{self.money} coins")
            database.remove_integrity(self.ctx.author.id, 10)
            database.remove_money(self.ctx.author.id, self.money)
        
    @discord.ui.button(label="Reject", style=discord.ButtonStyle.primary,)
    async def reject_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()

        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view=self)

        setup_chance = random.randint(1, 10)

        if(setup_chance > 8):
            await self.ctx.send("The criminal turned out to be from Internal Affairs!")
            await self.ctx.send(f"**IA Agent**: Good work **{self.ctx.author.name}**, you passed the test")
            await self.ctx.send(f"+15 Integrity +{self.money} coins")
            database.add_integrity(self.ctx.author.id, 15)
            database.add_money(self.ctx.author.id, self.money)
        else:
            await self.ctx.send(f"**Criminal:** I could've made you very rich..\n+5 Integrity +{self.money} coins")
            database.add_integrity(self.ctx.author.id, 5)
            database.add_money(self.ctx.author.id, self.money)


class patrolView(discord.ui.View):
    def __init__(self, ctx, target, money):
        super().__init__()
        self.ctx = ctx
        self.target = target
        self.money = money

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("Not for you!", ephemeral = True)
            return False
        return True
    
    @discord.ui.button(label="Arrest", style = discord.ButtonStyle.primary,)
    async def arrest_callback(self, interaction: discord.Interaction, button: discord.ui.Button,):
        await interaction.response.defer()

        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view=self)

        info = database.get_user(self.ctx.author.id, self.ctx.author.name)
        xp = random.randint(5, 15)*info["lvl"]
        success = random.triangular(1, 5, 3)

        if(success > self.target[1]):
            bribe_chance = random.randint(1, 10)
            if(bribe_chance == 5):
                embed = discord.Embed()
                embed.add_field(name="\u200b", value="The criminal gives you an offer to let him go :money_with_wings:...")
                await self.ctx.send(embed = embed, view= bribeView(self.ctx, self.money))
                return
    
            await self.ctx.send(f"You succesfully caught {self.target[0]}!\nYou got a bonus of +{self.money} coins\n+{self.target[1]*2} Integrity +{xp}XP")
            database.add_money(self.ctx.author.id, self.money)
            database.add_integrity(self.ctx.author.id, self.target[1]*2)

            (lvlcnt, bonus, newrole) = database.add_xp(self.ctx.author.id, xp)
            if(lvlcnt):
                await self.ctx.send(f"{self.ctx.author.name} leveled up! +{bonus} coins -{5*lvlcnt} Wanted +{5*lvlcnt} Integrity")
            if(newrole != None):
                await self.ctx.send(f"Congratulations **{self.ctx.author.name}**! You have been promoted to {newrole}!")
            
        else:
            await self.ctx.send(f"The criminal was too powerful for you! You had to give him your money to escape")
            await self.ctx.send(f"-{self.money} coins")
            database.remove_money(self.ctx.author.id, self.money)

    @discord.ui.button(label="Ignore", style= discord.ButtonStyle.primary,)
    async def ignore_callback(self, interaction: discord.Interaction, button: discord.ui.Button,):
        await interaction.response.defer()

        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view=self)

        await self.ctx.send(f"You chose to look the other way...\n -{self.target[1]} Integrity")
        database.remove_integrity(self.ctx.author.id, self.target[1])

@commands.cooldown(1, 2*60, commands.BucketType.user)
@bot.command()
async def patrol(ctx):
    info = database.get_user(ctx.author.id, ctx.author.name)
    guns = database.get_inventory(ctx.author.id)[0]
    role = info["user_role"]

    if(info["jail"]):
        await ctx.send("You are in jail!")
        return
    if(role != "rookie" and role != "detective" and role != "chief"):
        await ctx.send("You are not in the police!")
        return
    if len(guns) == 0:
            await ctx.send("You don't have a weapon!")
            return
    if(random.random() < info["wanted"]/10000):
        events.police_catch(ctx, 0, rand=False)
        await ctx.send("An undercover cop caught you for being corrupt...") #need to change dialogue
        return
    
    target = random.choice(messages.patrol_targets)
    money = int(100*target[1]*database.money_multiplier(info["lvl"]))
    rand_money = random.randint(money, money*2)
    money = rand_money
    embed = discord.Embed()

    danger = {1: "Very Low", 2: "Low", 3: "Medium", 4: "High", 5: "MAX"}
    embed.add_field(name="\u200b", value=f"Name: {target[0]} - {money:,} coins\nDanger Level: {danger[target[1]]}")
    if(ctx.author.avatar == None):
        embed.set_author(name=f"{ctx.author.name}'s patrol")
    else:
        embed.set_author(name=f"{ctx.author.name}'s patrol", icon_url=ctx.author.avatar.url)

    await ctx.send(embed=embed, view= patrolView(ctx, target, money))

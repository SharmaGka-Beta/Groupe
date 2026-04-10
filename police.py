from functions import bot
import discord
from discord.ext import commands
import messages
import random
import database
import events
import story
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

        true = random.randint(0, 10)
        
        await self.ctx.send("You accept the offer...")
        await asyncio.sleep(2)
        if(true >= 8):   
            await self.ctx.send(f"-5 Integrity +{self.money*2} coins")
            database.remove_integrity(self.ctx.author.id, 5)
            database.add_money(self.ctx.author.id, self.money*2)
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
            await self.ctx.send(f"IA Agent: Good work {self.ctx.author.name}, you passed the test")
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

        guns = database.get_inventory(self.ctx.author.id)[0]
        if len(guns) == 0:
            await self.ctx.send("You don't have a weapon!")
            return
        
        success = random.randint(1, 5)
        if(success > self.target[1]):
            bribe_chance = random.randint(1, 10)
            if(bribe_chance == 5):
                embed = discord.Embed()
                embed.add_field(name="\u200b", value="The criminal gives you an offer to let him go :money_with_wings:...")
                await self.ctx.send(embed = embed, view= bribeView(self.ctx, self.money))
                return

            await self.ctx.send(f"You succesfully caught {self.target[0]}!")
            await self.ctx.send(f"You got a bonus of +{self.money} coins")
            await self.ctx.send(f"+{self.target[1]*2} Integrity")
            database.add_money(self.ctx.author.id, self.money)
            database.add_integrity(self.ctx.author.id, self.target[1]*2)
        else:
            await self.ctx.send(f"The criminal was too powerful for you! And defeated you easily")
            await self.ctx.send(f"You barely survived...")

    @discord.ui.button(label="Ignore", style= discord.ButtonStyle.primary,)
    async def ignore_callback(self, interaction: discord.Interaction, button: discord.ui.Button,):
        await interaction.response.defer()

        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view=self)

        await self.ctx.send(f"You chose to look the other way...\n -{self.target[1]} Integrity")
        database.remove_integrity(self.ctx.author.id, self.target[1])
        
        



@bot.command()
async def patrol(ctx):
    info = database.get_user(ctx.author.id, ctx.author.name)
    role = info["user_role"]

    if(info["jail"]):
        await ctx.send("You are in jail!")
        return
    if(role != "rookie" and role != "detective" and role != "chief"):
        await ctx.send("You are not in the police!")
        return
    if(info["wanted"] >= 80):
        events.police_catch(ctx, 0, random=False)
        await ctx.send("It was a setup! you got caught....") #need to change dialogue
        return
    
    target = random.choice(messages.patrol_targets)
    money = 4000*target[1] #capped at 20k
    embed = discord.Embed()
    embed.add_field(name="\u200b", value=f"Name: {target[0]} - {money} coins\nDanger Level: {target[1]}")
    if(ctx.author.avatar == None):
        embed.set_author(name=f"{ctx.author.name}'s patrol")
    else:
        embed.set_author(name=f"{ctx.author.name}'s patrol", icon_url=ctx.author.avatar.url)

    await ctx.send(embed=embed, view= patrolView(ctx, target, money))

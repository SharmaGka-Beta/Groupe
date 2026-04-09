from functions import bot
import discord
import messages
import random
import database
import events
import story
import asyncio

class contribute(discord.ui.View):

    def __init__(self, ctx, money):
        super().__init__()
        self.ctx = ctx
        self.money = money

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("Not for you!", ephemeral = True)
            return False
        return True
    
    @discord.ui.button(label="All", style = discord.ButtonStyle.primary,)
    async def all_callback(self, interaction: discord.Interaction, button: discord.ui.Button,):

        await interaction.response.defer()
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view=self)

        await self.ctx.send("'You will go far if you keep making contributions like this!!'")

    @discord.ui.button(label = "Half", style = discord.ButtonStyle.primary,)
    async def half_callback(self, interaction: discord.Interaction, button: discord.ui.Button,):

        await interaction.response.defer()
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view=self)

        if (events.summon(self.ctx, 5, self.money)):
            await self.ctx.send("You have been summoned by the family for not making enough contributions")
            await self.ctx.send("'If you wanna survive here I'd advise you to step up your game!'")
            
        database.add_b_money(self.ctx.author.id, self.money//2)

    @discord.ui.button(label = "None", style = discord.ButtonStyle.primary,)
    async def none_callback(self, interaction: discord.Interaction, button: discord.ui.Button,):

        database.add_b_money(self.ctx.author.id, self.money)

        await interaction.response.defer()
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view=self)

        a = events.summon(self.ctx, 7, self.money)

        if (a == 1):
            await self.ctx.send("You have been summoned by the family for not making enough contributions!")
            await self.ctx.send("'If this behaviour continues we are gonna have a problem'")
            # database.add_money(self.ctx.author.id, self.money)

        elif (a == 2):
            await self.ctx.send("You have been summoned by the family for not making enough contributions!")
            await self.ctx.send("They roughed you up!")
            await self.ctx.send(f"-{(self.money)} coins")
            database.remove_money(self.ctx.author.id, self.money)

class extortView(discord.ui.View):
    
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
    
    @discord.ui.button(label="Accept", style = discord.ButtonStyle.primary,)
    async def accept_callback(self, interaction: discord.Interaction, button: discord.ui.Button,):
    
        await interaction.response.defer()

        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view=self)

        info = database.get_inventory(self.ctx.author.id)
        if len(info[0]) == 0:
            await self.ctx.send("You don't have a weapon!")
            return
        
        if (events.police_catch(self.ctx, 5)):
            await self.ctx.send(f"You were caught by the cops!")
            return

        database.remove_integrity(self.ctx.author.id, int(self.money//1000))
        database.add_wanted(self.ctx.author.id, self.money//1000)
        await self.ctx.send(f"+{self.money} coins")

        embed = discord.Embed()
        embed.add_field(name = "\u200b", value = "Contribute to the family?")

        await self.ctx.send(embed = embed, view = contribute(self.ctx, self.money))

    
    @discord.ui.button(label="Deny", style = discord.ButtonStyle.primary,)
    async def deny_callback(self, interaction: discord.Interaction, button: discord.ui.Button,):
        await interaction.response.defer()

        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view=self)

        await self.ctx.send("Coward")
        

@bot.command()
async def extort(ctx):

    info = database.get_user(ctx.author.id)

    role = info["user_role"]

    if (role != "associate" and role != "underboss" and role != "godfather"):
        await ctx.send("You're not in the mob!")
        return

    if info["jail"] == 1:
        await ctx.send("You are a convict! Get out of jail first!!")
        return

    target = random.choice(messages.extort_targets)
    money = random.randint(10000, 20000)
    embed = discord.Embed()

    embed.add_field(name = "\u200b", value = f"{target} - {money} coins")

    await ctx.send(embed = embed, view = extortView(ctx, target, money))


    
@bot.command()
async def sell(ctx):

    info = database.get_user(ctx.author.id)

    role = info["user_role"]

    if (role != "associate" and role != "underboss" and role != "godfather"):
        await ctx.send("You're not in the mob!")
        return

    if info["jail"] == 1:
        await ctx.send("You are a convict! Get out of jail first!!")
        return
    
    drug = random.choice(messages.items_drugs)[0]
    money = random.randint(10000, 20000)

    embed = discord.Embed()

    embed.add_field(name = "\u200b", value = f"{drug} - {money} coins")

    await ctx.send(embed = embed, view = extortView(ctx, drug, money))

@bot.command()
async def promote(ctx):

    info = database.get_user(ctx.author.id)

    role = info["user_role"]

    if (role != "associate" and role != "underboss"):
        await ctx.send("You're not eligible for a promotion!")
        return
    
    wntd_lvl = info["wanted"]
    intg_lvl = info["integrity"]

    if(wntd_lvl < 2*intg_lvl):
        await ctx.send("'You haven't contributed shit and want a promotion!!'")
        await ctx.send("They roughed you up!")
        database.remove_money(ctx.author.id, 15000)
        return
    
    if (role == "associate"):
        
        await ctx.send("'Alright then. A rival family has overstepped its bounds and needs to learn their lesson.'")
        await asyncio.sleep(2)
        embed = discord.Embed()
        embed.add_field(name = "\u200b", value = "Ready?")

        await ctx.send(embed = embed, view = story.aPromotionView(ctx))
    


    


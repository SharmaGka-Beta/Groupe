import discord
from functions import bot
import database
import messages
import random
import events

@bot.command()
async def work(ctx):
    info = database.get_user(ctx.author.id)

    if info["jail"] == 1:
        await ctx.send("You are a convict! Get out of jail first!!")
        return

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


class Charity_View(discord.ui.View):
    def __init__(self, user_id, amount, message, ctx):
        super().__init__()
        self.user_id = user_id
        self.amount = amount
        self.message = message
        self.ctx = ctx

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This isn't your charity!", ephemeral = True)
            return False
        return True

    @discord.ui.button(label="Donate", style=discord.ButtonStyle.primary)
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
        
        await interaction.response.defer()
        info = database.get_user(self.user_id)

        if(self.amount>info["money"]):
            await self.ctx.send("You don't have enough funds")
            return
        
        database.remove_money(self.user_id, self.amount)
        database.add_integrity(self.user_id, int(self.amount/1000))
        database.remove_wanted(self.user_id, int(self.amount/1000))

        for item in self.children:
            item.disabled = True
        await interaction.edit_original_response(view=self)

        await self.ctx.send(f'-{self.amount} Coins')
        await self.ctx.send(f'+{int(self.amount/1000)} Integrity')
        await self.ctx.send(f'-{int(self.amount/1000)}  Wanted')

    @discord.ui.button(label="Decline", style=discord.ButtonStyle.primary)
    async def decline(self, interaction: discord.Interaction, button: discord.ui.Button):
        
        await interaction.response.defer()
        for item in self.children:
            item.disabled = True
        await interaction.edit_original_response(view=self)

        await self.ctx.send("Ye jo gareeb hoye ye apni aadat se gareeb hoye!")

    

@bot.command()
async def charity(ctx):
    info = database.get_user(ctx.author.id)

    

    if  info["jail"]==1:
        await ctx.send("🚔 You're in jail! You can't donate from behind bars.")
        return
    
    if info["money"] <= 5000:
        await ctx.send("❌ You're broke. Nothing to donate.")
        return
    
    amount = random.randint(5000, 15000)
    message= random.choice(messages.charity_messages)

    embed = discord.Embed(
        title="💝 Charity Request",
        description=f"*{message}*",
        color=discord.Color.blurple()
    )
    embed.add_field(name="💸 Requested Amount", value=f"{amount}", inline=True)

    await ctx.send(embed=embed, view=Charity_View(ctx.author.id, amount, message, ctx))


class WeaponButton(discord.ui.Button):
    def __init__(self, gun, ctx, target, money):
        super().__init__(label=gun, style=discord.ButtonStyle.primary)
        self.gun = gun
        self.ctx = ctx
        self.target = target
        self.money = money

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"You used a {self.gun}")
        if(events.police_catch(self.ctx, 10)):
            await self.ctx.send("The police knew you were coming!")
            await self.ctx.send("You have been captured by the police!")
            await self.ctx.send("You can bribe, run, talk or give bail")
            return
        
        await self.ctx.send(f"You have successfully eliminated {self.target}")
        await self.ctx.send(f"+{self.money} coins")
        database.add_money(self.ctx.author.id, self.money)
        database.remove_integrity(self.ctx.author.id, int(self.money/1000))
        database.add_wanted(self.ctx.author.id, int(self.money/1000))
    
class acceptView(discord.ui.View):

    def __init__(self, ctx, weapons, target, money):
        super().__init__()
        self.ctx = ctx
        self.weapons = weapons
        for weapon in weapons:
            self.add_item(WeaponButton(weapon[0].capitalize(), self.ctx, target, money))

        

class hitView(discord.ui.View):
    
    def __init__(self, ctx, target, money):
        super().__init__()
        self.ctx = ctx
        self.target = target
        self.money = money

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("Get your own contract!", ephemeral = True)
            return False
        return True
    
    @discord.ui.button(label="Accept", style = discord.ButtonStyle.primary,)
    async def accept_callback(self, interaction: discord.Interaction, button: discord.ui.Button,):
    
        await interaction.response.defer()
        info = database.get_inventory(self.ctx.author.id)
        if len(info[0]) == 0:
            await interaction.response.send_message("You don't have a weapon!")
            return

        embed = discord.Embed()
        embed.add_field(name = "Which weapon would you like to use?", value = "\u200b")
        await self.ctx.send(embed = embed, view = acceptView(self.ctx, info[0], self.target, self.money))
        

        

    @discord.ui.button(label="Reject", style = discord.ButtonStyle.primary)
    async def reject_callback(self, interaction: discord.Interaction, button: discord.ui.Button,):

        await interaction.response.send_message("Coward")
        return
        



@bot.command()
async def hit(ctx):
    info = database.get_user(ctx.author.id)

    if info["jail"] == 1:
        await ctx.send("You are a convict! Get out of jail first!!")
        return
    
    if (events.police_catch(ctx, 8)):
        await ctx.send("Your contact turned out be an undercover cop!")
        await ctx.send("You have been captured by the cops. You can bribe, run, negotiate or pay bail.")
        return
    
    target = random.choice(messages.hit_targets)
    money = random.randint(5000, 15000)

    embed = discord.Embed()
    embed.add_field(name = '\u200b', value = f'{target} - {money} coins')

    await ctx.send(embed = embed, view = hitView(ctx, target, money))


class Volunteer_view(discord.ui.View):
    def __init__(self, user_id, message, ctx):
        super().__init__()
        self.user_id = user_id
        self.message = message
        self.ctx = ctx

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("This isn't your volunteering!", ephemeral = True)
            return False
        return True
    
    @discord.ui.button(label="Volunteer", style=discord.ButtonStyle.primary)
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
        
        await interaction.response.defer()
        info = database.get_user(self.user_id)

        amount=random.randint(5,15)

        database.add_integrity(self.user_id, amount)

        for item in self.children:
            item.disabled=True
        await interaction.edit_original_response(view=self)

        await self.ctx.send(f'+{amount} Integrity')
        await self.ctx.send(f'-{amount} Wanted')

    @discord.ui.button(label="Decline", style=discord.ButtonStyle.primary)
    async def decline(self, interaction: discord.Interaction, button: discord.ui.Button):
        
        await interaction.response.defer()
        for item in self.children:
            item.disabled = True
        await interaction.edit_original_response(view=self)

        await self.ctx.send("Ye gendu generation hai!")


@bot.command()
async def volunteer(ctx):
    info = database.get_user(ctx.author.id)

    if  info["jail"]==1:
        await ctx.send("🚔 You're in jail! You can't volunteer from behind bars.")
        return
    
    message=random.choice(messages.volunteer_messages)

    embed = discord.Embed(
        title="💝 Volunteer Request",
        description=f"*{message}*",
        color=discord.Color.gold()
    )

    await ctx.send(embed=embed, view=Volunteer_view(ctx.author.id, message, ctx))



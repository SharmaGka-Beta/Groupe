import discord
from discord.ext import commands
from functions import bot
import asyncio
import database
import messages
import random
import events

@commands.cooldown(1, 60, commands.BucketType.user) #1 min cooldown
@bot.command()
async def work(ctx):
    info = database.get_user(ctx.author.id, ctx.author.name)

    if info["jail"] == 1:
        await ctx.send("You are a convict! Get out of jail first!!")
        return

    if info["user_role"] != 'civilian':
        await ctx.send("Why would you still want to go to your puny day job!")
        return

    xp = random.randint(1, 25)*info["lvl"]
    a = random.randint(1, 100)
    money = int(random.randint(100, 500)*database.money_multiplier(info["lvl"]))

    if 1 <= a <= 89:
        mes = random.choice(messages.workp)
        await ctx.send(mes)
        await ctx.send(f"+{money} coins +{xp} XP")

        (lvlcnt, bonus, newrole) = database.add_xp(ctx.author.id, xp)

        if(lvlcnt):
            await ctx.send(f"{ctx.author.name} leveled up! +{bonus} coins -{5*lvlcnt} Wanted +{5*lvlcnt} Integrity")
        if(newrole != None):
            await ctx.send(f"Congratulations **{ctx.author.name}**! You have been promoted to {newrole}!")

        database.add_money(ctx.author.id, money)

    elif 90 <= a <= 100:
        mes = random.choice(messages.workn)
        await ctx.send(mes)
        await ctx.send(f"-{money} coins")
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

        for item in self.children:
            item.disabled = True
        await interaction.message.edit(view=self)
        
        info = database.get_user(self.user_id, self.ctx.author.name)
        rng = random.randint(1, 5)
        xp = random.randint(1, 25)*info["lvl"]

        database.remove_money(self.user_id, self.amount)
        database.add_integrity(self.user_id, rng)
        database.remove_wanted(self.user_id, rng)

        
        await self.ctx.send(f'-{self.amount} Coins +{xp}XP')
        await self.ctx.send(f'+{rng} Integrity -{rng} Wanted')

        (lvlcnt, bonus, newrole) = database.add_xp(self.ctx.author.id, xp)

        if(lvlcnt):
            await self.ctx.send(f"{self.ctx.author.name} leveled up! +{bonus} coins -{5*lvlcnt} Wanted +{5*lvlcnt} Integrity")
        if(newrole != None):
            await self.ctx.send(f"Congratulations **{self.ctx.author.name}**! You have been promoted to {newrole}!")

        

    @discord.ui.button(label="Decline", style=discord.ButtonStyle.primary)
    async def decline(self, interaction: discord.Interaction, button: discord.ui.Button):
        
        await interaction.response.defer()
        for item in self.children:
            item.disabled = True
        await interaction.message.edit(view=self)

        await self.ctx.send("Ye jo gareeb hai ye apni aadat se gareeb hai!")


    
@commands.cooldown(1, 2*60, commands.BucketType.user)
@bot.command()
async def charity(ctx):
    info = database.get_user(ctx.author.id, ctx.author.name)

    

    if  info["jail"]==1:
        await ctx.send("🚔 You're in jail! You can't donate from behind bars.")
        return
    
    
    amount = random.randint(info["money"]//20, info["money"]//10) #anywhere from 5 to 10% of wallet, cant donate black money

    if info["money"] <= amount:
        await ctx.send("❌ You're broke. You might qualify for charity though...")
        return 

    message= random.choice(messages.charity_messages)

    embed = discord.Embed(
        title="💝 Charity Request",
        description=f"*{message}*",
        color=discord.Color.blurple()
    )
    embed.add_field(name="💸 Requested Amount", value=f"{amount:,}", inline=True)

    await ctx.send(embed=embed, view=Charity_View(ctx.author.id, amount, message, ctx))


class WeaponButton(discord.ui.Button):
    def __init__(self, gun, ctx, target, money):
        super().__init__(label=gun, style=discord.ButtonStyle.primary)
        self.gun = gun.lower()
        self.ctx = ctx
        self.target = target
        self.money = money

    async def callback(self, interaction: discord.Interaction):

        await interaction.response.defer()

        for child in self.view.children:
            child.disabled = True
        await interaction.message.edit(view=self.view)

        await self.ctx.send(f"You used a {self.gun}")


        if(events.police_catch(self.ctx, 10)):
            await self.ctx.send("The police knew you were coming!")
            await self.ctx.send("You have been captured by the police!")
            await self.ctx.send("You can bribe, run, talk or give bail")
            return
        
        info = database.get_user(self.ctx.author.id, self.ctx.author.name)
        xp = random.randint(5, 50)*info["lvl"]
        break_chance = random.randint(1, 100) #5% chance gun breaks
        fail_chance = random.randint(-5, 5)
        wanted = random.randint(1, 5)

        if(fail_chance >  messages.hit_chance[self.gun]): #success increases with more expensive guns
            await self.ctx.send("Your weapon wasn't powerful enough, the target escaped..")
            return
        else:
            await self.ctx.send(f"You have successfully eliminated {self.target}")
            if(break_chance > 95):
                await self.ctx.send("Your gun overheated and broke...")
                database.update_inventory(self.ctx.author.id, self.gun, "ammunitions", -1)
            
            await self.ctx.send(f"+{self.money} black money +{xp} XP +{wanted} Wanted")

            (lvlcnt, bonus, newrole) = database.add_xp(self.ctx.author.id, xp)
            if(lvlcnt):
                await self.ctx.send(f"**{self.ctx.author.name}** leveled up! +{bonus} coins -{5*lvlcnt} Wanted +{5*lvlcnt} Integrity")
            if(newrole != None):
                await self.ctx.send(f"Congratulations **{self.ctx.author.name}**! You have been promoted to {newrole}!")

            database.add_b_money(self.ctx.author.id, self.money)
            database.add_wanted(self.ctx.author.id, wanted)
            
    
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

        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view=self)

        info = database.get_inventory(self.ctx.author.id)

        embed = discord.Embed()
        embed.add_field(name = "Which weapon would you like to use?", value = "\u200b")
        await self.ctx.send(embed = embed, view = acceptView(self.ctx, info[0], self.target, self.money))


    @discord.ui.button(label="Reject", style = discord.ButtonStyle.primary)
    async def reject_callback(self, interaction: discord.Interaction, button: discord.ui.Button,):

        await interaction.response.defer()
        await self.ctx.send("Coward")
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view=self)
        return
        


@commands.cooldown(1, 2*60, commands.BucketType.user)
@bot.command()
async def hit(ctx):
    info = database.get_user(ctx.author.id, ctx.author.name)
    inven = database.get_inventory(ctx.author.id)[0]
    if info["jail"] == 1:
        await ctx.send("You are a convict! Get out of jail first!!")
        return
    
    if len(inven) == 0:
            await ctx.send("You don't have a weapon!")
            return
    
    if (events.police_catch(ctx, 8)):
        await ctx.send("Your contact turned out be an undercover cop!")
        await ctx.send("You have been captured by the cops. You can bribe, run, negotiate or pay bail.")
        return
    
    target = random.choice(messages.hit_targets)
    money = int(random.randint(100, 1000)*database.money_multiplier(info["lvl"]))

    embed = discord.Embed()
    embed.add_field(name = '\u200b', value = f'{target} - {money:,} coins')

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

        rng=random.randint(1,5)


        for item in self.children:
            item.disabled=True
        await interaction.message.edit(view=self)

        info = database.get_user(self.ctx.author.id, self.ctx.author.name)
        xp = random.randint(1, 15)*info["lvl"]

        (lvlcnt, bonus, newrole) = database.add_xp(self.ctx.author.id, xp)

        if(lvlcnt):
           await self.ctx.send(f"{self.ctx.author.name} leveled up! +{bonus} coins -{5*lvlcnt} Wanted +{5*lvlcnt} Integrity")
        if(newrole != None):
           await self.ctx.send(f"Congratulations **{self.ctx.author.name}**! You have been promoted to {newrole}!")
        await self.ctx.send(f'+{rng} Integrity')
        await self.ctx.send(f'-{rng} Wanted')
        
        database.add_integrity(self.user_id, rng)
        database.remove_wanted(self.user_id, rng)

    @discord.ui.button(label="Decline", style=discord.ButtonStyle.primary)
    async def decline(self, interaction: discord.Interaction, button: discord.ui.Button):
        
        await interaction.response.defer()
        for item in self.children:
            item.disabled = True
        await interaction.message.edit(view=self)

        await self.ctx.send("Ye gendu generation hai!")

@commands.cooldown(1, 2*60, commands.BucketType.user) # 2 min cooldown
@bot.command()
async def volunteer(ctx):
    info = database.get_user(ctx.author.id, ctx.author.name)

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


class robView(discord.ui.View):
    
    def __init__(self, ctx, target, money):
        super().__init__()
        self.ctx = ctx
        self.target = target
        self.money = money

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("This is not your robbery!", ephemeral = True)
            return False
        return True
    
    @discord.ui.button(label="Go for it!", style = discord.ButtonStyle.primary,)
    async def accept_callback(self, interaction: discord.Interaction, button: discord.ui.Button,):
    
        await interaction.response.defer()

        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view=self)

        

        if (events.police_catch(self.ctx, 7)):
            await self.ctx.send(f"{self.target} caught you! They robbed you instead!")
            await self.ctx.send(f"-{self.money} coins")
            database.remove_money(self.ctx.author.id, self.money)
            database.update_jail(self.ctx.author.id, 0)
            return

        if (events.police_catch(self.ctx, 5)):
            await self.ctx.send("You have been captured by the police!")
            await self.ctx.send("You can bribe, run, talk or give bail")
            return
        
        info = database.get_user(self.ctx.author.id, self.ctx.author.name)
        xp = random.randint(10, 30)*info["lvl"]
        rng = random.randint(1, 5)

        (lvlcnt, bonus, newrole) = database.add_xp(self.ctx.author.id, xp)

        if(lvlcnt):
           await self.ctx.send(f"{self.ctx.author.name} leveled up! +{bonus} coins -{5*lvlcnt} Wanted +{5*lvlcnt} Integrity")
        if(newrole != None):
           await self.ctx.send(f"Congratulations **{self.ctx.author.name}**! You have been promoted to {newrole}!")
        
        await self.ctx.send(f"You have successfully robbed {self.target}!\n+{self.money} black money +{rng} Wanted -{rng} Integrity")
        database.add_b_money(self.ctx.author.id, self.money)
        database.add_wanted(self.ctx.author.id, rng)
        database.remove_integrity(self.ctx.author.id, rng)
                

    @discord.ui.button(label="Not today", style = discord.ButtonStyle.primary)
    async def reject_callback(self, interaction: discord.Interaction, button: discord.ui.Button,):

        await interaction.response.defer()

        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view=self)

        await self.ctx.send("Coward")
        return


@commands.cooldown(1, 2*60, commands.BucketType.user)
@bot.command()
async def rob(ctx):
    info = database.get_user(ctx.author.id, ctx.author.name)

    if info["jail"] == 1:
        await ctx.send("You are a convict! Get out of jail first!!")
        return
    
    target = random.choice(messages.rob_targets)
    money = int(random.randint(100, 500)*database.money_multiplier(info["lvl"]))

    embed = discord.Embed()

    embed.add_field(name = '\u200b', value = f'Target - {target}')

    await ctx.send(embed = embed, view = robView(ctx, target, money))

class roleView(discord.ui.View):

    def __init__(self, ctx, role):
        super().__init__()
        self.ctx = ctx
        self.role = role

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("Not yours!", ephemeral = True)
            return False
        return True
    
    @discord.ui.button(label="Accept", style = discord.ButtonStyle.primary,)
    async def accept_callback(self, interaction: discord.Interaction, button: discord.ui.Button,):
    
        await interaction.response.defer()

        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view=self)

        if(self.role == "mob"):
            database.update_role(self.ctx.author.id, "associate")
            underboss_message = random.choice(messages.mob_welcome_messages)
            await self.ctx.send(f"**NPC Underboss: {underboss_message}")

        elif(self.role == "police"):
            database.update_role(self.ctx.author.id, "rookie")
            detective_message = random.choice(messages.police_welcome_messages)
            await self.ctx.send(f"**NPC Detective**: {detective_message}")

    @discord.ui.button(label="Reject", style = discord.ButtonStyle.primary,)
    async def reject_callback(self, interaction: discord.Interaction, button: discord.ui.Button,):

        await self.ctx.send("You rejected the offer.")


@bot.command()
async def join(ctx, arg):
    arg = arg.lower()
    info = database.get_user(ctx.author.id,ctx.author.name)
    role = info["user_role"]
    inven = database.get_inventory(ctx.author.id)
    wntd_lvl = info["wanted"]
    intg_lvl = info["integrity"]

    if(arg != "mob"  and arg != "police"):
        await ctx.send("You can either join the police or the mob, type sin join <mob/police>")
        return
    
    if info["jail"] == 1:
            await ctx.send("You are a convict! Get out of jail first!!")
            return
    
    elif(arg == "mob"):

        if (role == "associate" or role == "underboss" or role == "godfather"):
            await ctx.send("You're already in the mob!")
            return
        if (role == "rookie" or role == "detective" or role == "chief"):
            await ctx.send("A cop walked into a bar full of mob members and got beat up...")
            await asyncio.sleep(1)
            await ctx.send(f"That cop was you.\n-5000 coins")
            database.remove_money(ctx.author.id, 5000)
            return
        
        if (len(inven[0]) == 0):
            await ctx.send("You don't even own a gun! Scram!")
            return
        
        if(info["lvl"] < 10):
            await ctx.send("You can only join the mob after level 10!")
            return

        if(wntd_lvl < 70 or wntd_lvl < 2*intg_lvl):
            await ctx.send("We don't take goody two shoes!!")
            await ctx.send("You seem like a rat!")
            await ctx.send("They stole your money! -5000 coins")
            database.remove_money(ctx.author.id, 5000)
            return

        embed = discord.Embed()
        embed.add_field(name = "\u200b", value = "Want to join the mob?\nThere's no turning back after this")
        await ctx.send(embed = embed, view = roleView(ctx, "mob"))

    elif(arg == "police"):

        if(role == "rookie" or role == "detective" or role == "chief"):
            await ctx.send("You are already in the police!")
            return
        elif(role != "civilian"):
            await ctx.send(f"You got arrested by the police!\nWhat did you think was going to happen if a {info['user_role']} walks into a police station")
            database.update_jail(ctx.author.id, 1)
        else:

            if(wntd_lvl > 90):
                await ctx.send("The police arrested you!\nMaybe going to the police while being highly wanted wasn't a good idea...")
                database.update_jail(ctx.author.id, 1)
            elif(info["lvl"] < 10):
                await ctx.send("You can only join the police after level 10!")
            elif(intg_lvl < 40):
                await ctx.send("You don't seem trustworthy... maybe try again later")
            
            else:
                embed = discord.Embed()
    
                embed.add_field(name="Want to join the police? There's no turning back later", value="\u200b")
                await ctx.send(embed = embed, view=roleView(ctx, "police"))
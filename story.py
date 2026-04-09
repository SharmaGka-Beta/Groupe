import discord
import asyncio
import database
import battle

# -----------------------------------------------------------------------------------------------

class oldladyView(discord.ui.View):

    def __init__(self, ctx):
        super().__init__()
        self.ctx = ctx

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("This is not your choice!", ephemeral = True)
            return False
        return True
    
    @discord.ui.button(label="Request", style = discord.ButtonStyle.primary,)
    async def request_callback(self, interaction: discord.Interaction, button: discord.ui.Button,):

        await interaction.response.defer()
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view=self)

        await self.ctx.send("'No no I don't owe anything!'")
        embed = discord.Embed()
        embed.add_field(name = "\u200b", value = "She doesn't owe anything! This is extortion!")
        await self.ctx.send(embed = embed, view = oldladyView(self.ctx))

    @discord.ui.button(label="...", style = discord.ButtonStyle.primary,)
    async def callback(self, interaction: discord.Interaction, button: discord.ui.Button,):

        await interaction.response.defer()
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view=self)
    
        await self.ctx.send("There's no other choice...")
        await asyncio.sleep(3)
        await self.ctx.send("It's you or her...")
        await asyncio.sleep(3)
        await self.ctx.send("You slowly raise your gun...")
        await asyncio.sleep(3)
        await self.ctx.send("'Wait no i'll pay you! How much do you want??!! No wait please!!'")
        await asyncio.sleep(3)
        await self.ctx.send("It's you or her...")
        await asyncio.sleep(3)
        await self.ctx.send("'WAIT NO PLEASE HOW MUCH DO YO-'")
        await asyncio.sleep(2)
        await self.ctx.send('Silence')
        await asyncio.sleep(5)
        await self.ctx.send("Welcome to Sin City...")

        database.update_role(self.ctx.author.id, "associate")




class copView(discord.ui.View):

    def __init__(self, ctx):
        super().__init__()
        self.ctx = ctx

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("This is not your choice!", ephemeral = True)
            return False
        return True
    
    async def callback(self):

        await self.ctx.send("'I will never give this to the likes of you!'")
        await asyncio.sleep(2)
        await self.ctx.send("He pulls out a gun and shoot you!!")
        await asyncio.sleep(2)
        await self.ctx.send("'FUCK YOU!'")
        await self.ctx.send("He spits on you and slams the door shut")
        await asyncio.sleep(3)
        await self.ctx.send("You reach defeated back to the underboss's house")
        await asyncio.sleep(2)
        await self.ctx.send("'I'll give you another chance. But if you mess this up you're a goner'")
        await self.ctx.send("'Retrieve our money from this old-geezer down on fifth street'")
        await asyncio.sleep(4)
        await self.ctx.send("An old lady opens the door and invites you in")
        await asyncio.sleep(2)
        await self.ctx.send("'No no I don't owe any money!'")

        embed = discord.Embed()
        embed.add_field(name = "\u200b", value = "Grandma denies owing anything and you hear some truth in her voice")
        await self.ctx.send(embed = embed, view = oldladyView(self.ctx))




    @discord.ui.button(label="Ask Politely", style = discord.ButtonStyle.primary,)
    async def polite_callback(self, interaction: discord.Interaction, button: discord.ui.Button,):

        await interaction.response.defer()

        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view=self)
        await self.callback()

    @discord.ui.button(label="Grab it", style = discord.ButtonStyle.primary,)
    async def grab_callback(self, interaction: discord.Interaction, button: discord.ui.Button,):

        await interaction.response.defer()

        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view=self)
        await self.callback()
    




class trialView(discord.ui.View):

    def __init__(self, ctx):
        super().__init__()
        self.ctx = ctx

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("This is not your choice!", ephemeral = True)
            return False
        return True
    
    @discord.ui.button(label="Ready", style = discord.ButtonStyle.primary,)
    async def ready_callback(self, interaction: discord.Interaction, button: discord.ui.Button,):
        
        await interaction.response.defer()

        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view=self)

        await self.ctx.send("'Alright then. You have to retrive a package from a no good. Here's the address'")
        await asyncio.sleep(2)
        await self.ctx.send("You head down to the antique looking house and get a familiar feeling.")
        await asyncio.sleep(2)

        await self.ctx.send("You knock on the door and an ex-cop comes out!")
        await asyncio.sleep(2)
        
        embed = discord.Embed()
        embed.add_field(name = "\u200b", value = "You can see the package lying on his counter. What do you do?")
        await self.ctx.send(embed = embed, view = copView(self.ctx))


    @discord.ui.button(label="Cold Feet", style = discord.ButtonStyle.primary,)
    async def callback(self, interaction: discord.Interaction, button: discord.ui.Button,):
        
        await interaction.response.defer()

        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view=self)

        await self.ctx.send("You dare waste our time!")
        await self.ctx.send("The roughed you up!")
        database.remove_money(self.ctx.author.id, 100000)


#-----------------------------------------------------------------------------------------------


class aPromotionView(discord.ui.View):

    def __init__(self, ctx):
        super().__init__()
        self.ctx = ctx

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("This is not your choice!", ephemeral = True)
            return False
        return True
    

        
    @discord.ui.button(label="Ready", style = discord.ButtonStyle.primary,)
    async def ready_callback(self, interaction: discord.Interaction, button: discord.ui.Button,):
        await interaction.response.defer()

        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view=self)

        inven = database.get_inventory(self.ctx.author.id)
        if (len(inven[0]) == 0):
            await self.ctx.send("You don't even own a gun!")
            return
        

        async def win():

            await asyncio.sleep(2)
            await self.ctx.send("You head back to the family house")
            await self.ctx.send("'Impressive!! I think you are ready!'")

            await asyncio.sleep(2)

            await self.ctx.send("You were prooted to underboss!")
            await self.ctx.send("You now report directly to The Godfather")

            database.update_role(self.ctx.author.id, "underboss")
        
        async def lose():
            await asyncio.sleep(2)
            await self.ctx.send("You head back to the family house, defeated")
            await self.ctx.send("'You aren't ready yet...'")

        await self.ctx.send("You head to the rival family's base of operations")

        await self.ctx.send("Waiting for you is the underboss of the family!")

        await battle.sbattle(self.ctx, [[('pistol', 3), ('ar', 2), ('machinegun', 2), ('sniper', 1)], [('lsd', 5)], []], win, lose)


    
    @discord.ui.button(label="Nevermind", style = discord.ButtonStyle.primary,)
    async def callback(self, interaction: discord.Interaction, button: discord.ui.Button,):
        
        await interaction.response.defer()

        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view=self)

        await self.ctx.send("You dare waste our time!")
        await self.ctx.send("The roughed you up!")
        database.remove_money(self.ctx.author.id, 100000)




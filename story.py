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
        database.remove_wanted(self.ctx.author.id, 60)




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
        await self.ctx.send("You head down to the antique looking house.")
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
            database.remove_wanted(self.ctx.author.id, 60)
        
        async def lose():
            await asyncio.sleep(2)
            await self.ctx.send("You head back to the family house, defeated")
            await self.ctx.send("'You aren't ready yet...'")

        await self.ctx.send("You head to the rival family's base of operations")

        await self.ctx.send("Waiting for you is the underboss of the rival family!")

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

#-----------------------------------------------------------------------------------------------------

async def back_again(ctx):

    await ctx.send("You head to The Godfather's room")
    await asyncio.sleep(1)
    await ctx.send("'I need you to retrieve some important documents for me'")
    await asyncio.sleep(2)

    await ctx.send("As you head to the location you get a familiar feeling.")
    await asyncio.sleep(1)
    await ctx.send("It's the same cop's house you met all that while back!")
    await asyncio.sleep(1)
    await ctx.send("How long had it really been?")
    await asyncio.sleep(1)
    await ctx.send("Everything went by in a breeze but now it felt like an eternity...")
    await asyncio.sleep(1)
    await ctx.send("What could be in that package that's so important??")
    await asyncio.sleep(3)
    await ctx.send("The door opens and the cop steps out instantly recognizing you!")
    await asyncio.sleep(3)
    await ctx.send("'You again??!! I won't let you go this time!'")
    await ctx.send("He goes to grab his gun but you've come prepared this time.")
    await asyncio.sleep(3)


    async def win_battle():

        await ctx.send("The cop falls to the ground bleeding out...")
        await asyncio.sleep(1)
        await ctx.send("You head to the package still lying on the counter and extract the first document.")
        await asyncio.sleep(1)
        await ctx.send("A warrant against the godfather")
        await asyncio.sleep(1)
        await ctx.send("Seen plenty of those")
        await asyncio.sleep(3)

        await ctx.send("You take out the second document")
        await asyncio.sleep(1)
        await ctx.send("You start reading.")
        await asyncio.sleep(1)
        await ctx.send("It's a list of names each marked a number")
        await asyncio.sleep(2)

        await ctx.send("'Noah R. - 11'")
        await asyncio.sleep(0.5)
        await ctx.send("'Emily B. - 13'")
        await asyncio.sleep(0.5)
        await ctx.send("'Sarah S. - 9'")
        await asyncio.sleep(0.5)
        await ctx.send("'Lucas D. - 10'")
        await asyncio.sleep(0.5)

        await ctx.send("The list went on and on")
        await asyncio.sleep(1)
        await ctx.send("And suddenly you realised...")
        await asyncio.sleep(1)

        await ctx.send("You flip back to the warrant.")
        await asyncio.sleep(1)
        await ctx.send("Trafficking of minors...")
        await asyncio.sleep(2)
        await ctx.send("Children were always off limits...")
        await asyncio.sleep(2)

        await ctx.send("You head back to the house with the documents, passing the old lady's house on the way.")
        await asyncio.sleep(2)
        await ctx.send("'You were always my most trusted soldier!!'")
        await asyncio.sleep(2)
        await ctx.send("'You didn't read those did you?'")
        await asyncio.sleep(3)

        await ctx.send("'No...'")
        await asyncio.sleep(1)
        await ctx.send("'Well all right then I'll take those.'")
        await asyncio.sleep(1)
        await ctx.send("He starts walking towards you...")
        await asyncio.sleep(2)

        await ctx.send("It's the perfect opportunity...")
        await asyncio.sleep(2)
        await ctx.send("As he nears you, you feel the cold blade of the knife in your pocket...")
        await asyncio.sleep(2)

        await ctx.send("You step forward.")
        await asyncio.sleep(2)
        await ctx.send("'I can't thank you enou-'")
        await asyncio.sleep(2)
        await ctx.send("You drive the knife deep into his abdomen...")
        await asyncio.sleep(2)
        await ctx.send("His eyes widen.")
        await asyncio.sleep(2)

        await ctx.send("'You said-'")
        await asyncio.sleep(2)
        await ctx.send("You drive the knife deeper")
        await asyncio.sleep(2)
        await ctx.send("'-children were off limits'")
        await asyncio.sleep(2)

        await ctx.send("His body drops to the ground")
        await asyncio.sleep(2)
        await ctx.send("You turn around...")
        await asyncio.sleep(2)
        await ctx.send("You see the godfather's teenage daughter standing there with a gun")
        await asyncio.sleep(2)
        await ctx.send("'He trusted you...'")
        await asyncio.sleep(2)

        await ctx.send("You feel your own pistol in your pocket...")
        await asyncio.sleep(2)
        await ctx.send("But...")
        await asyncio.sleep(2)
        await ctx.send("Off limits...")
        await asyncio.sleep(2)
        await ctx.send("You or her...")
        await asyncio.sleep(2)
        await ctx.send("The old lady...")
        await asyncio.sleep(2)

        await ctx.send("'HE TRUSTED YOU!!'")
        await asyncio.sleep(2)
        await ctx.send("You or her...")
        await asyncio.sleep(2)

        await ctx.send("AND THIS IS WHAT YOU DID!!")
        await asyncio.sleep(2)
        await ctx.send("You or her...")
        await asyncio.sleep(2)
        await ctx.send("You reach for your gun")
        await asyncio.sleep(2)
        await ctx.send("You or her...")
        await asyncio.sleep(2)

        await ctx.send("HOW COULD YOU!! WHEN HE GAVE YOU SO MU-")
        await ctx.send("Silence")
        await asyncio.sleep(5)

        await ctx.send("The police arrived 30 mins later")
        await asyncio.sleep(1)
        await ctx.send("The godfather's body was found with a knife protruding from his abdomen")
        await asyncio.sleep(2)
        await ctx.send("5 feet away, your body was found with a bullet in your head...")
        await asyncio.sleep(1)
        await ctx.send("...inflicted from your own gun.")

        await asyncio.sleep(5)

        await ctx.send("Money: 1000")
        await ctx.send("Wanted: 0")
        await ctx.send("Integrity: 0")

        database.remove_money(ctx.author.id, 10000000000000)
        database.remove_b_money(ctx.author.id, 1000000000000)
        database.add_money(ctx.author.id, 1000)
        database.remove_wanted(ctx.author.id, 100)
        database.remove_integrity(ctx.author.id, 100)
        database.update_role(ctx.author.id, 'civilian')

        await ctx.send("Welcome back to sin city...")
        
    async def lose_battle():
        await ctx.send("You somehow get out alive")
        await ctx.send("'Those documents are very important!! Get them ASAP!!'")

    inven = [[('pistol', 1), ('shotgun', 1), ('ar', 1), ('machinegun', 1), ('sniper', 1)], [('heroin', 3)], []]
    await battle.sbattle(ctx, inven, win_battle, lose_battle)







from functions import bot
import discord
import copy
import database
import random

battle_state = {}
## {user_id: [user_health, bot_health, bot_inven, user_inven]}
## bot_inven: [guns, drugs, items]
##             [(damage%, name, uses)], [(heal%, name, qty)]

inven_map = {"pistol": [6, 2], "smg": [5, 7], "shotgun": [4, 10], "ar": [3, 20], "machinegun": [2, 30], "sniper": [1, 50],
        "weed": [0, 0.1], "lsd": [0, 0.2], "cocaine": [0, 0.3], "bluemeth": [0, 0.4], "heroin": [0, 0.5]}

total_health = None

guns = ["pistol", "smg", "shotgun", "ar", "machinegun", "sniper"]

def bot_item(uid):
    # item_cat = 0
    # a = random.random()

    # if (len(battle_state[uid][2][1]) != 0):
    #     if ((battle_state[uid][1]/100)**1.5 < a):
    #         item_cat = 1

    # item_index = None
    # options = battle_state[uid][2][item_cat]
    # size = len(options)
    # options.sort()
    # a = random.randint(1, 2)

    # if(size == 0):
    #     return ()

    # if (a == 1):
    #     item_index = size - 1
    # elif(a == 2):
    #     item_index = random.randint(0, max(0, size - 2))


    # battle_state[uid][2][item_cat][item_index][2] -= 1
    # item = battle_state[uid][2][item_cat][item_index][1]
    # health_points = battle_state[uid][2][item_cat][item_index][0]

    # if (battle_state[uid][2][item_cat][item_index][2] <= 0):
    #     battle_state[uid][item_cat].pop(item_index)

    # return (item, item_cat, health_points)\

    if (len(battle_state[uid][2][0]) == 0 and len(battle_state[uid][2][1]) == 0):
        return ()

    guns = battle_state[uid][2][0][:]
    guns.sort()
    
    one_shot = [gun for gun in guns if gun[0] >= battle_state[uid][0]]

    if (len(one_shot) > 0): 
        return (one_shot[0][1], 0, one_shot[0])
    
    drugs = battle_state[uid][2][1][:]
    drugs.sort()

    one_shot_bot = [gun for gun in battle_state[uid][3][0] if gun[0] >= battle_state[uid][1]]

    if (len(one_shot_bot) != 0):
        
        d = [drug for drug in drugs if battle_state[uid][1] + drug[0] <= 100]
        if(len(d) != 0):
            return (d[-1][1], 1, d[-1][0])
        
    item_cat = None
    if (len(battle_state[uid][2][0]) == 0):
        item_cat = 1
    elif(len(battle_state[uid][2][1]) == 0):
        item_cat = 0
    else:
        item_cat = random.randint(0, 1)

    if (item_cat == 0):
        sz = len(guns)
        if (guns[-1][1] == "sniper"):
            sz = max(1, sz - 1)
        
        a = random.randint(1, 10)
        if (a <= 7):
            return (guns[-1][1], 0, guns[-1][0])
        else:
            b = random.randint(0, max(0, sz - 2))
            return (guns[b][1], 0, guns[b][0])
    
    elif (item_cat == 1):

        options = [drug for drug in drugs if drug[0] + battle_state[uid][1] <= 100]
        if (len(options) != 0):
            d = random.choice(options)
            return (d[1], 1, d[0])
        
        if (len(battle_state[uid][2][0]) == 0):
            return (0)
        sz = len(guns)
        if (guns[-1][1] == "sniper"):
            sz = max(1, sz - 1)
        
        a = random.randint(1, 10)
        if (a <= 7):
            return (guns[-1][1], 0, guns[-1][0])
        else:
            b = random.randint(0, max(0, sz - 2))
            return (guns[b][1], 0, guns[b][0])
        




    

    
        
    



def bot_turn(uid, item_info):

    pass

class battleButton(discord.ui.Button):

    def __init__(self, name, ctx):
        super().__init__(label=name, style=discord.ButtonStyle.primary)
        self.name = name
        self.ctx = ctx

    async def callback(self, interaction: discord.Interaction):

        await interaction.response.defer()
        await self.ctx.send(self.name)

class backButton(discord.ui.Button):

    def __init__(self, ctx):
        super().__init__(label="Back", style=discord.ButtonStyle.primary)
        self.ctx = ctx

    async def callback(self, interaction: discord.Interaction):

        embed = discord.Embed()

        embed.add_field(name = "\u200b", value = f"Your health = {battle_state[self.ctx.author.id][0]:.2f}", inline = False)
        embed.add_field(name = "\u200b", value = f"Opponent health = {battle_state[self.ctx.author.id][1]:.2f}", inline = False)

        await interaction.response.edit_message(embed = embed, view = battleView(self.ctx))

        


class gunView(discord.ui.View):


    def __init__(self, ctx):
        super().__init__()
        self.ctx = ctx
        for i in battle_state[ctx.author.id][3][0]:
            self.add_item(battleButton(i[1].capitalize(), self.ctx))

        self.add_item(backButton(self.ctx))

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("Not your battle!", ephemeral = True)
            return False
        return True 
    
class drugView(discord.ui.View):


    def __init__(self, ctx):
        super().__init__()
        self.ctx = ctx
        for i in battle_state[ctx.author.id][3][1]:
            self.add_item(battleButton(i[1].capitalize(), self.ctx))

        self.add_item(backButton(self.ctx))
        
    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("Not your battle!", ephemeral = True)
            return False
        return True 

class itemView(discord.ui.View):


    def __init__(self, ctx):
        super().__init__()
        self.ctx = ctx
        for i in battle_state[ctx.author.id][3][2]:
            self.add_item(battleButton(i[1].capitalize(), self.ctx))

        self.add_item(backButton(self.ctx))
 
    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("Not your battle!", ephemeral = True)
            return False
        return True 
    

class battleView(discord.ui.View):

    def __init__(self, ctx):
        super().__init__()
        self.ctx = ctx

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("Not your battle!", ephemeral = True)
            return False
        return True   
    
    @discord.ui.button(label="Guns", style = discord.ButtonStyle.primary)
    async def guns_callback(self, interaction: discord.Interaction, button: discord.ui.Button,):

        embed = discord.Embed()
        embed.add_field(name = "Weapon", value = "\u200b")
        embed.add_field(name = "Damage", value = "\u200b")
        embed.add_field(name = "Bullets", value = "\u200b")

        for i in battle_state[self.ctx.author.id][3][0]:
            
            embed.add_field(name = "\u200b", value = f"{i[1]}")
            embed.add_field(name = "\u200b", value = f"{i[0]}")
            embed.add_field(name = "\u200b", value = f"{i[2]}")

        await interaction.response.edit_message(embed=embed, view = gunView(self.ctx))

    @discord.ui.button(label="Drugs", style = discord.ButtonStyle.primary)
    async def drugs_callback(self, interaction: discord.Interaction, button: discord.ui.Button,):

        embed = discord.Embed()
        embed.add_field(name = "Drug", value = "\u200b")
        embed.add_field(name = "Heal", value = "\u200b")
        embed.add_field(name = "Qty", value = "\u200b")

        for i in battle_state[self.ctx.author.id][3][1]:
            
            embed.add_field(name = "\u200b", value = f"{i[1]}")
            embed.add_field(name = "\u200b", value = f"{i[0]:.2f}")
            embed.add_field(name = "\u200b", value = f"{i[2]}")

        await interaction.response.edit_message(embed=embed, view = drugView(self.ctx))

    @discord.ui.button(label="Items", style = discord.ButtonStyle.primary)
    async def items_callback(self, interaction: discord.Interaction, button: discord.ui.Button,):

        embed = discord.Embed()
        embed.add_field(name = "Item", value = "\u200b")
        embed.add_field(name = "Use", value = "\u200b")
        embed.add_field(name = "Qty", value = "\u200b")

        for i in battle_state[self.ctx.author.id][3][2]:
            
            embed.add_field(name = "\u200b", value = f"{i[1]}")
            embed.add_field(name = "\u200b", value = f"{i[0]}")
            embed.add_field(name = "\u200b", value = f"{i[2]}")
        
        await interaction.response.edit_message(embed=embed, view = itemView(self.ctx))

    @discord.ui.button(label = "Back", style = discord.ButtonStyle.primary)
    async def back_callback(self, interaction: discord.Interaction, button: discord.ui.Button,):

        embed = discord.Embed()

        embed.add_field(name = "\u200b", value = f"Your health = {battle_state[self.ctx.author.id][0]:.2f}", inline = False)
        embed.add_field(name = "\u200b", value = f"Opponent health = {battle_state[self.ctx.author.id][1]:.2f}", inline = False)

        await interaction.response.edit_message(embed = embed, view = battleView(self.ctx))
        

        



@bot.command()
async def battle(ctx):

    info = database.get_user(ctx.author.id)

    if (info["user_role"] == 'civilian'):
        await ctx.send("Civilians don't battle!")
        return
    
    if (info["jail"] == 1):
        await ctx.send("You're a convict! Get out of jail first!")
        return

    inven = database.get_inventory(ctx.author.id)

    if (len(inven[0]) == 0):
        await ctx.send("You don't even own a gun!")
        return
    
    dmg = 0

    for i in inven[0]:
        temp = inven_map[i[0]]
        dmg = dmg + temp[0]*temp[1]
    
    battle_inven = [inven[0], inven[1], inven[2]]

    dmg = 3*dmg/4
    for i in battle_inven:
        if len(i) == 0:
            continue
        for j in range(len(i)):
            uses = inven_map[i[j][0]][0]
            amount = inven_map[i[j][0]][1]
            if (uses == 0):
                uses = i[j][1]
                amount = dmg*inven_map[i[j][0]][1]
            i[j] = (amount, i[j][0], uses)

    battle_state[ctx.author.id] = [dmg, dmg, copy.deepcopy(battle_inven), battle_inven]

    global total_health
    total_health = dmg

    embed = discord.Embed()

    embed.add_field(name = "\u200b", value = f"Your health = {battle_state[ctx.author.id][0]:.2f}", inline = False)
    embed.add_field(name = "\u200b", value = f"Opponent health = {battle_state[ctx.author.id][1]:.2f}", inline = False)

    await ctx.send(embed = embed, view = battleView(ctx))


    



    

    

    
    


    

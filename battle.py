from functions import bot
import discord
import copy
import database
import random

battle_state = {}
## {user_id: [user_health, bot_health, bot_inven, user_inven]}
## bot_inven: [guns, drugs, items]
##             [(damage%, name, uses)], [(heal%, name, qty)]

map = {"pistol": [6, 2], "smg": [5, 7], "shotgun": [4, 10], "ar": [3, 20], "machinegun": [2, 30], "sniper": [1, 50],
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
        temp = map[i[0]]
        dmg = dmg + temp[0]*temp[1]
    
    battle_inven = [inven[0], inven[1], inven[2]]

    for i in battle_inven:
        if len(i) == 0:
            continue
        for j in range(len(i)):
            uses = map[i[j][0]][0]
            amount = map[i[j][0]][1]
            if (uses == 0):
                uses = i[j][1]
                amount = dmg*map[i[j][0]][1]
            i[j] = (amount, i[j][0], uses)

    battle_state[ctx.author.id] = [dmg, dmg, copy.deepcopy(battle_inven), battle_inven]
    dmg = 3*dmg/4

    global total_health
    total_health = dmg

    



    

    

    
    


    

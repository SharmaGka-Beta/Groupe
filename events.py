import random
import database
import messages

def police_catch(ctx, heat, random: True):
    if(random):
        info = database.get_user(ctx.author.id, ctx.author.name)
        catch_roll = max(0, info['wanted'] - 10 + heat)
        if (random.random() >= (catch_roll/100)**2):
            return 0
        else:
            database.update_jail(ctx.author.id, 1)
            return 1
    
    # await ctx.send("You have been captured by the police!")
    # await ctx.send("You can bribe, run, talk or give bail")
    else:
        database.update_jail(ctx.author.id, 1)

def it_raid(ctx):
    info = database.get_user(ctx.author.id, ctx.author.name)
    heat = info["wanted"]/100
    exposure = min(info["b_money"]/5000000, 1)
    if(random.random() <= (heat+exposure)/2):
        return True

def summon(ctx, danger, money):

    if (random.random() >= danger/10):
        return 0
    
    if (danger > 5):
        if (random.random() > 0.95):
            database.remove_wanted(ctx.author.id, money//1000)
            return 2
        database.remove_wanted(ctx.author.id, money//1000)
        
    else:
        database.remove_wanted(ctx.author.id, money//2000)
        

    return 1
    


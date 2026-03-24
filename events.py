import random
import database
import messages

async def police_catch(ctx):
    info = database.get_user(ctx.author.id)
    catch_roll = info['wanted']
    if (random.random() <= (catch_roll/100)**2):
        return 0
    
    await ctx.send("You have been captured by the police!")
    await ctx.send("You can bribe, run, talk or give bail")

    database.update_jail(ctx.author.id, 1)

    return 1


    
    


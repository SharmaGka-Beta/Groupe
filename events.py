import random
import database
import messages

async def police_catch(ctx):
    info = database.get_user(ctx.author.id)
    catch_roll = info['wanted']
    if (catch_roll <= random.randint(1, 100)):
        return 0
    
    await ctx.send("You have been captured by the police!")
    await ctx.send("You can bribe, run or talk it out")

    database.update_role(ctx.author.id, 1)

    return 1


    
    


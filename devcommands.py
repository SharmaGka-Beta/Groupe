from functions import bot
import events
import database
import battle

@bot.command()
async def catch(ctx):
    events.police_catch(ctx)
    await ctx.send("Done")

@bot.command()
async def wanted(ctx, arg):
    database.add_wanted(ctx.author.id, arg)
    await ctx.send("Done")

@bot.command()
async def integrity(ctx, arg):
    database.add_integrity(ctx.author.id, arg)
    await ctx.send("Done")

@bot.command()
async def getcaught(ctx):
    database.update_jail(ctx.author.id, 1)
    await ctx.send("Done")

@bot.command()
async def getout(ctx):
    database.update_jail(ctx.author.id, 0)
    await ctx.send("Done")

@bot.command()
async def addmoney(ctx, arg: int):
    database.add_money(ctx.author.id, arg)
    await ctx.send("Done")

@bot.command()
async def remwanted(ctx):
    database.remove_wanted(ctx.author.id, 20)
    await ctx.send("Done")

@bot.command()
async def remintegrity(ctx):
    database.remove_integrity(ctx.author.id, 20)
    await ctx.send("Done")

@bot.command()
async def change_role(ctx, arg: str = "civilian"):
    database.update_role(ctx.author.id, arg)
    await ctx.send("Done")

@bot.command()
async def change_blackmoney(ctx, arg: int):
    if(arg > 0):
        database.add_b_money(ctx.author.id, arg)
    else:
        database.remove_b_money(ctx.author.id, -arg)

@bot.command()
async def removecd(ctx):
    for command in bot.commands:
        command.reset_cooldown(ctx)
    await ctx.send("Done")

@bot.command()
async def win_battle(ctx):
    if (ctx.author.id in battle.battle_state):
        battle.battle_state[ctx.author.id][1] = 0
        await ctx.send("Done")
        return
    await ctx.send("No battle found")

@bot.command()
async def lose_battle(ctx):
    if (ctx.author.id in battle.battle_state):
        battle.battle_state[ctx.author.id][0] = 0
        await ctx.send("Done")
        return
    await ctx.send("No battle found")

@bot.command()
async def add_xp(ctx, amount: int):
    database.add_xp(ctx.author.id, amount)
    await ctx.send(f"Added {amount} xp")

@bot.command()
async def add_lvl(ctx, amount: int):
    database.add_lvl(ctx.author.id, amount)
    await ctx.send(f"Added {amount} levels")
    

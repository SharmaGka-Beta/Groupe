from functions import bot
import events
import database

@bot.command()
async def catch(ctx):
    events.police_catch(ctx)
    await ctx.send("Done")

@bot.command()
async def wanted(ctx):
    database.add_wanted(ctx.author.id, 100)
    await ctx.send("Done")

@bot.command()
async def integrity(ctx):
    database.add_integrity(ctx.author.id, 100)
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
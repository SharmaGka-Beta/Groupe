from functions import bot
import events
import database

@bot.command()
async def catch(ctx):
    await events.police_catch(ctx)

@bot.command()
async def w(ctx):
    database.add_wanted(ctx.author.id, 100)

@bot.command()
async def getcaught(ctx):
    database.update_jail(ctx.author.id, 1)

@bot.command()
async def u(ctx, arg: int = 0):
    database.update_jail(ctx.author.id, arg)

@bot.command()
async def m(ctx, arg: int):
    database.add_money(ctx.author.id, arg)

@bot.command()
async def wl(ctx):
    database.remove_wanted(ctx.author.id, -20)
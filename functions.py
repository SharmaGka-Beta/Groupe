import discord
from discord.ext import commands
import database
import random
import messages
import events

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix = "sin ", intents = intents)

@bot.event
async def on_ready():
    print("Bot is ready")
    database.create_tables()

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("I don't recognize that command. Type 'sin help' to view all commands")
    elif isinstance(error, commands.CommandOnCooldown):
        totaltime = error.retry_after
        hours = totaltime//3600
        minutes = (totaltime%3600)//60
        seconds = totaltime%60
        await ctx.send(f"Slow down! You just did {ctx.command}, try after {int(hours)}hrs {int(minutes)}mins {int(seconds)}s")
    elif isinstance(error, commands.UserInputError):
        await ctx.send("Your command format is incorrect. Type 'sin help' to view the command formats.")
    else:
        await ctx.send(f"error: {error}") # temporarily print all errors


@bot.command()
async def profile(ctx, member:discord.Member = None):
    if member == None:
        member = ctx.author             #you can get profile of other users too. defaults to self
    uid = member.id
    info = database.get_user(uid, ctx.author.name)
    
    embed = discord.Embed(title=f"{ctx.author.name} — {info['user_role'].upper()}", color=messages.role_colors[info["user_role"]])
    
    embed.set_thumbnail(url=member.display_avatar.url)

    embed.add_field(name="**MONEY**", value=f"__🪙 **Coins**:__ {info["money"]:,}\n💸 __**Black Money**:__ {info["b_money"]:,}", inline=False)

    embed.add_field(name="**STATS**", value=f"📈__**Level**__: {info["lvl"]}\n✨__**XP**__: {info["xp"]}/{int(100*(info["lvl"]**1.5))}\n🔥 __**Wanted**__: {info["wanted"]}\n 🤝__**Integrity**__: {info["integrity"]}", inline=False)

    await ctx.send(embed=embed)



class invenView(discord.ui.View):
    def __init__(self, ctx, inven):
        super().__init__()
        self.ctx = ctx
        self.inven = inven

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("Not your inventory!", ephemeral = True)
            return False
        return True
    

    #different buttons for all item types

    @discord.ui.button(label="Guns", style = discord.ButtonStyle.primary)
    async def gun_callback(self, interaction: discord.Interaction, button: discord.ui.Button,):

        embed = discord.Embed(title = "GUNS", color = discord.Color.brand_red())

        for item in self.inven[0]:
            a = None
            for i in messages.items_gun:
                if i[0].lower() == item[0]:             #selling cost of item will be half of buying cost
                    a = str(int(int(i[1])/2))
                    break
            embed.add_field(name = f"\u200b" , value=f"{item[0].capitalize()} | 🪙 {a} | Qty - {str(item[1])}", inline=False)

        await interaction.response.edit_message(embed = embed, view = invenView(self.ctx, self.inven))

    @discord.ui.button(label="Drugs", style = discord.ButtonStyle.primary)
    async def drug_callback(self, interaction: discord.Interaction, button: discord.ui.Button,):

        embed = discord.Embed(title = "DRUGS", color = discord.Color.brand_red())

        for item in self.inven[1]:
            a = None
            for i in messages.items_drugs:
                if i[0].lower() == item[0]:
                    a = str(int(int(i[1])/2))
                    break
            embed.add_field(name = f"\u200b" , value=f"{item[0].capitalize()} | 🪙 {a} | Qty - {str(item[1])}", inline=False)

        await interaction.response.edit_message(embed = embed, view = invenView(self.ctx, self.inven))

    @discord.ui.button(label="Items", style = discord.ButtonStyle.primary)
    async def item_callback(self, interaction: discord.Interaction, button: discord.ui.Button,):

        embed = discord.Embed(title = "ITEMS", color = discord.Color.brand_red())

        for item in self.inven[2]:
            a = None
            for i in messages.items_items:
                if i[0].lower() == item[0]:
                    a = str(int(int(i[1])/2))
                    break
            embed.add_field(name = f"\u200b" , value=f"{item[0].capitalize()} | 🪙 {a} | Qty - {str(item[1])}", inline=False)

        await interaction.response.edit_message(embed = embed, view = invenView(self.ctx, self.inven))
    
    
@bot.command()
async def inventory(ctx):

    database.add_user(ctx.author.id, ctx.author.name)
    inven = database.get_inventory(ctx.author.id)
    embed = discord.Embed(title = "GUNS", color = discord.Color.brand_red())

    for item in inven[0]:
        a = None
        for i in messages.items_gun:
            if i[0].lower() == item[0]:             #start with gun inventory and provide buttons
                a = str(int(int(i[1])/2))
                break
        embed.add_field(name = f"\u200b" , value=f"{item[0].capitalize()} | 🪙 {a} | Qty - {str(item[1])}", inline=False)

    
    await ctx.send(embed = embed, view = invenView(ctx, inven))

@bot.command()
async def sell(ctx, item, qty: int = 1):            #qty defaults to 1

    info = database.get_user(ctx.author.id, ctx.author.name)

    if info["jail"] == 1:
        await ctx.send("You are a convict! Get out of jail first!!")        #no selling in jail
        return
    
    inven = database.get_inventory(ctx.author.id)

    item = item.lower()             #case insensitive
    qty_owned = None
    price = None

    for it in messages.items:
        if (item == it[0].lower()):                 #see price from messages.items if change in price it will reflect throught just by changing there
            price = int(int(it[1])/2)
            break
    else:
        await ctx.send("Enter a valid item!!")
        return

    t = -1  
    cat = None

    for i in inven:                 #inven = [guns, drugs, items]
        t = t + 1
        for a in i:
            if a[0].lower() == item:    #check in each and get qty
                qty_owned = a[1]
                cat = t                 #category of item for database manipulation
                break                   #item found
        else:
            continue                    #if for loop breaks naturally else executes and continues to next index
        break                           #if found then break
    else:                               #if outer loop breaks naturally item not found
        await ctx.send(f"You don't own {item}!!")
        return

    if(qty <= 0):                       
        await ctx.send("Enter a valid quantity of items!")      #-ve check
        return
    
    if (qty > qty_owned):
        if (qty_owned == 1):
            await ctx.send(f"You only own {qty_owned} {item}. Defaulting to 1.")
            qty = 1
        else:
            await ctx.send(f"You only own {qty_owned} {item}s. Defaulting to {qty_owned}.")
            qty = qty_owned

    cat_map = {0: "ammunitions", 1: "drugs", 2: "others"}           #map cat to string
    database.update_inventory(ctx.author.id, item, cat_map[cat], -qty)      #remove from inven
    database.add_money(ctx.author.id, price*qty)
    
    await ctx.send("Sale Successful!")
    await ctx.send(f"You gained {price*qty} coins")

class shop_view(discord.ui.View):
    

    #different buttons for each item same as inven

    @discord.ui.button(label="Guns", style = discord.ButtonStyle.primary)
    async def gun_callback(self, interaction: discord.Interaction, button: discord.ui.Button,):

        embed = discord.Embed(title = "GUN SHOP", color = discord.Color.brand_red())
    
        embed.add_field(name="Welcome to Sin City Gun Shop! Buy any item with 'sin buy'", value = "\u200b" ,inline=False)

        for item in messages.items_gun:
            embed.add_field(name = f"{item[4]}__{item[0]}__ | 🪙 {item[1]}" , value=item[2], inline=False)

        await interaction.response.edit_message(embed = embed, view = shop_view())

        

    @discord.ui.button(label="Drugs", style = discord.ButtonStyle.primary)
    async def drugs_callback(self, interaction: discord.Interaction, button: discord.ui.Button,):

        embed = discord.Embed(title = "DRUG SHOP", color = discord.Color.brand_red())
    
        embed.add_field(name="Welcome to Sin City Drug Shop! Buy any item with 'sin buy'", value = "\u200b" ,inline=False)

        for item in messages.items_drugs:
            embed.add_field(name = f"{item[4]}__{item[0]}__ | 🪙 {item[1]}" , value=item[2], inline=False)

        await interaction.response.edit_message(embed = embed, view = shop_view())

    @discord.ui.button(label="Items", style = discord.ButtonStyle.primary)
    async def items_callback(self, interaction: discord.Interaction, button: discord.ui.Button,):

        embed = discord.Embed(title = "ITEM SHOP", color = discord.Color.brand_red())
    
        embed.add_field(name="Welcome to Sin City Item Shop! Buy any item with 'sin buy'", value = "\u200b" ,inline=False)

        for item in messages.items_items:
            embed.add_field(name = f"{item[4]}__{item[0]}__ | 🪙 {item[1]}" , value=item[2], inline=False)

        await interaction.response.edit_message(embed = embed, view = shop_view())   

@bot.command()
async def shop(ctx):
    database.add_user(ctx.author.id, ctx.author.name)
    
    embed = discord.Embed(title = "GUN SHOP", color = discord.Color.brand_red())    #start at gun same as inven
    
    embed.add_field(name="Welcome to Sin City Gun Shop! Buy any item with 'sin buy'", value = "\u200b" ,inline=False)

    for item in messages.items_gun:
        embed.add_field(name = f"{item[4]}__{item[0]}__ | 🪙 {item[1]}" , value=item[2], inline=False)

    await ctx.send(embed = embed, view = shop_view())

class leaderboard_view(discord.ui.View):

    @discord.ui.button(label="Coins", style = discord.ButtonStyle.primary)
    async def coins_callback(self, interaction: discord.Interaction, button: discord.ui.button):
        embed = discord.Embed(title="Coins Leaderboard", color=discord.Color.brand_red())

        player_info = database.get_leaderboard("money")
        i = 0
        for player in player_info:
            i += 1
            embed.add_field(name=f"{i}. {player[7]}: {player[1]}", value="\u200b")
        await interaction.response.edit_message(embed = embed, view = leaderboard_view())

    @discord.ui.button(label="Wanted", style = discord.ButtonStyle.primary)
    async def wanted_callback(self, interaction: discord.Interaction, button: discord.ui.button):
        embed = discord.Embed(title="Wanted Leaderboard", color=discord.Color.brand_red())

        player_info = database.get_leaderboard("wanted")
        i = 0
        for player in player_info:
            i += 1
            embed.add_field(name=f"{i}. {player[7]}: {player[2]}", value="\u200b")
        await interaction.response.edit_message(embed = embed, view = leaderboard_view())

    @discord.ui.button(label="Integrity", style = discord.ButtonStyle.primary)
    async def integrity_callback(self, interaction: discord.Interaction, button: discord.ui.button):
        embed = discord.Embed(title="Integrity Leaderboard", color=discord.Color.brand_red())

        player_info = database.get_leaderboard("integrity")
        i = 0
        for player in player_info:
            i += 1
            embed.add_field(name=f"{i}. {player[7]}: {player[3]}", value="\u200b")
        await interaction.response.edit_message(embed = embed, view = leaderboard_view())
    
    @discord.ui.button(label="Black Money", style = discord.ButtonStyle.primary)
    async def black_callback(self, interaction: discord.Interaction, button: discord.ui.button):
        embed = discord.Embed(title="Black Money Leaderboard", color=discord.Color.brand_red())

        player_info = database.get_leaderboard("b_money")
        i = 0
        for player in player_info:
            i += 1
            embed.add_field(name=f"{i}. {player[7]}: {player[6]}", value="\u200b")
        await interaction.response.edit_message(embed = embed, view = leaderboard_view())
        
@bot.command()
async def leaderboard(ctx):
    database.add_user(ctx.author.id, ctx.author.name)

    embed = discord.Embed(title="Coins Leaderboard", color=discord.Color.brand_red())

    player_info = database.get_leaderboard("money")
    i = 0
    for player in player_info:
        i += 1
        embed.add_field(name=f"{i}. {player[7]}: {player[1]}", value="\u200b")

    await ctx.send(embed = embed, view = leaderboard_view())


@bot.command()
async def transfer(ctx, amount:int , member:discord.Member):        #send to another player
    info = database.get_user(ctx.author.id, ctx.author.name)
    if info["jail"] == 1:
        await ctx.send("You are a convict! Get out of jail first!!")        #jail check
        return
    
    if info["money"] < amount:
        await ctx.send("You don't have the required funds")
        return

    payer=ctx.author.id
    receiver=member.id
    database.add_money(receiver,amount)
    database.remove_money(payer,amount)

    await ctx.send(f'{amount} has been sent to {member.display_name}')
    

@bot.command()
async def buy(ctx, item, qty:int = 1):
    info = database.get_user(ctx.author.id, ctx.author.name)

    if info["jail"] == 1:
        await ctx.send("You are a convict! Get out of jail first!!")
        return

    item = item.lower()     #case insensitive

    if(qty <= 0):
        await ctx.send("Enter a valid quantity of items!")
        return
    for it in messages.items:
        if(item == it[0].lower()):
            if(qty*int(it[1]) > info["money"]):
                await ctx.send("Balance Insufficient!")
                return
            database.update_inventory(ctx.author.id, it[0].lower(), it[3], qty)
            database.remove_money(ctx.author.id, qty*int(it[1]))
            
            await ctx.send(f"{qty} {item}(s) bought successfully!")     #bough
            
                
            return

    await ctx.send("Enter a valid item name!")

@commands.cooldown(1, 60, commands.BucketType.user)
@bot.command()
async def talk(ctx):
    info = database.get_user(ctx.author.id, ctx.author.name)
    
    if(info["jail"] == 1):
        respect = info["integrity"]                     #try to negotiate with cops
        if(random.random() < (respect/100)**2):         #prob proportional to square of respect
            await ctx.send(random.choice(messages.cop_messages_positive))
            database.update_jail(ctx.author.id, 0)
        else:
            await ctx.send(random.choice(messages.cop_messages_negative))
            database.remove_integrity(ctx.author.id, 5)
            await ctx.send("-5 Integrity")              #prevent spam
    else:
        await ctx.send("You are not even jail, do you just enjoy talking to cops?")

@commands.cooldown(1, 30, commands.BucketType.user)
@bot.command()
async def bribe(ctx, arg: int):
    info = database.get_user(ctx.author.id, ctx.author.name)

    if info["jail"] != 1:
        await ctx.send("You're not a convict!")
        return
    
    if (arg <= 0):
        await ctx.send("You think this is a joke!!")        #f around and find out
        await ctx.send("The cop roughed you up.")
        await ctx.send("-500 coins")
        database.remove_money(ctx.author.id, 500)
        return

    if (arg > info["money"]):
        await ctx.send("Insufficient balance")
        return
    
    database.remove_money(ctx.author.id, arg)
    await ctx.send(f"-{arg} coins")

    arg = arg/10000

    if (random.random() <= arg):
        database.update_jail(ctx.author.id, 0)
        await ctx.send("Alright we'll let you go this time")        #bribe prob related to money
        await ctx.send("-10 Wanted\n-10 Integrity")
        database.remove_integrity(ctx.author.id, 10)                #10k = 100%, 5k = 50%
        database.remove_wanted(ctx.author.id, 10)
        return
    
    await ctx.send("Not enough!!")

@commands.cooldown(1, 30, commands.BucketType.user)
@bot.command()
async def bail(ctx):
    info = database.get_user(ctx.author.id, ctx.author.name)

    if info["jail"] != 1:
        await ctx.send("You're not a convict!")
        return
    
    if (info["money"] < 100000):                                     #bail set at 100k
        await ctx.send("Insufficient Balance")
        return

    
    database.remove_money(ctx.author.id, 100000)
    await ctx.send("Released")
    database.update_jail(ctx.author.id, 0)
    database.remove_wanted(ctx.author.id, 10)

    
@commands.cooldown(1, 60, commands.BucketType.user)
@bot.command()
async def run(ctx):                                 #run purely based on rng. 5% chance
    info = database.get_user(ctx.author.id, ctx.author.name)

    if  info["jail"]==0:
        await ctx.send("🤨 You're not even in jail, why are you running?")
        return
    
    run_yes=random.randint(1,100)
    if(0<run_yes<=5):
        await ctx.send( f"🏃 **{ctx.author.name} made a run for it!**\n"
            f"The guards were distracted... you slipped through the fence and escaped! "
            f"You're free! For now. 😈")
        database.update_jail(ctx.author.id,0)
        database.remove_wanted(ctx.author.id,10)
    
    else: 
        await ctx.send(
            f"🚨 **{ctx.author.name} tried to escape... and got caught!**\n"
            f"The guards tackled you back to your cell. Better luck next time. 🔒"
        )

@commands.cooldown(1, 1*60*60, commands.BucketType.user) #1 hr cooldown
@bot.command()
async def launder(ctx, arg: int):
    info = database.get_user(ctx.author.id, ctx.author.name)

    if(info["jail"]):
        await ctx.send("You are in jail! The only laundering you can do here is for your clothes")
        return
    if(arg > info["b_money"]):
        await ctx.send("You aren't that rich pal, you can't launder air")
        return
    if(arg <= 0):
        await ctx.send("The magic laundering machine turned into a blackhole and swallowed your black money!")
        await ctx.send(f"-{int(0.05*info["b_money"])} coins")
        database.remove_b_money(ctx.author.id, 0.05*info["b_money"])
        return
    if(events.it_raid(ctx)):
        await ctx.send("You got set up by the IRS! They sent you to jail...")
        await ctx.send(f"-{int((info["wanted"]/100)*info["b_money"])}")
        database.update_jail(ctx.author.id, 1)
        database.remove_b_money(ctx.author.id, int((info["wanted"]/100)*info["b_money"]))
        return
    
    fee = info["wanted"]/200
    await ctx.send(f"You succesfully laundered {arg} coins. You got {int(arg*(1-fee))} legal money")
    database.remove_b_money(ctx.author.id, arg)
    database.add_money(ctx.author.id, arg*(1-fee))

@bot.command()
async def cooldowns(ctx):
    embed = discord.Embed()

    messages = []
    
    for command in bot.commands:
        if command.cooldown is None:
            continue
        cooldown = command.get_cooldown_retry_after(ctx)
        if cooldown > 0:
            hr = int(cooldown//3600)
            min = int((cooldown%3600)//60)
            s = int(cooldown%60)

            embed.add_field(name=f"```{command.name}```", value=f"{hr}hrs {min}mins {s}s", inline=False)
        else:
            embed.add_field(name=f"```{command.name}```", value=f"✅ Available", inline=False) 

    if len(embed.fields) == 0:
        await ctx.send("No active cooldowns!")
        return
    
    embed.set_author(name=f"{ctx.author.name}'s ~ cooldowns", icon_url=ctx.author.avatar.url)
    await ctx.send(embed = embed)

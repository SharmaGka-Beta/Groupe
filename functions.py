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
    elif isinstance(error, commands.UserInputError):
        await ctx.send("Your command format is incorrect. Type 'sin help' to view the command formats.")


@bot.command()
async def profile(ctx):
    info = database.get_user(ctx.author.id)
    embed = discord.Embed(title="Welcome to Sin City!", color= discord.Color.brand_red())

    embed.set_thumbnail(url=ctx.author.display_avatar.url)
    embed.add_field(name="\u200b", value="PLAYER INFO", inline=True)
    embed.add_field(name="\u200b", value=f"👤 Player Name: {ctx.author.name}", inline=False)
    embed.add_field(name="\u200b", value=f"🪙 Balance: {info["money"]}", inline=False)
    # embed.add_field(name="\u200b", value=f"🆙 Level: {info["level"]}", inline=False)


    embed.add_field(name="\u200b", value=f"🔥 WANTED METER: {info["wanted"]}", inline=False)
    embed.add_field(name="\u200b", value=f"📈 RESPECT METER: {info["integrity"]}", inline=False)
    embed.add_field(name="\u200b", value=f"🪪 ROLE: {info["user_role"]}", inline=False)

    await ctx.send(embed=embed)



class invenView(discord.ui.View):
    def __init__(self, ctx, inven):
        super().__init__()
        self.ctx = ctx
        self.inven = inven

    @discord.ui.button(label="Guns", style = discord.ButtonStyle.primary)
    async def gun_callback(self, interaction: discord.Interaction, button: discord.ui.Button,):

        embed = discord.Embed(title = "GUNS", color = discord.Color.brand_red())

        for item in self.inven[0]:
            a = None
            for i in messages.items_gun:
                if i[0][2:].lower() == item[0]:
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
                if i[0][2:].lower() == item[0]:
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
                if i[0][2:].lower() == item[0]:
                    a = str(int(int(i[1])/2))
                    break
            embed.add_field(name = f"\u200b" , value=f"{item[0].capitalize()} | 🪙 {a} | Qty - {str(item[1])}", inline=False)

        await interaction.response.edit_message(embed = embed, view = invenView(self.ctx, self.inven))
    
    
@bot.command()
async def inventory(ctx):

    database.add_user(ctx.author.id)
    inven = database.get_inventory(ctx.author.id)
    embed = discord.Embed(title = "GUNS", color = discord.Color.brand_red())

    for item in inven[0]:
        a = None
        for i in messages.items_gun:
            if i[0][2:].lower() == item[0]:
                a = str(int(int(i[1])/2))
                break
        embed.add_field(name = f"\u200b" , value=f"{item[0].capitalize()} | 🪙 {a} | Qty - {str(item[1])}", inline=False)

    
    await ctx.send(embed = embed, view = invenView(ctx, inven))

@bot.command()
async def sell(ctx, item, qty: int = 1):

    info = database.get_user(ctx.author.id)

    if info["jail"] == 1:
        await ctx.send("You are a convict! Get out of jail first!!")
        return
    
    inven = database.get_inventory(ctx.author.id)

    item = item.lower()
    qty_owned = None
    price = None

    for it in messages.items:
        if (item == it[0][2:].lower()):
            price = int(int(it[1])/2)
            db_item = it[0][2:]
            break
    else:
        await ctx.send("Enter a valid item!!")
        return

    t = -1  
    cat = None

    for i in inven:
        t = t + 1
        for a in i:
            if a[0].lower() == item:
                qty_owned = a[1]
                cat = t
                break
        else:
            continue
        break
    else:
        await ctx.send(f"You don't own {item}!!")
        return

    if(qty <= 0):
        await ctx.send("Enter a valid quantity of items!")
        return
    
    if (qty > qty_owned):
        if (qty_owned == 1):
            await ctx.send(f"You only own {qty_owned} {item}. Defaulting to 1.")
            qty = 1
        else:
            await ctx.send(f"You only own {qty_owned} {item}s. Defaulting to {qty_owned}.")
            qty = qty_owned

    cat_map = {0: "ammunitions", 1: "drugs", 2: "others"}
    database.update_inventory(ctx.author.id, item, cat_map[cat], -qty)
    database.add_money(ctx.author.id, price*qty)
    
    await ctx.send("Sale Successful!")
    await ctx.send(f"You gained {price*qty} coins")

class shop_view(discord.ui.View):
    

    @discord.ui.button(label="Guns", style = discord.ButtonStyle.primary)
    async def gun_callback(self, interaction: discord.Interaction, button: discord.ui.Button,):

        embed = discord.Embed(title = "GUN SHOP", color = discord.Color.brand_red())
    
        embed.add_field(name="Welcome to Sin City Gun Shop! Buy any item with 'sin buy'", value = "\u200b" ,inline=False)

        for item in messages.items_gun:
            embed.add_field(name = f"__{item[0]}__ | 🪙 {item[1]}" , value=item[2], inline=False)

        await interaction.response.edit_message(embed = embed, view = shop_view())

        

    @discord.ui.button(label="Drugs", style = discord.ButtonStyle.primary)
    async def drugs_callback(self, interaction: discord.Interaction, button: discord.ui.Button,):

        embed = discord.Embed(title = "DRUG SHOP", color = discord.Color.brand_red())
    
        embed.add_field(name="Welcome to Sin City Drug Shop! Buy any item with 'sin buy'", value = "\u200b" ,inline=False)

        for item in messages.items_drugs:
            embed.add_field(name = f"__{item[0]}__ | 🪙 {item[1]}" , value=item[2], inline=False)

        await interaction.response.edit_message(embed = embed, view = shop_view())

    @discord.ui.button(label="Items", style = discord.ButtonStyle.primary)
    async def items_callback(self, interaction: discord.Interaction, button: discord.ui.Button,):

        embed = discord.Embed(title = "ITEM SHOP", color = discord.Color.brand_red())
    
        embed.add_field(name="Welcome to Sin City Item Shop! Buy any item with 'sin buy'", value = "\u200b" ,inline=False)

        for item in messages.items_items:
            embed.add_field(name = f"__{item[0]}__ | 🪙 {item[1]}" , value=item[2], inline=False)

        await interaction.response.edit_message(embed = embed, view = shop_view())


@bot.command()
async def shop(ctx):
    database.add_user(ctx.author.id)
    
    embed = discord.Embed(title = "GUN SHOP", color = discord.Color.brand_red())
    
    embed.add_field(name="Welcome to Sin City Gun Shop! Buy any item with 'sin buy'", value = "\u200b" ,inline=False)

    for item in messages.items_gun:
        embed.add_field(name = f"__{item[0]}__ | 🪙 {item[1]}" , value=item[2], inline=False)

    await ctx.send(embed = embed, view = shop_view())



@bot.command()
async def transfer(ctx, amount:int , member:discord.Member):
    info = database.get_user(ctx.author.id)
    if info["jail"] == 1:
        await ctx.send("You are a convict! Get out of jail first!!")
        return
    
    if info["money"] < amount:
        await ctx.send("You don't have the required funds")

    payer=ctx.author.id
    receiver=member.id
    database.add_money(receiver,amount)
    database.remove_money(payer,amount)

    await ctx.send(f'{amount} has been sent to {member.display_name}')
    
@bot.command()
async def work(ctx):
    info = database.get_user(ctx.author.id)

    if info["jail"] == 1:
        await ctx.send("You are a convict! Get out of jail first!!")
        return

    if info["user_role"] != 'civilian':
        await ctx.send("Why would you still want to go to your puny day job")
        return

    
    a = random.randint(1, 100)
    money = random.randint(20, 50)
    if 1 <= a <= 89:
        mes = random.choice(messages.workp)
        await ctx.send(mes)
        await ctx.send(f" You gained {money} coins.")
        database.add_money(ctx.author.id, money)

    elif 90 <= a <= 100:
        mes = random.choice(messages.workn)
        await ctx.send(mes)
        await ctx.send(f"You lost {money} coins.")
        database.remove_money(ctx.author.id, money)

@bot.command()
async def buy(ctx, item, qty:int = 1):
    info = database.get_user(ctx.author.id)

    if info["jail"] == 1:
        await ctx.send("You are a convict! Get out of jail first!!")
        return

    item = item.lower()

    if(qty <= 0):
        await ctx.send("Enter a valid quantity of items!")
        return
    for it in messages.items:
        if(item == it[0][2:].lower()):
            if(qty*int(it[1]) > info["money"]):
                await ctx.send("Balance Insufficient!")
                return
            database.update_inventory(ctx.author.id, it[0][2:].lower(), it[3], qty)
            database.remove_money(ctx.author.id, qty*int(it[1]))
            if qty == 1:
                await ctx.send(f"{qty} {item} bough successfully!")
            elif qty > 1:
                await ctx.send(f"{qty} {item} bough successfully!")
            return

    await ctx.send("Enter a valid item name!")

@bot.command()
async def talk(ctx):
    info = database.get_user(ctx.author.id)
    
    if(info["jail"] == 1):
        respect = info["integrity"]
        if(random.random() < (respect/100)**2):
            await ctx.send(random.choice(messages.cop_messages_positive))
            database.update_jail(ctx.author.id, 0)
        else:
            await ctx.send(random.choice(messages.cop_messages_negative))
            database.remove_integrity(ctx.author.id, 5)
            await ctx.send("You lost 5 integrity!")
    else:
        await ctx.send("You are not even jail, do you just enjoy talking to cops?")

@bot.command()
async def getcaught(ctx):
    database.update_jail(ctx.author.id, 1)

@bot.command()
async def bribe(ctx, arg: int):
    info = database.get_user(ctx.author.id)

    if info["jail"] != 1:
        await ctx.send("You're not a convict!")
        return
    
    if (arg <= 0):
        await ctx.send("You think this is a joke!!")
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
        await ctx.send("Alright we'll let you go this time")
        database.remove_integrity(ctx.author.id, 10)
        database.remove_wanted(ctx.author.id, 10)
        return
    
    await ctx.send("Not enough!!")

@bot.command()
async def bail(ctx):
    info = database.get_user(ctx.author.id)

    if info["jail"] != 1:
        await ctx.send("You're not a convict!")
        return
    
    if (info["money"] < 10000):
        await ctx.send("Insufficient Balance")
        return

    
    database.remove_money(ctx.author.id, 10000)
    await ctx.send("Released")
    database.update_jail(ctx.author.id, 0)
    database.remove_wanted(ctx.author.id, 10)

    
    
@bot.command()
async def run(ctx):
    info = database.get_user(ctx.author.id)

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

@bot.command()
async def catch(ctx):
    await events.police_catch(ctx)

@bot.command()
async def w(ctx):
    database.add_wanted(ctx.author.id, 100)

@bot.command()
async def u(ctx, arg: int = 0):
    database.update_jail(ctx.author.id, arg)

@bot.command()
async def m(ctx, arg: int):
    database.add_money(ctx.author.id, arg)

@bot.command()
async def wl(ctx):
    database.remove_wanted(ctx.author.id, -20)


class WeaponButton(discord.ui.Button):
    def __init__(self, gun, ctx, target, money):
        super().__init__(label=gun, style=discord.ButtonStyle.primary)
        self.gun = gun
        self.ctx = ctx
        self.target = target
        self.money = money

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"You used a {self.gun}")
        if(await events.police_catch(self.ctx, 10)):
            await self.ctx.send("The police knew you were coming!")
            await self.ctx.send("You have been captured by the police!")
            await self.ctx.send("You can bribe, run, talk or give bail")
            return
        
        await self.ctx.send(f"You have successfully eliminated {self.target}")
        await self.ctx.send(f"+{self.money} coins")
        database.add_money(self.ctx.author.id, self.money)
        database.remove_integrity(self.ctx.author.id, int(self.money/1000))
        database.add_wanted(self.ctx.author.id, int(self.money/1000))
    
class acceptView(discord.ui.View):

    def __init__(self, ctx, weapons, target, money):
        super().__init__()
        self.ctx = ctx
        self.weapons = weapons
        for weapon in weapons:
            self.add_item(WeaponButton(weapon[0].capitalize(), self.ctx, target, money))

        

class hitView(discord.ui.View):
    
    def __init__(self, ctx, target, money):
        super().__init__()
        self.ctx = ctx
        self.target = target
        self.money = money

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("Get your own contract!", ephemeral = True)
            return False
        return True
    
    @discord.ui.button(label="Accept", style = discord.ButtonStyle.primary,)
    async def accept_callback(self, interaction: discord.Interaction, button: discord.ui.Button,):
    
        await interaction.response.defer()
        info = database.get_inventory(self.ctx.author.id)
        if len(info[0]) == 0:
            await interaction.response.send_message("You don't have a weapon!")
            return

        embed = discord.Embed()
        embed.add_field(name = "Which weapon would you like to use?", value = "\u200b")
        await self.ctx.send(embed = embed, view = acceptView(self.ctx, info[0], self.target, self.money))
        

        

    @discord.ui.button(label="Reject", style = discord.ButtonStyle.primary)
    async def reject_callback(self, interaction: discord.Interaction, button: discord.ui.Button,):

        await interaction.response.send_message("Coward")
        return
        



@bot.command()
async def hit(ctx):
    info = database.get_user(ctx.author.id)

    if info["jail"] == 1:
        await ctx.send("You are a convict! Get out of jail first!!")
        return
    
    if (await events.police_catch(ctx, 8)):
        await ctx.send("Your contact turned out be an undercover cop!")
        await ctx.send("You have been captured by the cops. You can bribe, run, negotiate or pay bail.")
        return
    
    target = random.choice(messages.hit_targets)
    money = random.randint(5000, 15000)

    embed = discord.Embed()
    embed.add_field(name = '\u200b', value = f'{target} - {money} coins')

    await ctx.send(embed = embed, view = hitView(ctx, target, money))

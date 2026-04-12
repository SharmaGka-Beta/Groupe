import os
from dotenv import load_dotenv
import functions
import gambling.gambling as gambling
import roles.civilian as civilian
import devcommands
import battle
import roles.mob as mob
import roles.police as police
import gambling.poker as poker


load_dotenv()
token = os.getenv("DISCORD_TOKEN")


functions.bot.run(token)


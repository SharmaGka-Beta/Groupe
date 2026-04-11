import os
from dotenv import load_dotenv
import functions
import gambling
import civilian
import devcommands
import battle
import mob
import police
import poker


load_dotenv()
token = os.getenv("DISCORD_TOKEN")


functions.bot.run(token)


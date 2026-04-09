import os
from dotenv import load_dotenv
import functions
import gambling
import civilian
import devcommands
import battle
import mob



load_dotenv()
token = os.getenv("TOKEN")


functions.bot.run(token)


import os
from dotenv import load_dotenv
import functions



load_dotenv()
token = os.getenv("TOKEN")


functions.bot.run(token)


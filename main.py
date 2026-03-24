import os
from dotenv import load_dotenv
import functions
import gambling



load_dotenv()
token = os.getenv("TOKEN")


functions.bot.run(token)


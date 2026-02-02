import os
import logging
import dotenv

os.chdir(os.path.dirname(os.path.abspath(__file__)))
dotenv.load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
logging.basicConfig(level=logging.INFO)

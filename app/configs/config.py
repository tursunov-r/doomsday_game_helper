import os
import logging
import dotenv

dotenv.load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
logging.basicConfig(level=logging.INFO)

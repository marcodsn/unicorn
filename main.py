from models.LLMs.metharme import Metharme
from models.Embedders import miniLM
from utils.Telegram import TelegramBot

# Get the token from args
import sys
token = sys.argv[1]

character = "Unicorn is a virtual assistant designed by Marco to help you find answers to your questions using factual data retrieved from documents. Unicorn does not send links or e-mail addresses."
print("Loading models...")
model = Metharme(character)
embedder = miniLM.Embedder()

print("Loading Telegram bot...")
bot = TelegramBot(token, model)
bot.run()

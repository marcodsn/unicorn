import os
import json

import telegram
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, ForceReply
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
import logging
from utils.Document import Document
from models.LLMs.metharme import Metharme
from utils.History import History
from utils.UsersManager import UsersManager


class TelegramBot:
    def __init__(self, token, llm):
        self.application = Application.builder().token(token).build()
        self.llm = llm
        self.users = UsersManager()
        self.logging = False

        wlist = open('whitelist.txt', 'r')
        # Skip first line
        wlist.readline()

        data = wlist.read()
        if data == '':
            self.whitelist = None
        else:
            self.whitelist = data.split('\n')
        wlist.close()

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Send a message when the command /start is issued."""
        user = update.effective_user
        await update.message.reply_text("Hi " + user.name + "!")

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Send a message when the command /help is issued."""
        help = "This bot is a demo of the Unicorn bot. You can ask it questions about a document, and it will answer you. To do so, you need to send a PDF file to the bot, and then ask it questions about it. You can also ask it questions without a document, but the answers will be less accurate. The bot is still in development, so it may not work properly. If you have any questions, feel free to contact @marcodsn."
        await update.message.reply_text(help)

    async def delete_doc(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Delete the document from the user's memory."""
        self.users.get(update.effective_user.id).doc = None
        await update.message.reply_text("Document deleted.")

    async def delete_history(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Delete the history from the user's memory."""
        self.users.get(update.effective_user.id).history = History()
        await update.message.reply_text("History deleted.")

    async def reset(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Delete the history and the document from the user's memory."""
        self.users.get(update.effective_user.id).history = History()
        self.users.get(update.effective_user.id).doc = None
        await update.message.reply_text("History and document deleted.")

    async def set_debug(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Set the debug mode. If debug mode is on, the bot will return the retrieved documents and the generated answers to the user."""
        self.users.get(update.effective_user.id).debug = not self.users.get(update.effective_user.id).debug
        await update.message.reply_text("Debug mode set to " + str(self.users.get(update.effective_user.id).debug))

    async def generate(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Use the LLM to generate an answer to the user's question."""
        doc = self.users.get(update.effective_user.id).doc
        history = self.users.get(update.effective_user.id).history

        if doc is not None:
            retrieved = doc.search(update.message.text)
            if self.users.get(update.effective_user.id).debug:
                await update.message.reply_text("Retrieved: " + str(retrieved))
        else:
            retrieved = None

        answer = self.llm.generate(update.message.text, retrieved, history.get(), top_k=50, temperature=0.1, top_p=0.95,
                                   repetition_penalty=1.05).strip()

        if self.logging:
            await self.users.get(update.effective_user.id).log(update.message.text, answer)
        
        history.add(update.message.text, None, answer)

        print(str(update.effective_user.id) + ':' + update.message.text + ':' + answer)
        await update.message.reply_text(answer)

    async def answer(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if self.whitelist is not None and str(update.effective_user.id) not in self.whitelist:
            print(update.effective_user.name + " with user_id " + str(update.effective_user.id) + " is not in the whitelist.")
            await update.message.reply_text("You are not authorized to use this bot.")
            return
        await self.generate(update, context)

    async def process_file(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if self.whitelist is not None and str(update.effective_user.id) not in self.whitelist:
            print(update.effective_user.name + " with user_id " + str(update.effective_user.id) + " is not in the whitelist.")
            await update.message.reply_text("You are not authorized to use this bot.")
            return
        
        """Process the file sent by the user."""
        file = update.message.effective_attachment

        # Check if the file is a pdf, and check size
        if file.file_size > 10000000: # 10 MB
            await update.message.reply_text("File too big.")
            return
        if file.mime_type != "application/pdf":
            await update.message.reply_text("File needs to be a PDF.")
            return

        # Download the file
        if not os.path.exists("temp"):
            os.mkdir("temp")
        file = await context.bot.get_file(file.file_id)
        out = open("temp/" + str(update.effective_user.id) + ".pdf", "wb")
        await file.download_to_memory(out)
        await update.message.reply_text("Document received. Please wait while I elaborate it...")

        # Convert the file to text
        # self.doc = Document(str(update.effective_user.id), path="temp/" + str(update.effective_user.id) + ".pdf")
        self.users.get(update.effective_user.id).doc = Document(str(update.effective_user.id), path="temp/" + str(update.effective_user.id) + ".pdf")
        await update.message.reply_text("Document elaborated successfully. You can now ask me questions about it.")

    def run(self):
        # on different commands - answer in Telegram
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("reset_doc", self.delete_doc))
        self.application.add_handler(CommandHandler("reset_history", self.delete_history))
        self.application.add_handler(CommandHandler("reset", self.reset))
        self.application.add_handler(CommandHandler("debug", self.set_debug))

        # on non command i.e messages, files
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.answer))
        self.application.add_handler(MessageHandler(filters.ATTACHMENT & ~filters.COMMAND, self.process_file))

        self.application.run_polling(allowed_updates=Update.ALL_TYPES)

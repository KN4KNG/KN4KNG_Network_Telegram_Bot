#!/usr/bin/env python3
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

import os

approved_users = ['{USER ID HERE}','{USER ID HERE}','{USER ID HERE}',]
asl_node = '{ENTER ASL Public Node}'
bot_token = '{ENTER BOT TOKEN}'

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}! You must be an approved users to control KN4KNG Network. Please reach out to @iDevDark to request access." + '\n' + "If you are already an approved user please use command /help for a list of commands.",
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    user_id = str(update.effective_user.id)
    username = str(update.effective_user.username)
    if not user_id in approved_users:
        await update.message.reply_text("Hello, @" + username + " your ID is " + user_id + ". Please message @iDevDark to be an approved user.")
    elif user_id in approved_users:
        await update.message.reply_text("Hello @" + username + "You are an approved user please message @iDevDark with any issues to report." + '\n' + "Lists of commands are as follows:" + '\n' + "/start - start bot" + '\n' + "/help - this message" + '\n' + "/drop_asl - drop all asl links" + '\n' + "/connect_asl - connect to asl node")

async def drop_asl(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /Drop_ASL is issued."""
    user_id = str(update.effective_user.id)
    username = str(update.effective_user.username)
    if not user_id in approved_users:
        await update.message.reply_text("Hello, @" + username + " your ID is " + user_id + ". Please message @iDevDark to be an approved user.")
    elif user_id in approved_users:
        await update.message.reply_text("Dropping All ASL Connections... Standby")
        os.system("""echo 'Disconnecting from all nodes'""")
        os.system("""/usr/sbin/asterisk -rx 'rpt cmd """ + asl_node + """ ilink 6 1999'""")
        os.system("""echo 'Connecting back to node 1999'""")
        os.system("""/usr/sbin/asterisk -rx 'rpt cmd """ + asl_node + """ ilink 3 1999'""")
        await update.message.reply_text("Node 1999 Reconnected for Digital Cross-Mode")

async def connect_asl(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Add a job to the queue."""
    user_id = str(update.effective_user.id)
    username = str(update.effective_user.username)
    if not user_id in approved_users:
        await update.message.reply_text("Hello, @" + username + " your ID is " + user_id + ". Please message @iDevDark to be an approved user.")
    elif user_id in approved_users:
        chat_id = update.effective_message.chat_id
        try:
            # args[0] should contain the asl node number greater than 1999
            asl_node_to_connect = context.args[0]
            if float(asl_node) < 2000:
                await update.effective_message.reply_text("Sorry we can not connect to private nodes! Please enter a node number greater than 1999!")
                return

            await update.effective_message.reply_text("Connecting to Node: " + asl_node)
            os.system("""echo Connecting to node: """ + asl_node)
            os.system("""/usr/sbin/asterisk -rx 'rpt cmd """ + asl_node + """ ilink 3 """ + asl_node_to_connect + "'")
            os.system("""echo Connected to node: """ + asl_node_to_connect)

        except (IndexError, ValueError):
            await update.effective_message.reply_text("Usage: /connect_asl <node>")

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(bot_token).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("drop_asl", drop_asl))
    application.add_handler(CommandHandler("connect_asl", connect_asl))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()

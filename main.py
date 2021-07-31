import os
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext


# READ TOKEN
TOKEN = os.environ["TOKEN"]
updater = Updater(TOKEN)

helpMSG = '''
1. /twitter

'''

def downloadTwitter(link) :
    payload = {
        "url" : link,
        "ver" : 1306
    }
    r = requests.post("https://tvdl-api.saif.dev", data = payload).json()
    print(r)
    downloadUrl = r["high"]["downloadURL"]
    r = requests.get(downloadUrl)
    open("./twitterVideo.mp4", "wb").write(r.content)


# send telegram message
def hello(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'Hello {update.effective_user.first_name}')


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'hello welcome to modalessiBot use /help to show commands')


def help(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(helpMSG)

   
def twitter(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    link = ""
    if "\n" in text:
        link = text.split("\n" )[1]
    
    elif text == "/twitter" :
        update.message.reply_text("please send the link with the command ex: \n /twitter PUT_YOUR_LINK_HERE")
    else :
        link = text.split()[1]
        
    
    downloadTwitter(link)
    # send file to telegram
    with open("./twitterVideo.mp4", "rb") as file:
        update.message.reply_video(file)
        
        
updater.dispatcher.add_handler(CommandHandler('hello', hello))
updater.dispatcher.add_handler(CommandHandler('twitter', twitter))
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('help', help))

updater.start_polling()
print("Bot is ready")
# updater.idle()




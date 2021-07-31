import os, json
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext


# Telegram bot token
TOKEN = os.environ["TOKEN"]
# API key for utrim.xyz
API_KEY = os.environ["API_KEY"]

updater = Updater(TOKEN)

helpMSG = '''
1. /twitter
2. /trim

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

def trimLink(link: str) -> str:
    if not API_KEY:
        return ""

    payload = json.dumps({
    "url": link
    })
    headers = {
    'x-api-key': '46dd21d0-fe89-4b15-9af7-22e6fcf575d5',
    'Content-Type': 'application/json'
    }
    url = "https://utrim.xyz/api/trim"
    r = requests.request("POST", url, headers=headers, data=payload)
    
    if r.status_code == 200:
        return r.json()["data"]["link"]
    return ""
    

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


def trim(update: Update, context: CallbackContext) -> None:
    msg = update.message.text
    if msg == "/trim":
        update.message.reply_text("please send the link with the command ex: \n /trim PUT_YOUR_LINK_HERE")
    else:
        link = msg.split()[1]
        if "\n" in msg:
            link = msg.split("\n")[1]
        
        trimmedLink = trimLink(link)
        update.message.reply_text(trimmedLink or "Sorry, something went wrong")

        
updater.dispatcher.add_handler(CommandHandler('hello', hello))
updater.dispatcher.add_handler(CommandHandler('twitter', twitter))
updater.dispatcher.add_handler(CommandHandler('trim', trim))
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('help', help))

updater.start_polling()
print("Bot is ready")
# updater.idle()




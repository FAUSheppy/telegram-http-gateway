#!/usr/bin/python3

import time
import argparse
import telegram.ext as tg
import telegram
import logging
import flask

HOST = "icinga.atlantishq.de"
CHAT_ID_FILE = "connected_chat_ids.txt"
app = flask.Flask("Telegram Notification Gateway")
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def dbWriteChatId(chatId):
    saves = []
    with open(CHAT_ID_FILE, "r") as f:
        for lines in f:
            saves += [int(lines)]
    saves += [chatId]
    saves = set(saves)
    with open(CHAT_ID_FILE, "w") as f:
        for s in saves:
            f.write(str(s) + "\n")

def dbRemoveChatId(chatId):
    saves = []
    with open(CHAT_ID_FILE, "r") as f:
        for lines in f:
            saves += [int(lines)]
    saves.remove(chatId)
    saves = set(saves)
    with open(CHAT_ID_FILE, "w") as f:
        for s in saves:
            f.write(str(s) + "\n")

def dbReadChatIdFile():
    saves = []
    with open(CHAT_ID_FILE, "r") as f:
        for line in f:
            saves += [int(line)]
    return saves

def sendMessageToAllClients(msg):
    for chatId in dbReadChatIdFile():
        chatId = int(chatId)
        updater.bot.send_message(chat_id=chatId, text=msg, parse_mode=telegram.ParseMode.MARKDOWN_V2)


def startHandler(update, context):
    startText = "Icinga Bot connected and listening on {}".format(HOST)
    dbWriteChatId(update.effective_chat.id)
    context.bot.send_message(chat_id=update.effective_chat.id, text=startText)

def unsubscribeHandler(update, context):
    text = "Unsubscribed. You won't receive anymore messages."
    dbRemoveChatId(update.effective_chat.id)
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


@app.route('/send-all', methods=["POST"])
def sendToAll():
    sendMessageToAllClients(flask.request.json["message"])
    return ("","204")

def escape(string):
    badChars = [".","-","=","(",")","+"]
    for c in badChars:
        string = string.replace(c,"\\"+c)
    return string

@app.route('/send-all-icinga', methods=["POST"])
def sendToAllIcinga():
    args = flask.request.json

    # markdown escape #
    for key in args.keys():
        if type(args[key]) == str:
            print(key)
            args[key] = escape(args[key])

    # build message #
    serviceName = args["service_name"]
    if args["service_display_name"]:
        serviceName = args["service_display_name"]

    message = "*{service} {state}* on [{host}]({host})\n{output}".format(service=serviceName,
                                                                            state=args["service_state"],
                                                                            host=args["service_host"],
                                                                            output=args["service_output"])
    sendMessageToAllClients(message)
    return ("","204")

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Simple Telegram Notification Interface',
                        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--interface', default="localhost", help='Interface on which to listen')
    parser.add_argument('--port', default="5000", help='Port on which to listen')
    parser.add_argument("--token-file", default="bot.token", help="File containing the Bot-Token")
    args = parser.parse_args()

    # create bot #
    updater = None
    with open(args.token_file, 'r') as f:
        updater = tg.Updater(token=f.read().strip("\n"), use_context=True)

    # add command handlers #
    updater.dispatcher.add_handler(tg.CommandHandler('start', startHandler))
    updater.dispatcher.add_handler(tg.CommandHandler('restart', startHandler))
    updater.dispatcher.add_handler(tg.CommandHandler('unsubscribe', unsubscribeHandler))

    # run bot #
    updater.start_polling()

    # run flask server #
    app.run(host=args.interface, port=args.port)


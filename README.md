# HTTP->Telegram Gateway Notification Service
Simplistic server that connect to a Telegram bot, takes messages via *POST*-requests containing json encoded data and sends them to all clients that are subscribed

# Telegram Setup
- create a bot as described [here](https://core.telegram.org/bots)
- add your bot as a contact

# Telegram Bot Commands

    /start          # subscribe
    /unsubscribe    # unsubscribe

# Server Setup

     usage: telegram-interface.py [-h] [--interface INTERFACE] [--port PORT]
                                  [--token-file TOKEN_FILE]
     
     optional arguments:
       -h, --help               show this help message and exit
       --interface INTERFACE    Interface on which to listen (default: localhost)
       --port PORT              Port on which to listen (default: 5000)
       --token-file TOKEN_FILE  File containing the Bot-Token (default: bot.token)

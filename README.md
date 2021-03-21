# HTTP->Telegram Gateway Notification Service
Simplistic server which connects to a Telegram bot, takes messages via *POST*-requests containing json encoded data and sends them to all clients subscribed.

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

# HTTP Request
The HTTP request must be a *POST*-request, with *Content-Type: application/json* and a json-field containing the key *"message"* with the value being the message you want to send.

The following locations are supported:

    /send-all   # send a message to all subscribed clients

# Example (curl)

    curl -X POST -H "Content-Type: application/json" --data '{"message":"hallo world"}' localhost:5000/send-all

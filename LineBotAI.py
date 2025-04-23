import os

from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, ImageMessage,TextMessage, TextSendMessage
from utils import predict_image

import requests



# Initialize Flask app
app = Flask(__name__)

# LINE Bot credentials from the LINE Developers Console
# CHANNEL_SECRET = 'LINE_CHANNEL_SECRET'  # Replace with your Channel Secret
# CHANNEL_ACCESS_TOKEN = 'LINE_CHANNEL_ACCESS_TOKEN'  # Replace with your Channel Access Token

# CHANNEL_ACCESS_TOKEN = "3v0P0QKM6SK5EtmW4tyzBZRgbenxgXjm9zNvPDvgOYZJRN/Z7gDp76rhOIMO/v/qmlZf6XFQGBlBC0v5sYPxcfU1JPl3i7ruOGNLn94HZgJZtnZbTojfwGANyD0Dy9rCNIH2HFXSYE9C90DMLsyjVAdB04t89/1O/w1cDnyilFU="
# CHANNEL_SECRET = "79bffdb9e50e19336e79aad0679665fc"

# Initialize LINE Bot API and Handler
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))


# Webhook for receiving LINE events
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers.get("X-Line-Signature")
    if not signature:
        abort(400)

    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK", 200



# def callback():
#     # Get X-Line-Signature header value
#     signature = request.headers['X-Line-Signature']

#     # Get request body as text
#     body = request.get_data(as_text=True)
#     app.logger.info("Request body: " + body)

#     # Verify the signature and handle the request
#     try:
#         handler.handle(body, signature)
#     except InvalidSignatureError:
#         abort(400)
#     return 'OK',200

# Event handler for text messages
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # Reply with a simple text message
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='Hello, this is a simple LINE Bot demo!')
    )

if __name__ == "__main__":
    # Run Flask app
    app.run(debug=True, port=5000)

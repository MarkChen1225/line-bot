
import os
from flask import Flask, request, jsonify
from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)
app = Flask(__name__)

# 環境變數
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')

if not LINE_CHANNEL_SECRET or not LINE_CHANNEL_ACCESS_TOKEN:
    raise ValueError("LINE_CHANNEL_SECRET or LINE_CHANNEL_ACCESS_TOKEN is not set.")

# 設定 Line Bot API
config = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)
messaging_api = MessagingApi(config)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/", methods=["GET"])
def home():
    return "LINE Bot is running on Render!"

@app.route("/webhook", methods=["POST"])
def webhook():
    body = request.get_data(as_text=True)
    print("Received Webhook:", body)
    
    try:
        handler.handle(body, request.headers["X-Line-Signature"])
    except Exception as e:
        print("Error:", str(e))
    
    return "OK"

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    reply_text = f"你說了：{event.message.text}"
    messaging_api.reply_message(ReplyMessageRequest(
        reply_token=event.reply_token,
        messages=[TextMessage(text=reply_text)]
    ))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

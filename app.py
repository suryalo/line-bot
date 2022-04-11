from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('Y3heDCJ4biTY9+8ZpC7bhvrC+lXMyEukA83qaFnAuZf3+rzRoBijoEg5YiEzLMHAKTX30y3OUOka40kSxwHAdDy+JHknadnpeHKPrU+xYQVygQq8/5PuHq/4uLZN5aZ95T5jbl7DfpY8o4wUWwI/FAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('0e8ba4d6ff48c3bc8ef3ff658be5ec6b')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    r = '抱歉，這個問題不在我的守備範圍！'

    if msg in ['hi', 'Hi']:
        r == 'Hello, 我是機器人Surya！'
    elif msg == '你吃飯了嗎？':
        r == '還沒'
    elif '訂位' in msg:
        r = '您想訂位，是嗎？'
    elif msg in ['Yes', '是']:
        r = '您想訂什麼時間？'

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r))


if __name__ == "__main__":
    app.run()
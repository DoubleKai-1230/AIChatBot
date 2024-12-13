from flask import Flask
app = Flask(__name__)

from flask import request, abort
from linebot import  LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import google.generativeai as genai

# line_bot_api = LineBotApi('你的 CHANNEL_ACCESS_TOKEN')
# handler = WebhookHandler('你的 CHANNEL_SECRET')
line_bot_api = LineBotApi('2r0uM+EyclNAfJobqVNqgas6ATfvdR6Ux/mThqABbB+LhR9ZD5VCsXtJAPLUA7BHoQ8kz1RbYvtYDfKOzi4HdAANLBvB+GXh0brqW2a7hERYoKyF8wUPG+FHpBkx04XKHlB8O6NK7Pm8JX7i/wHgmwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('f6851b7663569c8da4020e8074c93b02')

api_key = 'AIzaSyAAmRV7qkP76eLE0R_gREFUKPtqBJsL3qo'
genai.configure(api_key = api_key)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_msg = event.message.text
    
    model = genai.GenerativeModel(
        'gemini-1.5-flash',
        system_instruction="你是一位使用繁體中文的萬能助理。"
        )
    response = model.generate_content(user_msg)
    result = response.text
    print(result)
    
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text = result))
    
if __name__ == '__main__':
    app.run()
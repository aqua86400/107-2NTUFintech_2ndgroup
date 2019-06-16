from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    LineBotApiError, InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom )
import numpy as np
import pandas as pd
import joblib

app = Flask(__name__)


line_bot_api = LineBotApi("kSQveLUxgYMM07g2vX52UbRurNBl6TvodrZYE/D1YQtPQrW/kQzxF6+I0gryIfXda2nkRkS0UKTlMEgCEhONj07rrtRAxNlIMTmnSKevZh8XoY6M9mkM9/eNv2ZCPkueUQ5Ttn11eNFNfglQ4CjxdgdB04t89/1O/w1cDnyilFU=", "http://localhost:8080")
handler = WebhookHandler("469ef739c1ca0abb369b4427c6828fc9")


@app.route("/callback", methods=['POST'])

def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    print(body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except LineBotApiError as e:
        print("Got exception from LINE Messaging API: %s\n" % e.message)
        for m in e.error.details:
            print("  %s: %s" % (m.property, m.message))
        print("\n")
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)


def message_text(event):
    # your code is here
    #userid = event.source.user_id
    
    
    while event.message.text != 'res':
        infor = []
        
        if len(event.message.text) <= 10:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='A請問您此次投資目的是否是為了追求長期投資報酬? 1.是 0.否'))
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='B請問您的家庭年收入約在以下哪個範圍？ 1.50萬以下 2.50~100萬 3.100~300萬 4.300~500萬 5.500萬以上'))
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='C請問您對於基金類型的投資標的偏好為何？ 1.貨幣型基金 2.已開發國家政府公債債券基金、已開發國家投資級公司債券基金 3.平衡型基金、已開發國家非投資及公司債券基金、新興市場債券基金 4.全球股票基金、歐美成熟國家股票基金、大中華或亞太股票基金 5.新興市場股票基金、單一新興國家股票基金、產業類股型基金、店頭市場基金'))
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='D若緊急突發事件發生時，請問您所持有的備用金相當於您幾個月的家庭開銷？ 1.無備用金 2.不到3個月 3.介於3~6個月 4.介於6~9個月 5.超過9個月'))
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='E請問您習慣的基金方式為何？ 1.不曾投資過 2.只買過貨幣型基金 3.定時定額 4.單筆（不含貨幣型基金）和定時定額都有 5.單筆或私募基金'))
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='輸入格式: A選項 B選項 C選項 D選項 E選項   ; 重新輸入可以再計算.'))

        while True:
            if len(event.message.text) >= 10:
                break
        answer = event.message.text.split(' ')

        for i in range(5):
            infor.append(int(answer[i][1:]))
            
        infor_in = pd.DataFrame([infor])

        knn = joblib.load('knn_model.pkl')
        c_value = int(knn.predict(infor_in))
        advice = ['野村貨幣市場基金', '野村全球短期收益基金', '野村環球基金、野村亞太新興債券基金', '野村全球不動產證券化基金、野村亞太複合高收益債基金', '野村巴西基金、野村大俄羅斯基金']
        
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text = '您的風險屬性等級為:' + str(c_value) + '我們推薦您可以參考我們的' + advice[c_value-1] + '。'))
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text = '如有任何疑問，歡迎到我們的網站：https://www.nomurafunds.com.tw了解更多相關資訊，或來電洽詢：(02)8758-1568，由專人為您服務'))

        
        event.message.text = 'res'


if __name__ == "__main__":
    app.run()



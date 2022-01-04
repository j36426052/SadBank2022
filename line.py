import requests
import json

#my_data = {'key1': 'value1', 'key2': 'value2'}



def postMessage(yourID,inID,money,cancelURL,checkURL):
    line_bot_api = 'Bearer '+'your bot ID'
    

    #讀取
    tem = json.load(open('card.json','r',encoding='utf-8'))
    #設定區
    ##設定轉出人
        #tem['body']['contents'][1]['contents'][1]['contents'][1]['text'] = 'Q蛇銀行'
    tem['body']['contents'][1]['contents'][1]['contents'][1]['text'] = inID
    
    ##設定金額
    tem['body']['contents'][1]['contents'][2]['contents'][1]['text'] = '$'+str(money)+'NTD'

    ##設定取消url
    #tem['footer']['contents'][0]['action']['uri'] = "http://linecorp.com/"
    tem['footer']['contents'][0]['action']['uri'] = cancelURL
    
    ##設定確認
    #tem['footer']['contents'][1]['action']['uri'] = 'https://www.google.com'
    tem['footer']['contents'][1]['action']['uri'] = checkURL

    FlexMessage = {
        "to":yourID,
        "messages":[{"type":"flex","altText":"轉帳通知","contents":tem}]
    }

    a = json.dumps(FlexMessage)


    # 將資料加入 POST 請求中
    my_headers = {'Content-Type': 'application/json','Authorization':line_bot_api}
    r = requests.post('https://api.line.me/v2/bot/message/push', data = a,headers=my_headers)
    return r.content
    # print(a)
    # print(r.content)
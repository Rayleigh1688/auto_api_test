import requests

BOT_TOKEN = '7705196107:AAHGr5-36HIPxH1giWR_GaR91fWpE93wNs4'
CHAT_ID = -4800086743  # 来自你贴的 getUpdates 返回
TEXT = '🚨 达文西是2b'

url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
payload = {
    'chat_id': CHAT_ID,
    'text': TEXT
}

response = requests.post(url, data=payload)
print(response.status_code)
print(response.text)
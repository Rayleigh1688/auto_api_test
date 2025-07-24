import hashlib
import requests

# 参数
from_time = "2025-06-24 00:00:00"
to_time = "2025-06-25 00:00:00"
return_rows = "1"
secret_key = "234234"
page_number = "1"
page_size = "20"

# 生成 signature（如果不需要加密签名，用 signature = secret_key）
raw_signature = from_time + to_time + return_rows + secret_key
signature = hashlib.md5(raw_signature.encode('utf-8')).hexdigest()

# 请求体
payload = {
    "from": from_time,
    "to": to_time,
    "return_rows": int(return_rows),
    "signature": signature,  # 或直接用 secret_key，如果后端不验签
    "page_number": page_number,
    "page_size": page_size
}



# 注意 URL 要一致
url = "https://admin-pagcor-fat.filbet2025.com/cmpl/record/api"

# 发起请求
response = requests.post(url, json=payload)

# 输出响应
print(response.status_code)
print(response.text)
print(response.json())

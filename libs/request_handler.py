import requests
import cbor2
from config import context
from utils.replace_vars import render_with_context

class RequestHandler:
    def __init__(self, base_url):
        self.base_url = base_url

    def send(self, method, endpoint, params=None, content_type="cbor", headers=None):
        url = self.base_url + endpoint
        data = render_with_context(params or {})
        headers = render_with_context(headers or {})

        headers.setdefault("lang", "en_US")
        headers.setdefault("d", "25")
        headers.setdefault("User-Agent", "Restfox/0.36.0")

        token = context.GLOBAL_VARS.get("access_token")
        if token:
            headers.setdefault("Authorization", f"Bearer {token}")
            headers.setdefault("t", token)

        method = method.upper()

        # ✅ 打印功能测试请求信息
        print("📤 [功能测试] 请求开始")
        print("→ URL:", url)
        print("→ Method:", method)
        print("→ Headers:", headers)
        print("→ Params:", data)

        if content_type == "cbor":
            encoded_data = cbor2.dumps(data)
            print("→ CBOR Encoded:", encoded_data.hex())
            resp = requests.request(method, url, data=encoded_data, headers=headers)
        elif content_type == "json":
            headers["Content-Type"] = "application/json"
            resp = requests.request(method, url, json=data, headers=headers)
        elif method == "GET":
            resp = requests.get(url, params=data, headers=headers)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")

        print("🟢 Raw response content:", resp.content)

        try:
            return resp.status_code, cbor2.loads(resp.content)
        except Exception:
            try:
                return resp.status_code, resp.json()
            except:
                return resp.status_code, {}
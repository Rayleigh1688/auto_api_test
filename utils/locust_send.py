import time
import cbor2
from locust import events
from config import context  # ✅ 注入全局 token 用

def send_with_client(client, method, url, params=None, headers=None, content_type="cbor"):
    method = method.upper()
    params = params or {}
    headers = headers or {}

    # ✅ 设置默认请求头
    headers.setdefault("lang", "en_US")
    headers.setdefault("d", "25")
    headers.setdefault("User-Agent", "Restfox/0.36.0")

    # ✅ 注入 token（如果已登录）
    token = context.GLOBAL_VARS.get("access_token")
    if token:
        headers.setdefault("Authorization", f"Bearer {token}")
        headers.setdefault("t", token)

    # ✅ 打印请求
    print("📤 [Locust] 请求开始")
    print("→ Params:", params)

    start_time = time.time()

    try:
        # ✅ 构造请求体
        if content_type == "cbor":
            headers["Content-Type"] = "application/cbor"
            encoded_data = cbor2.dumps(params)
            print("→ CBOR Encoded:", encoded_data.hex())
            request_args = {"data": encoded_data}
        elif content_type == "json":
            headers["Content-Type"] = "application/json"
            request_args = {"json": params}
        else:
            raise ValueError(f"Unsupported content type: {content_type}")

        # ✅ 发请求并手动处理响应 success/failure
        with client.request(method, url, headers=headers, catch_response=True, **request_args) as resp:
            duration = int((time.time() - start_time) * 1000)
            raw = resp.content

            # ✅ 解析响应
            try:
                body = cbor2.loads(raw)
            except Exception:
                try:
                    body = resp.json()
                except:
                    body = {}

            print("🔙 响应内容:", body)

            # ✅ 状态判断
            if resp.status_code != 200:
                resp.failure(f"HTTP 状态码断言失败: {resp.status_code}")
            elif isinstance(body, dict) and body.get("status") is not True:
                resp.failure(f"业务断言失败: status ≠ true，实际为 {body.get('status')}")
            else:
                resp.success()

            return resp.status_code, body, raw

    except Exception as e:
        duration = int((time.time() - start_time) * 1000)
        events.request_failure.fire(
            request_type=method,
            name=url,
            response_time=duration,
            exception=e
        )
        raise e
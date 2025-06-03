from locust import HttpUser, task, between, events
import random

class GoogleUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def access_google(self):
        # 模拟一半成功，一半失败
        if random.randint(1, 10) <= 5:
            # 成功请求
            with self.client.get("/", name="/", catch_response=True) as resp:
                if resp.status_code == 200:
                    resp.success()
                else:
                    resp.failure(f"Unexpected status code: {resp.status_code}")
        else:
            # 故意请求不存在页面 → 返回 404
            with self.client.get("/404", name="/404", catch_response=True) as resp:
                if resp.status_code == 404:
                    resp.failure("Simulated failure: 404")
                else:
                    resp.success()
from locust import HttpUser, task, between, constant
from locust_runner.runner import LocustTestRunner

class APITestUser(HttpUser):
    wait_time = constant(0)

    def on_start(self):
        self.runner = LocustTestRunner(client=self.client, base_url=self.host)
        self.run_count = 0  # ✅ 初始化每个线程的执行计数器

    @task
    def run_case(self):
        # if self.run_count >= 10:
        #     return
        self.runner.run_one_case()
        self.run_count += 1
import os
import time
from config import context
from config.settings import BASE_URL
from utils.yaml_loader import load_test_cases
from utils.replace_vars import render_with_context
from jsonpath_ng import parse
from utils.locust_send import send_with_client

class LocustTestRunner:
    def __init__(self, case_dir="data", client=None, base_url=None):
        self.test_cases = self.load_all_cases(case_dir)
        self.client = client
        self.base_url = base_url or BASE_URL
        self._index = 0

    def load_all_cases(self, directory):
        cases = []
        for file in os.listdir(directory):
            if file.endswith(".yaml") or file.endswith(".yml"):
                file_cases = load_test_cases(os.path.join(directory, file))
                if isinstance(file_cases, list):
                    cases.extend([c for c in file_cases if c])
                elif file_cases:
                    cases.append(file_cases)
        print(f"✅ 加载用例数: {len(cases)}")
        return cases

    def run_one_case(self):
        if not self.test_cases:
            print("⚠️ 没有可用测试用例")
            return

        if self._index >= len(self.test_cases):
            self._index = 0

        case = self.test_cases[self._index]
        self._index += 1
        self._run_case(case)

    def _run_case(self, case):
        if case is None or not isinstance(case, dict):
            print("[⚠️ 跳过无效用例] case 为 None 或非法结构")
            return

        name = case.get("name", case.get("url"))
        method = case.get("method", "POST")
        endpoint = case.get("url", "")
        params = render_with_context(case.get("params", {}))
        headers = render_with_context(case.get("headers", {}))
        content_type = case.get("content_type", "cbor")
        expected_status = case.get("expected", {}).get("status_code", 200)
        asserts = case.get("asserts", [])
        extract = case.get("extract", {})

        print(f"\n🚀 执行用例: {name}")
        print(f"📤 请求 Params: {params}")

        try:
            full_url = self.base_url + endpoint
            status_code, resp, _ = send_with_client(
                client=self.client,
                method=method,
                url=full_url,
                params=params,
                headers=headers,
                content_type=content_type
            )

            print(f"🔍 实际响应: {resp}")

            if status_code != expected_status:
                raise AssertionError(f"状态码断言失败: {status_code} != {expected_status}")

            self._assert_response(name, resp, asserts)
            self._extract_vars(resp, extract)
            print(f"[✅ PASS] {name}")

        except Exception as e:
            print(f"[❌ ERROR] {name} 异常: {e}")
            raise e

    def _assert_response(self, name, resp, asserts):
        for assertion in asserts:
            path = assertion.get("path")
            expected = assertion.get("equals")
            should_exist = assertion.get("exists")

            try:
                matches = list(parse(path).find(resp))
                if should_exist and not matches:
                    raise AssertionError(f"{name} → 断言失败: {path} 不存在\n实际响应: {resp}")
                elif expected is not None:
                    actual_val = matches[0].value if matches else None
                    if not matches or actual_val != expected:
                        raise AssertionError(f"{name} → {path} = {actual_val} ≠ 期望 {expected}\n实际响应: {resp}")
            except Exception as e:
                raise AssertionError(f"{name} → JSONPath 解析失败 {path}: {e}\n实际响应: {resp}")

    def _extract_vars(self, resp, extract):
        for var_name, path in extract.items():
            try:
                match = list(parse(path).find(resp))
                if match:
                    context.GLOBAL_VARS[var_name] = match[0].value
                    print(f"🔧 提取变量: {var_name} = {match[0].value}")
            except Exception as e:
                print(f"[❌ 提取失败] {var_name} ← {path}: {e}")
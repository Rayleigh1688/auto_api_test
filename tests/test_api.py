import pytest
import os
import json
import allure
import glob
from libs.request_handler import RequestHandler
from utils.yaml_loader import load_test_cases
from config.settings import BASE_URL
from jsonpath_ng import parse
from config import context

handler = RequestHandler(BASE_URL)

# 用于动态加载指定的 YAML 文件
def load_selected_cases(data_dir, keyword=''):
    all_cases = []
    pattern = f"*{keyword}*_cases.yaml" if keyword else "*_cases.yaml"
    yaml_files = glob.glob(os.path.join(data_dir, pattern))

    for file_path in yaml_files:
        cases = load_test_cases(file_path)
        all_cases.extend(cases)
    return all_cases

# 用于 pytest 动态参数化
def pytest_generate_tests(metafunc):
    if 'case' in metafunc.fixturenames:
        case_arg = metafunc.config.getoption("case")
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(current_dir, '..', 'data')
        cases = load_selected_cases(os.path.normpath(data_dir), case_arg)
        metafunc.parametrize("case", cases)

# 测试函数
def test_api(case):
    method = case['method']
    url = case['url']
    params = case.get('params', {})
    expected = case.get('expected', {})
    asserts = case.get('asserts', [])
    content_type = case.get('content_type', 'cbor')
    headers = case.get('headers', {})

    print(f"=== Running: {case['name']} ===")
    status_code, resp,  = handler.send(method, url, params, content_type, headers)

    with allure.step("请求参数"):
        allure.attach(json.dumps(params, indent=2, ensure_ascii=False), name="Request", attachment_type=allure.attachment_type.JSON)
    with allure.step("响应结果"):
        allure.attach(json.dumps(resp, indent=2, ensure_ascii=False), name="Response", attachment_type=allure.attachment_type.JSON)

    assert status_code == expected.get('status_code'), (
        f"[状态码断言失败] 实际: {status_code}，预期: {expected.get('status_code')}。\n完整响应: {json.dumps(resp, ensure_ascii=False)}"
    )

    # 提取变量
    extracts = case.get("extract", {})
    for key, jsonpath_expr in extracts.items():
        try:
            expr = parse(jsonpath_expr)
            match = expr.find(resp)
            if match:
                context.GLOBAL_VARS[key] = match[0].value
                print(f"🟢 提取变量: {key} = {match[0].value}")
        except Exception as e:
            print(f"❌ 提取变量失败: {key} - {e}")

    # 断言校验
    for a in asserts:
        expr = parse(a['path'])
        match = expr.find(resp)

        if 'equals' in a:
            assert match, f"[断言失败] 路径 {a['path']} 未找到！完整响应: {json.dumps(resp, ensure_ascii=False)}"
            actual_value = match[0].value
            expected_value = a['equals']
            print(json.dumps(resp, ensure_ascii=False))
            assert actual_value == expected_value, (
                f"[断言失败] 路径 {a['path']}，实际值: {actual_value}，预期值: {expected_value}。\n完整响应: {json.dumps(resp, ensure_ascii=False)}"
            )

        if 'exists' in a:
            actual_exists = bool(match)
            expected_exists = a['exists']
            assert actual_exists == expected_exists, (
                f"[断言失败] 路径 {a['path']} 是否存在，实际: {actual_exists}，预期: {expected_exists}。\n完整响应: {json.dumps(resp, ensure_ascii=False)}"
            )
# conftest.py
def pytest_addoption(parser):
    parser.addoption(
        "--case",
        action="store",
        default="",
        help="指定只运行某个模块的用例，例如 --case=login 将只运行 login_cases.yaml"
    )
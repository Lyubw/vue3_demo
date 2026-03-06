"""pytest conftest - 共享 fixture 与报告生成"""
import json
import os
import pytest
from datetime import datetime

@pytest.fixture(scope="session")
def base_url():
    return "https://jsonplaceholder.typicode.com"

def pytest_sessionfinish(session, exitstatus):
    """测试结束后生成 JSON 报告"""
    try:
        from test_api import _case_results
    except ImportError:
        _case_results = []
    report_dir = os.path.dirname(os.path.abspath(__file__))
    report_path = os.path.join(report_dir, "test_report_data.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(_case_results, f, ensure_ascii=False, indent=2)

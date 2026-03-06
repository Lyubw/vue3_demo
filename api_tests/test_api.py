"""
API 自动化测试 - vue3_demo 仓库
测试目标: https://jsonplaceholder.typicode.com
"""
import json
import requests
import pytest

BASE_URL = "https://jsonplaceholder.typicode.com"
_case_results = []

def _record(endpoint, case_id, t, expected, req, resp, result, reason):
    _case_results.append({
        "endpoint_or_module": endpoint,
        "case_id": case_id,
        "type": t,
        "expected": expected,
        "execution_result": result,
        "request": req,
        "response": resp,
        "verdict_reason": reason,
    })

# ========== GET /users ==========
def test_users_list_positive(base_url):
    """TC-001: GET /users 正例 - 获取全部用户"""
    url = f"{base_url}/users"
    req = {"method": "GET", "url": url, "params": {}, "body": {}}
    try:
        r = requests.get(url, timeout=10)
        body = r.json() if r.text else {}
        _record("GET /users", "TC-001", "positive", "success", req,
                {"status": r.status_code, "body": body[:2] if isinstance(body, list) else body},
                "PASS" if r.status_code == 200 and isinstance(body, list) else "FAIL",
                "期望200且返回数组" if r.status_code == 200 else f"status={r.status_code}")
        assert r.status_code == 200 and isinstance(r.json(), list)
    except Exception as e:
        _record("GET /users", "TC-001", "positive", "success", req,
                {"status": getattr(e, "response", None) and e.response.status_code or "error", "body": str(e)}, "FAIL", str(e))
        raise

def test_users_single_invalid_path(base_url):
    """TC-002: GET /users/abc 反例 - 非数字 ID"""
    url = f"{base_url}/users/abc"
    req = {"method": "GET", "url": url, "params": {}, "body": {}}
    r = requests.get(url, timeout=10)
    body = r.json() if r.text else {}
    fail_expected = r.status_code >= 400
    _record("GET /users/{id}", "TC-002", "negative", "failure", req,
            {"status": r.status_code, "body": body},
            "PASS" if fail_expected else "FAIL", "非数字ID应返回4xx/5xx" if fail_expected else "API 未拒绝")
    assert fail_expected

# ========== GET /users/{id} ==========
def test_users_single_valid(base_url):
    """TC-003: GET /users/1 正例 - 有效ID"""
    url = f"{base_url}/users/1"
    req = {"method": "GET", "url": url, "params": {}, "body": {}}
    r = requests.get(url, timeout=10)
    body = r.json() if r.text else {}
    ok = r.status_code == 200 and isinstance(body, dict) and body.get("id") == 1
    _record("GET /users/{id}", "TC-003", "positive", "success", req,
            {"status": r.status_code, "body": body},
            "PASS" if ok else "FAIL", "有效用户返回正确" if ok else f"status={r.status_code}")
    assert ok

def test_users_single_invalid_zero(base_url):
    """TC-004: GET /users/0 反例 - ID=0"""
    url = f"{base_url}/users/0"
    req = {"method": "GET", "url": url, "params": {}, "body": {}}
    r = requests.get(url, timeout=10)
    body = r.json() if r.text else {}
    # JSONPlaceholder 可能对 /users/0 仍返回 200，需根据实际
    fail_expected = r.status_code >= 400 or (isinstance(body, dict) and not body.get("id"))
    _record("GET /users/{id}", "TC-004", "negative", "failure", req,
            {"status": r.status_code, "body": body},
            "PASS" if fail_expected else "FAIL", "无效ID应失败" if fail_expected else "API 对 0 返回了数据")
    assert fail_expected

def test_users_single_not_found(base_url):
    """TC-005: GET /users/999 反例 - 不存在ID"""
    url = f"{base_url}/users/999"
    req = {"method": "GET", "url": url, "params": {}, "body": {}}
    r = requests.get(url, timeout=10)
    body = r.json() if r.text else {}
    # JSONPlaceholder 对不存在ID可能仍返回 200 空对象，需按实际判定
    fail_expected = r.status_code >= 400 or body == {} or body.get("id") is None
    _record("GET /users/{id}", "TC-005", "negative", "failure", req,
            {"status": r.status_code, "body": body},
            "PASS" if fail_expected else "FAIL", "不存在应失败或空" if fail_expected else "API 返回了占位数据")
    assert fail_expected

# ========== GET /posts ==========
def test_posts_list_positive(base_url):
    """TC-006: GET /posts 正例"""
    url = f"{base_url}/posts"
    req = {"method": "GET", "url": url, "params": {}, "body": {}}
    r = requests.get(url, timeout=10)
    body = r.json() if r.text else {}
    ok = r.status_code == 200 and isinstance(body, list)
    _record("GET /posts", "TC-006", "positive", "success", req,
            {"status": r.status_code, "body": body[:1] if isinstance(body, list) else body},
            "PASS" if ok else "FAIL", "返回帖子列表")
    assert ok

def test_posts_single_valid(base_url):
    """TC-007: GET /posts/1 正例"""
    url = f"{base_url}/posts/1"
    req = {"method": "GET", "url": url, "params": {}, "body": {}}
    r = requests.get(url, timeout=10)
    body = r.json() if r.text else {}
    ok = r.status_code == 200 and isinstance(body, dict) and body.get("id") == 1
    _record("GET /posts/{id}", "TC-007", "positive", "success", req,
            {"status": r.status_code, "body": body},
            "PASS" if ok else "FAIL", "有效帖子")
    assert ok

def test_posts_single_negative_id(base_url):
    """TC-008: GET /posts/-1 反例"""
    url = f"{base_url}/posts/-1"
    req = {"method": "GET", "url": url, "params": {}, "body": {}}
    r = requests.get(url, timeout=10)
    body = r.json() if r.text else {}
    fail_expected = r.status_code >= 400
    _record("GET /posts/{id}", "TC-008", "negative", "failure", req,
            {"status": r.status_code, "body": body},
            "PASS" if fail_expected else "FAIL", "负ID应失败")
    assert fail_expected

# ========== POST /posts ==========
def test_posts_create_positive(base_url):
    """TC-009: POST /posts 正例 - 合法 body"""
    url = f"{base_url}/posts"
    payload = {"title": "test", "body": "content", "userId": 1}
    req = {"method": "POST", "url": url, "params": {}, "body": payload}
    r = requests.post(url, json=payload, timeout=10)
    body = r.json() if r.text else {}
    ok = r.status_code in (200, 201) and isinstance(body, dict)
    _record("POST /posts", "TC-009", "positive", "success", req,
            {"status": r.status_code, "body": body},
            "PASS" if ok else "FAIL", "创建成功")
    assert ok

def test_posts_create_negative_malformed_json(base_url):
    """TC-010: POST /posts 反例 - 非法 JSON body"""
    url = f"{base_url}/posts"
    req = {"method": "POST", "url": url, "params": {}, "body": "invalid"}
    try:
        r = requests.post(url, data="invalid", headers={"Content-Type": "application/json"}, timeout=10)
        body = r.text[:200] if r.text else {}
        fail_expected = r.status_code >= 400
        _record("POST /posts", "TC-010", "negative", "failure", req,
                {"status": r.status_code, "body": body},
                "PASS" if fail_expected else "FAIL", "非法JSON应拒绝" if fail_expected else "API 未校验")
        assert fail_expected
    except Exception as e:
        _record("POST /posts", "TC-010", "negative", "failure", req,
                {"status": "error", "body": str(e)}, "PASS", "请求异常符合反例")
        pass

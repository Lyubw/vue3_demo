# vue3_demo API 自动化测试 — 人类可读总结

## 执行概况

| 指标 | 数值 |
|------|------|
| 总用例数 | 10 |
| 通过 | 10 |
| 失败 | 0 |
| 跳过 | 0 |
| 通过率 | 100.00% |
| 接口通过 | 5/5 |

## 测试目标

- **仓库**: https://github.com/Lyubw/vue3_demo (main)
- **测试类型**: API
- **被测地址**: https://jsonplaceholder.typicode.com
- **原因**: 仓库无内置后端，`example.ts` 的 `fetchData(url)` 设计为调用外部 API，故选用 JSONPlaceholder 作为联调/回归对象。

## 失败清单

无。全部 10 个用例通过。

## 修复建议

1. 全量通过，建议将 `api_tests/` 纳入 CI 流水线定期执行。
2. 若后续接入自有后端，可替换 `base_url` 指向真实环境后复用本套用例。

## 关键执行日志证据

```
test_api.py::test_users_list_positive PASSED
test_api.py::test_users_single_invalid_path PASSED
test_api.py::test_users_single_valid PASSED
test_api.py::test_users_single_invalid_zero PASSED
test_api.py::test_users_single_not_found PASSED
test_api.py::test_posts_list_positive PASSED
test_api.py::test_posts_single_valid PASSED
test_api.py::test_posts_single_negative_id PASSED
test_api.py::test_posts_create_positive PASSED
test_api.py::test_posts_create_negative_malformed_json PASSED
============================== 10 passed in 0.44s ==============================
```

## 请求响应证据示例

**TC-001 GET /users 正例**
- 请求: `GET https://jsonplaceholder.typicode.com/users`
- 响应: `200 OK`，body 为 10 个用户对象的数组

**TC-010 POST 非法 JSON 反例**
- 请求: `POST https://jsonplaceholder.typicode.com/posts`，body: `"invalid"`
- 响应: `500 Internal Server Error`，body 含 JSON 解析错误信息

## 产物路径

- `api_tests/pytest_report.html` — HTML 报告
- `api_tests/AUTO_TEST_REPORT.json` — 结构化 JSON 报告
- `api_tests/test_report_data.json` — 原始用例明细

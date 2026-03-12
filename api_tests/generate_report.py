#!/usr/bin/env python3
"""
根据测试数据生成结构化报告
"""
import json
import os
import subprocess
import sys
from datetime import datetime

def load_case_results():
    report_path = os.path.join(os.path.dirname(__file__), "test_report_data.json")
    if not os.path.exists(report_path):
        return []
    with open(report_path, "r", encoding="utf-8") as f:
        return json.load(f)

def build_report(case_details_raw):
    passed = sum(1 for c in case_details_raw if c.get("execution_result") == "PASS")
    failed = sum(1 for c in case_details_raw if c.get("execution_result") == "FAIL")
    total = len(case_details_raw)
    pass_rate = f"{(passed / total * 100):.2f}%" if total else "0.00%"

    interfaces = {}
    for c in case_details_raw:
        ep = c.get("endpoint_or_module", "unknown")
        if ep not in interfaces:
            interfaces[ep] = {"passed": 0, "failed": 0}
        if c.get("execution_result") == "PASS":
            interfaces[ep]["passed"] += 1
        else:
            interfaces[ep]["failed"] += 1
    interface_passed = sum(1 for v in interfaces.values() if v["failed"] == 0)
    interface_not_passed = len(interfaces) - interface_passed

    failures = [f"{c.get('case_id','?'):s}: {c.get('verdict_reason','')}" for c in case_details_raw if c.get("execution_result") == "FAIL"]

    case_details = []
    for c in case_details_raw:
        ep = c.get("endpoint_or_module", "unknown")
        iv = "interface_passed" if interfaces.get(ep, {}).get("failed", 1) == 0 else "interface_not_passed"
        case_details.append({
            "endpoint_or_module": ep,
            "case_id": c.get("case_id", ""),
            "type": c.get("type", ""),
            "expected": c.get("expected", ""),
            "execution_result": c.get("execution_result", ""),
            "interface_verdict": iv,
            "request": c.get("request", {}),
            "response": c.get("response", {}),
            "verdict_reason": c.get("verdict_reason", ""),
        })

    recommendations = []
    if failed > 0:
        recommendations.append("检查失败用例的请求参数与预期响应")
    if interface_not_passed > 0:
        recommendations.append("对接口进行专项回归")
    if not recommendations:
        recommendations.append("全量通过，建议将 api_tests 纳入 CI 定期执行")

    return {
        "report_title": "vue3_demo API 自动化测试报告",
        "test_type": "api",
        "repository": "https://github.com/Lyubw/vue3_demo",
        "ref": "main",
        "summary": {
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_cases": total,
            "passed": passed,
            "failed": failed,
            "skipped": 0,
            "pass_rate": pass_rate,
            "interface_verdict": {
                "interface_passed": interface_passed,
                "interface_not_passed": interface_not_passed,
            },
        },
        "failures": failures,
        "case_details": case_details,
        "recommendations": recommendations,
        "artifacts": [
            {"name": "pytest_report.html", "description": "pytest-html 生成的 HTML 报告"},
            {"name": "test_report_data.json", "description": "用例执行明细原始数据"},
        ],
    }

def main():
    case_details_raw = load_case_results()
    report = build_report(case_details_raw)

    out_path = os.path.join(os.path.dirname(__file__), "AUTO_TEST_REPORT.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"Report written to {out_path}")
    return report

if __name__ == "__main__":
    main()

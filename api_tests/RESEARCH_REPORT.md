# vue3_demo 仓库调研报告

## 1. 仓库概况
- **仓库**: https://github.com/Lyubw/vue3_demo
- **分支**: main
- **最新提交**: 2f40d48 - Add user processing and database connection functions

## 2. 代码结构
仓库为极简结构，仅包含：
- `README.md` - 项目说明（仅标题）
- `example.ts` - 含三个函数：
  - `processUsers(users)` - 遍历用户并输出 name
  - `connectToDb(password)` - 构建数据库连接字符串
  - `fetchData(url)` - 异步从 URL 拉取 JSON 数据

## 3. 测试目标说明
**仓库内无内置 API 服务。** `fetchData` 设计为调用外部 URL，与 REST API 交互模式一致。
**测试策略**: 使用 JSONPlaceholder 公共 API 作为被测目标，因其与 `example.ts` 中的 users/数据获取场景高度匹配。

**测试目标地址**: `https://jsonplaceholder.typicode.com`
- GET /users - 用户列表
- GET /users/{id} - 单用户
- GET /posts - 帖子列表
- GET /posts/{id} - 单帖子
- POST /posts - 创建帖子

## 4. 测试数据矩阵

| 功能/接口 | 用例ID | 类型 | 预期 | 说明 |
|-----------|--------|------|------|------|
| GET /users | TC-001 | positive | success | 获取全部用户 |
| GET /users/{id} | TC-002 | negative | failure | 非数字 ID (abc) |
| GET /users/1 | TC-003 | positive | success | 获取有效ID用户 |
| GET /users/0 | TC-004 | negative | failure | 无效ID边界 |
| GET /users/999 | TC-005 | negative | failure | 不存在的ID |
| GET /posts | TC-006 | positive | success | 获取全部帖子 |
| GET /posts/1 | TC-007 | positive | success | 获取有效帖子 |
| GET /posts/-1 | TC-008 | negative | failure | 负ID |
| POST /posts | TC-009 | positive | success | 合法body创建 |
| POST /posts | TC-010 | negative | failure | 非法 JSON body |

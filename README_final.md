# NAS Bot - 增强版聊天机器人

这是一个功能丰富的OneBot 11协议聊天机器人，基于Flask框架开发，支持多种聊天功能和群组互动。

## ✨ 功能特性

### 🤖 智能聊天

- 关键词智能识别和回复
- 情感分析和响应
- 智能问答系统
- 自然语言处理

### 🎮 娱乐游戏

- 猜数字游戏
- 石头剪刀布
- 随机抽签
- 趣味问答

### 🛠️ 实用工具

- 天气查询
- 计算器功能
- 时间查询
- 随机笑话

### 👥 群组功能

- 群签到系统
- 积分管理
- @提醒响应
- 群组管理命令

### 🔧 系统功能

- YAML配置管理
- 多服务器支持
- 详细日志记录
- API状态监控

## 📁 文件结构

### 🚀 主要服务器

- **`enhanced_chat_bot.py`** - 增强版聊天机器人 (推荐)
  - 丰富的聊天功能
  - 游戏和娱乐系统
  - 群组互动功能
  - YAML配置支持

### 🔧 配置文件

- **`config.yml`** - 主配置文件
  - NapCat API设置
  - 聊天功能配置
  - 服务器设置

### 📚 其他实现

- `flask_onebot_server.py` - 基础OneBot服务器
- `flask_message_handler.py` - 简化消息处理器
- `flask_message_viewer.py` - 消息查看器
- `flask_json_capture.py` - 请求捕获器

## 🛠️ 安装和使用

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置机器人

编辑 `config.yml` 文件：

```yaml
# NapCat API 配置
napcat:
  host: "localhost"
  port: 3000
  token: "5Z?Rm$@2JwDFS:Ut"
```

### 3. 运行机器人

```bash
# 启动增强版聊天机器人
python enhanced_chat_bot.py
```

## 🎮 使用指南

### 基础命令

```
/help - 显示帮助信息
/time - 查看当前时间
/weather 城市 - 查询天气
/calc 表达式 - 计算器
/joke - 随机笑话
```

### 游戏命令

```
/guess - 开始猜数字游戏
/rps 石头/剪刀/布 - 石头剪刀布
/draw - 随机抽签
/quiz - 趣味问答
```

### 群组命令

```
/signin - 群签到
/points - 查看积分
/rank - 积分排行榜
```

## 📊 API端点

- `POST /` - 接收OneBot消息推送
- `GET /status` - 获取机器人状态
- `GET /stats` - 查看统计数据

## 🔍 故障排除

### 常见问题

1. **机器人不响应**: 检查NapCat配置和网络连接
2. **游戏功能异常**: 检查config.yml中的游戏设置
3. **积分系统问题**: 检查数据存储文件权限

### 调试步骤

1. 运行 `flask_json_capture.py` 查看原始请求
2. 检查 `/status` 端点确认服务器运行状态
3. 查看控制台输出的错误信息

## 📄 许可证

MIT License
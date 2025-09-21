# NAS Bot - 智能聊天机器人

这是一个功能丰富的OneBot 11协议聊天机器人，基于Flask框架开发，支持智能对话、游戏娱乐、群组互动等多种功能。

## ✨ 主要特性

### 🤖 智能对话
- 情感识别和响应
- 关键词智能回复
- 上下文理解
- 自然语言交互

### 🎮 游戏娱乐
- 猜数字游戏
- 石头剪刀布
- 掷骰子和抛硬币
- 抽签占卜
- 随机笑话

### 🔧 实用工具
- 计算器功能
- 时间查询
- 文本回显
- 随机数生成

### 👥 群组功能
- 每日签到系统
- 积分奖励机制
- 消息统计
- @提醒响应

## 📁 项目结构

### 🚀 推荐使用

- **`enhanced_chat_bot.py`** - 增强版聊天机器人 (⭐ 推荐)
  - 完整的智能对话系统
  - 游戏和娱乐功能
  - 群组互动和积分系统
  - YAML配置管理

- **`config.yml`** - 配置文件
  - NapCat API设置
  - 机器人功能配置
  - 游戏和聊天参数

### � Flask服务器系列

- **`flask_onebot_server.py`** - 完整的OneBot 11 HTTP服务器
  - 支持完整的消息处理和自动回复
  - 包含配置管理和API集成
  - 支持命令处理和关键词响应

- **`flask_message_handler.py`** - 简化的消息处理器
  - 专注于用户消息内容和发送者信息
  - 支持基础命令和关键词回复
  - 轻量级实现

- **`flask_message_viewer.py`** - 消息查看器
  - 只显示消息，不自动回复
  - 适合消息监控和调试

- **`flask_json_capture.py`** - 原始请求捕获器
  - 捕获并保存NapCat的原始请求
  - 支持API查看已保存的请求
  - 用于调试和分析

### 📚 原始实现 (仅供参考)

- `onebot_server.py` - 原始HTTP服务器实现
- `message_handler.py` - 简化消息处理器
- `message_viewer.py` - 消息查看器
- `napcat_json_capture.py` - JSON捕获器

## 🛠️ 安装和使用

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置NapCat

在NapCat中设置HTTP回调地址：
```
http://your-server:8080/
```

### 3. 运行服务器

选择一个Flask服务器运行：

```bash
# 完整服务器
python flask_onebot_server.py

# 简化处理器
python flask_message_handler.py

# 消息查看器
python flask_message_viewer.py

# 请求捕获器
python flask_json_capture.py
```

## ⚙️ 配置

### onebot_config.json (flask_onebot_server.py使用)

```json
{
  "napcat": {
    "host": "localhost",
    "port": 3000,
    "token": "your-token"
  },
  "bot": {
    "name": "NAS Bot",
    "auto_reply": true,
    "command_prefix": "/",
    "admin_users": []
  },
  "server": {
    "host": "0.0.0.0",
    "port": 8080,
    "debug": false
  }
}
```

## 📊 API端点

### 通用端点

- `POST /` - 接收OneBot消息推送
- `GET /status` - 获取服务器状态

### flask_json_capture.py 特有端点

- `GET /files` - 列出已捕获的文件
- `GET /files/<filename>` - 获取指定文件内容

## 🔧 功能特性

### 消息处理
- ✅ 私聊和群聊消息处理
- ✅ 发送者信息提取
- ✅ 消息内容解析
- ✅ 附件类型识别

### 命令系统
- ✅ `/help` - 显示帮助
- ✅ `/time` - 显示当前时间
- ✅ `/hello` - 打招呼

### 关键词响应
- ✅ 你好/hello - 自动问候
- ✅ 帮助 - 显示帮助信息

### 调试功能
- ✅ 详细错误日志
- ✅ 原始数据保存
- ✅ JSON解析错误处理

## 🚀 选择建议

- **新手用户**: 使用 `flask_message_viewer.py` 先观察消息
- **简单自动回复**: 使用 `flask_message_handler.py`
- **完整功能**: 使用 `flask_onebot_server.py`
- **调试分析**: 使用 `flask_json_capture.py`

## 📝 注意事项

1. 确保NapCat正在运行并配置了正确的回调地址
2. 检查防火墙设置，确保8080端口可访问
3. 在生产环境中建议修改默认端口和token
4. 建议使用虚拟环境安装依赖

## 🔍 故障排除

### 常见问题

1. **连接被拒绝**: 检查NapCat是否运行，端口是否正确
2. **JSON解析错误**: 使用捕获器查看原始请求
3. **消息不回复**: 检查token配置和API地址
4. **权限错误**: 确保机器人有发送消息的权限

### 调试步骤

1. 运行 `flask_json_capture.py` 查看原始请求
2. 检查 `/status` 端点确认服务器运行状态
3. 查看控制台输出的错误信息
4. 验证NapCat配置和网络连接

## 📄 许可证

MIT License
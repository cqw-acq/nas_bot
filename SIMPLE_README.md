# 简化版OneBot消息处理器

这里提供了三个简化版的OneBot服务器，专门用于处理用户发送的消息内容和发送者信息。

## 📁 文件说明

### 1. `message_viewer.py` - 消息查看器（推荐用于调试）
- 🔍 **功能**: 显示接收到的消息详细信息
- 👁️ **用途**: 调试和查看NapCat推送的消息格式
- 📋 **输出**: 格式化显示消息内容、发送者信息等

### 2. `message_handler.py` - 消息处理器（推荐用于实际使用）
- 🤖 **功能**: 处理消息并支持自动回复
- ⚡ **特性**: 支持命令处理、关键词回复
- 🔧 **命令**: `/time`, `/hello`, `/help`
- 💬 **回复**: 自动识别"你好"、"帮助"等关键词

### 3. `simple_onebot.py` - 基础框架
- 🏗️ **功能**: 提供基础的消息处理框架
- 🔧 **用途**: 可以基于此进行自定义开发

## 🚀 快速开始

### 1. 启动消息查看器（调试推荐）
```bash
python message_viewer.py
```

**输出示例:**
```
⏰ 时间: 14:30:25
💬 私聊消息
👤 发送者: 张三 (QQ: 123456789)
💭 消息内容: 你好
🔧 检测到命令: /help
```

### 2. 启动消息处理器（实际使用推荐）
```bash
python message_handler.py
```

**功能:**
- 自动回复"你好"等关键词
- 处理 `/time`、`/hello`、`/help` 命令
- 可以发送回复到QQ（需要配置NapCat信息）

### 3. 配置NapCat

在 `message_handler.py` 中修改配置：
```python
NAPCAT_HOST = "localhost"    # NapCat地址
NAPCAT_PORT = 3000          # NapCat端口
NAPCAT_TOKEN = "your_token" # 你的token
```

在NapCat配置中添加推送地址：
```json
{
  "http": {
    "enable": true,
    "postUrls": ["http://localhost:8080/"]
  }
}
```

## 📋 核心功能

### 提取的信息
```python
user_id = data.get('user_id')           # 发送者QQ号
message = data.get('raw_message', '')   # 消息内容
nickname = sender.get('nickname', '')   # 发送者昵称
message_type = data.get('message_type') # private/group
group_id = data.get('group_id')         # 群号（群聊时）
```

### 消息类型判断
```python
if message_type == 'private':
    # 私聊消息
    print(f"私聊 | {nickname}: {message}")
    
elif message_type == 'group':
    # 群聊消息
    print(f"群聊({group_id}) | {nickname}: {message}")
```

### 命令处理
```python
if message.startswith('/'):
    command = message[1:].split()[0]
    if command == 'time':
        # 处理时间命令
    elif command == 'help':
        # 处理帮助命令
```

## 🧪 测试

运行测试脚本：
```bash
python test_simple.py
```

测试包括：
- ✅ 私聊消息处理
- ✅ 群聊消息处理
- ✅ 命令识别
- ✅ 无效JSON处理

## 📝 自定义开发

### 添加新命令
在 `message_handler.py` 的 `process_command` 方法中添加：

```python
elif command == 'weather':
    reply = "今天天气不错"
    self.send_reply(reply, user_id, group_id, message_type)
```

### 添加新关键词
在 `process_keyword` 方法中添加：

```python
elif '天气' in message:
    reply = "今天天气很好"
    self.send_reply(reply, user_id, group_id, message_type)
```

### 保存消息到文件
```python
def save_message(self, user_id, nickname, message):
    with open('messages.txt', 'a', encoding='utf-8') as f:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"[{timestamp}] {nickname}({user_id}): {message}\n")
```

## 🔧 故障排除

### 1. JSON解析错误
- ✅ 已自动处理控制字符
- ✅ 自动忽略解析失败的数据
- ✅ 详细错误日志记录

### 2. 连接问题
```bash
# 检查端口占用
lsof -i :8080

# 检查服务器状态
curl http://localhost:8080/
```

### 3. NapCat配置
确保NapCat的HTTP推送功能已启用，并且推送地址正确。

## ⚡ 性能特点

- 🚀 **轻量级**: 只处理必要的消息信息
- 🔒 **稳定性**: 自动处理JSON解析错误
- 📝 **简洁性**: 专注于消息内容和发送者
- 🛠️ **易扩展**: 简单的代码结构，易于修改

## 💡 使用建议

1. **调试阶段**: 使用 `message_viewer.py` 查看消息格式
2. **开发阶段**: 基于 `message_handler.py` 添加功能
3. **生产环境**: 根据需要选择合适的版本

这三个简化版本专门设计用于只处理消息内容和发送者信息，去除了复杂的功能，让你可以专注于核心的消息处理逻辑。
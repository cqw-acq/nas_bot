# OneBot 11 HTTP服务端

这是一个完整的OneBot 11标准HTTP服务端实现，专门用于接收NapCat推送的消息和事件。

## 📋 功能特性

### 🔧 核心功能
- ✅ 符合OneBot 11标准的HTTP服务端
- ✅ 接收NapCat推送的所有事件类型
- ✅ 支持消息、通知、请求、元事件处理
- ✅ 完整的API调用功能
- ✅ 安全验证（Token、签名）
- ✅ 消息队列和日志记录

### 🤖 消息处理
- ✅ 私聊和群聊消息处理
- ✅ 图片、语音、视频等多媒体消息
- ✅ CQ码解析和构建
- ✅ 自动回复机制
- ✅ 自定义命令系统

### 👨‍💼 管理功能
- ✅ 群管理命令（踢人、禁言、解禁）
- ✅ 权限控制系统
- ✅ 群白名单机制
- ✅ 管理员专用命令

### 🛠️ 开发友好
- ✅ 易于扩展的插件架构
- ✅ 完整的API封装
- ✅ 详细的日志记录
- ✅ 配置文件热重载

## 📁 文件结构

```
nas_bot/
├── onebot_server.py      # 主服务端文件
├── onebot_api.py         # API调用模块
├── onebot_example.py     # 使用示例和扩展演示
├── onebot_config.json    # 配置文件
└── onebot.log           # 日志文件（运行时生成）
```

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install requests
```

### 2. 配置文件

编辑 `onebot_config.json`：

```json
{
  "host": "0.0.0.0",
  "port": 8080,
  "napcat_host": "localhost",
  "napcat_port": 3000,
  "napcat_token": "your_token_here",
  "secret": "your_secret_here",
  "access_token": "your_access_token_here",
  "enable_heartbeat": true,
  "heartbeat_interval": 5000,
  "enable_message_log": true,
  "enable_auto_reply": true,
  "auto_reply_keywords": {
    "你好": "你好！有什么可以帮助你的吗？",
    "帮助": "输入 /help 查看可用命令",
    "ping": "pong! 机器人在线"
  }
}
```

### 3. 启动服务器

#### 基础版本：
```bash
python onebot_server.py
```

#### 扩展版本（推荐）：
```bash
python onebot_example.py
```

### 4. 配置NapCat

在NapCat的配置文件中添加HTTP推送地址：

```json
{
  "http": {
    "enable": true,
    "host": "0.0.0.0",
    "port": 3000,
    "secret": "your_secret_here",
    "enableHeart": true,
    "enablePost": true,
    "postUrls": ["http://localhost:8080/"]
  }
}
```

## 📝 配置说明

### 服务器配置
- `host`: 监听地址（0.0.0.0表示所有接口）
- `port`: 监听端口
- `napcat_host`: NapCat的地址
- `napcat_port`: NapCat的端口

### 安全配置
- `napcat_token`: NapCat的访问令牌
- `secret`: HTTP推送签名密钥
- `access_token`: 访问令牌验证

### 功能配置
- `enable_heartbeat`: 是否启用心跳
- `heartbeat_interval`: 心跳间隔（毫秒）
- `enable_message_log`: 是否记录消息日志
- `enable_auto_reply`: 是否启用自动回复
- `auto_reply_keywords`: 自动回复关键词配置

## 🎯 使用示例

### 基本命令（所有用户）

```
/help          - 显示帮助菜单
/time          - 显示当前时间
/ping          - 测试机器人连接
/status        - 显示机器人状态
/random 1 100  - 生成1-100随机数
/quote         - 显示随机名言
/weather 北京   - 查询天气（需要接入API）
/translate Hello - 翻译文本（需要接入API）
```

### 管理员命令（需要权限）

```
!kick @用户      - 踢出群成员
!ban @用户 30    - 禁言用户30分钟
!unban @用户     - 解除用户禁言
!mute on        - 开启全体禁言
!mute off       - 关闭全体禁言
!info @用户     - 获取用户信息
!say 内容       - 让机器人发送消息
```

### 自动回复

在配置文件中设置的关键词会自动触发回复：

```
用户: 你好
机器人: 你好！有什么可以帮助你的吗？

用户: ping
机器人: pong! 机器人在线
```

## 🔧 API调用示例

```python
from onebot_api import OneBotAPI, MessageBuilder

# 初始化API客户端
api = OneBotAPI(host='localhost', port=3000, token='your_token')

# 发送文本消息
api.send_private_msg(user_id=123456789, message="Hello!")

# 发送带@的群消息
message = MessageBuilder.combine(
    MessageBuilder.at(123456789),
    MessageBuilder.text(" 你好！"),
    MessageBuilder.face(1)
)
api.send_group_msg(group_id=987654321, message=message)

# 获取群列表
groups = api.get_group_list()
print(groups)

# 获取好友列表
friends = api.get_friend_list()
print(friends)
```

## 🛠️ 自定义扩展

### 1. 自定义消息处理器

```python
from onebot_server import OneBotMessageProcessor

class MyMessageProcessor(OneBotMessageProcessor):
    def handle_custom_message(self, data):
        message = data.get('raw_message', '')
        
        # 添加你的自定义逻辑
        if '天气' in message:
            self.send_reply(data, "请使用 /weather 城市名 查询天气")
        elif '翻译' in message:
            self.send_reply(data, "请使用 /translate 文本 进行翻译")
```

### 2. 添加新功能

```python
def handle_command(self, data, message):
    command = message[1:].split()[0].lower()
    args = message[1:].split()[1:]
    
    if command == 'mycommand':
        self.handle_my_command(data, args)
    else:
        super().handle_command(data, message)

def handle_my_command(self, data, args):
    # 实现你的自定义命令
    self.send_reply(data, "这是我的自定义命令!")
```

## 📊 事件类型

### 消息事件 (message)
- `private`: 私聊消息
- `group`: 群聊消息

### 通知事件 (notice)
- `group_increase`: 群成员增加
- `group_decrease`: 群成员减少
- `friend_add`: 好友添加

### 请求事件 (request)
- `friend`: 好友请求
- `group`: 群请求

### 元事件 (meta_event)
- `heartbeat`: 心跳
- `lifecycle`: 生命周期

## 🔒 安全注意事项

1. **修改默认配置**: 务必修改配置文件中的token和secret
2. **网络安全**: 在生产环境中使用HTTPS和防火墙
3. **权限控制**: 合理配置管理员列表和群白名单
4. **日志监控**: 定期检查日志文件，监控异常行为

## 🐛 故障排除

### 常见问题

1. **端口被占用**
   ```bash
   lsof -i :8080
   # 杀死占用进程或更换端口
   ```

2. **NapCat连接失败**
   - 检查NapCat是否正常运行
   - 检查网络连接和防火墙设置
   - 验证token和地址配置

3. **消息发送失败**
   - 检查API地址和端口
   - 验证访问令牌
   - 查看日志文件获取详细错误信息

4. **权限验证失败**
   - 检查secret配置是否正确
   - 确认NapCat的签名设置
   - 验证access_token配置

### 日志文件

查看 `onebot.log` 文件获取详细的运行日志：

```bash
tail -f onebot.log
```

## 🔄 更新日志

### v1.0.0
- ✅ 实现完整的OneBot 11标准
- ✅ 支持所有消息和事件类型
- ✅ 完整的API调用功能
- ✅ 安全验证和权限控制
- ✅ 丰富的示例和文档

## 📞 支持

如果遇到问题或需要帮助：

1. 查看日志文件 `onebot.log`
2. 检查配置文件是否正确
3. 参考示例代码 `onebot_example.py`
4. 阅读OneBot 11官方文档

## 📄 许可证

本项目基于MIT许可证开源。
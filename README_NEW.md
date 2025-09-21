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

# 机器人设置
bot:
  name: "NAS Bot"
  master_qq: []  # 主人QQ号列表
  
# 聊天功能
chat:
  auto_reply: true
  smart_reply: true
  emotion_response: true
```

### 3. 运行机器人

```bash
# 启动增强版聊天机器人
python enhanced_chat_bot.py

# 或使用启动器
python run_flask.py enhanced
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
/admin help - 管理员命令
```

### 智能对话

机器人支持自然语言对话：

```
"你好" → 自动问候
"谢谢" → 客气回应
"再见" → 告别回应
"天气怎么样" → 引导天气查询
"无聊" → 推荐游戏
```

## 📊 API端点

### 主要端点

- `POST /` - 接收OneBot消息推送
- `GET /status` - 获取机器人状态
- `GET /stats` - 查看统计数据

### 管理端点

- `GET /config` - 查看配置信息
- `POST /config` - 更新配置
- `GET /logs` - 查看日志

## 🔧 高级配置

### 自定义回复

在 `config.yml` 中添加自定义回复：

```yaml
custom_replies:
  keywords:
    "早上好": ["早上好！", "早安～", "新的一天开始了！"]
    "晚安": ["晚安～", "好梦！", "明天见！"]
  
  patterns:
    "我是(.+)": "你好 {1}，很高兴认识你！"
    "(.+)多少钱": "这个我不太清楚价格呢"
```

### 群组管理

```yaml
group_settings:
  signin_reward: 10  # 签到奖励积分
  max_points: 10000  # 最大积分
  admin_commands: true  # 启用管理命令
  
  welcome_message: "欢迎新成员加入群组！"
  goodbye_message: "再见，希望你一切顺利！"
```

### 游戏设置

```yaml
games:
  guess_number:
    min_range: 1
    max_range: 100
    max_attempts: 6
  
  quiz:
    categories: ["general", "tech", "entertainment"]
    difficulty: "medium"
```

## 🚀 部署建议

### 本地开发

```bash
python enhanced_chat_bot.py
```

### 生产环境

```bash
# 使用 gunicorn
gunicorn -w 4 -b 0.0.0.0:8080 enhanced_chat_bot:app

# 使用 systemd 服务
sudo systemctl start nas-bot
sudo systemctl enable nas-bot
```

### Docker 部署

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8080

CMD ["python", "enhanced_chat_bot.py"]
```

## 🔍 故障排除

### 常见问题

1. **机器人不响应**
   - 检查NapCat配置和网络连接
   - 验证token和API地址
   - 查看控制台错误日志

2. **游戏功能异常**
   - 检查config.yml中的游戏设置
   - 确认用户权限配置
   - 查看游戏状态存储

3. **积分系统问题**
   - 检查数据存储文件权限
   - 验证群组配置
   - 重置积分数据

### 调试模式

```bash
# 启用详细日志
export FLASK_ENV=development
python enhanced_chat_bot.py

# 使用调试配置
python enhanced_chat_bot.py --debug
```

## 📈 统计功能

机器人自动记录：
- 消息处理数量
- 命令使用统计
- 游戏参与数据
- 用户活跃度
- 群组互动情况

访问 `/stats` 端点查看详细统计。

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 发起 Pull Request

## 📄 许可证

MIT License

## 📞 联系方式

如有问题或建议，请提交 Issue 或联系开发者。

---

💡 **提示**: 建议先使用 `flask_message_viewer.py` 观察消息格式，再启用完整的聊天功能。
# 🚀 快速使用指南

## 1. 启动机器人

```bash
# 方式1: 直接启动
python enhanced_chat_bot.py

# 方式2: 使用启动脚本
python start.py
```

## 2. 测试DeepSeek API

```bash
python test_deepseek.py
```

## 3. 配置说明

### 基本配置 (config.yml)

```yaml
# NapCat API 配置
napcat:
  host: localhost
  port: 3000
  token: "你的token"

# DeepSeek AI 配置  
deepseek:
  enabled: true
  api_key: "sk-xxx"  # 填入你的API密钥
```

### 获取DeepSeek API密钥

1. 访问 https://platform.deepseek.com/
2. 注册/登录账号
3. 创建API密钥
4. 将密钥填入config.yml

## 4. 功能测试

### 私聊测试
- 直接发送消息给机器人
- 机器人会使用DeepSeek AI回复

### 群聊测试
- 在群里@机器人
- 机器人会使用DeepSeek AI回复

### 命令测试
```
/help - 查看帮助
/time - 当前时间
/60s - 60秒读懂世界
/clear_chat - 清除AI聊天记录
```

### 60秒新闻功能
- 发送 `/60s` 获取每日新闻
- 或发送包含"60s"、"60秒"、"今日新闻"的消息
- 优先返回新闻图片，如无图片则返回文字版

## 5. 常见问题

### API不工作
1. 检查API密钥是否正确
2. 运行测试脚本: `python test_deepseek.py`
3. 检查网络连接

### 机器人不回复
1. 检查NapCat是否运行
2. 检查token是否正确
3. 检查端口8080是否被占用

### @功能不工作
1. 确保在群聊中@机器人
2. 检查配置中`use_deepseek: true`
3. 查看控制台日志

## 6. 日志查看

启动后查看控制台输出:
- `🤖 使用DeepSeek处理消息` - AI处理中
- `✅ DeepSeek回复` - AI回复成功
- `❌ DeepSeek回复失败` - AI回复失败

## 7. 调试技巧

1. 启用详细日志:
   ```yaml
   server:
     debug: true
   ```

2. 测试API连接:
   ```bash
   python test_deepseek.py
   ```

3. 检查消息格式:
   - 查看控制台的消息日志
   - 确认@检测是否正确

祝你使用愉快！🎉
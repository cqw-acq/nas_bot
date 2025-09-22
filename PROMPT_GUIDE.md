# Prompt管理系统使用指南

## 🎯 功能概述

NAS Bot现在支持多种AI personality，你可以通过聊天命令轻松切换不同的AI角色！

## 📝 可用的Prompt类型

系统预置了6种不同的AI人格：

1. **default** - 默认助手：友好、专业的通用助手
2. **technical** - 技术专家：专注于技术问题解答
3. **funny** - 幽默大师：轻松幽默的聊天风格
4. **supportive** - 心理支持：温暖关怀的陪伴者
5. **professional** - 商务助手：正式严谨的商务风格
6. **creative** - 创意伙伴：富有想象力的创作助手

## 💬 聊天命令

### 查看可用Prompt
```
/prompts
```
显示所有可用的AI人格列表

### 切换Prompt
```
/prompt <名称>
```
切换到指定的AI人格，例如：
- `/prompt technical` - 切换到技术专家
- `/prompt funny` - 切换到幽默大师
- `/prompt supportive` - 切换到心理支持

### 创建自定义Prompt
```
/create_prompt <名称> <内容>
```
创建自己的AI人格，例如：
```
/create_prompt gaming 你是一个游戏专家，熟悉各种游戏攻略和技巧...
```

## 🎪 使用示例

1. **查看当前可用的人格**：
   ```
   用户: /prompts
   Bot: 📋 可用的prompts:
        • default (当前)
        • technical
        • funny
        • supportive
        • professional
        • creative
   ```

2. **切换到幽默模式**：
   ```
   用户: /prompt funny
   Bot: 🎭 已切换到 funny prompt！
   
   用户: @Bot 你好
   Bot: 哟！大侠好啊！今天有什么好玩的事情要跟我分享吗？🤪
   ```

3. **切换到技术专家模式**：
   ```
   用户: /prompt technical
   Bot: 🔧 已切换到 technical prompt！
   
   用户: @Bot Python如何处理异常？
   Bot: 在Python中处理异常主要使用try-except语句块...
   ```

## ⚙️ 配置说明

在 `config.yml` 中可以设置：

```yaml
prompts:
  default_prompt: "default"  # 启动时使用的默认人格
  prompts_dir: "prompts"     # prompt文件存储目录
```

## 📁 文件结构

```
nas_bot/
├── prompts/                 # prompt文件目录
│   ├── default.txt         # 默认助手
│   ├── technical.txt       # 技术专家
│   ├── funny.txt          # 幽默大师
│   ├── supportive.txt     # 心理支持
│   ├── professional.txt   # 商务助手
│   └── creative.txt       # 创意伙伴
├── config.yml             # 配置文件
└── enhanced_chat_bot.py   # 主程序
```

## 🔧 高级功能

### 自定义Prompt文件

你可以直接编辑 `prompts/` 目录下的文件来自定义AI人格：

1. 创建新文件：`prompts/your_style.txt`
2. 写入prompt内容
3. 使用 `/prompt your_style` 切换

### 动态加载

系统支持动态加载新的prompt文件，无需重启Bot！

## 🚀 开始使用

1. 确保Bot正在运行
2. 在群里@Bot并使用 `/prompts` 查看可用人格
3. 使用 `/prompt <名称>` 切换人格
4. 开始与不同人格的AI聊天！

## 🆘 常见问题

**Q: 如何恢复默认设置？**
A: 使用 `/prompt default` 即可

**Q: 可以创建多少个自定义prompt？**
A: 理论上没有限制，只要存储空间允许

**Q: prompt文件格式有要求吗？**
A: 普通文本文件即可，UTF-8编码

---

✨ 享受与不同AI人格的聊天体验吧！
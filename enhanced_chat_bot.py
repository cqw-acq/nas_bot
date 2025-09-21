#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强版聊天机器人服务器
支持智能对话、游戏、群组互动等功能
基于Flask和YAML配置
"""

import json
import yaml
import random
import re
import math
import os
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
import requests
from typing import Dict, List, Any, Optional


class BotConfig:
    """配置管理器"""
    
    def __init__(self, config_file='config.yml'):
        self.config_file = config_file
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """加载YAML配置文件"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            print(f"⚠️  配置文件 {self.config_file} 不存在，使用默认配置")
            return self.get_default_config()
        except Exception as e:
            print(f"❌ 配置文件加载失败: {e}")
            return self.get_default_config()
    
    def get_default_config(self) -> Dict[str, Any]:
        """默认配置"""
        return {
            'napcat': {
                'host': 'localhost',
                'port': 3000,
                'token': '5Z?Rm$@2JwDFS:Ut',
                'timeout': 10
            },
            'bot': {
                'name': 'NAS Bot',
                'auto_reply': True,
                'command_prefix': '/'
            },
            'server': {
                'host': '0.0.0.0',
                'port': 8080,
                'debug': False
            }
        }
    
    def get(self, path: str, default=None):
        """获取配置值，支持点号路径如 'napcat.host'"""
        keys = path.split('.')
        value = self.config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value


class DataManager:
    """数据管理器"""
    
    def __init__(self, config: BotConfig):
        self.config = config
        self.user_data = {}
        self.group_data = {}
        self.game_data = {}
        self.ensure_data_dirs()
        self.load_data()
    
    def ensure_data_dirs(self):
        """确保数据目录存在"""
        for dir_path in ['data', 'logs']:
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
    
    def load_data(self):
        """加载所有数据文件"""
        self.user_data = self.load_json_file('data/user_data.json', {})
        self.group_data = self.load_json_file('data/group_data.json', {})
        self.game_data = self.load_json_file('data/game_data.json', {})
    
    def load_json_file(self, filepath: str, default: Any) -> Any:
        """加载JSON文件"""
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"⚠️  加载数据文件 {filepath} 失败: {e}")
        return default
    
    def save_data(self):
        """保存所有数据文件"""
        self.save_json_file('data/user_data.json', self.user_data)
        self.save_json_file('data/group_data.json', self.group_data)
        self.save_json_file('data/game_data.json', self.game_data)
    
    def save_json_file(self, filepath: str, data: Any):
        """保存JSON文件"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"❌ 保存数据文件 {filepath} 失败: {e}")
    
    def get_user_data(self, user_id: str) -> Dict[str, Any]:
        """获取用户数据"""
        if user_id not in self.user_data:
            self.user_data[user_id] = {
                'points': 0,
                'last_checkin': None,
                'checkin_streak': 0,
                'message_count': 0,
                'join_date': datetime.now().isoformat()
            }
        return self.user_data[user_id]
    
    def get_group_data(self, group_id: str) -> Dict[str, Any]:
        """获取群组数据"""
        if group_id not in self.group_data:
            self.group_data[group_id] = {
                'total_messages': 0,
                'active_users': {},
                'settings': {}
            }
        return self.group_data[group_id]


class CommandHandler:
    """命令处理器"""
    
    def __init__(self, config: BotConfig, data_manager: DataManager):
        self.config = config
        self.data = data_manager
        self.jokes = [
            "为什么程序员总是混淆圣诞节和万圣节？因为 Oct 31 == Dec 25！",
            "程序员最讨厌的事情：1. 写注释 2. 别人不写注释",
            "为什么程序员喜欢黑暗？因为光明会产生 bug！",
            "如何产生一个随机字符串？让新手写代码...",
            "程序员的三大美德：懒惰、急躁、傲慢",
            "为什么程序员总是戴耳机？因为他们不想听到编译错误的声音！"
        ]
    
    def handle_help(self, args: List[str]) -> str:
        """帮助命令"""
        return """🤖 NAS Bot 命令帮助

📋 基础命令:
/help - 显示此帮助
/time - 显示当前时间
/ping - 测试响应
/echo [文本] - 回显文本

🔧 工具命令:
/calc [表达式] - 计算器
/dice [面数] - 掷骰子 (默认6面)
/coin - 抛硬币

🎮 游戏命令:
/guess - 猜数字游戏
/rps [石头/剪刀/布] - 石头剪刀布
/fortune - 抽签占卜

😄 娱乐命令:
/joke - 随机笑话
/roll [数量] - 随机数

👥 群组命令:
/checkin - 每日签到
/points - 查看积分
/rank - 积分排行榜

💡 输入任何文字开始智能对话！"""
    
    def handle_time(self, args: List[str]) -> str:
        """时间命令"""
        now = datetime.now()
        return f"🕐 当前时间: {now.strftime('%Y-%m-%d %H:%M:%S')}\n📅 星期{['一','二','三','四','五','六','日'][now.weekday()]}"
    
    def handle_ping(self, args: List[str]) -> str:
        """Ping命令"""
        return "🏓 Pong! 机器人运行正常！"
    
    def handle_echo(self, args: List[str]) -> str:
        """回显命令"""
        if not args:
            return "📢 请提供要回显的文本，例如: /echo 你好世界"
        return f"📢 {' '.join(args)}"
    
    def handle_calc(self, args: List[str]) -> str:
        """计算器命令"""
        if not args:
            return "🔢 请提供计算表达式，例如: /calc 1+2*3"
        
        expression = ' '.join(args)
        try:
            # 只允许安全的数学运算
            allowed_chars = set('0123456789+-*/().,^% ')
            if not all(c in allowed_chars for c in expression):
                return "❌ 表达式包含不允许的字符"
            
            # 替换一些常见符号
            expression = expression.replace('^', '**')
            expression = expression.replace('%', '/100')
            
            # 添加数学函数支持
            safe_dict = {
                '__builtins__': {},
                'abs': abs, 'round': round, 'min': min, 'max': max,
                'sqrt': math.sqrt, 'sin': math.sin, 'cos': math.cos,
                'tan': math.tan, 'pi': math.pi, 'e': math.e
            }
            
            result = eval(expression, safe_dict)
            return f"🔢 {expression} = {result}"
            
        except Exception as e:
            return f"❌ 计算错误: 请检查表达式是否正确"
    
    def handle_dice(self, args: List[str]) -> str:
        """掷骰子命令"""
        sides = 6
        if args:
            try:
                sides = int(args[0])
                if sides < 2 or sides > 100:
                    return "🎲 骰子面数必须在2-100之间"
            except ValueError:
                return "🎲 请提供有效的数字，例如: /dice 20"
        
        result = random.randint(1, sides)
        return f"🎲 掷出了 {sides} 面骰子: {result}"
    
    def handle_coin(self, args: List[str]) -> str:
        """抛硬币命令"""
        result = random.choice(['正面', '反面'])
        emoji = '🪙' if result == '正面' else '🔘'
        return f"{emoji} 硬币落地: {result}!"
    
    def handle_joke(self, args: List[str]) -> str:
        """笑话命令"""
        joke = random.choice(self.jokes)
        return f"😄 {joke}"
    
    def handle_roll(self, args: List[str]) -> str:
        """随机数命令"""
        count = 1
        if args:
            try:
                count = int(args[0])
                if count < 1 or count > 10:
                    return "🎰 数量必须在1-10之间"
            except ValueError:
                return "🎰 请提供有效的数字"
        
        results = [random.randint(1, 100) for _ in range(count)]
        return f"🎰 随机数 (1-100): {', '.join(map(str, results))}"
    
    def handle_checkin(self, args: List[str], user_id: str) -> str:
        """签到命令"""
        user_data = self.data.get_user_data(user_id)
        today = datetime.now().date().isoformat()
        
        if user_data['last_checkin'] == today:
            return "✅ 今天已经签到过了！明天再来吧~"
        
        # 计算连续签到
        yesterday = (datetime.now().date() - timedelta(days=1)).isoformat()
        if user_data['last_checkin'] == yesterday:
            user_data['checkin_streak'] += 1
        else:
            user_data['checkin_streak'] = 1
        
        # 计算积分奖励
        base_points = self.config.get('group.checkin.daily_points', 10)
        bonus_points = user_data['checkin_streak'] * self.config.get('group.checkin.continuous_bonus', 5)
        total_points = base_points + bonus_points
        
        user_data['last_checkin'] = today
        user_data['points'] += total_points
        
        self.data.save_data()
        
        return f"✅ 签到成功！\n📅 连续签到: {user_data['checkin_streak']} 天\n💰 获得积分: {total_points}\n🏆 总积分: {user_data['points']}"
    
    def handle_points(self, args: List[str], user_id: str) -> str:
        """积分查询命令"""
        user_data = self.data.get_user_data(user_id)
        return f"💰 你的积分: {user_data['points']}\n📅 连续签到: {user_data['checkin_streak']} 天\n💬 消息数: {user_data['message_count']}"
    
    def handle_fortune(self, args: List[str]) -> str:
        """抽签命令"""
        fortunes = self.config.get('games.fortune_telling.fortunes', [
            "大吉：今天是幸运的一天！",
            "中吉：会有小小的惊喜等着你",
            "小吉：保持乐观，好事将至"
        ])
        
        fortune = random.choice(fortunes)
        return f"🔮 今日运势: {fortune}"


class GameManager:
    """游戏管理器"""
    
    def __init__(self, config: BotConfig, data_manager: DataManager):
        self.config = config
        self.data = data_manager
        self.active_games = {}
    
    def start_guess_game(self, user_id: str) -> str:
        """开始猜数字游戏"""
        if user_id in self.active_games:
            return "🎮 你已经在游戏中了！发送数字来猜测，或发送 /quit 退出"
        
        max_num = self.config.get('games.guess_number.range_max', 100)
        secret_number = random.randint(1, max_num)
        max_attempts = self.config.get('games.guess_number.max_attempts', 6)
        
        self.active_games[user_id] = {
            'type': 'guess_number',
            'secret': secret_number,
            'attempts': 0,
            'max_attempts': max_attempts
        }
        
        return f"🎯 猜数字游戏开始！\n我想了一个1-{max_num}的数字\n你有{max_attempts}次机会来猜测\n直接发送数字即可！"
    
    def handle_guess_input(self, user_id: str, message: str) -> Optional[str]:
        """处理猜数字输入"""
        if user_id not in self.active_games:
            return None
        
        game = self.active_games[user_id]
        if game['type'] != 'guess_number':
            return None
        
        if message.strip() == '/quit':
            del self.active_games[user_id]
            return "🎮 游戏已退出！答案是 " + str(game['secret'])
        
        try:
            guess = int(message.strip())
        except ValueError:
            return "🔢 请输入一个有效的数字，或发送 /quit 退出游戏"
        
        game['attempts'] += 1
        secret = game['secret']
        
        if guess == secret:
            del self.active_games[user_id]
            # 奖励积分
            user_data = self.data.get_user_data(user_id)
            bonus = max(10, 50 - game['attempts'] * 5)
            user_data['points'] += bonus
            self.data.save_data()
            return f"🎉 恭喜！你猜对了！\n答案确实是 {secret}\n用了 {game['attempts']} 次尝试\n💰 获得 {bonus} 积分！"
        
        if game['attempts'] >= game['max_attempts']:
            del self.active_games[user_id]
            return f"💔 游戏结束！\n答案是 {secret}\n下次加油哦！"
        
        hint = "太大了" if guess > secret else "太小了"
        remaining = game['max_attempts'] - game['attempts']
        return f"❌ {guess} {hint}！\n还有 {remaining} 次机会"
    
    def play_rps(self, user_choice: str) -> str:
        """石头剪刀布游戏"""
        choices = {'石头': 0, '剪刀': 1, '布': 2}
        choice_names = ['石头', '剪刀', '布']
        choice_emojis = ['🪨', '✂️', '📄']
        
        # 标准化用户输入
        user_choice = user_choice.strip()
        if user_choice not in choices:
            return "🎮 请选择: 石头、剪刀、布"
        
        user_num = choices[user_choice]
        bot_num = random.randint(0, 2)
        bot_choice = choice_names[bot_num]
        
        result_text = f"你: {choice_emojis[user_num]} {user_choice}\n我: {choice_emojis[bot_num]} {bot_choice}\n\n"
        
        if user_num == bot_num:
            return result_text + "🤝 平局！"
        elif (user_num + 1) % 3 == bot_num:
            return result_text + "🎉 你赢了！"
        else:
            return result_text + "😅 我赢了！"


class SmartReply:
    """智能回复系统"""
    
    def __init__(self, config: BotConfig):
        self.config = config
        self.positive_words = config.get('chat.emotion.positive_words', [])
        self.negative_words = config.get('chat.emotion.negative_words', [])
    
    def get_emotion_response(self, message: str) -> Optional[str]:
        """情感响应"""
        message_lower = message.lower()
        
        positive_count = sum(1 for word in self.positive_words if word in message_lower)
        negative_count = sum(1 for word in self.negative_words if word in message_lower)
        
        if positive_count > negative_count and positive_count > 0:
            return random.choice([
                "😊 看起来你心情不错呢！",
                "🎉 真为你高兴！",
                "😄 正能量满满！",
                "👍 继续保持好心情！"
            ])
        elif negative_count > positive_count and negative_count > 0:
            return random.choice([
                "😔 不要难过，会好起来的",
                "🤗 我陪着你呢",
                "💪 加油，相信你能克服困难！",
                "🌈 风雨之后见彩虹"
            ])
        
        return None
    
    def get_keyword_response(self, message: str) -> Optional[str]:
        """关键词响应"""
        message_lower = message.lower()
        
        greetings = self.config.get('chat.keywords.greetings', [])
        goodbye = self.config.get('chat.keywords.goodbye', [])
        thanks = self.config.get('chat.keywords.thanks', [])
        
        if any(word in message_lower for word in greetings):
            return random.choice([
                "你好！很高兴见到你 😊",
                "嗨！今天过得怎么样？",
                "你好呀！有什么可以帮助你的吗？",
                "Hi~ 欢迎来聊天！"
            ])
        
        if any(word in message_lower for word in goodbye):
            return random.choice([
                "再见！期待下次相遇 👋",
                "拜拜！要开心哦~",
                "下次聊！保重身体",
                "Bye~ 有空再来玩！"
            ])
        
        if any(word in message_lower for word in thanks):
            return random.choice([
                "不客气！很高兴能帮到你 😊",
                "没关系的，这是我应该做的",
                "不用谢！随时为你服务",
                "客气什么，我们是朋友嘛~"
            ])
        
        return None


class ChatBot:
    """主聊天机器人类"""
    
    def __init__(self):
        self.config = BotConfig()
        self.data_manager = DataManager(self.config)
        self.command_handler = CommandHandler(self.config, self.data_manager)
        self.game_manager = GameManager(self.config, self.data_manager)
        self.smart_reply = SmartReply(self.config)
        
        # Flask应用
        self.app = Flask(__name__)
        self.setup_routes()
    
    def setup_routes(self):
        """设置Flask路由"""
        
        @self.app.route('/', methods=['POST'])
        def handle_message():
            try:
                data = request.get_json()
                if not data:
                    return jsonify({'error': 'No JSON data'}), 400
                
                if data.get('post_type') == 'message':
                    self.process_message(data)
                
                return jsonify({'status': 'ok'})
                
            except Exception as e:
                print(f"❌ 处理消息错误: {e}")
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/status', methods=['GET'])
        def get_status():
            return jsonify({
                'status': 'running',
                'timestamp': datetime.now().isoformat(),
                'bot_name': self.config.get('bot.name'),
                'active_games': len(self.game_manager.active_games)
            })
        
        @self.app.route('/config', methods=['GET'])
        def get_config():
            return jsonify(self.config.config)
    
    def process_message(self, data: Dict[str, Any]):
        """处理收到的消息"""
        user_id = str(data.get('user_id', ''))
        message = data.get('raw_message', '')
        message_type = data.get('message_type')
        group_id = str(data.get('group_id', '')) if message_type == 'group' else None
        
        sender = data.get('sender', {})
        nickname = sender.get('nickname', '未知')
        
        # 打印消息日志
        timestamp = datetime.now().strftime('%H:%M:%S')
        if message_type == 'private':
            print(f"💬 {timestamp} | 私聊 | {nickname}({user_id}): {message}")
        else:
            print(f"👥 {timestamp} | 群聊({group_id}) | {nickname}({user_id}): {message}")
        
        # 更新用户数据
        user_data = self.data_manager.get_user_data(user_id)
        user_data['message_count'] += 1
        
        # 处理游戏输入
        game_response = self.game_manager.handle_guess_input(user_id, message)
        if game_response:
            self.send_reply(game_response, user_id, group_id, message_type)
            return
        
        # 处理命令
        if message.startswith(self.config.get('bot.command_prefix', '/')):
            response = self.handle_command(message, user_id, group_id, message_type)
            if response:
                self.send_reply(response, user_id, group_id, message_type)
                return
        
        # 智能回复
        if self.config.get('bot.auto_reply', True):
            response = self.get_smart_response(message, user_id)
            if response:
                self.send_reply(response, user_id, group_id, message_type)
        
        # 保存数据
        self.data_manager.save_data()
    
    def handle_command(self, message: str, user_id: str, group_id: Optional[str], message_type: str) -> Optional[str]:
        """处理命令"""
        parts = message[1:].split()
        if not parts:
            return None
        
        command = parts[0].lower()
        args = parts[1:]
        
        # 基础命令
        if command == 'help':
            return self.command_handler.handle_help(args)
        elif command == 'time':
            return self.command_handler.handle_time(args)
        elif command == 'ping':
            return self.command_handler.handle_ping(args)
        elif command == 'echo':
            return self.command_handler.handle_echo(args)
        
        # 工具命令
        elif command == 'calc':
            return self.command_handler.handle_calc(args)
        elif command == 'dice':
            return self.command_handler.handle_dice(args)
        elif command == 'coin':
            return self.command_handler.handle_coin(args)
        elif command == 'joke':
            return self.command_handler.handle_joke(args)
        elif command == 'roll':
            return self.command_handler.handle_roll(args)
        elif command == 'fortune':
            return self.command_handler.handle_fortune(args)
        
        # 游戏命令
        elif command == 'guess':
            return self.game_manager.start_guess_game(user_id)
        elif command == 'rps':
            if args:
                return self.game_manager.play_rps(' '.join(args))
            return "🎮 石头剪刀布！请选择: /rps 石头 或 /rps 剪刀 或 /rps 布"
        
        # 群组命令
        elif command == 'checkin':
            return self.command_handler.handle_checkin(args, user_id)
        elif command == 'points':
            return self.command_handler.handle_points(args, user_id)
        
        return f"❓ 未知命令: {command}\n发送 /help 查看所有可用命令"
    
    def get_smart_response(self, message: str, user_id: str) -> Optional[str]:
        """获取智能回复"""
        
        # 情感响应
        emotion_response = self.smart_reply.get_emotion_response(message)
        if emotion_response:
            return emotion_response
        
        # 关键词响应
        keyword_response = self.smart_reply.get_keyword_response(message)
        if keyword_response:
            return keyword_response
        
        # 特殊消息响应
        message_lower = message.lower()
        
        if '你是谁' in message or 'who are you' in message_lower:
            return f"我是 {self.config.get('bot.name', 'NAS Bot')}，你的智能助手！🤖\n发送 /help 查看我能做什么~"
        
        if '你好吗' in message or 'how are you' in message_lower:
            return "我很好，谢谢关心！😊 你今天过得怎么样？"
        
        if '时间' in message and '几点' in message:
            return self.command_handler.handle_time([])
        
        if any(word in message for word in ['计算', '算', '等于']):
            return "我可以帮你计算哦！使用 /calc 命令，例如: /calc 1+2*3"
        
        if any(word in message for word in ['游戏', '玩', '娱乐']):
            return "🎮 我有很多游戏可以玩：\n/guess - 猜数字\n/rps 石头 - 石头剪刀布\n/dice - 掷骰子\n/fortune - 抽签"
        
        return None
    
    def send_reply(self, message: str, user_id: str, group_id: Optional[str], message_type: str):
        """发送回复"""
        try:
            napcat_host = self.config.get('napcat.host', 'localhost')
            napcat_port = self.config.get('napcat.port', 3000)
            napcat_token = self.config.get('napcat.token')
            
            if message_type == 'private':
                url = f"http://{napcat_host}:{napcat_port}/send_private_msg"
                data = {'user_id': int(user_id), 'message': message}
            else:
                url = f"http://{napcat_host}:{napcat_port}/send_group_msg"
                data = {'group_id': int(group_id), 'message': message}
            
            headers = {'Content-Type': 'application/json'}
            if napcat_token:
                headers['Authorization'] = f"Bearer {napcat_token}"
            
            timeout = self.config.get('napcat.timeout', 10)
            response = requests.post(url, json=data, headers=headers, timeout=timeout)
            
            if response.status_code == 200:
                print(f"✅ 回复发送成功: {message[:50]}{'...' if len(message) > 50 else ''}")
            else:
                print(f"❌ 回复发送失败: {response.status_code}")
                
        except Exception as e:
            print(f"❌ 发送回复异常: {e}")
    
    def run(self):
        """启动服务器"""
        print("🚀 增强版聊天机器人启动")
        print("=" * 50)
        print(f"🤖 机器人名称: {self.config.get('bot.name')}")
        print(f"🔧 配置文件: {self.config.config_file}")
        print(f"📡 监听端口: {self.config.get('server.port')}")
        print(f"🔗 NapCat: {self.config.get('napcat.host')}:{self.config.get('napcat.port')}")
        print("=" * 50)
        print("🎮 支持功能:")
        print("   • 智能对话和情感响应")
        print("   • 丰富的命令系统")
        print("   • 游戏娱乐功能")
        print("   • 群组互动系统")
        print("   • 积分和签到系统")
        print("=" * 50)
        print("✅ 服务器运行中...")
        
        self.app.run(
            host=self.config.get('server.host', '0.0.0.0'),
            port=self.config.get('server.port', 8080),
            debug=self.config.get('server.debug', False),
            threaded=True
        )


def main():
    """主函数"""
    bot = ChatBot()
    try:
        bot.run()
    except KeyboardInterrupt:
        print("\n👋 机器人已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OneBot 11服务端使用示例
演示如何扩展和自定义消息处理逻辑
"""

import json
import time
import random
from datetime import datetime
from onebot_server import OneBotServer, OneBotMessageProcessor
from onebot_api import OneBotAPI, MessageBuilder


class CustomMessageProcessor(OneBotMessageProcessor):
    """自定义消息处理器"""
    
    def __init__(self, config):
        super().__init__(config)
        # 初始化API客户端
        self.api = OneBotAPI(
            host=config.napcat_host,
            port=config.napcat_port,
            token=config.napcat_token
        )
        
        # 管理员列表
        self.admin_users = [123456789]  # 替换为实际的管理员QQ号
        
        # 群聊白名单
        self.allowed_groups = []  # 如果为空则允许所有群
        
        # 功能开关
        self.features = {
            'weather': True,
            'translate': True,
            'admin_commands': True,
            'group_management': True
        }
    
    def handle_custom_message(self, data):
        """扩展的自定义消息处理"""
        message = data.get('raw_message', '').strip()
        user_id = data.get('user_id', '')
        group_id = data.get('group_id', '')
        message_type = data.get('message_type', '')
        
        # 群聊白名单检查
        if message_type == 'group' and self.allowed_groups:
            if int(group_id) not in self.allowed_groups:
                return
        
        # 处理命令
        if message.startswith('/'):
            self.handle_command(data, message)
        elif message.startswith('!'):
            self.handle_admin_command(data, message)
        else:
            self.handle_normal_message(data, message)
    
    def handle_command(self, data, message):
        """处理普通命令"""
        command = message[1:].split()[0].lower()
        args = message[1:].split()[1:] if len(message.split()) > 1 else []
        
        if command == 'help':
            self.send_help(data)
        elif command == 'time':
            self.send_time(data)
        elif command == 'ping':
            self.send_reply(data, "pong! 机器人运行正常")
        elif command == 'status':
            self.send_status(data)
        elif command == 'weather' and self.features['weather']:
            self.send_weather(data, args)
        elif command == 'translate' and self.features['translate']:
            self.send_translate(data, args)
        elif command == 'random':
            self.send_random_number(data, args)
        elif command == 'quote':
            self.send_random_quote(data)
        else:
            self.send_reply(data, f"未知命令: {command}\n输入 /help 查看可用命令")
    
    def handle_admin_command(self, data, message):
        """处理管理员命令"""
        user_id = int(data.get('user_id', '0'))
        
        if user_id not in self.admin_users:
            self.send_reply(data, "❌ 权限不足，仅管理员可使用此命令")
            return
        
        if not self.features['admin_commands']:
            self.send_reply(data, "❌ 管理员命令功能已禁用")
            return
        
        command = message[1:].split()[0].lower()
        args = message[1:].split()[1:] if len(message.split()) > 1 else []
        
        if command == 'kick' and data.get('message_type') == 'group':
            self.admin_kick_user(data, args)
        elif command == 'ban' and data.get('message_type') == 'group':
            self.admin_ban_user(data, args)
        elif command == 'unban' and data.get('message_type') == 'group':
            self.admin_unban_user(data, args)
        elif command == 'mute' and data.get('message_type') == 'group':
            self.admin_mute_all(data, args)
        elif command == 'info':
            self.admin_get_info(data, args)
        elif command == 'say':
            self.admin_say(data, args)
        else:
            self.send_reply(data, f"未知管理员命令: {command}")
    
    def handle_normal_message(self, data, message):
        """处理普通消息"""
        # 这里可以添加自然语言处理、关键词回复等功能
        
        # 示例：简单的关键词回复
        keywords_responses = {
            '早上好': '早上好！今天也要加油哦~',
            '晚安': '晚安，好梦~',
            '谢谢': '不客气～',
            '怎么样': '我很好，谢谢关心！',
        }
        
        for keyword, response in keywords_responses.items():
            if keyword in message:
                self.send_reply(data, response)
                break
    
    def send_help(self, data):
        """发送帮助信息"""
        help_text = """🤖 机器人帮助菜单

📝 基础命令:
/help - 显示此帮助
/time - 显示当前时间
/ping - 测试连接
/status - 显示机器人状态

🔧 实用功能:
/weather [城市] - 查询天气 (暂未实现)
/translate [文本] - 翻译文本 (暂未实现)
/random [min] [max] - 生成随机数
/quote - 随机名言

👨‍💼 管理员命令 (需要权限):
!kick @用户 - 踢出用户
!ban @用户 [时间] - 禁言用户
!unban @用户 - 解除禁言
!mute [on/off] - 全体禁言
!info @用户 - 获取用户信息
!say [内容] - 让机器人说话"""
        
        self.send_reply(data, help_text)
    
    def send_time(self, data):
        """发送当前时间"""
        now = datetime.now()
        time_text = f"🕐 当前时间: {now.strftime('%Y年%m月%d日 %H:%M:%S')}"
        self.send_reply(data, time_text)
    
    def send_status(self, data):
        """发送机器人状态"""
        try:
            status_info = self.api.get_status()
            if status_info.get('status') == 'ok':
                status_data = status_info.get('data', {})
                online = status_data.get('online', False)
                good = status_data.get('good', False)
                
                status_text = f"""🤖 机器人状态:
在线状态: {'✅ 在线' if online else '❌ 离线'}
运行状态: {'✅ 正常' if good else '⚠️ 异常'}
当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""
            else:
                status_text = "❌ 无法获取机器人状态"
        except Exception as e:
            status_text = f"❌ 获取状态失败: {str(e)}"
        
        self.send_reply(data, status_text)
    
    def send_weather(self, data, args):
        """发送天气信息（示例）"""
        if not args:
            self.send_reply(data, "请指定城市名称，例如: /weather 北京")
            return
        
        city = ' '.join(args)
        # 这里应该调用天气API，暂时返回示例数据
        weather_text = f"🌤️ {city}天气:\n温度: 25°C\n天气: 晴转多云\n风力: 3-4级\n\n(这是示例数据，请接入实际天气API)"
        self.send_reply(data, weather_text)
    
    def send_translate(self, data, args):
        """发送翻译结果（示例）"""
        if not args:
            self.send_reply(data, "请输入要翻译的文本，例如: /translate Hello World")
            return
        
        text = ' '.join(args)
        # 这里应该调用翻译API，暂时返回示例数据
        translate_text = f"🌐 翻译结果:\n原文: {text}\n译文: (请接入翻译API)\n\n支持多种语言互译"
        self.send_reply(data, translate_text)
    
    def send_random_number(self, data, args):
        """发送随机数"""
        try:
            if len(args) >= 2:
                min_num = int(args[0])
                max_num = int(args[1])
            elif len(args) == 1:
                min_num = 1
                max_num = int(args[0])
            else:
                min_num = 1
                max_num = 100
            
            if min_num > max_num:
                min_num, max_num = max_num, min_num
            
            random_num = random.randint(min_num, max_num)
            self.send_reply(data, f"🎲 随机数 ({min_num}-{max_num}): {random_num}")
            
        except ValueError:
            self.send_reply(data, "❌ 请输入有效的数字")
    
    def send_random_quote(self, data):
        """发送随机名言"""
        quotes = [
            "生活就像一盒巧克力，你永远不知道下一颗是什么味道。",
            "今天的努力，是为了明天的收获。",
            "成功不是终点，失败也不是末日，继续前进的勇气才最重要。",
            "每一个不曾起舞的日子，都是对生命的辜负。",
            "路虽远行则将至，事虽难做则必成。",
            "不要等待机会，而要创造机会。",
            "相信自己，你比想象中更强大。"
        ]
        
        quote = random.choice(quotes)
        self.send_reply(data, f"💭 随机名言:\n{quote}")
    
    def admin_kick_user(self, data, args):
        """管理员踢人"""
        group_id = data.get('group_id', '')
        if not group_id:
            return
        
        # 解析@的用户ID
        message = data.get('message', [])
        target_user = None
        
        for msg_item in message:
            if msg_item.get('type') == 'at':
                target_user = msg_item.get('data', {}).get('qq')
                break
        
        if not target_user:
            self.send_reply(data, "❌ 请@要踢出的用户")
            return
        
        try:
            result = self.api.set_group_kick(group_id, target_user)
            if result.get('status') == 'ok':
                self.send_reply(data, f"✅ 已踢出用户 {target_user}")
            else:
                self.send_reply(data, f"❌ 踢出失败: {result.get('msg', '未知错误')}")
        except Exception as e:
            self.send_reply(data, f"❌ 操作失败: {str(e)}")
    
    def admin_ban_user(self, data, args):
        """管理员禁言"""
        group_id = data.get('group_id', '')
        if not group_id:
            return
        
        # 解析@的用户ID和禁言时间
        message = data.get('message', [])
        target_user = None
        
        for msg_item in message:
            if msg_item.get('type') == 'at':
                target_user = msg_item.get('data', {}).get('qq')
                break
        
        if not target_user:
            self.send_reply(data, "❌ 请@要禁言的用户")
            return
        
        # 解析禁言时间（分钟）
        duration = 30 * 60  # 默认30分钟
        if args and len(args) > 0:
            try:
                duration = int(args[-1]) * 60  # 转换为秒
            except ValueError:
                pass
        
        try:
            result = self.api.set_group_ban(group_id, target_user, duration)
            if result.get('status') == 'ok':
                self.send_reply(data, f"✅ 已禁言用户 {target_user} {duration//60}分钟")
            else:
                self.send_reply(data, f"❌ 禁言失败: {result.get('msg', '未知错误')}")
        except Exception as e:
            self.send_reply(data, f"❌ 操作失败: {str(e)}")
    
    def admin_unban_user(self, data, args):
        """管理员解除禁言"""
        group_id = data.get('group_id', '')
        if not group_id:
            return
        
        # 解析@的用户ID
        message = data.get('message', [])
        target_user = None
        
        for msg_item in message:
            if msg_item.get('type') == 'at':
                target_user = msg_item.get('data', {}).get('qq')
                break
        
        if not target_user:
            self.send_reply(data, "❌ 请@要解除禁言的用户")
            return
        
        try:
            result = self.api.set_group_ban(group_id, target_user, 0)
            if result.get('status') == 'ok':
                self.send_reply(data, f"✅ 已解除用户 {target_user} 的禁言")
            else:
                self.send_reply(data, f"❌ 解除禁言失败: {result.get('msg', '未知错误')}")
        except Exception as e:
            self.send_reply(data, f"❌ 操作失败: {str(e)}")
    
    def admin_mute_all(self, data, args):
        """管理员全体禁言"""
        group_id = data.get('group_id', '')
        if not group_id:
            return
        
        enable = True
        if args and args[0].lower() in ['off', 'false', '0', '关']:
            enable = False
        
        try:
            result = self.api.set_group_whole_ban(group_id, enable)
            if result.get('status') == 'ok':
                status = "开启" if enable else "关闭"
                self.send_reply(data, f"✅ 已{status}全体禁言")
            else:
                self.send_reply(data, f"❌ 操作失败: {result.get('msg', '未知错误')}")
        except Exception as e:
            self.send_reply(data, f"❌ 操作失败: {str(e)}")
    
    def admin_get_info(self, data, args):
        """管理员获取用户信息"""
        # 解析@的用户ID
        message = data.get('message', [])
        target_user = None
        
        for msg_item in message:
            if msg_item.get('type') == 'at':
                target_user = msg_item.get('data', {}).get('qq')
                break
        
        if not target_user:
            self.send_reply(data, "❌ 请@要查询的用户")
            return
        
        try:
            # 获取用户信息
            result = self.api.get_stranger_info(target_user)
            if result.get('status') == 'ok':
                user_info = result.get('data', {})
                info_text = f"""👤 用户信息:
QQ号: {user_info.get('user_id', target_user)}
昵称: {user_info.get('nickname', '未知')}
性别: {user_info.get('sex', '未知')}
年龄: {user_info.get('age', '未知')}
等级: {user_info.get('level', '未知')}"""
                self.send_reply(data, info_text)
            else:
                self.send_reply(data, f"❌ 获取用户信息失败: {result.get('msg', '未知错误')}")
        except Exception as e:
            self.send_reply(data, f"❌ 操作失败: {str(e)}")
    
    def admin_say(self, data, args):
        """管理员让机器人说话"""
        if not args:
            self.send_reply(data, "❌ 请输入要说的内容")
            return
        
        content = ' '.join(args)
        self.send_reply(data, content)


class CustomOneBotServer(OneBotServer):
    """自定义OneBot服务器"""
    
    def __init__(self, config_file: str = "onebot_config.json"):
        super().__init__(config_file)
        # 使用自定义消息处理器
        self.processor = CustomMessageProcessor(self.config)


def main():
    """主函数"""
    print("🚀 启动自定义OneBot 11服务器")
    print("📝 配置文件: onebot_config.json")
    print("📚 示例功能已加载:")
    print("   - 基础命令 (/help, /time, /ping)")
    print("   - 实用功能 (/weather, /translate, /random, /quote)")
    print("   - 管理员命令 (!kick, !ban, !unban, !mute)")
    print("   - 自动回复关键词")
    print()
    
    server = CustomOneBotServer()
    server.start()


if __name__ == "__main__":
    main()
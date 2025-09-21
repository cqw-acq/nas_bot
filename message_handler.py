#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化OneBot服务器的使用示例
展示如何处理用户消息和发送者信息
"""

import json
import logging
from datetime import datetime
import http.server
import socketserver
import requests


# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MessageHandler(http.server.BaseHTTPRequestHandler):
    """消息处理器 - 专注于消息内容和发送者"""
    
    # 在这里配置你的NapCat信息
    NAPCAT_HOST = "localhost"
    NAPCAT_PORT = 3000
    NAPCAT_TOKEN = "1145"  # 你的token
    
    def do_POST(self):
        """处理NapCat推送的消息"""
        try:
            # 读取数据
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            # 解析JSON
            try:
                data = json.loads(post_data.decode('utf-8', errors='ignore'))
            except:
                self.send_response(400)
                self.end_headers()
                return
            
            # 只处理消息
            if data.get('post_type') == 'message':
                self.handle_message(data)
            
            # 回复OK
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status": "ok"}')
            
        except Exception as e:
            logger.error(f"处理消息错误: {e}")
            self.send_response(500)
            self.end_headers()
    
    def handle_message(self, data):
        """处理消息 - 只关心内容和发送者"""
        
        # 提取关键信息
        user_id = data.get('user_id')           # 发送者QQ号
        message = data.get('raw_message', '')   # 消息内容
        message_type = data.get('message_type') # private/group
        
        # 发送者信息
        sender = data.get('sender', {})
        nickname = sender.get('nickname', '未知')
        
        # 群信息（如果是群消息）
        group_id = data.get('group_id') if message_type == 'group' else None
        
        # 打印消息信息
        if message_type == 'private':
            print(f"💬 私聊 | {nickname}({user_id}): {message}")
        else:
            print(f"👥 群聊({group_id}) | {nickname}({user_id}): {message}")
        
        # 处理命令
        if message.startswith('/'):
            self.process_command(user_id, nickname, message, message_type, group_id)
        
        # 处理关键词
        elif any(keyword in message for keyword in ['你好', 'hello', '帮助']):
            self.process_keyword(user_id, nickname, message, message_type, group_id)
    
    def process_command(self, user_id, nickname, message, message_type, group_id):
        """处理命令"""
        command = message[1:].split()[0].lower()
        
        print(f"🔧 检测到命令: {command} (来自 {nickname})")
        
        if command == 'time':
            reply = f"现在时间: {datetime.now().strftime('%H:%M:%S')}"
            self.send_reply(reply, user_id, group_id, message_type)
            
        elif command == 'hello':
            reply = f"你好 {nickname}! 👋"
            self.send_reply(reply, user_id, group_id, message_type)
            
        elif command == 'help':
            reply = "可用命令:\n/time - 显示时间\n/hello - 打招呼\n/help - 显示帮助"
            self.send_reply(reply, user_id, group_id, message_type)
    
    def process_keyword(self, user_id, nickname, message, message_type, group_id):
        """处理关键词"""
        print(f"🔍 检测到关键词 (来自 {nickname})")
        
        if '你好' in message or 'hello' in message.lower():
            reply = f"你好 {nickname}!"
            self.send_reply(reply, user_id, group_id, message_type)
            
        elif '帮助' in message:
            reply = "输入 /help 查看可用命令"
            self.send_reply(reply, user_id, group_id, message_type)
    
    def send_reply(self, message, user_id, group_id, message_type):
        """发送回复"""
        try:
            if message_type == 'private':
                url = f"http://{self.NAPCAT_HOST}:{self.NAPCAT_PORT}/send_private_msg"
                data = {'user_id': user_id, 'message': message}
            else:
                url = f"http://{self.NAPCAT_HOST}:{self.NAPCAT_PORT}/send_group_msg"
                data = {'group_id': group_id, 'message': message}
            
            headers = {'Content-Type': 'application/json'}
            if self.NAPCAT_TOKEN:
                headers['Authorization'] = f"Bearer {self.NAPCAT_TOKEN}"
            
            response = requests.post(url, json=data, headers=headers, timeout=5)
            
            if response.status_code == 200:
                print(f"✅ 回复发送成功: {message}")
            else:
                print(f"❌ 回复发送失败: {response.status_code}")
                
        except Exception as e:
            print(f"❌ 发送回复异常: {e}")
    
    def log_message(self, format, *args):
        """简化日志"""
        pass


def main():
    """启动简化的消息处理服务器"""
    print("🚀 启动简化OneBot消息处理器")
    print("📝 只处理消息内容和发送者信息")
    print("🔧 支持基础命令和关键词回复")
    print("=" * 50)
    
    try:
        with socketserver.TCPServer(("0.0.0.0", 8080), MessageHandler) as httpd:
            print("✅ 服务器启动成功，监听端口 8080")
            print("📡 等待NapCat推送消息...")
            print("按 Ctrl+C 停止服务器")
            print("=" * 50)
            
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n👋 服务器已停止")
    except Exception as e:
        print(f"❌ 服务器启动失败: {e}")


if __name__ == "__main__":
    main()
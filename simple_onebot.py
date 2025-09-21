#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化版OneBot 11 HTTP服务端
只处理消息内容和发送者信息
"""

import json
import logging
from datetime import datetime
import http.server
import socketserver


# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('onebot_simple.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class SimpleOneBotHandler(http.server.BaseHTTPRequestHandler):
    """简化的OneBot HTTP请求处理器"""
    
    def do_POST(self):
        """处理POST请求"""
        try:
            # 验证路径
            if self.path != '/':
                self.send_response(404)
                self.end_headers()
                return
            
            # 读取请求体
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            # 解析JSON数据
            try:
                event_data = json.loads(post_data.decode('utf-8'))
            except json.JSONDecodeError as e:
                logger.error(f"JSON解析失败: {e}")
                self.send_response(400)
                self.end_headers()
                return
            
            # 只处理消息事件
            if event_data.get('post_type') == 'message':
                self.process_message(event_data)
            
            # 发送成功响应
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            response_data = json.dumps({'status': 'ok'}, ensure_ascii=False)
            self.wfile.write(response_data.encode('utf-8'))
            
        except Exception as e:
            logger.error(f"处理请求时发生错误: {e}")
            self.send_response(500)
            self.end_headers()
    
    def process_message(self, data):
        """处理消息事件，只提取关键信息"""
        try:
            # 提取基本信息
            message_type = data.get('message_type', '')  # private 或 group
            user_id = data.get('user_id', '')           # 发送者QQ号
            raw_message = data.get('raw_message', '')    # 消息内容
            
            # 群聊特有信息
            group_id = data.get('group_id', '') if message_type == 'group' else None
            
            # 发送者信息
            sender = data.get('sender', {})
            nickname = sender.get('nickname', '未知用户')
            
            # 记录消息
            if message_type == 'private':
                logger.info(f"私聊消息 - 用户: {nickname}({user_id}) 内容: {raw_message}")
            elif message_type == 'group':
                logger.info(f"群聊消息 - 群: {group_id} 用户: {nickname}({user_id}) 内容: {raw_message}")
            
            # 在这里添加你的消息处理逻辑
            self.handle_user_message(message_type, user_id, nickname, raw_message, group_id)
            
        except Exception as e:
            logger.error(f"处理消息时发生错误: {e}")
    
    def handle_user_message(self, message_type, user_id, nickname, message, group_id=None):
        """处理用户消息的核心逻辑"""
        
        # 简单的命令处理示例
        if message.startswith('/'):
            command = message[1:].split()[0].lower()
            
            if command == 'hello':
                logger.info(f"用户 {nickname} 发送了问候命令")
                
            elif command == 'help':
                logger.info(f"用户 {nickname} 请求帮助")
                
            # 在这里添加更多命令处理
        
        # 关键词回复示例
        keywords = {
            '你好': f"你好 {nickname}！",
            'ping': 'pong!',
            '时间': f"现在是 {datetime.now().strftime('%H:%M:%S')}"
        }
        
        for keyword, reply in keywords.items():
            if keyword in message:
                logger.info(f"检测到关键词 '{keyword}'，准备回复: {reply}")
                # 在这里可以调用发送消息的API
                break
        
        # 记录所有消息到这里，可以保存到数据库或文件
        message_data = {
            'timestamp': datetime.now().isoformat(),
            'type': message_type,
            'user_id': user_id,
            'nickname': nickname,
            'message': message,
            'group_id': group_id
        }
        
        # 这里可以保存到数据库或文件
        logger.debug(f"消息数据: {message_data}")
    
    def log_message(self, format, *args):
        """自定义日志格式"""
        logger.info(f"{self.address_string()} - {format % args}")


class SimpleOneBotServer:
    """简化的OneBot服务器"""
    
    def __init__(self, host='0.0.0.0', port=8080):
        self.host = host
        self.port = port
    
    def start(self):
        """启动服务器"""
        try:
            with socketserver.TCPServer((self.host, self.port), SimpleOneBotHandler) as httpd:
                logger.info(f"简化OneBot服务器启动成功")
                logger.info(f"监听地址: {self.host}:{self.port}")
                logger.info("只处理消息内容和发送者信息")
                logger.info("按 Ctrl+C 停止服务器")
                
                httpd.serve_forever()
                
        except KeyboardInterrupt:
            logger.info("服务器正在停止...")
        except Exception as e:
            logger.error(f"服务器启动失败: {e}")
        finally:
            logger.info("简化OneBot服务器已停止")


if __name__ == "__main__":
    import sys
    
    # 可以通过命令行参数指定端口
    port = 8080
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            logger.error("无效的端口号")
            sys.exit(1)
    
    server = SimpleOneBotServer(port=port)
    server.start()
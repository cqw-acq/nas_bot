#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OneBot 11 HTTP服务端
接收NapCat推送的消息和事件
"""

import json
import time
import hmac
import hashlib
import logging
from datetime import datetime
from typing import Dict, Any, Optional
import http.server
import socketserver
import urllib.parse
import requests
from threading import Thread
import queue


# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('onebot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class OneBotConfig:
    """OneBot配置类"""
    
    def __init__(self, config_file: str = "onebot_config.json"):
        self.config_file = config_file
        self.load_config()
    
    def load_config(self):
        """加载配置"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
        except FileNotFoundError:
            logger.warning(f"配置文件 {self.config_file} 不存在，使用默认配置")
            config = {}
        
        # 服务器配置
        self.host = config.get('host', '0.0.0.0')
        self.port = config.get('port', 8080)
        
        # NapCat配置
        self.napcat_host = config.get('napcat_host', 'localhost')
        self.napcat_port = config.get('napcat_port', 3000)
        self.napcat_token = config.get('napcat_token', '')
        
        # 安全配置
        self.secret = config.get('secret', '')
        self.access_token = config.get('access_token', '')
        
        # 功能配置
        self.enable_heartbeat = config.get('enable_heartbeat', True)
        self.heartbeat_interval = config.get('heartbeat_interval', 5000)
        self.enable_message_log = config.get('enable_message_log', True)
        self.enable_auto_reply = config.get('enable_auto_reply', False)
        self.auto_reply_keywords = config.get('auto_reply_keywords', {})
        
        logger.info(f"配置加载完成: {self.host}:{self.port}")


class OneBotMessageProcessor:
    """OneBot消息处理器"""
    
    def __init__(self, config: OneBotConfig):
        self.config = config
        self.message_queue = queue.Queue()
        
    def process_event(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """处理事件数据"""
        try:
            post_type = event_data.get('post_type', '')
            
            if post_type == 'message':
                return self.process_message(event_data)
            elif post_type == 'notice':
                return self.process_notice(event_data)
            elif post_type == 'request':
                return self.process_request(event_data)
            elif post_type == 'meta_event':
                return self.process_meta_event(event_data)
            else:
                logger.warning(f"未知的事件类型: {post_type}")
                return {'status': 'ok'}
                
        except Exception as e:
            logger.error(f"处理事件时发生错误: {e}")
            return {'status': 'failed', 'error': str(e)}
    
    def process_message(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """处理消息事件"""
        message_type = data.get('message_type', '')
        user_id = data.get('user_id', '')
        message = data.get('message', '')
        group_id = data.get('group_id', '')
        
        # 解析消息内容
        raw_message = data.get('raw_message', message)
        
        logger.info(f"收到{message_type}消息 - 用户:{user_id} 内容:{raw_message}")
        
        if group_id:
            logger.info(f"群组ID: {group_id}")
        
        # 记录消息到队列
        if self.config.enable_message_log:
            self.message_queue.put({
                'timestamp': datetime.now().isoformat(),
                'type': message_type,
                'user_id': user_id,
                'group_id': group_id,
                'message': raw_message,
                'data': data
            })
        
        # 自动回复处理
        if self.config.enable_auto_reply:
            reply = self.get_auto_reply(raw_message)
            if reply:
                self.send_reply(data, reply)
        
        # 自定义消息处理
        self.handle_custom_message(data)
        
        return {'status': 'ok'}
    
    def process_notice(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """处理通知事件"""
        notice_type = data.get('notice_type', '')
        logger.info(f"收到通知事件: {notice_type}")
        
        if notice_type == 'group_increase':
            # 群成员增加
            user_id = data.get('user_id', '')
            group_id = data.get('group_id', '')
            logger.info(f"用户 {user_id} 加入群 {group_id}")
            
        elif notice_type == 'group_decrease':
            # 群成员减少
            user_id = data.get('user_id', '')
            group_id = data.get('group_id', '')
            logger.info(f"用户 {user_id} 离开群 {group_id}")
            
        elif notice_type == 'friend_add':
            # 好友添加
            user_id = data.get('user_id', '')
            logger.info(f"添加好友: {user_id}")
        
        return {'status': 'ok'}
    
    def process_request(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """处理请求事件"""
        request_type = data.get('request_type', '')
        logger.info(f"收到请求事件: {request_type}")
        
        if request_type == 'friend':
            # 好友请求
            user_id = data.get('user_id', '')
            comment = data.get('comment', '')
            logger.info(f"好友请求 - 用户:{user_id} 验证消息:{comment}")
            
        elif request_type == 'group':
            # 群请求
            user_id = data.get('user_id', '')
            group_id = data.get('group_id', '')
            comment = data.get('comment', '')
            logger.info(f"群请求 - 用户:{user_id} 群:{group_id} 验证消息:{comment}")
        
        return {'status': 'ok'}
    
    def process_meta_event(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """处理元事件"""
        meta_event_type = data.get('meta_event_type', '')
        
        if meta_event_type == 'heartbeat':
            # 心跳事件
            status = data.get('status', {})
            logger.debug(f"收到心跳事件: {status}")
        elif meta_event_type == 'lifecycle':
            # 生命周期事件
            sub_type = data.get('sub_type', '')
            logger.info(f"生命周期事件: {sub_type}")
        
        return {'status': 'ok'}
    
    def get_auto_reply(self, message: str) -> Optional[str]:
        """获取自动回复内容"""
        for keyword, reply in self.config.auto_reply_keywords.items():
            if keyword in message:
                return reply
        return None
    
    def send_reply(self, original_data: Dict[str, Any], reply_message: str):
        """发送回复消息"""
        try:
            message_type = original_data.get('message_type', '')
            user_id = original_data.get('user_id', '')
            group_id = original_data.get('group_id', '')
            
            if message_type == 'private':
                # 私聊回复
                self.send_private_message(user_id, reply_message)
            elif message_type == 'group':
                # 群聊回复
                self.send_group_message(group_id, reply_message)
                
        except Exception as e:
            logger.error(f"发送回复失败: {e}")
    
    def send_private_message(self, user_id: str, message: str):
        """发送私聊消息"""
        api_url = f"http://{self.config.napcat_host}:{self.config.napcat_port}/send_private_msg"
        data = {
            'user_id': user_id,
            'message': message
        }
        self.call_api(api_url, data)
    
    def send_group_message(self, group_id: str, message: str):
        """发送群消息"""
        api_url = f"http://{self.config.napcat_host}:{self.config.napcat_port}/send_group_msg"
        data = {
            'group_id': group_id,
            'message': message
        }
        self.call_api(api_url, data)
    
    def call_api(self, url: str, data: Dict[str, Any]):
        """调用NapCat API"""
        try:
            headers = {'Content-Type': 'application/json'}
            if self.config.napcat_token:
                headers['Authorization'] = f"Bearer {self.config.napcat_token}"
            
            response = requests.post(url, json=data, headers=headers, timeout=10)
            
            if response.status_code == 200:
                logger.info(f"API调用成功: {url}")
            else:
                logger.error(f"API调用失败: {response.status_code} - {response.text}")
                
        except Exception as e:
            logger.error(f"API调用异常: {e}")
    
    def handle_custom_message(self, data: Dict[str, Any]):
        """自定义消息处理逻辑"""
        # 在这里添加你的自定义消息处理逻辑
        message = data.get('raw_message', '')
        user_id = data.get('user_id', '')
        
        # 示例：处理特定命令
        if message.startswith('/help'):
            reply = "可用命令:\n/help - 显示帮助\n/time - 显示当前时间\n/ping - 测试连接"
            self.send_reply(data, reply)
        elif message.startswith('/time'):
            reply = f"当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            self.send_reply(data, reply)
        elif message.startswith('/ping'):
            reply = "pong! 连接正常"
            self.send_reply(data, reply)


class OneBotHTTPHandler(http.server.BaseHTTPRequestHandler):
    """OneBot HTTP请求处理器"""
    
    def __init__(self, *args, config: OneBotConfig, processor: OneBotMessageProcessor, **kwargs):
        self.config = config
        self.processor = processor
        super().__init__(*args, **kwargs)
    
    def do_POST(self):
        """处理POST请求"""
        try:
            # 验证路径
            if self.path != '/':
                self.send_response(404)
                self.end_headers()
                return
            
            # 获取请求头
            content_length = int(self.headers.get('Content-Length', 0))
            content_type = self.headers.get('Content-Type', '')
            
            # 验证访问令牌
            if self.config.access_token:
                auth_header = self.headers.get('Authorization', '')
                if not auth_header.startswith(f'Bearer {self.config.access_token}'):
                    self.send_response(401)
                    self.end_headers()
                    return
            
            # 读取请求体
            post_data = self.rfile.read(content_length)
            
            # 验证签名
            if self.config.secret:
                signature = self.headers.get('X-Signature', '')
                if not self.verify_signature(post_data, signature):
                    self.send_response(401)
                    self.end_headers()
                    return
            
            # 解析JSON数据
            try:
                event_data = json.loads(post_data.decode('utf-8'))
            except json.JSONDecodeError as e:
                error_msg = f"JSON解析失败: {e}, 原始数据: {post_data.decode('utf-8', errors='replace')}"
                logger.error(error_msg)
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                
                error_response = {
                    'status': 'failed',
                    'error': 'JSON解析失败',
                    'details': str(e),
                    'raw_data': post_data.decode('utf-8', errors='replace')
                }
                response_data = json.dumps(error_response, ensure_ascii=False)
                self.wfile.write(response_data.encode('utf-8'))
                return
            
            # 处理事件
            result = self.processor.process_event(event_data)
            
            # 发送响应
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            response_data = json.dumps(result, ensure_ascii=False)
            self.wfile.write(response_data.encode('utf-8'))
            
        except Exception as e:
            logger.error(f"处理POST请求时发生错误: {e}")
            self.send_response(500)
            self.end_headers()
    
    def do_GET(self):
        """处理GET请求"""
        if self.path == '/status':
            # 状态检查
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            status = {
                'status': 'online',
                'timestamp': datetime.now().isoformat(),
                'config': {
                    'host': self.config.host,
                    'port': self.config.port,
                    'napcat_host': self.config.napcat_host,
                    'napcat_port': self.config.napcat_port
                }
            }
            
            response_data = json.dumps(status, ensure_ascii=False)
            self.wfile.write(response_data.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
    
    def verify_signature(self, data: bytes, signature: str) -> bool:
        """验证HMAC签名"""
        if not signature.startswith('sha1='):
            return False
        
        expected_signature = 'sha1=' + hmac.new(
            self.config.secret.encode('utf-8'),
            data,
            hashlib.sha1
        ).hexdigest()
        
        return hmac.compare_digest(signature, expected_signature)
    
    def log_message(self, format, *args):
        """自定义日志格式"""
        logger.info(f"{self.address_string()} - {format % args}")


class OneBotServer:
    """OneBot HTTP服务器"""
    
    def __init__(self, config_file: str = "onebot_config.json"):
        self.config = OneBotConfig(config_file)
        self.processor = OneBotMessageProcessor(self.config)
        self.httpd = None
    
    def start(self):
        """启动服务器"""
        try:
            # 创建HTTP服务器
            handler_class = lambda *args, **kwargs: OneBotHTTPHandler(
                *args, config=self.config, processor=self.processor, **kwargs
            )
            
            self.httpd = socketserver.TCPServer((self.config.host, self.config.port), handler_class)
            
            logger.info(f"OneBot 11 HTTP服务器启动成功")
            logger.info(f"监听地址: {self.config.host}:{self.config.port}")
            logger.info(f"NapCat地址: {self.config.napcat_host}:{self.config.napcat_port}")
            logger.info("按 Ctrl+C 停止服务器")
            
            # 启动消息队列处理线程
            message_thread = Thread(target=self.process_message_queue, daemon=True)
            message_thread.start()
            
            # 开始监听
            self.httpd.serve_forever()
            
        except KeyboardInterrupt:
            logger.info("服务器正在停止...")
        except Exception as e:
            logger.error(f"服务器启动失败: {e}")
        finally:
            if self.httpd:
                self.httpd.shutdown()
                self.httpd.server_close()
            logger.info("OneBot服务器已停止")
    
    def process_message_queue(self):
        """处理消息队列"""
        while True:
            try:
                if not self.processor.message_queue.empty():
                    message = self.processor.message_queue.get(timeout=1)
                    # 在这里可以添加消息持久化逻辑
                    logger.debug(f"处理队列消息: {message['type']} - {message['user_id']}")
                else:
                    time.sleep(0.1)
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"处理消息队列时发生错误: {e}")


if __name__ == "__main__":
    import sys
    
    config_file = "onebot_config.json"
    if len(sys.argv) > 1:
        config_file = sys.argv[1]
    
    server = OneBotServer(config_file)
    server.start()
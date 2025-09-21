#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flask版OneBot 11 HTTP服务端
"""

import json
import logging
from datetime import datetime
from flask import Flask, request, jsonify
import requests
import os


# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('onebot_flask.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)


class OneBotConfig:
    """OneBot配置类"""
    
    def __init__(self):
        self.load_config()
    
    def load_config(self):
        """加载配置"""
        try:
            with open('onebot_config.json', 'r', encoding='utf-8') as f:
                config = json.load(f)
        except FileNotFoundError:
            logger.warning("配置文件不存在，使用默认配置")
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
        self.enable_auto_reply = config.get('enable_auto_reply', True)
        self.auto_reply_keywords = config.get('auto_reply_keywords', {})


# 全局配置实例
config = OneBotConfig()


class MessageProcessor:
    """消息处理器"""
    
    def __init__(self, config):
        self.config = config
    
    def process_event(self, event_data):
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
    
    def process_message(self, data):
        """处理消息事件"""
        message_type = data.get('message_type', '')
        user_id = data.get('user_id', '')
        raw_message = data.get('raw_message', '')
        group_id = data.get('group_id', '')
        
        # 发送者信息
        sender = data.get('sender', {})
        nickname = sender.get('nickname', '未知用户')
        
        logger.info(f"收到{message_type}消息 - 用户:{nickname}({user_id}) 内容:{raw_message}")
        
        if group_id:
            logger.info(f"群组ID: {group_id}")
        
        # 处理命令
        if raw_message.startswith('/'):
            self.handle_command(data, raw_message)
        
        # 自动回复处理
        if self.config.enable_auto_reply:
            reply = self.get_auto_reply(raw_message)
            if reply:
                self.send_reply(data, reply)
        
        return {'status': 'ok'}
    
    def process_notice(self, data):
        """处理通知事件"""
        notice_type = data.get('notice_type', '')
        logger.info(f"收到通知事件: {notice_type}")
        return {'status': 'ok'}
    
    def process_request(self, data):
        """处理请求事件"""
        request_type = data.get('request_type', '')
        logger.info(f"收到请求事件: {request_type}")
        return {'status': 'ok'}
    
    def process_meta_event(self, data):
        """处理元事件"""
        meta_event_type = data.get('meta_event_type', '')
        if meta_event_type == 'heartbeat':
            logger.debug(f"收到心跳事件")
        elif meta_event_type == 'lifecycle':
            sub_type = data.get('sub_type', '')
            logger.info(f"生命周期事件: {sub_type}")
        return {'status': 'ok'}
    
    def handle_command(self, data, message):
        """处理命令"""
        command = message[1:].split()[0].lower()
        args = message[1:].split()[1:] if len(message.split()) > 1 else []
        
        if command == 'help':
            reply = "可用命令:\n/help - 显示帮助\n/time - 显示当前时间\n/ping - 测试连接"
            self.send_reply(data, reply)
        elif command == 'time':
            reply = f"当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            self.send_reply(data, reply)
        elif command == 'ping':
            reply = "pong! 连接正常"
            self.send_reply(data, reply)
    
    def get_auto_reply(self, message):
        """获取自动回复内容"""
        for keyword, reply in self.config.auto_reply_keywords.items():
            if keyword in message:
                return reply
        return None
    
    def send_reply(self, original_data, reply_message):
        """发送回复消息"""
        try:
            message_type = original_data.get('message_type', '')
            user_id = original_data.get('user_id', '')
            group_id = original_data.get('group_id', '')
            
            if message_type == 'private':
                self.send_private_message(user_id, reply_message)
            elif message_type == 'group':
                self.send_group_message(group_id, reply_message)
                
        except Exception as e:
            logger.error(f"发送回复失败: {e}")
    
    def send_private_message(self, user_id, message):
        """发送私聊消息"""
        url = f"http://{self.config.napcat_host}:{self.config.napcat_port}/send_private_msg"
        data = {'user_id': user_id, 'message': message}
        self.call_api(url, data)
    
    def send_group_message(self, group_id, message):
        """发送群消息"""
        url = f"http://{self.config.napcat_host}:{self.config.napcat_port}/send_group_msg"
        data = {'group_id': group_id, 'message': message}
        self.call_api(url, data)
    
    def call_api(self, url, data):
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


# 全局消息处理器实例
processor = MessageProcessor(config)


@app.route('/', methods=['POST'])
def handle_webhook():
    """处理OneBot Webhook"""
    try:
        # 验证访问令牌
        if config.access_token:
            auth_header = request.headers.get('Authorization', '')
            if not auth_header.startswith(f'Bearer {config.access_token}'):
                return jsonify({'error': 'Unauthorized'}), 401
        
        # 获取JSON数据
        try:
            event_data = request.get_json()
            if not event_data:
                return jsonify({'error': 'No JSON data'}), 400
        except Exception as e:
            logger.error(f"JSON解析失败: {e}")
            return jsonify({
                'status': 'failed',
                'error': 'JSON解析失败',
                'details': str(e)
            }), 400
        
        # 处理事件
        result = processor.process_event(event_data)
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"处理Webhook时发生错误: {e}")
        return jsonify({'status': 'failed', 'error': str(e)}), 500


@app.route('/status', methods=['GET'])
def get_status():
    """获取服务器状态"""
    status = {
        'status': 'online',
        'timestamp': datetime.now().isoformat(),
        'config': {
            'host': config.host,
            'port': config.port,
            'napcat_host': config.napcat_host,
            'napcat_port': config.napcat_port
        }
    }
    return jsonify(status)


@app.route('/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})


@app.errorhandler(404)
def not_found(error):
    """404错误处理"""
    return jsonify({'error': 'Not Found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """500错误处理"""
    return jsonify({'error': 'Internal Server Error'}), 500


def main():
    """启动Flask应用"""
    logger.info(f"OneBot 11 Flask服务器启动")
    logger.info(f"监听地址: {config.host}:{config.port}")
    logger.info(f"NapCat地址: {config.napcat_host}:{config.napcat_port}")
    
    # 启动Flask应用
    app.run(
        host=config.host,
        port=config.port,
        debug=False,
        threaded=True
    )


if __name__ == "__main__":
    main()
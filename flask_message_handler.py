#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flask版简化消息处理器
专注于处理用户消息内容和发送者信息
"""

import json
import requests
from datetime import datetime
from flask import Flask, request, jsonify


app = Flask(__name__)

# 配置
NAPCAT_HOST = "localhost"
NAPCAT_PORT = 3000
NAPCAT_TOKEN = "1145"


@app.route('/', methods=['POST'])
def handle_message():
    """处理NapCat推送的消息"""
    try:
        # 获取JSON数据
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data'}), 400
        
        # 只处理消息事件
        if data.get('post_type') == 'message':
            process_message(data)
        
        return jsonify({'status': 'ok'})
        
    except Exception as e:
        print(f"❌ 处理消息错误: {e}")
        return jsonify({'error': str(e)}), 500


def process_message(data):
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
    timestamp = datetime.now().strftime('%H:%M:%S')
    if message_type == 'private':
        print(f"💬 {timestamp} | 私聊 | {nickname}({user_id}): {message}")
    else:
        print(f"👥 {timestamp} | 群聊({group_id}) | {nickname}({user_id}): {message}")
    
    # 处理命令
    if message.startswith('/'):
        process_command(user_id, nickname, message, message_type, group_id)
    
    # 处理关键词
    elif any(keyword in message for keyword in ['你好', 'hello', '帮助']):
        process_keyword(user_id, nickname, message, message_type, group_id)


def process_command(user_id, nickname, message, message_type, group_id):
    """处理命令"""
    command = message[1:].split()[0].lower()
    
    print(f"🔧 检测到命令: {command} (来自 {nickname})")
    
    if command == 'time':
        reply = f"现在时间: {datetime.now().strftime('%H:%M:%S')}"
        send_reply(reply, user_id, group_id, message_type)
        
    elif command == 'hello':
        reply = f"你好 {nickname}! 👋"
        send_reply(reply, user_id, group_id, message_type)
        
    elif command == 'help':
        reply = "可用命令:\n/time - 显示时间\n/hello - 打招呼\n/help - 显示帮助"
        send_reply(reply, user_id, group_id, message_type)


def process_keyword(user_id, nickname, message, message_type, group_id):
    """处理关键词"""
    print(f"🔍 检测到关键词 (来自 {nickname})")
    
    if '你好' in message or 'hello' in message.lower():
        reply = f"你好 {nickname}!"
        send_reply(reply, user_id, group_id, message_type)
        
    elif '帮助' in message:
        reply = "输入 /help 查看可用命令"
        send_reply(reply, user_id, group_id, message_type)


def send_reply(message, user_id, group_id, message_type):
    """发送回复"""
    try:
        if message_type == 'private':
            url = f"http://{NAPCAT_HOST}:{NAPCAT_PORT}/send_private_msg"
            data = {'user_id': user_id, 'message': message}
        else:
            url = f"http://{NAPCAT_HOST}:{NAPCAT_PORT}/send_group_msg"
            data = {'group_id': group_id, 'message': message}
        
        headers = {'Content-Type': 'application/json'}
        if NAPCAT_TOKEN:
            headers['Authorization'] = f"Bearer {NAPCAT_TOKEN}"
        
        response = requests.post(url, json=data, headers=headers, timeout=5)
        
        if response.status_code == 200:
            print(f"✅ 回复发送成功: {message}")
        else:
            print(f"❌ 回复发送失败: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 发送回复异常: {e}")


@app.route('/status', methods=['GET'])
def get_status():
    """获取状态"""
    return jsonify({
        'status': 'running',
        'timestamp': datetime.now().isoformat(),
        'napcat': f"{NAPCAT_HOST}:{NAPCAT_PORT}"
    })


def main():
    """启动Flask应用"""
    print("🚀 Flask版简化OneBot消息处理器")
    print("📝 只处理消息内容和发送者信息")
    print("🔧 支持基础命令和关键词回复")
    print("=" * 50)
    print("✅ 服务器启动中...")
    print("📡 监听端口: 8080")
    print("🔔 等待NapCat推送消息...")
    print("=" * 50)
    
    app.run(
        host='0.0.0.0',
        port=8080,
        debug=False,
        threaded=True
    )


if __name__ == "__main__":
    main()
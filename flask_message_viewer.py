#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flask版消息查看器
只显示用户消息内容和发送者信息，不回复
"""

import json
from datetime import datetime
from flask import Flask, request, jsonify


app = Flask(__name__)


@app.route('/', methods=['POST'])
def view_message():
    """查看消息 - 只显示不回复"""
    try:
        # 获取JSON数据
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data'}), 400
        
        # 只处理消息事件
        if data.get('post_type') == 'message':
            display_message(data)
        else:
            # 显示其他事件类型
            display_other_event(data)
        
        return jsonify({'status': 'viewed'})
        
    except Exception as e:
        print(f"❌ 查看消息错误: {e}")
        # 显示原始数据
        try:
            raw_data = request.get_data()
            print(f"📋 原始数据: {raw_data.decode('utf-8', errors='replace')}")
        except:
            pass
        return jsonify({'error': str(e)}), 500


def display_message(data):
    """显示消息信息"""
    
    # 提取关键信息
    user_id = data.get('user_id')           # 发送者QQ号
    message = data.get('raw_message', '')   # 消息内容
    message_type = data.get('message_type') # private/group
    
    # 发送者信息
    sender = data.get('sender', {})
    nickname = sender.get('nickname', '未知')
    card = sender.get('card', '')  # 群名片
    role = sender.get('role', '')  # 群角色
    
    # 群信息（如果是群消息）
    group_id = data.get('group_id') if message_type == 'group' else None
    
    # 时间戳
    message_time = data.get('time', 0)
    if message_time:
        time_str = datetime.fromtimestamp(message_time).strftime('%H:%M:%S')
    else:
        time_str = datetime.now().strftime('%H:%M:%S')
    
    # 构建显示信息
    display_name = nickname
    if card:
        display_name = f"{card}({nickname})"
    
    if message_type == 'private':
        print(f"💬 {time_str} | 私聊 | {display_name}({user_id})")
    else:
        role_emoji = "👑" if role == "owner" else "⭐" if role == "admin" else "👤"
        print(f"👥 {time_str} | 群聊({group_id}) | {role_emoji}{display_name}({user_id})")
    
    # 显示消息内容
    if message:
        print(f"   📝 消息: {message}")
    else:
        print(f"   📝 消息: (空)")
    
    # 如果有图片、文件等附件，显示简要信息
    message_data = data.get('message', [])
    if isinstance(message_data, list):
        attachments = []
        for item in message_data:
            if isinstance(item, dict):
                msg_type = item.get('type', '')
                if msg_type == 'image':
                    attachments.append('图片')
                elif msg_type == 'record':
                    attachments.append('语音')
                elif msg_type == 'video':
                    attachments.append('视频')
                elif msg_type == 'file':
                    attachments.append('文件')
        
        if attachments:
            print(f"   📎 附件: {', '.join(attachments)}")
    
    print("-" * 50)


def display_other_event(data):
    """显示其他事件类型"""
    post_type = data.get('post_type', 'unknown')
    time_str = datetime.now().strftime('%H:%M:%S')
    
    if post_type == 'notice':
        notice_type = data.get('notice_type', '')
        user_id = data.get('user_id', '')
        group_id = data.get('group_id', '')
        
        print(f"🔔 {time_str} | 通知 | {notice_type}")
        if user_id:
            print(f"   👤 用户: {user_id}")
        if group_id:
            print(f"   👥 群组: {group_id}")
            
    elif post_type == 'request':
        request_type = data.get('request_type', '')
        user_id = data.get('user_id', '')
        comment = data.get('comment', '')
        
        print(f"📬 {time_str} | 请求 | {request_type}")
        if user_id:
            print(f"   👤 用户: {user_id}")
        if comment:
            print(f"   💬 备注: {comment}")
            
    elif post_type == 'meta_event':
        meta_event_type = data.get('meta_event_type', '')
        print(f"⚙️  {time_str} | 元事件 | {meta_event_type}")
        
    else:
        print(f"❓ {time_str} | 未知事件 | {post_type}")
    
    print("-" * 30)


@app.route('/status', methods=['GET'])
def get_status():
    """获取状态"""
    return jsonify({
        'status': 'running',
        'timestamp': datetime.now().isoformat(),
        'mode': 'view_only',
        'description': 'OneBot消息查看器 - 只显示不回复'
    })


@app.route('/stats', methods=['GET'])
def get_stats():
    """获取统计信息"""
    # 这里可以添加消息统计功能
    return jsonify({
        'uptime': 'running',
        'total_messages': 'N/A',
        'last_message': 'N/A'
    })


def main():
    """启动Flask应用"""
    print("🚀 Flask版OneBot消息查看器")
    print("👀 只显示消息，不自动回复")
    print("📊 API端点:")
    print("   - POST / : 接收消息")
    print("   - GET /status : 获取状态")
    print("   - GET /stats : 获取统计")
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
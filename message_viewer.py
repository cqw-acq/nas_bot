#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最简化的OneBot消息查看器
用于调试和查看NapCat推送的消息格式
"""

import json
import http.server
import socketserver
from datetime import datetime


class MessageViewer(http.server.BaseHTTPRequestHandler):
    """消息查看器 - 仅显示关键信息"""
    
    def do_POST(self):
        """接收并显示消息"""
        try:
            # 读取数据
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            # 尝试解析JSON
            try:
                data = json.loads(post_data.decode('utf-8', errors='replace'))
                self.display_message(data)
            except Exception as e:
                print(f"❌ JSON解析失败: {e}")
                print(f"原始数据: {post_data}")
            
            # 总是返回成功
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status": "ok"}')
            
        except Exception as e:
            print(f"❌ 处理请求错误: {e}")
            self.send_response(500)
            self.end_headers()
    
    def display_message(self, data):
        """显示消息信息"""
        event_type = data.get('post_type', '未知事件')
        
        if event_type == 'message':
            # 消息事件
            self.show_message_info(data)
        elif event_type == 'notice':
            # 通知事件
            print(f"📢 通知事件: {data.get('notice_type', '未知')}")
        elif event_type == 'meta_event':
            # 元事件（心跳等）
            print(f"💓 元事件: {data.get('meta_event_type', '未知')}")
        else:
            print(f"❓ 未知事件类型: {event_type}")
    
    def show_message_info(self, data):
        """显示消息详细信息"""
        
        # 基本信息
        message_type = data.get('message_type', '未知')
        user_id = data.get('user_id', '未知')
        message = data.get('raw_message', '')
        
        # 发送者信息
        sender = data.get('sender', {})
        nickname = sender.get('nickname', '未知用户')
        
        # 时间
        timestamp = datetime.now().strftime('%H:%M:%S')
        
        print("=" * 60)
        print(f"⏰ 时间: {timestamp}")
        
        if message_type == 'private':
            print(f"💬 私聊消息")
            print(f"👤 发送者: {nickname} (QQ: {user_id})")
            
        elif message_type == 'group':
            group_id = data.get('group_id', '未知')
            card = sender.get('card', '')
            role = sender.get('role', 'member')
            
            print(f"👥 群聊消息")
            print(f"🏠 群号: {group_id}")
            print(f"👤 发送者: {nickname} (QQ: {user_id})")
            if card:
                print(f"🏷️ 群名片: {card}")
            print(f"👑 角色: {role}")
        
        print(f"💭 消息内容: {message}")
        
        # 如果是命令，特别标注
        if message.startswith('/'):
            print(f"🔧 检测到命令: {message.split()[0]}")
        
        # 显示完整数据结构（可选）
        if len(message) < 100:  # 只对短消息显示详细信息
            print(f"📋 完整数据: {json.dumps(data, ensure_ascii=False, indent=2)}")
        
        print("=" * 60)
    
    def log_message(self, format, *args):
        """禁用默认日志"""
        pass


def main():
    """启动消息查看器"""
    print("🔍 OneBot消息查看器")
    print("📋 显示用户消息和发送者信息")
    print("🚀 启动服务器...")
    
    try:
        with socketserver.TCPServer(("0.0.0.0", 8080), MessageViewer) as httpd:
            print("✅ 服务器启动成功!")
            print("📡 监听地址: http://0.0.0.0:8080")
            print("🔔 等待接收消息...")
            print("按 Ctrl+C 停止")
            print("-" * 40)
            
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n👋 已停止服务器")
    except Exception as e:
        print(f"❌ 启动失败: {e}")


if __name__ == "__main__":
    main()
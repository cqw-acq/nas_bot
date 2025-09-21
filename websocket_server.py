#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WebSocket服务器监听8080端口
接收和处理WebSocket消息
需要安装: pip install websockets
"""

import asyncio
import websockets
import json
from datetime import datetime


class WebSocketMessageServer:
    """WebSocket消息服务器"""
    
    def __init__(self, host='localhost', port=8080):
        self.host = host
        self.port = port
        self.clients = set()
    
    async def register_client(self, websocket):
        """注册新客户端"""
        self.clients.add(websocket)
        print(f"[{datetime.now()}] 新客户端连接: {websocket.remote_address}")
        
        # 发送欢迎消息
        welcome_message = {
            'type': 'welcome',
            'message': '欢迎连接到WebSocket服务器',
            'timestamp': datetime.now().isoformat()
        }
        await websocket.send(json.dumps(welcome_message, ensure_ascii=False))
    
    async def unregister_client(self, websocket):
        """注销客户端"""
        if websocket in self.clients:
            self.clients.remove(websocket)
            print(f"[{datetime.now()}] 客户端断开连接: {websocket.remote_address}")
    
    async def handle_message(self, websocket, message):
        """处理收到的消息"""
        try:
            # 尝试解析JSON消息
            data = json.loads(message)
            print(f"[{datetime.now()}] 收到JSON消息: {data}")
            
            # 根据消息类型处理
            message_type = data.get('type', 'unknown')
            
            if message_type == 'echo':
                # 回显消息
                response = {
                    'type': 'echo_response',
                    'original_message': data,
                    'timestamp': datetime.now().isoformat()
                }
            elif message_type == 'broadcast':
                # 广播消息给所有客户端
                broadcast_data = {
                    'type': 'broadcast',
                    'message': data.get('message', ''),
                    'from': str(websocket.remote_address),
                    'timestamp': datetime.now().isoformat()
                }
                await self.broadcast_message(broadcast_data, exclude=websocket)
                
                response = {
                    'type': 'broadcast_sent',
                    'message': '消息已广播',
                    'timestamp': datetime.now().isoformat()
                }
            else:
                # 默认响应
                response = {
                    'type': 'message_received',
                    'received_data': data,
                    'timestamp': datetime.now().isoformat()
                }
            
        except json.JSONDecodeError as e:
            # 处理非JSON消息，包含详细的解析错误信息
            error_msg = f"JSON解析失败: {e}, 原始消息: {message}"
            print(f"[{datetime.now()}] {error_msg}")
            response = {
                'type': 'json_parse_error',
                'error': 'JSON解析失败',
                'details': str(e),
                'message': '收到非JSON格式的消息',
                'received_data': message,
                'timestamp': datetime.now().isoformat()
            }
        
        # 发送响应
        await websocket.send(json.dumps(response, ensure_ascii=False))
    
    async def broadcast_message(self, message, exclude=None):
        """向所有客户端广播消息"""
        if self.clients:
            message_str = json.dumps(message, ensure_ascii=False)
            disconnected_clients = set()
            
            for client in self.clients:
                if client != exclude:
                    try:
                        await client.send(message_str)
                    except websockets.exceptions.ConnectionClosed:
                        disconnected_clients.add(client)
            
            # 移除断开连接的客户端
            for client in disconnected_clients:
                await self.unregister_client(client)
    
    async def handle_client(self, websocket, path):
        """处理客户端连接"""
        await self.register_client(websocket)
        
        try:
            async for message in websocket:
                await self.handle_message(websocket, message)
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            await self.unregister_client(websocket)
    
    def start_server(self):
        """启动WebSocket服务器"""
        print(f"WebSocket服务器启动成功，监听 {self.host}:{self.port}")
        print(f"WebSocket URL: ws://{self.host}:{self.port}")
        print("按 Ctrl+C 停止服务器")
        
        start_server = websockets.serve(
            self.handle_client,
            self.host,
            self.port
        )
        
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()


# 简单的WebSocket客户端测试
async def test_websocket_client():
    """测试WebSocket客户端"""
    uri = "ws://localhost:8080"
    
    try:
        async with websockets.connect(uri) as websocket:
            print("连接到WebSocket服务器")
            
            # 发送测试消息
            test_messages = [
                '{"type": "echo", "message": "测试回显消息"}',
                '{"type": "broadcast", "message": "这是一条广播消息"}',
                '{"type": "custom", "data": {"key": "value", "number": 123}}',
                '普通文本消息'
            ]
            
            for message in test_messages:
                print(f"发送: {message}")
                await websocket.send(message)
                
                response = await websocket.recv()
                print(f"收到: {response}")
                print("-" * 50)
                
                # 等待1秒
                await asyncio.sleep(1)
                
    except Exception as e:
        print(f"客户端测试失败: {e}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "client":
        # 运行测试客户端
        asyncio.run(test_websocket_client())
    else:
        # 运行服务器
        try:
            server = WebSocketMessageServer(port=8080)
            server.start_server()
        except KeyboardInterrupt:
            print("\nWebSocket服务器已停止")
        except ImportError:
            print("WebSocket服务器需要安装websockets库: pip install websockets")
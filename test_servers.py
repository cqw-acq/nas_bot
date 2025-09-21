#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试8080端口服务器的脚本
"""

import requests
import socket
import json
import time
import threading
from datetime import datetime


def test_http_server():
    """测试HTTP服务器"""
    print("=" * 50)
    print("测试HTTP服务器")
    print("=" * 50)
    
    base_url = "http://localhost:8080"
    
    try:
        # 测试GET请求
        print("1. 测试GET请求...")
        response = requests.get(f"{base_url}/test?message=hello&user=test")
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
        print()
        
        # 测试POST JSON请求
        print("2. 测试POST JSON请求...")
        json_data = {
            "type": "test",
            "message": "Hello HTTP Server",
            "timestamp": datetime.now().isoformat()
        }
        response = requests.post(f"{base_url}/message", json=json_data)
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
        print()
        
        # 测试POST文本请求
        print("3. 测试POST文本请求...")
        response = requests.post(
            f"{base_url}/message",
            data="这是一条文本消息",
            headers={'Content-Type': 'text/plain'}
        )
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
        
    except requests.exceptions.ConnectionError:
        print("❌ HTTP服务器未启动或无法连接")
        print("请先运行: python http_server.py")
    except Exception as e:
        print(f"❌ HTTP测试失败: {e}")


def test_tcp_server():
    """测试TCP服务器"""
    print("=" * 50)
    print("测试TCP服务器")
    print("=" * 50)
    
    try:
        # 创建TCP连接
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('localhost', 8080))
        print("✅ TCP连接成功")
        
        # 测试消息
        test_messages = [
            "Hello TCP Server!",
            '{"type": "test", "message": "JSON消息测试"}',
            "中文消息测试"
        ]
        
        for i, message in enumerate(test_messages, 1):
            print(f"\n{i}. 发送消息: {message}")
            sock.send(message.encode('utf-8'))
            
            # 接收响应
            response = sock.recv(1024).decode('utf-8')
            print(f"收到响应: {response}")
        
        sock.close()
        
    except socket.error as e:
        print("❌ TCP服务器未启动或无法连接")
        print("请先运行: python tcp_server.py")
    except Exception as e:
        print(f"❌ TCP测试失败: {e}")


def test_websocket_server():
    """测试WebSocket服务器（需要websockets库）"""
    print("=" * 50)
    print("测试WebSocket服务器")
    print("=" * 50)
    
    try:
        import websockets
        import asyncio
        
        async def websocket_test():
            uri = "ws://localhost:8080"
            try:
                async with websockets.connect(uri) as websocket:
                    print("✅ WebSocket连接成功")
                    
                    # 测试消息
                    test_messages = [
                        '{"type": "echo", "message": "回显测试"}',
                        '{"type": "custom", "data": {"key": "value"}}',
                        '普通文本消息'
                    ]
                    
                    for i, message in enumerate(test_messages, 1):
                        print(f"\n{i}. 发送消息: {message}")
                        await websocket.send(message)
                        
                        response = await websocket.recv()
                        print(f"收到响应: {response}")
                        
                        await asyncio.sleep(0.5)
                        
            except Exception as e:
                print("❌ WebSocket服务器未启动或无法连接")
                print("请先运行: python websocket_server.py")
        
        # 运行异步测试
        asyncio.run(websocket_test())
        
    except ImportError:
        print("❌ 未安装websockets库")
        print("请安装: pip install websockets")
    except Exception as e:
        print(f"❌ WebSocket测试失败: {e}")


def check_port_8080():
    """检查8080端口是否被占用"""
    print("=" * 50)
    print("检查8080端口状态")
    print("=" * 50)
    
    try:
        # 尝试连接8080端口
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('localhost', 8080))
        sock.close()
        
        if result == 0:
            print("✅ 8080端口有服务在监听")
            return True
        else:
            print("❌ 8080端口没有服务在监听")
            return False
    except Exception as e:
        print(f"❌ 检查端口时出错: {e}")
        return False


def main():
    """主测试函数"""
    print("🚀 开始测试8080端口的服务器")
    print(f"测试时间: {datetime.now()}")
    
    # 检查端口状态
    if not check_port_8080():
        print("\n💡 提示:")
        print("请先启动一个服务器:")
        print("- HTTP服务器: python http_server.py")
        print("- TCP服务器: python tcp_server.py")
        print("- WebSocket服务器: python websocket_server.py")
        return
    
    print("\n请选择要测试的服务器类型:")
    print("1. HTTP服务器")
    print("2. TCP服务器")
    print("3. WebSocket服务器")
    print("4. 自动检测并测试所有类型")
    
    try:
        choice = input("\n请输入选择 (1-4): ").strip()
        
        if choice == '1':
            test_http_server()
        elif choice == '2':
            test_tcp_server()
        elif choice == '3':
            test_websocket_server()
        elif choice == '4':
            # 尝试所有类型
            test_http_server()
            time.sleep(1)
            test_tcp_server()
            time.sleep(1)
            test_websocket_server()
        else:
            print("❌ 无效选择")
            
    except KeyboardInterrupt:
        print("\n测试被中断")
    except Exception as e:
        print(f"❌ 测试过程中出错: {e}")


if __name__ == "__main__":
    main()
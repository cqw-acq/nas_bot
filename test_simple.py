#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试简化版OneBot服务器
发送模拟消息来测试服务器功能
"""

import json
import time
import requests
from datetime import datetime


def test_simple_server():
    """测试简化版服务器"""
    print("🧪 测试简化版OneBot服务器")
    print("=" * 40)
    
    # 模拟的消息数据
    test_messages = [
        {
            "name": "私聊普通消息",
            "data": {
                "time": int(time.time()),
                "self_id": 123456789,
                "post_type": "message",
                "message_type": "private",
                "sub_type": "friend",
                "message_id": 12345,
                "user_id": 987654321,
                "message": [{"type": "text", "data": {"text": "你好"}}],
                "raw_message": "你好",
                "font": 0,
                "sender": {
                    "user_id": 987654321,
                    "nickname": "测试用户",
                    "sex": "unknown",
                    "age": 20
                }
            }
        },
        {
            "name": "群聊命令消息",
            "data": {
                "time": int(time.time()),
                "self_id": 123456789,
                "post_type": "message",
                "message_type": "group",
                "sub_type": "normal",
                "message_id": 12346,
                "group_id": 456789123,
                "user_id": 111222333,
                "message": [{"type": "text", "data": {"text": "/time"}}],
                "raw_message": "/time",
                "font": 0,
                "sender": {
                    "user_id": 111222333,
                    "nickname": "群友",
                    "card": "测试群友",
                    "sex": "unknown",
                    "age": 25,
                    "area": "",
                    "level": "1",
                    "role": "member",
                    "title": ""
                }
            }
        },
        {
            "name": "帮助命令",
            "data": {
                "time": int(time.time()),
                "self_id": 123456789,
                "post_type": "message",
                "message_type": "private",
                "sub_type": "friend",
                "message_id": 12347,
                "user_id": 444555666,
                "message": [{"type": "text", "data": {"text": "/help"}}],
                "raw_message": "/help",
                "font": 0,
                "sender": {
                    "user_id": 444555666,
                    "nickname": "新用户",
                    "sex": "unknown",
                    "age": 18
                }
            }
        }
    ]
    
    for test_case in test_messages:
        print(f"\n📨 发送测试: {test_case['name']}")
        
        try:
            response = requests.post(
                "http://localhost:8080/",
                json=test_case['data'],
                headers={'Content-Type': 'application/json'},
                timeout=5
            )
            
            if response.status_code == 200:
                print("✅ 消息发送成功")
            else:
                print(f"❌ 消息发送失败: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print("❌ 无法连接到服务器")
            print("请先启动服务器: python message_viewer.py")
            break
        except Exception as e:
            print(f"❌ 发送失败: {e}")
        
        time.sleep(1)  # 等待1秒


def test_invalid_json():
    """测试无效JSON处理"""
    print("\n🧪 测试无效JSON处理")
    print("=" * 40)
    
    invalid_cases = [
        ("不完整JSON", '{"message": '),
        ("控制字符", '{"message": "test\x00"}'),
        ("非JSON", "这不是JSON"),
    ]
    
    for name, data in invalid_cases:
        print(f"\n📨 测试: {name}")
        print(f"数据: {repr(data)}")
        
        try:
            response = requests.post(
                "http://localhost:8080/",
                data=data.encode('utf-8'),
                headers={'Content-Type': 'application/json'},
                timeout=5
            )
            
            print(f"状态码: {response.status_code}")
            
        except requests.exceptions.ConnectionError:
            print("❌ 无法连接到服务器")
            break
        except Exception as e:
            print(f"❌ 测试失败: {e}")


def main():
    """主函数"""
    print("🚀 OneBot简化版服务器测试")
    print(f"🕐 时间: {datetime.now().strftime('%H:%M:%S')}")
    print("\n💡 请确保已启动其中一个服务器:")
    print("   python message_viewer.py   - 消息查看器")
    print("   python message_handler.py - 消息处理器")
    print("   python simple_onebot.py   - 简化服务器")
    
    input("\n按回车开始测试...")
    
    # 测试正常消息
    test_simple_server()
    
    # 测试错误处理
    test_invalid_json()
    
    print("\n" + "=" * 50)
    print("✅ 测试完成")
    print("📋 检查服务器输出查看消息处理结果")


if __name__ == "__main__":
    main()
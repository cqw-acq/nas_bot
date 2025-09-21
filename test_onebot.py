#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OneBot 11服务端测试脚本
测试服务器的各项功能
"""

import json
import time
import requests
import threading
from datetime import datetime
from onebot_api import OneBotAPI, MessageBuilder


def test_server_status():
    """测试服务器状态"""
    print("=" * 50)
    print("🔍 测试服务器状态")
    print("=" * 50)
    
    try:
        response = requests.get("http://localhost:8080/status", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ 服务器在线")
            print(f"📊 状态信息: {json.dumps(data, indent=2, ensure_ascii=False)}")
        else:
            print(f"❌ 服务器响应异常: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到服务器")
        print("请确保OneBot服务器正在运行在 localhost:8080")
    except Exception as e:
        print(f"❌ 测试失败: {e}")


def test_webhook_endpoint():
    """测试Webhook端点"""
    print("\n" + "=" * 50)
    print("📡 测试Webhook端点")
    print("=" * 50)
    
    # 模拟NapCat发送的消息事件
    test_message_event = {
        "time": int(time.time()),
        "self_id": 123456789,
        "post_type": "message",
        "message_type": "private",
        "sub_type": "friend",
        "message_id": 12345,
        "user_id": 987654321,
        "message": [
            {"type": "text", "data": {"text": "Hello OneBot!"}}
        ],
        "raw_message": "Hello OneBot!",
        "font": 0,
        "sender": {
            "user_id": 987654321,
            "nickname": "测试用户",
            "card": "",
            "sex": "unknown",
            "age": 0,
            "area": "",
            "level": "1"
        }
    }
    
    try:
        headers = {'Content-Type': 'application/json'}
        response = requests.post(
            "http://localhost:8080/", 
            json=test_message_event, 
            headers=headers,
            timeout=5
        )
        
        if response.status_code == 200:
            print("✅ Webhook端点正常")
            result = response.json()
            print(f"📝 响应: {json.dumps(result, ensure_ascii=False)}")
        else:
            print(f"❌ Webhook响应异常: {response.status_code}")
            print(f"响应内容: {response.text}")
            
    except Exception as e:
        print(f"❌ Webhook测试失败: {e}")


def test_api_calls():
    """测试API调用"""
    print("\n" + "=" * 50)
    print("🔧 测试API调用")
    print("=" * 50)
    
    # 使用默认配置测试API
    api = OneBotAPI(host='localhost', port=3000)
    
    print("🔍 测试获取登录信息...")
    try:
        login_info = api.get_login_info()
        if login_info.get('status') == 'ok':
            print("✅ 获取登录信息成功")
            print(f"📱 机器人信息: {json.dumps(login_info.get('data', {}), ensure_ascii=False)}")
        else:
            print(f"❌ 获取登录信息失败: {login_info.get('msg', '未知错误')}")
    except Exception as e:
        print(f"❌ API调用异常: {e}")
        print("💡 这是正常的，因为NapCat可能没有运行")
    
    print("\n🔍 测试获取状态...")
    try:
        status = api.get_status()
        if status.get('status') == 'ok':
            print("✅ 获取状态成功")
            print(f"📊 状态信息: {json.dumps(status.get('data', {}), ensure_ascii=False)}")
        else:
            print(f"❌ 获取状态失败: {status.get('msg', '未知错误')}")
    except Exception as e:
        print(f"❌ API调用异常: {e}")
        print("💡 这是正常的，因为NapCat可能没有运行")


def test_message_builder():
    """测试消息构建器"""
    print("\n" + "=" * 50)
    print("🛠️ 测试消息构建器")
    print("=" * 50)
    
    # 测试各种消息类型
    test_cases = [
        ("文本消息", MessageBuilder.text("Hello World!")),
        ("@消息", MessageBuilder.at(123456789, "测试用户")),
        ("@全体", MessageBuilder.at_all()),
        ("表情", MessageBuilder.face(1)),
        ("图片", MessageBuilder.image("test.jpg")),
        ("语音", MessageBuilder.record("test.amr")),
        ("回复", MessageBuilder.reply(12345)),
        ("组合消息", MessageBuilder.combine(
            MessageBuilder.at(123456789),
            MessageBuilder.text(" 你好！"),
            MessageBuilder.face(1)
        ))
    ]
    
    for name, message in test_cases:
        print(f"✅ {name}: {message}")


def test_multiple_events():
    """测试多种事件类型"""
    print("\n" + "=" * 50)
    print("📨 测试多种事件类型")
    print("=" * 50)
    
    # 群消息事件
    group_message = {
        "time": int(time.time()),
        "self_id": 123456789,
        "post_type": "message",
        "message_type": "group",
        "sub_type": "normal",
        "message_id": 12346,
        "group_id": 987654321,
        "user_id": 111222333,
        "anonymous": None,
        "message": [{"type": "text", "data": {"text": "/help"}}],
        "raw_message": "/help",
        "font": 0,
        "sender": {
            "user_id": 111222333,
            "nickname": "群友",
            "card": "测试群友",
            "sex": "unknown",
            "age": 0,
            "area": "",
            "level": "1",
            "role": "member",
            "title": ""
        }
    }
    
    # 通知事件
    notice_event = {
        "time": int(time.time()),
        "self_id": 123456789,
        "post_type": "notice",
        "notice_type": "group_increase",
        "sub_type": "approve",
        "group_id": 987654321,
        "operator_id": 123456789,
        "user_id": 444555666
    }
    
    # 心跳事件
    heartbeat_event = {
        "time": int(time.time()),
        "self_id": 123456789,
        "post_type": "meta_event",
        "meta_event_type": "heartbeat",
        "status": {
            "online": True,
            "good": True
        },
        "interval": 5000
    }
    
    events = [
        ("群消息事件", group_message),
        ("通知事件", notice_event),
        ("心跳事件", heartbeat_event)
    ]
    
    for name, event_data in events:
        print(f"\n🧪 测试 {name}...")
        try:
            headers = {'Content-Type': 'application/json'}
            response = requests.post(
                "http://localhost:8080/", 
                json=event_data, 
                headers=headers,
                timeout=5
            )
            
            if response.status_code == 200:
                print(f"✅ {name} 处理成功")
                result = response.json()
                print(f"📝 响应: {result.get('status', '未知')}")
            else:
                print(f"❌ {name} 处理失败: {response.status_code}")
                
        except Exception as e:
            print(f"❌ {name} 测试异常: {e}")


def test_security_features():
    """测试安全功能"""
    print("\n" + "=" * 50)
    print("🔒 测试安全功能")
    print("=" * 50)
    
    # 测试无效路径
    print("🧪 测试无效路径...")
    try:
        response = requests.post("http://localhost:8080/invalid", timeout=5)
        if response.status_code == 404:
            print("✅ 无效路径正确返回404")
        else:
            print(f"❌ 无效路径返回异常状态码: {response.status_code}")
    except Exception as e:
        print(f"❌ 测试失败: {e}")
    
    # 测试无效JSON
    print("\n🧪 测试无效JSON...")
    try:
        headers = {'Content-Type': 'application/json'}
        response = requests.post(
            "http://localhost:8080/", 
            data="invalid json", 
            headers=headers,
            timeout=5
        )
        if response.status_code == 400:
            print("✅ 无效JSON正确返回400")
        else:
            print(f"❌ 无效JSON返回异常状态码: {response.status_code}")
    except Exception as e:
        print(f"❌ 测试失败: {e}")


def stress_test():
    """压力测试"""
    print("\n" + "=" * 50)
    print("⚡ 压力测试")
    print("=" * 50)
    
    def send_test_message(thread_id):
        """发送测试消息"""
        test_event = {
            "time": int(time.time()),
            "self_id": 123456789,
            "post_type": "message",
            "message_type": "private",
            "sub_type": "friend",
            "message_id": 10000 + thread_id,
            "user_id": 100000 + thread_id,
            "message": [{"type": "text", "data": {"text": f"Test message {thread_id}"}}],
            "raw_message": f"Test message {thread_id}",
            "font": 0,
            "sender": {"user_id": 100000 + thread_id, "nickname": f"User{thread_id}"}
        }
        
        try:
            headers = {'Content-Type': 'application/json'}
            response = requests.post(
                "http://localhost:8080/", 
                json=test_event, 
                headers=headers,
                timeout=5
            )
            return response.status_code == 200
        except:
            return False
    
    # 启动多个线程发送消息
    thread_count = 10
    message_count = 5
    success_count = 0
    total_count = thread_count * message_count
    
    print(f"🚀 启动 {thread_count} 个线程，每个发送 {message_count} 条消息...")
    
    threads = []
    results = []
    
    def worker(thread_id):
        thread_results = []
        for i in range(message_count):
            result = send_test_message(thread_id * message_count + i)
            thread_results.append(result)
            time.sleep(0.1)  # 避免过于频繁
        results.extend(thread_results)
    
    start_time = time.time()
    
    for i in range(thread_count):
        thread = threading.Thread(target=worker, args=(i,))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    end_time = time.time()
    success_count = sum(results)
    
    print(f"📊 压力测试结果:")
    print(f"   总消息数: {total_count}")
    print(f"   成功处理: {success_count}")
    print(f"   失败数量: {total_count - success_count}")
    print(f"   成功率: {success_count/total_count*100:.1f}%")
    print(f"   总耗时: {end_time - start_time:.2f}秒")
    print(f"   平均QPS: {total_count/(end_time - start_time):.1f}")


def main():
    """主测试函数"""
    print("🚀 OneBot 11服务端功能测试")
    print(f"🕐 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n💡 请确保OneBot服务器正在运行: python onebot_server.py")
    
    # 等待用户确认
    input("\n按回车键开始测试...")
    
    # 执行各项测试
    test_server_status()
    test_webhook_endpoint()
    test_api_calls()
    test_message_builder()
    test_multiple_events()
    test_security_features()
    
    # 询问是否进行压力测试
    stress_test_choice = input("\n是否进行压力测试？(y/N): ").strip().lower()
    if stress_test_choice in ['y', 'yes']:
        stress_test()
    
    print("\n" + "=" * 50)
    print("✅ 测试完成")
    print("=" * 50)
    print("📝 测试总结:")
    print("   - 服务器状态检查")
    print("   - Webhook端点测试")
    print("   - API调用测试")
    print("   - 消息构建器测试")
    print("   - 多种事件类型测试")
    print("   - 安全功能测试")
    if stress_test_choice in ['y', 'yes']:
        print("   - 压力测试")
    print("\n📚 查看服务器日志: tail -f onebot.log")


if __name__ == "__main__":
    main()
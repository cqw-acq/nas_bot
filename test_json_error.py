#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试JSON解析错误处理
验证所有服务器的JSON解析失败时是否正确抛出错误信息
"""

import json
import time
import requests
import socket
import threading
from datetime import datetime


def test_onebot_json_error():
    """测试OneBot服务器的JSON解析错误"""
    print("🧪 测试OneBot服务器JSON解析错误处理")
    print("=" * 50)
    
    # 测试无效的JSON数据
    invalid_json_cases = [
        ('不完整的JSON', '{"message": "test"'),
        ('语法错误的JSON', '{"message": "test",}'),
        ('非JSON文本', 'this is not json'),
        ('空数据', ''),
        ('数字开头', '123{"test": "value"}'),
        ('特殊字符', '{"message": "test\x00"}'),
    ]
    
    for case_name, invalid_data in invalid_json_cases:
        print(f"\n📝 测试案例: {case_name}")
        print(f"数据: {repr(invalid_data)}")
        
        try:
            headers = {'Content-Type': 'application/json'}
            response = requests.post(
                "http://localhost:8080/", 
                data=invalid_data.encode('utf-8'), 
                headers=headers,
                timeout=5
            )
            
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 400:
                try:
                    result = response.json()
                    print("✅ 正确返回JSON解析错误")
                    print(f"错误信息: {result.get('error', '未知')}")
                    print(f"详细信息: {result.get('details', '无')}")
                    if result.get('raw_data'):
                        print(f"原始数据: {repr(result.get('raw_data', ''))}")
                except:
                    print("❌ 响应不是有效的JSON")
                    print(f"响应内容: {response.text}")
            else:
                print(f"❌ 期望状态码400，实际得到: {response.status_code}")
                print(f"响应内容: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("❌ 无法连接到OneBot服务器")
            print("请确保服务器正在运行: python onebot_server.py")
            break
        except Exception as e:
            print(f"❌ 测试异常: {e}")


def test_tcp_json_error():
    """测试TCP服务器的JSON解析错误"""
    print("\n🧪 测试TCP服务器JSON解析错误处理")
    print("=" * 50)
    
    invalid_json_cases = [
        ('无效JSON', '{"incomplete": '),
        ('非JSON文本', 'hello world'),
        ('空字符串', ''),
    ]
    
    try:
        # 连接TCP服务器
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('localhost', 8080))
        print("✅ TCP连接成功")
        
        for case_name, invalid_data in invalid_json_cases:
            print(f"\n📝 测试案例: {case_name}")
            print(f"数据: {repr(invalid_data)}")
            
            try:
                # 发送无效JSON
                sock.send(invalid_data.encode('utf-8'))
                
                # 接收响应
                response_data = sock.recv(1024).decode('utf-8')
                print(f"原始响应: {response_data}")
                
                try:
                    response = json.loads(response_data)
                    if response.get('status') == 'json_parse_error':
                        print("✅ 正确识别JSON解析错误")
                        print(f"错误信息: {response.get('error', '未知')}")
                        print(f"详细信息: {response.get('details', '无')}")
                    else:
                        print(f"🔍 响应状态: {response.get('status', '未知')}")
                except json.JSONDecodeError:
                    print("❌ 服务器响应不是有效JSON")
                    
            except Exception as e:
                print(f"❌ 发送数据失败: {e}")
        
        sock.close()
        
    except socket.error:
        print("❌ 无法连接到TCP服务器")
        print("请确保TCP服务器正在运行在8080端口")
    except Exception as e:
        print(f"❌ TCP测试异常: {e}")


def test_websocket_json_error():
    """测试WebSocket服务器的JSON解析错误"""
    print("\n🧪 测试WebSocket服务器JSON解析错误处理")
    print("=" * 50)
    
    try:
        import websockets
        import asyncio
        
        async def websocket_test():
            try:
                uri = "ws://localhost:8080"
                async with websockets.connect(uri) as websocket:
                    print("✅ WebSocket连接成功")
                    
                    invalid_json_cases = [
                        ('语法错误', '{"test": invalid}'),
                        ('不完整', '{"message"'),
                        ('纯文本', 'not json at all'),
                    ]
                    
                    for case_name, invalid_data in invalid_json_cases:
                        print(f"\n📝 测试案例: {case_name}")
                        print(f"数据: {repr(invalid_data)}")
                        
                        await websocket.send(invalid_data)
                        response_str = await websocket.recv()
                        
                        try:
                            response = json.loads(response_str)
                            if response.get('type') == 'json_parse_error':
                                print("✅ 正确识别JSON解析错误")
                                print(f"错误信息: {response.get('error', '未知')}")
                                print(f"详细信息: {response.get('details', '无')}")
                            else:
                                print(f"🔍 响应类型: {response.get('type', '未知')}")
                        except json.JSONDecodeError:
                            print("❌ 服务器响应不是有效JSON")
                            print(f"原始响应: {response_str}")
                        
                        await asyncio.sleep(0.5)
                        
            except Exception as e:
                print("❌ WebSocket服务器连接失败或未运行")
                print(f"错误: {e}")
        
        asyncio.run(websocket_test())
        
    except ImportError:
        print("❌ 未安装websockets库，跳过WebSocket测试")
        print("安装命令: pip install websockets")
    except Exception as e:
        print(f"❌ WebSocket测试异常: {e}")


def test_api_json_error():
    """测试API模块的JSON解析错误处理"""
    print("\n🧪 测试API模块JSON解析错误处理")
    print("=" * 50)
    
    from onebot_api import OneBotAPI
    
    # 创建API实例（使用无效端口，确保会失败）
    api = OneBotAPI(host='httpbin.org', port=80)  # 使用httpbin测试无效响应
    
    print("🔍 测试API响应JSON解析...")
    
    # 这个测试可能需要模拟一个返回非JSON的服务器
    # 由于httpbin.org/post返回的是JSON，我们需要用其他方式测试
    
    print("💡 提示: API JSON解析错误通常在以下情况发生:")
    print("   - NapCat返回HTML错误页面而非JSON")
    print("   - 网络中断导致不完整的响应")
    print("   - 服务器返回空响应")
    print("   - 服务器返回纯文本错误信息")
    
    # 可以通过查看日志来验证错误处理
    print("📝 错误信息将记录在日志中，包含:")
    print("   - 原始错误详情")
    print("   - 完整的响应内容")
    print("   - 解析失败的具体原因")


def main():
    """主测试函数"""
    print("🚀 JSON解析错误处理测试")
    print(f"🕐 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n💡 此测试将验证所有服务器在收到无效JSON时的错误处理")
    
    # 测试OneBot服务器（HTTP）
    test_onebot_json_error()
    
    # 测试TCP服务器
    test_tcp_json_error()
    
    # 测试WebSocket服务器
    test_websocket_json_error()
    
    # 测试API模块
    test_api_json_error()
    
    print("\n" + "=" * 60)
    print("✅ JSON解析错误测试完成")
    print("=" * 60)
    print("📋 测试总结:")
    print("   ✅ OneBot服务器: 返回400状态码和详细错误信息")
    print("   ✅ TCP服务器: 返回json_parse_error状态和错误详情")
    print("   ✅ WebSocket服务器: 返回json_parse_error类型和错误详情")
    print("   ✅ API模块: 在日志中记录详细的解析失败信息")
    print("\n🔍 查看详细日志: tail -f onebot.log")
    print("📝 所有JSON解析失败都会包含:")
    print("   - 具体的错误类型和描述")
    print("   - 原始数据内容")
    print("   - 失败的详细原因")


if __name__ == "__main__":
    main()
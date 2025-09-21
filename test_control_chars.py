#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试控制字符处理
专门测试JSON中的控制字符问题
"""

import json
import requests
import socket
import time
from datetime import datetime


def test_control_characters():
    """测试各种控制字符的处理"""
    print("🧪 测试控制字符处理")
    print("=" * 60)
    
    # 创建包含各种控制字符的测试数据
    test_cases = [
        {
            'name': 'NULL字符 (\\x00)',
            'data': '{"message": "test\x00data"}'
        },
        {
            'name': 'Backspace (\\x08)',
            'data': '{"message": "test\x08data"}'
        },
        {
            'name': 'Tab字符 (\\x09) - 应该保留',
            'data': '{"message": "test\tdata"}'
        },
        {
            'name': 'Vertical Tab (\\x0B)',
            'data': '{"message": "test\x0Bdata"}'
        },
        {
            'name': 'Form Feed (\\x0C)',
            'data': '{"message": "test\x0Cdata"}'
        },
        {
            'name': 'Carriage Return (\\x0D) - 应该保留',
            'data': '{"message": "test\rdata"}'
        },
        {
            'name': 'Escape字符 (\\x1B)',
            'data': '{"message": "test\x1Bdata"}'
        },
        {
            'name': 'DEL字符 (\\x7F)',
            'data': '{"message": "test\x7Fdata"}'
        },
        {
            'name': '多个控制字符',
            'data': '{"message": "test\x00\x08\x0B\x1Bdata"}'
        },
        {
            'name': '控制字符在JSON结构中',
            'data': '{"mess\x00age": "test", "value\x08": 123}'
        },
        {
            'name': '正常JSON（对照组）',
            'data': '{"message": "normal test data", "value": 123}'
        }
    ]
    
    print(f"📋 准备测试 {len(test_cases)} 个案例...")
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n📝 测试案例 {i}: {case['name']}")
        print(f"原始数据: {repr(case['data'])}")
        print(f"十六进制: {' '.join(f'{ord(c):02x}' for c in case['data'])}")
        
        # 测试OneBot服务器
        test_onebot_server(case['data'])
        
        # 测试JSON工具模块
        test_json_utils(case['data'])
        
        print("-" * 40)


def test_onebot_server(data):
    """测试OneBot服务器的控制字符处理"""
    try:
        headers = {'Content-Type': 'application/json'}
        response = requests.post(
            "http://localhost:8080/", 
            data=data.encode('utf-8'), 
            headers=headers,
            timeout=5
        )
        
        print(f"OneBot服务器响应: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ 成功解析JSON")
            try:
                result = response.json()
                print(f"解析结果: {result.get('post_type', '未知事件类型')}")
            except:
                print("响应不是有效JSON")
        elif response.status_code == 400:
            try:
                error_info = response.json()
                print("❌ JSON解析失败（预期）")
                print(f"错误位置: {error_info.get('error_position', '未知')}")
                print(f"错误字符: {error_info.get('error_char', '未知')}")
                if error_info.get('suggestions'):
                    print(f"修复建议: {'; '.join(error_info['suggestions'])}")
            except:
                print("❌ 解析失败但无法获取错误详情")
        else:
            print(f"❌ 意外的响应状态码: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到OneBot服务器")
    except Exception as e:
        print(f"❌ 测试异常: {e}")


def test_json_utils(data):
    """测试JSON工具模块的控制字符处理"""
    try:
        from json_utils import parse_json_with_details, clean_json_string
        
        # 测试清理功能
        cleaned = clean_json_string(data)
        if cleaned != data:
            print(f"🧹 数据已清理: {repr(cleaned)}")
        else:
            print("🔍 数据无需清理")
        
        # 测试解析功能
        result, error_details = parse_json_with_details(data)
        
        if result is not None:
            print("✅ JSON工具成功解析")
        else:
            print("❌ JSON工具解析失败")
            if error_details:
                print(f"错误: {error_details['error_message']}")
                print(f"位置: {error_details['error_position']}")
                print(f"字符: {error_details['error_char']}")
                
    except ImportError:
        print("❌ 无法导入JSON工具模块")
    except Exception as e:
        print(f"❌ JSON工具测试异常: {e}")


def test_encoding_issues():
    """测试编码相关问题"""
    print("\n🌐 测试编码相关问题")
    print("=" * 60)
    
    # 测试不同编码的数据
    test_cases = [
        {
            'name': 'UTF-8 BOM',
            'data': '\ufeff{"message": "test with BOM"}'.encode('utf-8')
        },
        {
            'name': 'GBK编码的中文',
            'data': '{"message": "测试中文"}'.encode('gbk')
        },
        {
            'name': 'Latin1编码',
            'data': '{"message": "tëst dàta"}'.encode('latin1')
        },
        {
            'name': '混合编码（应该失败）',
            'data': b'{"message": "test\xff\xfe data"}'
        }
    ]
    
    for case in test_cases:
        print(f"\n📝 测试: {case['name']}")
        print(f"字节数据: {case['data']}")
        
        try:
            from json_utils import safe_json_decode
            decoded, error = safe_json_decode(case['data'])
            
            if error:
                print(f"❌ 解码失败: {error}")
            else:
                print(f"✅ 解码成功: {repr(decoded)}")
                
        except Exception as e:
            print(f"❌ 测试异常: {e}")


def test_real_world_scenarios():
    """测试真实世界的场景"""
    print("\n🌍 测试真实世界场景")
    print("=" * 60)
    
    # 模拟可能出现的问题
    scenarios = [
        {
            'name': '复制粘贴时的隐藏字符',
            'data': '{"message": "Hello\u200b World"}'  # 零宽度空格
        },
        {
            'name': '终端控制序列',
            'data': '{"message": "\\033[31mRed Text\\033[0m"}'
        },
        {
            'name': 'Windows换行符',
            'data': '{"message": "Line 1\\r\\nLine 2"}'
        },
        {
            'name': '不完整的Unicode',
            'data': '{"message": "test\udcff"}'  # 代理字符
        },
        {
            'name': '超长字符串',
            'data': '{"message": "' + 'A' * 10000 + '"}'
        }
    ]
    
    for scenario in scenarios:
        print(f"\n📝 场景: {scenario['name']}")
        test_onebot_server(scenario['data'])


def main():
    """主测试函数"""
    print("🚀 控制字符处理测试")
    print(f"🕐 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n💡 此测试专门验证JSON中控制字符的处理能力")
    print("请确保OneBot服务器正在运行: python onebot_server.py\n")
    
    # 主要测试
    test_control_characters()
    
    # 编码测试
    test_encoding_issues()
    
    # 真实场景测试
    test_real_world_scenarios()
    
    print("\n" + "=" * 60)
    print("✅ 控制字符处理测试完成")
    print("=" * 60)
    print("📋 测试总结:")
    print("   🧹 自动清理有害控制字符")
    print("   📍 精确定位错误位置")
    print("   🔍 提供十六进制分析")
    print("   💡 给出修复建议")
    print("   🌐 处理多种编码格式")
    print("\n📝 查看详细日志: tail -f onebot.log")


if __name__ == "__main__":
    main()
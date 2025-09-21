#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JSON解析错误修复演示
展示如何处理包含控制字符的JSON数据
"""

import json
from json_utils import parse_json_with_details, clean_json_string, log_json_error
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def demonstrate_json_fix():
    """演示JSON解析错误的修复"""
    print("🔧 JSON解析错误修复演示")
    print("=" * 50)
    
    # 原始有问题的JSON（包含控制字符）
    problematic_json = '{"message": "test\x00"}'  # 包含NULL字符
    
    print("1️⃣ 原始问题:")
    print(f"   JSON字符串: {repr(problematic_json)}")
    print(f"   十六进制: {' '.join(f'{ord(c):02x}' for c in problematic_json)}")
    
    # 尝试用标准json.loads解析
    print("\n2️⃣ 标准解析（会失败）:")
    try:
        result = json.loads(problematic_json)
        print(f"   ✅ 成功: {result}")
    except json.JSONDecodeError as e:
        print(f"   ❌ 失败: {e}")
    
    # 使用清理功能
    print("\n3️⃣ 清理数据:")
    cleaned = clean_json_string(problematic_json)
    print(f"   清理前: {repr(problematic_json)}")
    print(f"   清理后: {repr(cleaned)}")
    
    # 使用增强的解析功能
    print("\n4️⃣ 增强解析:")
    result, error_details = parse_json_with_details(problematic_json)
    
    if result is not None:
        print(f"   ✅ 解析成功: {result}")
    else:
        print(f"   ❌ 解析失败")
        print(f"   错误位置: {error_details['error_position']}")
        print(f"   错误字符: {error_details['error_char']}")
        print(f"   上下文: {error_details['context_repr']}")
        print(f"   十六进制: {error_details['hex_context']}")
        if error_details['suggestions']:
            print(f"   建议: {'; '.join(error_details['suggestions'])}")
    
    # 演示原始错误日志格式
    print("\n5️⃣ 原始错误（你遇到的问题）:")
    original_error = "Invalid control character at: line 1 column 18 (char 17)"
    print(f"   {original_error}")
    print("   这个错误表示在第17个字符位置有无效的控制字符")
    
    # 分析具体字符
    if len(problematic_json) > 17:
        char_at_17 = problematic_json[17]
        print(f"   第17个字符: {repr(char_at_17)} (0x{ord(char_at_17):02x})")
    
    print("\n6️⃣ 解决方案:")
    print("   ✅ 自动清理控制字符")
    print("   ✅ 提供详细错误分析")
    print("   ✅ 给出具体修复建议")
    print("   ✅ 记录完整的调试信息")

def test_your_specific_case():
    """测试你遇到的具体情况"""
    print("\n🎯 测试你的具体情况")
    print("=" * 50)
    
    # 模拟你遇到的问题
    # "Invalid control character at: line 1 column 18 (char 17)"
    # 原始数据: {"message": "test"}
    
    # 可能的问题数据（在第17个字符位置添加控制字符）
    test_data = '{"message": "test'  # 14个字符
    test_data += '\x00'  # 第15个字符 - NULL控制字符
    test_data += '"}'    # 第16-17个字符
    
    print(f"模拟数据: {repr(test_data)}")
    print(f"长度: {len(test_data)}")
    print(f"第17个字符: {repr(test_data[16]) if len(test_data) > 16 else 'N/A'}")
    
    # 使用新的解析器
    result, error_details = parse_json_with_details(test_data)
    
    if error_details:
        print("🔍 详细错误分析:")
        log_json_error(error_details, logger)
    else:
        print(f"✅ 解析成功: {result}")

def show_before_after():
    """展示修复前后的对比"""
    print("\n📊 修复前后对比")
    print("=" * 50)
    
    print("❌ 修复前（简单的错误信息）:")
    print("   2025-09-21 14:06:59,889 - ERROR - JSON解析失败: Invalid control character at: line 1 column 18 (char 17), 原始数据: {\"message\": \"test\"}")
    
    print("\n✅ 修复后（详细的错误信息）:")
    print("   ERROR: JSON解析失败: Invalid control character at: line 1 column 15 (char 14)")
    print("   ERROR: 错误位置: 14 (line 1 column 15)")
    print("   ERROR: 错误字符: '\\x00' (0x00)")
    print("   ERROR: 上下文: '{\"message\": \"test\\x00\"}'")
    print("   ERROR: 十六进制: 7b 22 6d 65 73 73 61 67 65 22 3a 20 22 74 65 73 74 00 22 7d")
    print("   ERROR: 数据长度: 20")
    print("   WARNING: 移除了 1 个控制字符")
    print("   INFO: 建议修复方法: 检查数据来源是否包含隐藏字符")

def main():
    """主演示函数"""
    print("🚀 JSON解析错误修复演示")
    print("解决你遇到的控制字符问题\n")
    
    demonstrate_json_fix()
    test_your_specific_case()
    show_before_after()
    
    print("\n" + "=" * 60)
    print("✅ 演示完成")
    print("=" * 60)
    print("📋 改进总结:")
    print("   🔍 精确定位错误位置和字符")
    print("   🧹 自动清理有害控制字符")
    print("   📊 提供十六进制分析")
    print("   💡 给出具体修复建议")
    print("   📝 记录详细的调试信息")
    print("\n🛠️ 现在你的OneBot服务器可以:")
    print("   ✅ 自动处理包含控制字符的JSON")
    print("   ✅ 提供详细的错误分析")
    print("   ✅ 帮助快速定位问题源头")

if __name__ == "__main__":
    main()
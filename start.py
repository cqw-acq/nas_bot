#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速启动脚本
"""

import sys
import os
import subprocess

def check_dependencies():
    """检查依赖"""
    required_packages = [
        ('flask', 'flask'),
        ('requests', 'requests'), 
        ('yaml', 'pyyaml')  # 包名和import名不同
    ]
    missing_packages = []
    
    for import_name, package_name in required_packages:
        try:
            __import__(import_name)
        except ImportError:
            missing_packages.append(package_name)
    
    if missing_packages:
        print(f"❌ 缺少依赖包: {', '.join(missing_packages)}")
        print("请运行: pip install -r requirements.txt")
        return False
    
    print("✅ 所有依赖包已安装")
    return True

def check_config():
    """检查配置文件"""
    if not os.path.exists('config.yml'):
        print("❌ 配置文件 config.yml 不存在")
        return False
    
    print("✅ 配置文件存在")
    return True

def main():
    """主函数"""
    print("🚀 NAS Bot 启动检查")
    print("=" * 40)
    
    # 检查依赖
    if not check_dependencies():
        return
    
    # 检查配置
    if not check_config():
        return
    
    print("\n选择要启动的服务:")
    print("1. enhanced_chat_bot.py - 增强版聊天机器人 (推荐)")
    print("2. test_deepseek.py - 测试DeepSeek API连接")
    print("3. 退出")
    
    choice = input("\n请选择 (1-3): ").strip()
    
    if choice == "1":
        print("\n🚀 启动增强版聊天机器人...")
        try:
            subprocess.run([sys.executable, "enhanced_chat_bot.py"])
        except KeyboardInterrupt:
            print("\n👋 机器人已停止")
    elif choice == "2":
        print("\n🧪 测试DeepSeek API...")
        try:
            subprocess.run([sys.executable, "test_deepseek.py"])
        except Exception as e:
            print(f"❌ 测试失败: {e}")
    elif choice == "3":
        print("👋 再见！")
    else:
        print("❌ 无效选择")

if __name__ == "__main__":
    main()
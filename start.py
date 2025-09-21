#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速启动脚本
"""

import sys
import os

def main():
    """主函数"""
    print("🚀 NAS Bot 快速启动")
    print("=" * 40)
    print("1. enhanced_chat_bot.py - 增强版聊天机器人")
    print("2. flask_message_viewer.py - 消息查看器") 
    print("3. flask_json_capture.py - 请求捕获器")
    print("=" * 40)
    
    choice = input("请选择要启动的服务器 (1-3): ").strip()
    
    if choice == "1":
        print("启动增强版聊天机器人...")
        os.system("python enhanced_chat_bot.py")
    elif choice == "2":
        print("启动消息查看器...")
        os.system("python flask_message_viewer.py")
    elif choice == "3":
        print("启动请求捕获器...")
        os.system("python flask_json_capture.py")
    else:
        print("无效选择，启动默认服务器...")
        os.system("python enhanced_chat_bot.py")

if __name__ == "__main__":
    main()
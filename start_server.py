#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
服务器启动脚本
选择并启动不同类型的8080端口监听服务器
"""

import sys
import subprocess
import os
from datetime import datetime


def show_menu():
    """显示菜单"""
    print("=" * 60)
    print("🚀 8080端口消息监听服务器")
    print("=" * 60)
    print("请选择要启动的服务器类型:")
    print()
    print("1. HTTP服务器 (http_server.py)")
    print("   - 支持GET/POST请求")
    print("   - 适合REST API和Web服务")
    print("   - 测试: curl http://localhost:8080")
    print()
    print("2. TCP服务器 (tcp_server.py)")
    print("   - 支持多客户端连接")
    print("   - 适合自定义协议")
    print("   - 测试: telnet localhost 8080")
    print()
    print("3. WebSocket服务器 (websocket_server.py)")
    print("   - 支持实时双向通信")
    print("   - 适合实时应用")
    print("   - 需要安装: pip install websockets")
    print()
    print("4. 测试服务器 (test_servers.py)")
    print("   - 测试已启动的服务器")
    print()
    print("5. 安装依赖")
    print("   - 安装所需的Python包")
    print()
    print("0. 退出")
    print("=" * 60)


def install_dependencies():
    """安装依赖"""
    print("正在安装依赖...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True)
        print("✅ 依赖安装成功")
    except subprocess.CalledProcessError:
        print("❌ 依赖安装失败")
        print("你可以手动安装: pip install -r requirements.txt")
    except FileNotFoundError:
        print("❌ requirements.txt文件不存在")


def start_server(script_name, server_name):
    """启动服务器"""
    if not os.path.exists(script_name):
        print(f"❌ {script_name} 文件不存在")
        return
    
    print(f"正在启动 {server_name}...")
    print(f"时间: {datetime.now()}")
    print(f"脚本: {script_name}")
    print("-" * 40)
    print("按 Ctrl+C 停止服务器")
    print("-" * 40)
    
    try:
        subprocess.run([sys.executable, script_name], check=True)
    except KeyboardInterrupt:
        print(f"\n{server_name} 已停止")
    except subprocess.CalledProcessError as e:
        print(f"❌ {server_name} 启动失败: {e}")
    except FileNotFoundError:
        print("❌ Python解释器未找到")


def run_tests():
    """运行测试"""
    if not os.path.exists("test_servers.py"):
        print("❌ test_servers.py 文件不存在")
        return
    
    print("正在运行服务器测试...")
    try:
        subprocess.run([sys.executable, "test_servers.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ 测试失败: {e}")
    except KeyboardInterrupt:
        print("\n测试被中断")


def main():
    """主函数"""
    while True:
        show_menu()
        
        try:
            choice = input("请输入选择 (0-5): ").strip()
            
            if choice == '0':
                print("👋 再见！")
                break
            elif choice == '1':
                start_server("http_server.py", "HTTP服务器")
            elif choice == '2':
                start_server("tcp_server.py", "TCP服务器")
            elif choice == '3':
                start_server("websocket_server.py", "WebSocket服务器")
            elif choice == '4':
                run_tests()
            elif choice == '5':
                install_dependencies()
            else:
                print("❌ 无效选择，请输入0-5之间的数字")
            
            if choice != '0':
                input("\n按回车键继续...")
                print("\n" * 2)  # 清空一些行
                
        except KeyboardInterrupt:
            print("\n\n👋 再见！")
            break
        except Exception as e:
            print(f"❌ 发生错误: {e}")
            input("按回车键继续...")


if __name__ == "__main__":
    main()
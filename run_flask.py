#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flask启动脚本
根据参数启动不同的Flask服务器
"""

import sys
import os

def print_help():
    """显示帮助信息"""
    print("🚀 Flask OneBot服务器启动器")
    print("=" * 50)
    print("用法: python run_flask.py [server_type]")
    print()
    print("可用的服务器类型:")
    print("  server    - 完整的OneBot 11服务器 (默认)")
    print("  handler   - 简化的消息处理器")
    print("  viewer    - 消息查看器 (只显示不回复)")
    print("  capture   - 原始请求捕获器")
    print()
    print("示例:")
    print("  python run_flask.py server   # 启动完整服务器")
    print("  python run_flask.py handler  # 启动消息处理器")
    print("  python run_flask.py viewer   # 启动消息查看器")
    print("  python run_flask.py capture  # 启动请求捕获器")
    print()
    print("配置文件:")
    print("  onebot_config.json - 主服务器配置")
    print("  requirements.txt   - 依赖列表")
    print("=" * 50)


def run_server(server_type):
    """运行指定类型的服务器"""
    
    server_files = {
        'server': 'flask_onebot_server.py',
        'handler': 'flask_message_handler.py',
        'viewer': 'flask_message_viewer.py',
        'capture': 'flask_json_capture.py'
    }
    
    if server_type not in server_files:
        print(f"❌ 未知的服务器类型: {server_type}")
        print("使用 'python run_flask.py help' 查看帮助")
        return
    
    server_file = server_files[server_type]
    
    # 检查文件是否存在
    if not os.path.exists(server_file):
        print(f"❌ 服务器文件不存在: {server_file}")
        return
    
    print(f"🚀 启动 {server_type} 服务器...")
    print(f"📁 文件: {server_file}")
    print("=" * 30)
    
    # 导入并运行服务器
    try:
        if server_type == 'server':
            from flask_onebot_server import main
        elif server_type == 'handler':
            from flask_message_handler import main
        elif server_type == 'viewer':
            from flask_message_viewer import main
        elif server_type == 'capture':
            from flask_json_capture import main
        
        main()
        
    except KeyboardInterrupt:
        print("\n👋 服务器已停止")
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        print("请确保已安装所需依赖: pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ 启动失败: {e}")


def main():
    """主函数"""
    
    # 获取命令行参数
    if len(sys.argv) < 2:
        server_type = 'server'  # 默认启动完整服务器
    else:
        server_type = sys.argv[1].lower()
    
    # 处理帮助参数
    if server_type in ['help', '-h', '--help']:
        print_help()
        return
    
    # 启动服务器
    run_server(server_type)


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTTP服务器监听8080端口
接收和处理HTTP请求消息
"""

import http.server
import socketserver
import json
import urllib.parse
from datetime import datetime


class MessageHandler(http.server.BaseHTTPRequestHandler):
    """处理HTTP请求的处理器"""
    
    def do_GET(self):
        """处理GET请求"""
        print(f"[{datetime.now()}] 收到GET请求: {self.path}")
        
        # 解析URL参数
        parsed_path = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_path.query)
        
        # 响应头
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        # 响应内容
        response_data = {
            'status': 'success',
            'message': '收到GET请求',
            'path': parsed_path.path,
            'params': query_params,
            'timestamp': datetime.now().isoformat()
        }
        
        self.wfile.write(json.dumps(response_data, ensure_ascii=False).encode('utf-8'))
    
    def do_POST(self):
        """处理POST请求"""
        print(f"[{datetime.now()}] 收到POST请求: {self.path}")
        
        # 获取请求内容长度
        content_length = int(self.headers.get('Content-Length', 0))
        
        # 读取请求体
        post_data = self.rfile.read(content_length)
        
        try:
            # 尝试解析JSON数据
            if self.headers.get('Content-Type') == 'application/json':
                message_data = json.loads(post_data.decode('utf-8'))
                print(f"收到JSON消息: {message_data}")
            else:
                message_data = post_data.decode('utf-8')
                print(f"收到文本消息: {message_data}")
        except Exception as e:
            message_data = f"解析消息失败: {str(e)}"
            print(message_data)
        
        # 响应头
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        # 响应内容
        response_data = {
            'status': 'success',
            'message': '消息已接收',
            'received_data': message_data,
            'timestamp': datetime.now().isoformat()
        }
        
        self.wfile.write(json.dumps(response_data, ensure_ascii=False).encode('utf-8'))
    
    def do_OPTIONS(self):
        """处理OPTIONS请求(CORS预检请求)"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def log_message(self, format, *args):
        """自定义日志格式"""
        print(f"[{datetime.now()}] {format % args}")


def start_http_server(port=8080):
    """启动HTTP服务器"""
    try:
        with socketserver.TCPServer(("", port), MessageHandler) as httpd:
            print(f"HTTP服务器启动成功，监听端口 {port}")
            print(f"访问 http://localhost:{port} 来测试服务器")
            print("按 Ctrl+C 停止服务器")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n服务器已停止")
    except Exception as e:
        print(f"服务器启动失败: {e}")


if __name__ == "__main__":
    start_http_server(8080)
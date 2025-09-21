#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NapCat原始请求捕获器
记录NapCat发送的原始HTTP请求，一字不差
"""

import http.server
import socketserver
import time
import os
from datetime import datetime


class RawRequestCapture(http.server.BaseHTTPRequestHandler):
    """原始请求捕获器"""
    
    def log_raw_request(self, method):
        """记录原始请求的所有细节"""
        
        # 创建日志文件名（按时间）
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')[:-3]
        filename = f"napcat_raw_{timestamp}.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                # 记录时间戳
                f.write(f"=== NapCat原始请求捕获 ===\n")
                f.write(f"捕获时间: {datetime.now().isoformat()}\n")
                f.write(f"时间戳: {time.time()}\n")
                f.write(f"请求方法: {method}\n\n")
                
                # 记录请求行
                f.write(f"=== 请求行 ===\n")
                f.write(f"{method} {self.path} {self.request_version}\n\n")
                
                # 记录所有请求头
                f.write(f"=== 请求头 ===\n")
                for header, value in self.headers.items():
                    f.write(f"{header}: {value}\n")
                f.write("\n")
                
                # 记录客户端信息
                f.write(f"=== 客户端信息 ===\n")
                f.write(f"客户端地址: {self.client_address[0]}\n")
                f.write(f"客户端端口: {self.client_address[1]}\n")
                f.write(f"服务器地址: {self.server.server_address[0]}\n")
                f.write(f"服务器端口: {self.server.server_address[1]}\n\n")
                
                # 如果是POST/PUT，记录请求体
                if method in ['POST', 'PUT', 'PATCH']:
                    content_length = int(self.headers.get('Content-Length', 0))
                    if content_length > 0:
                        f.write(f"=== 请求体 ===\n")
                        f.write(f"Content-Length: {content_length}\n")
                        
                        # 读取原始字节数据
                        raw_data = self.rfile.read(content_length)
                        
                        # 记录原始字节（十六进制）
                        f.write(f"\n--- 原始字节数据 (HEX) ---\n")
                        hex_data = raw_data.hex()
                        # 每16字节一行，格式化显示
                        for i in range(0, len(hex_data), 32):
                            f.write(f"{i//2:08x}: {hex_data[i:i+32]}\n")
                        
                        # 记录UTF-8解码尝试
                        f.write(f"\n--- UTF-8解码尝试 ---\n")
                        try:
                            utf8_text = raw_data.decode('utf-8')
                            f.write(utf8_text)
                        except UnicodeDecodeError as e:
                            f.write(f"UTF-8解码失败: {e}\n")
                            # 尝试忽略错误的解码
                            utf8_text = raw_data.decode('utf-8', errors='replace')
                            f.write(f"强制解码结果:\n{utf8_text}")
                        
                        # 记录Latin-1解码（保持原始字节）
                        f.write(f"\n--- Latin-1解码 (保持原始字节) ---\n")
                        latin1_text = raw_data.decode('latin-1')
                        f.write(latin1_text)
                        
                        # 显示每个字符的详细信息
                        f.write(f"\n--- 字符详细分析 ---\n")
                        for i, byte_val in enumerate(raw_data):
                            char = chr(byte_val) if 32 <= byte_val <= 126 else f'\\x{byte_val:02x}'
                            f.write(f"位置{i:3d}: 字节{byte_val:3d} (0x{byte_val:02x}) = '{char}'\n")
                    else:
                        f.write(f"=== 请求体 ===\n空请求体\n")
                
                f.write(f"\n=== 原始请求结束 ===\n")
            
            print(f"📝 原始请求已保存到: {filename}")
            return filename
            
        except Exception as e:
            print(f"❌ 保存请求失败: {e}")
            return None
    
    def do_GET(self):
        """处理GET请求"""
        print(f"\n📥 收到GET请求: {self.path}")
        filename = self.log_raw_request('GET')
        
        # 返回响应
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        
        response = f'{{"status": "ok", "method": "GET", "captured_file": "{filename}"}}'
        self.wfile.write(response.encode('utf-8'))
    
    def do_POST(self):
        """处理POST请求"""
        print(f"\n📥 收到POST请求: {self.path}")
        filename = self.log_raw_request('POST')
        
        # 返回响应
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        
        response = f'{{"status": "ok", "method": "POST", "captured_file": "{filename}"}}'
        self.wfile.write(response.encode('utf-8'))
    
    def do_PUT(self):
        """处理PUT请求"""
        print(f"\n📥 收到PUT请求: {self.path}")
        filename = self.log_raw_request('PUT')
        
        # 返回响应
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        
        response = f'{{"status": "ok", "method": "PUT", "captured_file": "{filename}"}}'
        self.wfile.write(response.encode('utf-8'))
    
    def log_message(self, format, *args):
        """自定义日志输出"""
        timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
        print(f"[{timestamp}] {format % args}")


def main():
    """启动原始请求捕获服务器"""
    host = '0.0.0.0'
    port = 8080
    
    print("🔍 NapCat原始请求捕获器")
    print("=" * 50)
    print("📋 功能:")
    print("  ✅ 捕获完整的HTTP请求")
    print("  ✅ 记录所有请求头")
    print("  ✅ 保存原始字节数据")
    print("  ✅ 多种编码解码尝试")
    print("  ✅ 字符级别详细分析")
    print("=" * 50)
    
    try:
        with socketserver.TCPServer((host, port), RawRequestCapture) as httpd:
            print(f"🚀 服务器启动成功")
            print(f"📡 监听地址: http://{host}:{port}")
            print(f"📁 日志文件: napcat_raw_[timestamp].txt")
            print("🔔 等待NapCat发送请求...")
            print("按 Ctrl+C 停止服务器")
            print("=" * 50)
            
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n👋 服务器已停止")
    except Exception as e:
        print(f"❌ 服务器启动失败: {e}")


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NapCat原始请求捕获器
保存所有请求数据为JSON文件，一字不差
"""

import json
import time
import os
from datetime import datetime
import http.server
import socketserver


class RawRequestCapture(http.server.BaseHTTPRequestHandler):
    """原始请求捕获器"""
    
    def do_POST(self):
        """捕获POST请求"""
        self.capture_request('POST')
    
    def do_GET(self):
        """捕获GET请求"""
        self.capture_request('GET')
    
    def do_PUT(self):
        """捕获PUT请求"""
        self.capture_request('PUT')
    
    def do_DELETE(self):
        """捕获DELETE请求"""
        self.capture_request('DELETE')
    
    def capture_request(self, method):
        """捕获并保存请求数据"""
        try:
            # 获取当前时间戳
            timestamp = datetime.now()
            timestamp_str = timestamp.strftime('%Y%m%d_%H%M%S_%f')[:-3]  # 精确到毫秒
            
            # 读取请求体
            content_length = int(self.headers.get('Content-Length', 0))
            body_data = b''
            if content_length > 0:
                body_data = self.rfile.read(content_length)
            
            # 构建完整的请求数据
            request_data = {
                'timestamp': timestamp.isoformat(),
                'method': method,
                'path': self.path,
                'headers': dict(self.headers),
                'client_address': f"{self.client_address[0]}:{self.client_address[1]}",
                'server_version': self.server_version,
                'protocol_version': self.protocol_version,
                'body_raw_bytes': body_data.hex() if body_data else '',
                'body_size': len(body_data),
                'body_text': '',
                'body_json': None,
                'parsing_info': {
                    'can_decode_utf8': False,
                    'is_valid_json': False,
                    'decode_error': None,
                    'json_error': None
                }
            }
            
            # 尝试解码为文本
            if body_data:
                try:
                    body_text = body_data.decode('utf-8')
                    request_data['body_text'] = body_text
                    request_data['parsing_info']['can_decode_utf8'] = True
                    
                    # 尝试解析为JSON
                    try:
                        body_json = json.loads(body_text)
                        request_data['body_json'] = body_json
                        request_data['parsing_info']['is_valid_json'] = True
                    except json.JSONDecodeError as e:
                        request_data['parsing_info']['json_error'] = str(e)
                        
                except UnicodeDecodeError as e:
                    request_data['parsing_info']['decode_error'] = str(e)
                    # 尝试其他编码
                    for encoding in ['gbk', 'latin1', 'ascii']:
                        try:
                            body_text = body_data.decode(encoding)
                            request_data['body_text'] = f"[decoded as {encoding}] {body_text}"
                            break
                        except:
                            continue
            
            # 保存到JSON文件
            filename = f"napcat_request_{timestamp_str}.json"
            filepath = os.path.join('napcat_captures', filename)
            
            # 确保目录存在
            os.makedirs('napcat_captures', exist_ok=True)
            
            # 保存JSON文件
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(request_data, f, ensure_ascii=False, indent=2)
            
            # 控制台输出
            print(f"📥 {timestamp.strftime('%H:%M:%S')} | {method} {self.path}")
            print(f"💾 保存到: {filename}")
            if request_data['parsing_info']['is_valid_json']:
                print(f"✅ 有效JSON数据")
            elif request_data['parsing_info']['can_decode_utf8']:
                print(f"📝 文本数据")
            else:
                print(f"🔢 二进制数据 ({len(body_data)} bytes)")
            print("-" * 50)
            
            # 发送响应
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            response = {'status': 'captured', 'timestamp': timestamp.isoformat()}
            self.wfile.write(json.dumps(response).encode('utf-8'))
            
        except Exception as e:
            print(f"❌ 捕获请求时发生错误: {e}")
            self.send_response(500)
            self.end_headers()
    
    def log_message(self, format, *args):
        """禁用默认日志"""
        pass


def main():
    """启动捕获器"""
    port = 8080
    
    print("🎯 NapCat原始请求捕获器")
    print("=" * 50)
    print(f"📡 监听端口: {port}")
    print(f"💾 保存目录: ./napcat_captures/")
    print(f"📋 文件格式: JSON")
    print("🔄 支持所有HTTP方法")
    print("=" * 50)
    
    try:
        with socketserver.TCPServer(("0.0.0.0", port), RawRequestCapture) as httpd:
            print(f"✅ 服务器启动成功!")
            print(f"🌐 URL: http://localhost:{port}")
            print("🔔 等待NapCat请求...")
            print("按 Ctrl+C 停止捕获")
            print("=" * 50)
            
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n👋 捕获器已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")


if __name__ == "__main__":
    main()
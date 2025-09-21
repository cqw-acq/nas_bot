#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NapCat请求收集器
将所有请求保存到一个JSON文件中
"""

import json
import time
import threading
from datetime import datetime
import http.server
import socketserver


class RequestCollector(http.server.BaseHTTPRequestHandler):
    """请求收集器"""
    
    # 全局请求列表
    requests_data = []
    lock = threading.Lock()
    
    def do_POST(self):
        self.collect_request('POST')
    
    def do_GET(self):
        self.collect_request('GET')
    
    def do_PUT(self):
        self.collect_request('PUT')
    
    def do_DELETE(self):
        self.collect_request('DELETE')
    
    def collect_request(self, method):
        """收集请求数据"""
        try:
            timestamp = datetime.now()
            
            # 读取请求体
            content_length = int(self.headers.get('Content-Length', 0))
            body_data = b''
            if content_length > 0:
                body_data = self.rfile.read(content_length)
            
            # 构建请求数据
            request_info = {
                'id': len(self.requests_data) + 1,
                'timestamp': timestamp.isoformat(),
                'method': method,
                'path': self.path,
                'headers': dict(self.headers),
                'client_ip': self.client_address[0],
                'client_port': self.client_address[1],
                'body_size': len(body_data),
                'body_hex': body_data.hex() if body_data else '',
                'body_text': None,
                'body_json': None,
                'errors': []
            }
            
            # 尝试解码文本
            if body_data:
                try:
                    body_text = body_data.decode('utf-8')
                    request_info['body_text'] = body_text
                    
                    # 尝试解析JSON
                    try:
                        body_json = json.loads(body_text)
                        request_info['body_json'] = body_json
                    except json.JSONDecodeError as e:
                        request_info['errors'].append(f"JSON解析失败: {e}")
                        
                except UnicodeDecodeError as e:
                    request_info['errors'].append(f"UTF-8解码失败: {e}")
            
            # 线程安全地添加到列表
            with self.lock:
                self.requests_data.append(request_info)
                
                # 每收集到一个请求就保存一次
                self.save_all_requests()
            
            # 控制台输出
            print(f"📥 #{request_info['id']} | {method} {self.path} | {len(body_data)} bytes | {timestamp.strftime('%H:%M:%S')}")
            
            # 发送响应
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            response = {
                'status': 'collected',
                'request_id': request_info['id'],
                'timestamp': timestamp.isoformat()
            }
            self.wfile.write(json.dumps(response).encode('utf-8'))
            
        except Exception as e:
            print(f"❌ 收集请求失败: {e}")
            self.send_response(500)
            self.end_headers()
    
    @classmethod
    def save_all_requests(cls):
        """保存所有请求到JSON文件"""
        try:
            output_data = {
                'capture_info': {
                    'total_requests': len(cls.requests_data),
                    'last_updated': datetime.now().isoformat(),
                    'capture_started': cls.requests_data[0]['timestamp'] if cls.requests_data else None
                },
                'requests': cls.requests_data
            }
            
            with open('napcat_all_requests.json', 'w', encoding='utf-8') as f:
                json.dump(output_data, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f"❌ 保存文件失败: {e}")
    
    def log_message(self, format, *args):
        """禁用默认日志"""
        pass


def main():
    """启动收集器"""
    port = 8080
    
    print("📦 NapCat请求收集器")
    print("=" * 50)
    print(f"📡 监听端口: {port}")
    print(f"💾 输出文件: napcat_all_requests.json")
    print("🔄 实时保存所有请求")
    print("=" * 50)
    
    try:
        with socketserver.TCPServer(("0.0.0.0", port), RequestCollector) as httpd:
            print(f"✅ 收集器启动成功!")
            print(f"🌐 配置NapCat推送到: http://localhost:{port}")
            print("🔔 等待请求...")
            print("按 Ctrl+C 停止并查看JSON文件")
            print("=" * 50)
            
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print(f"\n📋 收集完成! 共收集 {len(RequestCollector.requests_data)} 个请求")
        print("💾 所有数据已保存到: napcat_all_requests.json")
        
        # 最终保存一次
        if RequestCollector.requests_data:
            RequestCollector.save_all_requests()
            print("✅ 文件保存完成")
        
    except Exception as e:
        print(f"❌ 启动失败: {e}")


if __name__ == "__main__":
    main()
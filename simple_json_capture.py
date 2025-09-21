#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最简单的NapCat JSON捕获器
直接输出和保存原始JSON数据
"""

import json
import http.server
import socketserver
from datetime import datetime


class SimpleJSONCapture(http.server.BaseHTTPRequestHandler):
    """简单JSON捕获器"""
    
    def do_POST(self):
        """捕获POST请求"""
        try:
            # 读取请求体
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0:
                self.send_response(400)
                self.end_headers()
                return
            
            raw_data = self.rfile.read(content_length)
            
            # 保存原始数据到文件
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')[:-3]
            
            # 保存原始字节数据
            with open(f'raw_{timestamp}.bin', 'wb') as f:
                f.write(raw_data)
            
            # 尝试解码并保存JSON
            try:
                text_data = raw_data.decode('utf-8')
                
                # 保存原始文本
                with open(f'raw_{timestamp}.txt', 'w', encoding='utf-8') as f:
                    f.write(text_data)
                
                # 尝试解析和美化JSON
                try:
                    json_data = json.loads(text_data)
                    
                    # 保存美化的JSON
                    with open(f'parsed_{timestamp}.json', 'w', encoding='utf-8') as f:
                        json.dump(json_data, f, ensure_ascii=False, indent=2)
                    
                    print(f"✅ JSON数据已保存: parsed_{timestamp}.json")
                    print("=" * 60)
                    print(json.dumps(json_data, ensure_ascii=False, indent=2))
                    print("=" * 60)
                    
                except json.JSONDecodeError as e:
                    print(f"❌ JSON解析失败: {e}")
                    print(f"原始文本: {text_data}")
                    
            except UnicodeDecodeError as e:
                print(f"❌ UTF-8解码失败: {e}")
                print(f"原始字节: {raw_data.hex()}")
            
            # 发送成功响应
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status": "ok"}')
            
        except Exception as e:
            print(f"❌ 处理请求失败: {e}")
            self.send_response(500)
            self.end_headers()
    
    def log_message(self, format, *args):
        """禁用默认日志"""
        pass


def main():
    """启动简单捕获器"""
    port = 8080
    
    print("📋 NapCat简单JSON捕获器")
    print("=" * 40)
    print(f"📡 端口: {port}")
    print("💾 保存格式:")
    print("  - raw_*.bin  (原始二进制)")
    print("  - raw_*.txt  (原始文本)")
    print("  - parsed_*.json (解析后JSON)")
    print("=" * 40)
    
    try:
        with socketserver.TCPServer(("0.0.0.0", port), SimpleJSONCapture) as httpd:
            print("✅ 服务器启动!")
            print("🔔 等待NapCat推送...")
            print("=" * 40)
            
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n👋 停止捕获")
    except Exception as e:
        print(f"❌ 错误: {e}")


if __name__ == "__main__":
    main()
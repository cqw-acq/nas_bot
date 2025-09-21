#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NapCat原始请求完整捕获器
保存一字不差的原始HTTP请求
"""

import socket
import threading
import time
from datetime import datetime


class RawHTTPCapture:
    """原始HTTP请求捕获器"""
    
    def __init__(self, host='0.0.0.0', port=8080):
        self.host = host
        self.port = port
        self.running = False
    
    def start_server(self):
        """启动原始捕获服务器"""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.sock.listen(5)
        self.running = True
        
        print("🔍 NapCat原始HTTP请求捕获器")
        print("=" * 50)
        print(f"📡 监听地址: {self.host}:{self.port}")
        print("📝 将保存完整的原始HTTP请求")
        print("🔔 等待连接...")
        print("按 Ctrl+C 停止")
        print("=" * 50)
        
        try:
            while self.running:
                try:
                    client_sock, client_addr = self.sock.accept()
                    print(f"\n📞 新连接: {client_addr[0]}:{client_addr[1]}")
                    
                    # 为每个连接创建处理线程
                    thread = threading.Thread(
                        target=self.handle_client,
                        args=(client_sock, client_addr)
                    )
                    thread.daemon = True
                    thread.start()
                    
                except socket.error:
                    if self.running:
                        print("❌ 接受连接时出错")
                    break
                    
        except KeyboardInterrupt:
            print("\n👋 正在停止服务器...")
        finally:
            self.stop_server()
    
    def handle_client(self, client_sock, client_addr):
        """处理客户端连接"""
        try:
            # 设置接收超时
            client_sock.settimeout(30)
            
            # 接收所有数据
            all_data = b''
            
            while True:
                try:
                    chunk = client_sock.recv(4096)
                    if not chunk:
                        break
                    all_data += chunk
                    
                    # 检查是否接收完整（简单检查）
                    if b'\r\n\r\n' in all_data:
                        # 检查是否有Content-Length
                        headers_part = all_data.split(b'\r\n\r\n')[0]
                        content_length = 0
                        
                        for line in headers_part.split(b'\r\n'):
                            if line.lower().startswith(b'content-length:'):
                                content_length = int(line.split(b':')[1].strip())
                                break
                        
                        if content_length > 0:
                            headers_end = all_data.find(b'\r\n\r\n') + 4
                            body_received = len(all_data) - headers_end
                            
                            if body_received >= content_length:
                                break
                        else:
                            # 没有请求体，接收完成
                            break
                
                except socket.timeout:
                    print("⏰ 接收超时，数据可能不完整")
                    break
                except socket.error:
                    break
            
            if all_data:
                self.save_raw_request(all_data, client_addr)
                self.send_response(client_sock)
            
        except Exception as e:
            print(f"❌ 处理客户端 {client_addr} 时出错: {e}")
        finally:
            client_sock.close()
    
    def save_raw_request(self, raw_data, client_addr):
        """保存原始请求数据"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')[:-3]
        filename = f"napcat_raw_{timestamp}.txt"
        
        try:
            with open(filename, 'wb') as f:
                # 写入元信息（UTF-8编码）
                meta_info = f"""=== NapCat原始HTTP请求 ===
捕获时间: {datetime.now().isoformat()}
客户端地址: {client_addr[0]}:{client_addr[1]}
数据长度: {len(raw_data)} 字节
原始数据开始标记: >>>RAW_DATA_START<<<

""".encode('utf-8')
                f.write(meta_info)
                
                # 写入完全原始的HTTP数据
                f.write(raw_data)
                
                # 写入结束标记
                end_marker = f"""

>>>RAW_DATA_END<<<
=== 请求结束 ===
""".encode('utf-8')
                f.write(end_marker)
            
            print(f"💾 原始请求已保存: {filename}")
            print(f"📊 数据大小: {len(raw_data)} 字节")
            
            # 尝试显示请求的基本信息
            try:
                request_str = raw_data.decode('utf-8', errors='replace')
                lines = request_str.split('\n')
                if lines:
                    print(f"📝 请求行: {lines[0].strip()}")
            except:
                print("📝 请求包含二进制数据")
            
        except Exception as e:
            print(f"❌ 保存失败: {e}")
    
    def send_response(self, client_sock):
        """发送HTTP响应"""
        response = b"""HTTP/1.1 200 OK\r
Content-Type: application/json\r
Content-Length: 25\r
Connection: close\r
\r
{"status": "captured"}"""
        
        try:
            client_sock.send(response)
        except:
            pass  # 忽略发送错误
    
    def stop_server(self):
        """停止服务器"""
        self.running = False
        if hasattr(self, 'sock'):
            try:
                self.sock.close()
            except:
                pass
        print("🛑 服务器已停止")


def main():
    """主函数"""
    capture = RawHTTPCapture()
    capture.start_server()


if __name__ == "__main__":
    main()
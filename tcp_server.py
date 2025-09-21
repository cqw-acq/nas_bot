#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TCP服务器监听8080端口
接收和处理TCP连接和消息
"""

import socket
import threading
import json
from datetime import datetime


class TCPMessageServer:
    """TCP消息服务器"""
    
    def __init__(self, host='localhost', port=8080):
        self.host = host
        self.port = port
        self.server_socket = None
        self.running = False
        self.clients = []
    
    def handle_client(self, client_socket, client_address):
        """处理客户端连接"""
        print(f"[{datetime.now()}] 新客户端连接: {client_address}")
        self.clients.append(client_socket)
        
        try:
            while self.running:
                # 接收数据
                data = client_socket.recv(1024)
                if not data:
                    break
                
                message = data.decode('utf-8')
                print(f"[{datetime.now()}] 收到来自 {client_address} 的消息: {message}")
                
                # 尝试解析JSON消息
                try:
                    json_message = json.loads(message)
                    response = {
                        'status': 'success',
                        'message': '消息已接收',
                        'received_data': json_message,
                        'timestamp': datetime.now().isoformat()
                    }
                except json.JSONDecodeError as e:
                    error_msg = f"JSON解析失败: {e}, 原始消息: {message}"
                    print(f"[{datetime.now()}] {error_msg}")
                    response = {
                        'status': 'json_parse_error',
                        'error': 'JSON解析失败',
                        'details': str(e),
                        'message': '文本消息已接收',
                        'received_data': message,
                        'timestamp': datetime.now().isoformat()
                    }
                
                # 发送响应
                response_str = json.dumps(response, ensure_ascii=False)
                client_socket.send(response_str.encode('utf-8'))
                
        except Exception as e:
            print(f"[{datetime.now()}] 处理客户端 {client_address} 时发生错误: {e}")
        finally:
            if client_socket in self.clients:
                self.clients.remove(client_socket)
            client_socket.close()
            print(f"[{datetime.now()}] 客户端 {client_address} 断开连接")
    
    def start_server(self):
        """启动TCP服务器"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self.running = True
            
            print(f"TCP服务器启动成功，监听 {self.host}:{self.port}")
            print("等待客户端连接...")
            print("按 Ctrl+C 停止服务器")
            
            while self.running:
                try:
                    client_socket, client_address = self.server_socket.accept()
                    # 为每个客户端创建一个线程
                    client_thread = threading.Thread(
                        target=self.handle_client,
                        args=(client_socket, client_address)
                    )
                    client_thread.daemon = True
                    client_thread.start()
                except socket.error:
                    if self.running:
                        print("服务器套接字错误")
                    break
                    
        except KeyboardInterrupt:
            print("\n正在停止服务器...")
        except Exception as e:
            print(f"服务器启动失败: {e}")
        finally:
            self.stop_server()
    
    def stop_server(self):
        """停止TCP服务器"""
        self.running = False
        
        # 关闭所有客户端连接
        for client in self.clients:
            try:
                client.close()
            except:
                pass
        self.clients.clear()
        
        # 关闭服务器套接字
        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass
        
        print("TCP服务器已停止")


def test_tcp_client():
    """测试TCP客户端"""
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', 8080))
        
        # 发送测试消息
        test_messages = [
            "Hello TCP Server!",
            '{"type": "test", "message": "JSON消息测试", "timestamp": "' + datetime.now().isoformat() + '"}',
            "这是中文消息测试"
        ]
        
        for message in test_messages:
            print(f"发送消息: {message}")
            client_socket.send(message.encode('utf-8'))
            
            # 接收响应
            response = client_socket.recv(1024).decode('utf-8')
            print(f"收到响应: {response}")
            print("-" * 50)
        
        client_socket.close()
        
    except Exception as e:
        print(f"客户端测试失败: {e}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "client":
        # 运行测试客户端
        test_tcp_client()
    else:
        # 运行服务器
        server = TCPMessageServer(port=8080)
        server.start_server()
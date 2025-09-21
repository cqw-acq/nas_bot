#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NapCat超详细请求分析器
提供最详细的原始请求分析
"""

import http.server
import socketserver
import time
import json
import hashlib
from datetime import datetime
from urllib.parse import parse_qs, unquote


class UltraDetailedCapture(http.server.BaseHTTPRequestHandler):
    """超详细请求捕获器"""
    
    def capture_request(self, method):
        """超详细捕获请求"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')[:-3]
        
        # 创建详细分析文件
        analysis_file = f"napcat_analysis_{timestamp}.txt"
        raw_file = f"napcat_raw_{timestamp}.bin"
        json_file = f"napcat_data_{timestamp}.json"
        
        request_data = {
            'capture_time': datetime.now().isoformat(),
            'timestamp': time.time(),
            'method': method,
            'path': self.path,
            'version': self.request_version,
            'client_address': self.client_address,
            'server_address': self.server.server_address,
            'headers': dict(self.headers),
            'raw_data': None,
            'analysis': {}
        }
        
        # 读取请求体（如果有）
        raw_body = b''
        if method in ['POST', 'PUT', 'PATCH']:
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                raw_body = self.rfile.read(content_length)
                
                # 保存原始二进制数据
                with open(raw_file, 'wb') as f:
                    f.write(raw_body)
        
        # 分析数据
        self.analyze_data(raw_body, request_data, analysis_file)
        
        # 保存JSON格式的请求数据
        try:
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(request_data, f, indent=2, ensure_ascii=False, default=str)
        except Exception as e:
            print(f"保存JSON失败: {e}")
        
        print(f"📋 详细分析: {analysis_file}")
        print(f"💾 原始数据: {raw_file}")
        print(f"📊 JSON数据: {json_file}")
        
        return analysis_file
    
    def analyze_data(self, raw_body, request_data, analysis_file):
        """详细分析数据"""
        try:
            with open(analysis_file, 'w', encoding='utf-8') as f:
                self.write_header(f, request_data)
                self.write_request_line(f, request_data)
                self.write_headers_analysis(f, request_data)
                self.write_body_analysis(f, raw_body, request_data)
                self.write_security_analysis(f, request_data)
                self.write_recommendations(f, request_data)
                
        except Exception as e:
            print(f"分析失败: {e}")
    
    def write_header(self, f, request_data):
        """写入文件头"""
        f.write("🔍 NapCat超详细请求分析报告\n")
        f.write("=" * 80 + "\n")
        f.write(f"分析时间: {request_data['capture_time']}\n")
        f.write(f"Unix时间戳: {request_data['timestamp']}\n")
        f.write(f"请求ID: {hashlib.md5(str(request_data['timestamp']).encode()).hexdigest()[:8]}\n")
        f.write("=" * 80 + "\n\n")
    
    def write_request_line(self, f, request_data):
        """分析请求行"""
        f.write("📝 请求行分析\n")
        f.write("-" * 40 + "\n")
        f.write(f"方法: {request_data['method']}\n")
        f.write(f"路径: {request_data['path']}\n")
        f.write(f"协议版本: {request_data['version']}\n")
        
        # 分析路径
        if '?' in request_data['path']:
            path, query = request_data['path'].split('?', 1)
            f.write(f"基础路径: {path}\n")
            f.write(f"查询字符串: {query}\n")
            
            # 解析查询参数
            try:
                params = parse_qs(query)
                f.write("查询参数:\n")
                for key, values in params.items():
                    for value in values:
                        f.write(f"  {key} = {value}\n")
            except Exception as e:
                f.write(f"查询参数解析失败: {e}\n")
        
        f.write("\n")
    
    def write_headers_analysis(self, f, request_data):
        """分析请求头"""
        f.write("📋 请求头分析\n")
        f.write("-" * 40 + "\n")
        
        headers = request_data['headers']
        
        # 逐个分析重要头部
        important_headers = [
            'Host', 'User-Agent', 'Content-Type', 'Content-Length',
            'Authorization', 'X-Signature', 'Accept', 'Accept-Encoding',
            'Connection', 'Cache-Control'
        ]
        
        f.write("重要头部:\n")
        for header in important_headers:
            if header in headers:
                f.write(f"  {header}: {headers[header]}\n")
        
        f.write("\n所有头部:\n")
        for header, value in headers.items():
            f.write(f"  {header}: {value}\n")
        
        # 分析特殊头部
        if 'Content-Type' in headers:
            content_type = headers['Content-Type']
            f.write(f"\nContent-Type分析:\n")
            f.write(f"  类型: {content_type}\n")
            
            if 'application/json' in content_type:
                f.write("  格式: JSON数据\n")
            elif 'application/x-www-form-urlencoded' in content_type:
                f.write("  格式: 表单数据\n")
            elif 'multipart/form-data' in content_type:
                f.write("  格式: 多部分表单数据\n")
        
        f.write("\n")
    
    def write_body_analysis(self, f, raw_body, request_data):
        """分析请求体"""
        f.write("📦 请求体分析\n")
        f.write("-" * 40 + "\n")
        
        if not raw_body:
            f.write("空请求体\n\n")
            return
        
        f.write(f"数据长度: {len(raw_body)} 字节\n")
        f.write(f"MD5哈希: {hashlib.md5(raw_body).hexdigest()}\n")
        f.write(f"SHA1哈希: {hashlib.sha1(raw_body).hexdigest()}\n\n")
        
        # 字节统计
        f.write("字节统计:\n")
        byte_counts = {}
        for byte in raw_body:
            byte_counts[byte] = byte_counts.get(byte, 0) + 1
        
        # 显示特殊字符
        special_chars = []
        for byte_val in sorted(byte_counts.keys()):
            if byte_val < 32 or byte_val > 126:
                special_chars.append((byte_val, byte_counts[byte_val]))
        
        if special_chars:
            f.write("发现特殊字符:\n")
            for byte_val, count in special_chars:
                f.write(f"  0x{byte_val:02x} ({byte_val}): {count}次\n")
        else:
            f.write("未发现特殊字符 (全部为可打印ASCII)\n")
        
        # 编码分析
        f.write("\n编码分析:\n")
        
        # UTF-8分析
        try:
            utf8_text = raw_body.decode('utf-8')
            f.write("✅ UTF-8解码成功\n")
            request_data['analysis']['utf8_valid'] = True
            request_data['analysis']['utf8_text'] = utf8_text
            
            # JSON分析
            if utf8_text.strip().startswith(('{', '[')):
                try:
                    json_data = json.loads(utf8_text)
                    f.write("✅ JSON解析成功\n")
                    f.write(f"JSON类型: {type(json_data).__name__}\n")
                    request_data['analysis']['json_valid'] = True
                    request_data['analysis']['json_data'] = json_data
                    
                    # 分析JSON结构
                    if isinstance(json_data, dict):
                        f.write(f"JSON键数量: {len(json_data)}\n")
                        f.write("JSON键列表:\n")
                        for key in json_data.keys():
                            f.write(f"  - {key}\n")
                except json.JSONDecodeError as e:
                    f.write(f"❌ JSON解析失败: {e}\n")
                    request_data['analysis']['json_valid'] = False
                    request_data['analysis']['json_error'] = str(e)
            
        except UnicodeDecodeError as e:
            f.write(f"❌ UTF-8解码失败: {e}\n")
            request_data['analysis']['utf8_valid'] = False
            request_data['analysis']['utf8_error'] = str(e)
            
            # 尝试其他编码
            encodings = ['latin1', 'gbk', 'gb2312', 'big5']
            for encoding in encodings:
                try:
                    text = raw_body.decode(encoding)
                    f.write(f"✅ {encoding.upper()}解码成功\n")
                    break
                except:
                    f.write(f"❌ {encoding.upper()}解码失败\n")
        
        # 原始数据展示
        f.write("\n原始数据展示:\n")
        f.write("十六进制格式:\n")
        hex_data = raw_body.hex()
        for i in range(0, len(hex_data), 32):
            offset = i // 2
            hex_part = hex_data[i:i+32]
            # 格式化为每两个字符一组
            hex_formatted = ' '.join(hex_part[j:j+2] for j in range(0, len(hex_part), 2))
            f.write(f"{offset:08x}: {hex_formatted}\n")
        
        # 可打印字符版本
        f.write("\n可打印字符版本:\n")
        printable = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in raw_body)
        for i in range(0, len(printable), 64):
            f.write(f"{i:08x}: {printable[i:i+64]}\n")
        
        f.write("\n")
    
    def write_security_analysis(self, f, request_data):
        """安全分析"""
        f.write("🔒 安全分析\n")
        f.write("-" * 40 + "\n")
        
        headers = request_data['headers']
        
        # 检查认证头
        if 'Authorization' in headers:
            auth = headers['Authorization']
            if auth.startswith('Bearer '):
                f.write("✅ 发现Bearer Token认证\n")
                token = auth[7:]
                f.write(f"Token长度: {len(token)}\n")
                f.write(f"Token前缀: {token[:10]}...\n")
            else:
                f.write(f"认证类型: {auth.split()[0] if auth else '未知'}\n")
        else:
            f.write("⚠️ 未发现Authorization头\n")
        
        # 检查签名
        if 'X-Signature' in headers:
            f.write("✅ 发现X-Signature签名\n")
            sig = headers['X-Signature']
            if sig.startswith('sha1='):
                f.write("签名算法: SHA1\n")
                f.write(f"签名值: {sig[5:]}\n")
        else:
            f.write("⚠️ 未发现X-Signature签名\n")
        
        # 检查内容类型安全
        if 'Content-Type' in headers:
            content_type = headers['Content-Type']
            if 'application/json' in content_type:
                f.write("✅ JSON内容类型安全\n")
            else:
                f.write(f"⚠️ 非标准内容类型: {content_type}\n")
        
        f.write("\n")
    
    def write_recommendations(self, f, request_data):
        """写入建议"""
        f.write("💡 处理建议\n")
        f.write("-" * 40 + "\n")
        
        if request_data['analysis'].get('utf8_valid'):
            f.write("✅ 数据编码正常，可以直接处理\n")
        else:
            f.write("⚠️ 数据编码异常，需要特殊处理\n")
        
        if request_data['analysis'].get('json_valid'):
            f.write("✅ JSON格式正确，可以正常解析\n")
        else:
            f.write("❌ JSON格式异常，需要错误处理\n")
        
        f.write("\n处理代码示例:\n")
        f.write("```python\n")
        f.write("try:\n")
        f.write("    data = json.loads(request_body.decode('utf-8'))\n")
        f.write("    # 处理数据\n")
        f.write("except UnicodeDecodeError:\n")
        f.write("    # 处理编码错误\n")
        f.write("except json.JSONDecodeError:\n")
        f.write("    # 处理JSON错误\n")
        f.write("```\n")
    
    def do_POST(self):
        """处理POST请求"""
        print(f"\n📥 收到POST请求: {self.path}")
        print(f"🕐 时间: {datetime.now().strftime('%H:%M:%S.%f')[:-3]}")
        
        analysis_file = self.capture_request('POST')
        
        # 返回响应
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        
        response = {
            'status': 'ok',
            'message': '请求已捕获和分析',
            'analysis_file': analysis_file,
            'timestamp': time.time()
        }
        
        self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
    
    def do_GET(self):
        """处理GET请求"""
        print(f"\n📥 收到GET请求: {self.path}")
        analysis_file = self.capture_request('GET')
        
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        
        response = {'status': 'ok', 'analysis_file': analysis_file}
        self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
    
    def log_message(self, format, *args):
        """禁用默认日志"""
        pass


def main():
    """启动超详细捕获服务器"""
    print("🔬 NapCat超详细请求分析器")
    print("=" * 60)
    print("🎯 功能特性:")
    print("  📋 完整请求信息捕获")
    print("  🔍 字节级数据分析")
    print("  🔤 多编码解码尝试")
    print("  📊 JSON结构分析")
    print("  🔒 安全特性检测")
    print("  💾 多格式数据保存")
    print("  💡 处理建议生成")
    print("=" * 60)
    
    try:
        with socketserver.TCPServer(('0.0.0.0', 8080), UltraDetailedCapture) as httpd:
            print("🚀 超详细分析服务器启动成功!")
            print("📡 监听地址: http://0.0.0.0:8080")
            print("📁 输出文件:")
            print("  - napcat_analysis_[时间].txt (详细分析)")
            print("  - napcat_raw_[时间].bin (原始二进制)")
            print("  - napcat_data_[时间].json (结构化数据)")
            print("🔔 等待NapCat发送请求...")
            print("按 Ctrl+C 停止")
            print("-" * 60)
            
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n👋 分析服务器已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flask版原始请求捕获器
保存NapCat的原始请求到JSON文件
"""

import json
import os
from datetime import datetime
from flask import Flask, request, jsonify


app = Flask(__name__)

# 配置
JSON_OUTPUT_DIR = "napcat_requests"
MAX_FILES = 100  # 最多保存文件数


@app.route('/', methods=['POST'])
def capture_request():
    """捕获并保存原始请求"""
    try:
        # 创建输出目录
        if not os.path.exists(JSON_OUTPUT_DIR):
            os.makedirs(JSON_OUTPUT_DIR)
        
        # 获取原始数据
        raw_data = request.get_data()
        content_type = request.headers.get('Content-Type', '')
        
        # 准备保存的数据
        captured_data = {
            'timestamp': datetime.now().isoformat(),
            'method': request.method,
            'url': request.url,
            'headers': dict(request.headers),
            'content_type': content_type,
            'raw_data': raw_data.decode('utf-8', errors='replace'),
            'raw_data_hex': raw_data.hex(),
            'content_length': len(raw_data)
        }
        
        # 尝试解析JSON
        try:
            if raw_data:
                json_data = json.loads(raw_data.decode('utf-8'))
                captured_data['parsed_json'] = json_data
                captured_data['parse_status'] = 'success'
                
                # 提取关键信息用于文件名
                if isinstance(json_data, dict):
                    post_type = json_data.get('post_type', 'unknown')
                    message_type = json_data.get('message_type', '')
                    user_id = json_data.get('user_id', '')
                    
                    if message_type:
                        file_prefix = f"{post_type}_{message_type}"
                    else:
                        file_prefix = post_type
                    
                    if user_id:
                        file_prefix += f"_user{user_id}"
                else:
                    file_prefix = "raw_data"
            else:
                file_prefix = "empty_request"
                
        except json.JSONDecodeError as e:
            captured_data['parsed_json'] = None
            captured_data['parse_status'] = 'failed'
            captured_data['parse_error'] = str(e)
            file_prefix = "parse_failed"
            print(f"⚠️  JSON解析失败: {e}")
        
        # 生成文件名
        timestamp_str = datetime.now().strftime('%Y%m%d_%H%M%S_%f')[:-3]
        filename = f"{timestamp_str}_{file_prefix}.json"
        filepath = os.path.join(JSON_OUTPUT_DIR, filename)
        
        # 保存到文件
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(captured_data, f, ensure_ascii=False, indent=2)
        
        # 打印信息
        print(f"📁 已保存: {filename}")
        if 'parsed_json' in captured_data and captured_data['parsed_json']:
            json_data = captured_data['parsed_json']
            if json_data.get('post_type') == 'message':
                user_id = json_data.get('user_id')
                message = json_data.get('raw_message', '')
                print(f"💬 消息 | 用户{user_id}: {message[:50]}{'...' if len(message) > 50 else ''}")
        
        # 清理旧文件
        cleanup_old_files()
        
        return jsonify({'status': 'captured', 'file': filename})
        
    except Exception as e:
        print(f"❌ 捕获失败: {e}")
        return jsonify({'error': str(e)}), 500


def cleanup_old_files():
    """清理旧文件，保持文件数量在限制内"""
    try:
        if not os.path.exists(JSON_OUTPUT_DIR):
            return
        
        files = []
        for filename in os.listdir(JSON_OUTPUT_DIR):
            if filename.endswith('.json'):
                filepath = os.path.join(JSON_OUTPUT_DIR, filename)
                files.append((filepath, os.path.getctime(filepath)))
        
        # 按创建时间排序
        files.sort(key=lambda x: x[1])
        
        # 删除超出限制的旧文件
        while len(files) > MAX_FILES:
            old_file = files.pop(0)
            try:
                os.remove(old_file[0])
                print(f"🗑️  删除旧文件: {os.path.basename(old_file[0])}")
            except Exception as e:
                print(f"⚠️  删除文件失败: {e}")
                
    except Exception as e:
        print(f"⚠️  清理文件失败: {e}")


@app.route('/status', methods=['GET'])
def get_status():
    """获取状态信息"""
    try:
        file_count = 0
        total_size = 0
        
        if os.path.exists(JSON_OUTPUT_DIR):
            for filename in os.listdir(JSON_OUTPUT_DIR):
                if filename.endswith('.json'):
                    filepath = os.path.join(JSON_OUTPUT_DIR, filename)
                    file_count += 1
                    total_size += os.path.getsize(filepath)
        
        return jsonify({
            'status': 'running',
            'timestamp': datetime.now().isoformat(),
            'output_dir': JSON_OUTPUT_DIR,
            'captured_files': file_count,
            'total_size_bytes': total_size,
            'max_files': MAX_FILES
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/files', methods=['GET'])
def list_files():
    """列出已捕获的文件"""
    try:
        files = []
        
        if os.path.exists(JSON_OUTPUT_DIR):
            for filename in os.listdir(JSON_OUTPUT_DIR):
                if filename.endswith('.json'):
                    filepath = os.path.join(JSON_OUTPUT_DIR, filename)
                    stat = os.stat(filepath)
                    files.append({
                        'name': filename,
                        'size': stat.st_size,
                        'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                        'modified': datetime.fromtimestamp(stat.st_mtime).isoformat()
                    })
        
        # 按创建时间倒序排序
        files.sort(key=lambda x: x['created'], reverse=True)
        
        return jsonify({
            'files': files,
            'count': len(files)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/files/<filename>', methods=['GET'])
def get_file(filename):
    """获取指定文件内容"""
    try:
        filepath = os.path.join(JSON_OUTPUT_DIR, filename)
        
        if not os.path.exists(filepath):
            return jsonify({'error': 'File not found'}), 404
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return jsonify(data)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def main():
    """启动Flask应用"""
    print("🚀 Flask版NapCat原始请求捕获器")
    print("📁 保存目录: napcat_requests/")
    print("📊 API端点:")
    print("   - POST / : 捕获请求")
    print("   - GET /status : 获取状态")
    print("   - GET /files : 列出文件")
    print("   - GET /files/<name> : 获取文件内容")
    print("=" * 50)
    print("✅ 服务器启动中...")
    print("📡 监听端口: 8080")
    print("🔔 等待NapCat请求...")
    print("=" * 50)
    
    app.run(
        host='0.0.0.0',
        port=8080,
        debug=False,
        threaded=True
    )


if __name__ == "__main__":
    main()
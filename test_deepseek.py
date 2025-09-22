#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DeepSeek API 测试脚本
"""

import yaml
import requests
import json


def load_config():
    """加载配置"""
    try:
        with open('config.yml', 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"❌ 配置文件加载失败: {e}")
        return None


def test_deepseek_api():
    """测试DeepSeek API"""
    config = load_config()
    if not config:
        return
    
    deepseek_config = config.get('deepseek', {})
    api_key = deepseek_config.get('api_key', '')
    base_url = deepseek_config.get('base_url', 'https://api.deepseek.com')
    model = deepseek_config.get('model', 'deepseek-chat')
    
    print("🧪 测试DeepSeek API连接...")
    print(f"📡 API地址: {base_url}")
    print(f"🤖 模型: {model}")
    print(f"🔑 API密钥: {api_key[:20]}...{api_key[-4:] if len(api_key) > 24 else api_key}")
    print("-" * 50)
    
    if not api_key or api_key == 'sk-your-deepseek-api-key-here':
        print("❌ API密钥未配置或使用默认值")
        return
    
    # 测试API调用
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": "你是一个测试助手。"},
            {"role": "user", "content": "请说'测试成功'"}
        ],
        "max_tokens": 100,
        "temperature": 0.7
    }
    
    try:
        print("⏳ 正在测试API调用...")
        response = requests.post(
            f"{base_url}/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        
        print(f"📊 响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if 'choices' in result and len(result['choices']) > 0:
                reply = result['choices'][0]['message']['content']
                print(f"✅ API测试成功！")
                print(f"🤖 AI回复: {reply}")
                
                # 显示token使用信息
                if 'usage' in result:
                    usage = result['usage']
                    print(f"📈 Token使用: 输入{usage.get('prompt_tokens', 0)} + 输出{usage.get('completion_tokens', 0)} = 总计{usage.get('total_tokens', 0)}")
            else:
                print(f"❌ API响应格式异常: {result}")
        else:
            print(f"❌ API调用失败: {response.status_code}")
            try:
                error_detail = response.json()
                print(f"错误详情: {error_detail}")
            except:
                print(f"错误内容: {response.text}")
                
    except requests.exceptions.Timeout:
        print("⏰ API调用超时")
    except requests.exceptions.RequestException as e:
        print(f"❌ 网络请求异常: {e}")
    except Exception as e:
        print(f"❌ 测试异常: {e}")


def test_config_loading():
    """测试配置加载"""
    print("🔧 测试配置加载...")
    config = load_config()
    if config:
        print("✅ 配置文件加载成功")
        
        # 检查关键配置项
        napcat = config.get('napcat', {})
        deepseek = config.get('deepseek', {})
        
        print(f"📡 NapCat: {napcat.get('host')}:{napcat.get('port')}")
        print(f"🧠 DeepSeek启用: {deepseek.get('enabled', False)}")
        print(f"🤖 DeepSeek模型: {deepseek.get('model', 'N/A')}")
        
        return True
    else:
        print("❌ 配置文件加载失败")
        return False


def main():
    """主函数"""
    print("🚀 NAS Bot DeepSeek API 测试工具")
    print("=" * 50)
    
    # 测试配置加载
    if test_config_loading():
        print()
        # 测试API连接
        test_deepseek_api()
    
    print("\n" + "=" * 50)
    print("测试完成")


if __name__ == "__main__":
    main()
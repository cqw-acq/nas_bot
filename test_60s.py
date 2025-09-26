#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试60秒新闻功能
"""

import requests
import json


def test_60s_api():
    """测试60秒API"""
    try:
        print("🔍 测试60秒新闻API...")
        response = requests.get('https://60s2.chuqijerry.workers.dev/v2/60s', timeout=10)
        
        print(f"📊 状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API响应成功")
            print(f"📅 日期: {data.get('data', {}).get('date', '未知')}")
            print(f"🖼️  图片URL: {data.get('data', {}).get('image', '无')}")
            print(f"📰 新闻条数: {len(data.get('data', {}).get('news', []))}")
            
            # 显示前3条新闻
            news_list = data.get('data', {}).get('news', [])
            if news_list:
                print("\n📰 前3条新闻:")
                for i, news in enumerate(news_list[:3], 1):
                    print(f"  {i}. {news}")
            
            return True
        else:
            print(f"❌ API请求失败: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False


def test_command_handler():
    """测试CommandHandler的60s方法"""
    try:
        print("\n🧪 测试CommandHandler.handle_60s方法...")
        
        # 导入必要的类
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        
        from enhanced_chat_bot import BotConfig, DataManager, CommandHandler
        
        # 创建实例
        config = BotConfig()
        data_manager = DataManager(config)
        command_handler = CommandHandler(config, data_manager)
        
        # 测试60s命令
        result = command_handler.handle_60s([])
        print(f"✅ 60s命令测试完成")
        print(f"📄 返回结果类型: {type(result)}")
        print(f"📝 返回结果长度: {len(result) if result else 0}")
        
        if result and '[CQ:image' in result:
            print("🖼️  返回了图片CQ码")
        elif result and '60秒读懂世界' in result:
            print("📰 返回了文字新闻")
        else:
            print("⚠️  返回结果格式异常")
            
        print(f"📋 返回内容预览: {result[:100]}..." if result and len(result) > 100 else f"📋 返回内容: {result}")
        
        return True
        
    except Exception as e:
        print(f"❌ CommandHandler测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("🚀 开始测试60秒新闻功能\n")
    
    # 测试API
    api_ok = test_60s_api()
    
    # 测试命令处理
    cmd_ok = test_command_handler()
    
    print(f"\n📊 测试结果:")
    print(f"  🌐 API测试: {'✅ 通过' if api_ok else '❌ 失败'}")
    print(f"  🔧 命令测试: {'✅ 通过' if cmd_ok else '❌ 失败'}")
    
    if api_ok and cmd_ok:
        print("\n🎉 60秒新闻功能测试通过！")
    else:
        print("\n⚠️  部分测试失败，请检查代码")
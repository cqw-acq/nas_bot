#!/usr/bin/env python3
"""测试prompt管理系统"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from enhanced_chat_bot import BotConfig, PromptManager

def test_prompt_system():
    """测试prompt管理系统"""
    print("🧪 测试Prompt管理系统...")
    
    try:
        # 初始化配置和prompt管理器
        config = BotConfig()
        prompt_manager = PromptManager(config)
        
        # 测试获取默认prompt
        print(f"📝 当前prompt: {prompt_manager.current_prompt}")
        
        # 测试获取可用的prompts
        prompts = prompt_manager.list_prompts()
        print(f"📋 可用的prompts: {prompts}")
        
        # 测试获取prompt内容
        for prompt_name in prompts:
            try:
                content = prompt_manager.get_prompt(prompt_name)
                print(f"✅ {prompt_name}: {content[:50]}...")
            except Exception as e:
                print(f"❌ {prompt_name}: {e}")
        
        # 测试切换prompt
        if 'technical' in prompts:
            print(f"\n🔄 切换到技术prompt...")
            success = prompt_manager.set_prompt('technical')
            if success:
                print(f"✅ 切换成功，当前prompt: {prompt_manager.current_prompt}")
                content = prompt_manager.get_current_prompt()
                print(f"📄 内容: {content[:100]}...")
            else:
                print("❌ 切换失败")
        
        print("\n✅ Prompt系统测试完成！")
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_prompt_system()
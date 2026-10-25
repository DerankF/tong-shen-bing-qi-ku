#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agnes API 快速启动脚本
Quick Start Script for Agnes API Integration

功能：
- 一键配置API
- 测试连接
- 快速演示

使用方法：
python quick_start.py

作者: 高府认证团队
版本: 1.0.0
"""

import asyncio
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from agnes_api_client import AgnesAPIClient, AgnesAPIConfig
from config.example_config import setup_agnes_api, verify_config, quick_test


async def demo_chat():
    """演示聊天功能"""
    print("\n🎯 聊天功能演示")
    print("-" * 40)

    config = AgnesAPIConfig(
        api_key="sk-nwd2JHWgNxdXcbAMCSzkI8x5QSdNDMe7zwLhMFhWihK9Blng",
        base_url="https://apihub.agnes-ai.com/v1",
        rate_limit=60
    )

    async with AgnesAPIClient(config) as client:
        try:
            messages = [
                {"role": "user", "content": "请介绍一下高府帝意综合评估系统"}
            ]

            response = await client.chat(
                messages=messages,
                model="default",
                max_tokens=200
            )

            # 提取响应内容
            if 'choices' in response and len(response['choices']) > 0:
                content = response['choices'][0]['message']['content']
                print(f"🤖 AI回复:\n{content}")
            else:
                print("❌ 响应格式异常")
                print(f"完整响应: {response}")

        except Exception as e:
            print(f"❌ 聊天失败: {str(e)}")


async def demo_models():
    """演示获取模型列表"""
    print("\n📋 模型列表演示")
    print("-" * 40)

    config = AgnesAPIConfig(
        api_key="sk-nwd2JHWgNxdXcbAMCSzkI8x5QSdNDMe7zwLhMFhWihK9Blng",
        base_url="https://apihub.agnes-ai.com/v1"
    )

    async with AgnesAPIClient(config) as client:
        try:
            models = await client.models()
            print("✅ 获取模型列表成功")

            if 'data' in models and isinstance(models['data'], list):
                print(f"\n🎯 可用模型 ({len(models['data'])}个):")
                for model in models['data'][:5]:  # 显示前5个
                    id = model.get('id', 'Unknown')
                    object_type = model.get('object', 'Unknown')
                    created = model.get('created', 'Unknown')
                    print(f"  - {id} ({object_type})")
                if len(models['data']) > 5:
                    print(f"  ... 还有 {len(models['data']) - 5} 个模型")
            else:
                print("❌ 模型列表格式异常")
                print(f"完整响应: {models}")

        except Exception as e:
            print(f"❌ 获取模型列表失败: {str(e)}")


async def main():
    """主函数"""
    print("🚀 Agnes API 快速启动")
    print("=" * 50)

    # 1. 配置API
    print("\n1️⃣ 配置 Agnes API...")
    if not setup_agnes_api():
        print("❌ 配置失败，请检查API密钥")
        return

    # 2. 验证配置
    print("\n2️⃣ 验证配置...")
    if not verify_config():
        print("❌ 配置验证失败")
        return

    # 3. 测试连接
    print("\n3️⃣ 测试基本连接...")
    if not quick_test():
        print("❌ 连接测试失败")
        return

    # 4. 功能演示
    print("\n4️⃣ 功能演示...")
    await demo_chat()
    await demo_models()

    # 5. 完成提示
    print("\n" + "=" * 50)
    print("🎉 快速启动完成！")
    print("\n💡 下一步建议:")
    print("  1. 查看 examples/agnes_integration_example.py 了解更多用法")
    print("  2. 阅读 README_Agnes_Integration.md 获取详细文档")
    print("  3. 集成到您的高府帝意评估系统中")
    print("=" * 50)


if __name__ == "__main__":
    # 运行主程序
    asyncio.run(main())
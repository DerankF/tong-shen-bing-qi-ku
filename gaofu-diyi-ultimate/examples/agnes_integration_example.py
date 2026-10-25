#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agnes AI 集成示例
Agnes AI Integration Examples

示例：
1. 基础聊天功能
2. 嵌入生成
3. 模型列表查询
4. 自定义端点调用
5. 批量处理
6. 错误处理

作者: 高府认证团队
版本: 1.0.0
"""

import asyncio
import json
from typing import List, Dict, Any
from agnes_api_client import AgnesAPIClient, AgnesAPIConfig, AgnesAPIError
from config.agnes_config import get_config, set_api_key, update_config


def print_response(response: Dict[str, Any], title: str = ""):
    """格式化打印响应"""
    if title:
        print(f"\n{'='*60}")
        print(f"{title}")
        print(f"{'='*60}")

    if isinstance(response, dict):
        # 美化打印JSON
        print(json.dumps(response, indent=2, ensure_ascii=False))
    else:
        print(response)


async def example_1_basic_chat():
    """示例1: 基础聊天功能"""
    print("\n📝 示例1: 基础聊天功能")
    print("-" * 50)

    # 获取配置
    config = get_config("sk-nwd2JHWgNxdXcbAMCSzkI8x5QSdNDMe7zwLhMFhWihK9Blng")
    if not config:
        print("❌ 无法获取配置，请检查API密钥")
        return

    # 创建客户端
    async with AgnesAPIClient(config) as client:
        messages = [
            {"role": "system", "content": "你是一个专业的AI助手，请用中文回答。"},
            {"role": "user", "content": "你好，请介绍一下高府帝意综合评估系统"}
        ]

        try:
            # 发送聊天请求
            response = await client.chat(
                messages=messages,
                model="default",
                temperature=0.7,
                max_tokens=1000
            )

            print_response(response, "聊天响应")

        except AgnesAPIError as e:
            print(f"❌ API错误: {str(e)}")


async def example_2_embeddings():
    """示例2: 嵌入生成"""
    print("\n📝 示例2: 嵌入生成")
    print("-" * 50)

    config = get_config("sk-nwd2JHWgNxdXcbAMCSzkI8x5QSdNDMe7zwLhMFhWihK9Blng")
    if not config:
        return

    async with AgnesAPIClient(config) as client:
        text = "高府帝意综合评估系统是一个创新的AI评估框架"

        try:
            # 生成嵌入
            response = await client.embeddings(
                text=text,
                model="text-embedding"
            )

            print_response(response, "嵌入向量")

        except AgnesAPIError as e:
            print(f"❌ API错误: {str(e)}")


async def example_3_models():
    """示例3: 查询可用模型"""
    print("\n📝 示例3: 查询可用模型")
    print("-" * 50)

    config = get_config("sk-nwd2JHWgNxdXcbAMCSzkI8x5QSdNDMe7zwLhMFhWihK9Blng")
    if not config:
        return

    async with AgnesAPIClient(config) as client:
        try:
            # 获取模型列表
            response = await client.models()

            print_response(response, "可用模型")

        except AgnesAPIError as e:
            print(f"❌ API错误: {str(e)}")


async def example_4_usage():
    """示例4: 查询使用统计"""
    print("\n📝 示例4: 查询使用统计")
    print("-" * 50)

    config = get_config("sk-nwd2JHWgNxdXcbAMCSzkI8x5QSdNDMe7zwLhMFhWihK9Blng")
    if not config:
        return

    async with AgnesAPIClient(config) as client:
        try:
            # 获取使用统计
            response = await client.usage()

            print_response(response, "使用统计")

            # 获取客户端统计
            stats = client.get_stats()
            print_response(stats, "客户端统计")

        except AgnesAPIError as e:
            print(f"❌ API错误: {str(e)}")


async def example_5_batch_processing():
    """示例5: 批量处理"""
    print("\n📝 示例5: 批量处理多个请求")
    print("-" * 50)

    config = get_config("sk-nwd2JHWgNxdXcbAMCSzkI8x5QSdNDMe7zwLhMFhWihK9Blng")
    if not config:
        return

    async with AgnesAPIClient(config) as client:
        # 定义多个任务
        tasks = [
            ("聊天", [
                {"role": "user", "content": "什么是人工智能？"}
            ]),
            ("聊天", [
                {"role": "user", "content": "机器学习的基本原理是什么？"}
            ]),
            ("聊天", [
                {"role": "user", "content": "深度学习与传统机器学习的区别"}
            ])
        ]

        results = []

        # 并发执行
        for task_name, messages in tasks:
            try:
                response = await client.chat(
                    messages=messages,
                    model="default",
                    max_tokens=500
                )
                results.append({
                    "task": task_name,
                    "success": True,
                    "response": response
                })
                print(f"✅ {task_name} 完成")

            except AgnesAPIError as e:
                results.append({
                    "task": task_name,
                    "success": False,
                    "error": str(e)
                })
                print(f"❌ {task_name} 失败: {str(e)}")

        # 打印结果汇总
        print_response(results, "批量处理结果汇总")


async def example_6_custom_endpoint():
    """示例6: 自定义端点"""
    print("\n📝 示例6: 自定义端点调用")
    print("-" * 50)

    config = get_config("sk-nwd2JHWgNxdXcbAMCSzkI8x5QSdNDMe7zwLhMFhWihK9Blng")
    if not config:
        return

    async with AgnesAPIClient(config) as client:
        # 自定义请求数据
        data = {
            "query": "分析市场趋势",
            "context": "2024年AI行业",
            "format": "json"
        }

        try:
            # 调用自定义端点
            response = await client.custom_endpoint(
                endpoint="/analysis/market",
                data=data
            )

            print_response(response, "自定义端点响应")

        except AgnesAPIError as e:
            print(f"❌ API错误: {str(e)}")


async def example_7_error_handling():
    """示例7: 错误处理"""
    print("\n📝 示例7: 错误处理演示")
    print("-" * 50)

    config = get_config("sk-nwd2JHWgNxdXcbAMCSzkI8x5QSdNDMe7zwLhMFhWihK9Blng")
    if not config:
        return

    # 测试不同的错误场景
    error_tests = [
        ("无效的API密钥", "invalid-key"),
        ("不存在的端点", "/nonexistent"),
        ("超时设置", None)
    ]

    async with AgnesAPIClient(config) as client:
        for test_name, api_key in error_tests:
            print(f"\n测试: {test_name}")

            if api_key:
                # 使用无效密钥
                test_config = AgnesAPIConfig(api_key=api_key)
                async with AgnesAPIClient(test_config) as test_client:
                    try:
                        await test_client.chat([{"role": "user", "content": "test"}])
                    except AgnesAPIError as e:
                        print(f"✅ 预期错误: {str(e)}")
            else:
                # 测试其他错误
                try:
                    await client.custom_endpoint("/nonexistent")
                except AgnesAPIError as e:
                    print(f"✅ 预期错误: {str(e)}")


async def example_8_configuration():
    """示例8: 配置管理"""
    print("\n📝 示例8: 配置管理")
    print("-" * 50)

    # 设置API密钥
    api_key = "sk-nwd2JHWgNxdXcbAMCSzkI8x5QSdNDMe7zwLhMFhWihK9Blng"
    if set_api_key(api_key):
        print("✅ API密钥已设置")

    # 更新配置
    update_config(
        rate_limit=200,
        timeout=45,
        enable_cache=False
    )
    print("✅ 配置已更新")

    # 获取配置
    config = get_config()
    if config:
        print(f"📋 当前配置:")
        print(f"  - 速率限制: {config.rate_limit} req/min")
        print(f"  - 超时时间: {config.timeout}s")
        print(f"  - 缓存启用: {config.enable_cache}")
        print(f"  - 最大重试: {config.max_retries}")


async def main():
    """运行所有示例"""
    print("🚀 Agnes AI 集成示例演示")
    print("=" * 60)

    # 检查依赖
    try:
        import aiohttp
        import cryptography
    except ImportError as e:
        print(f"❌ 缺少依赖: {e}")
        print("请安装: pip install aiohttp cryptography")
        return

    # 运行示例
    await example_8_configuration()
    await example_1_basic_chat()
    await example_2_embeddings()
    await example_3_models()
    await example_4_usage()
    await example_5_batch_processing()
    await example_6_custom_endpoint()
    await example_7_error_handling()

    print("\n" + "=" * 60)
    print("🎉 所有示例演示完成！")
    print("=" * 60)


if __name__ == "__main__":
    # 运行示例
    asyncio.run(main())
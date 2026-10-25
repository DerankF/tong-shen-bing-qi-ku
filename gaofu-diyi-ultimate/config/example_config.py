#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agnes API 配置示例
Agnes API Configuration Example

基于官方文档更新：
- Base URL: https://apihub.agnes-ai.com/v1
- 认证方式: Bearer Token
- API Key: sk-nwd2JHWgNxdXcbAMCSzkI8x5QSdNDMe7zwLhMFhWihK9Blng

作者: 高府认证团队
版本: 1.0.0
"""

from config.agnes_config import AgnesConfig, get_config_manager


def setup_agnes_api():
    """设置 Agnes API 配置"""

    # 使用提供的 API Key
    api_key = "sk-nwd2JHWgNxdXcbAMCSzkI8x5QSdNDMe7zwLhMFhWihK9Blng"

    # 创建配置
    config = AgnesConfig(
        api_key=api_key,
        base_url="https://apihub.agnes-ai.com/v1",  # 官方 Base URL
        rate_limit=60,  # 每分钟请求次数
        timeout=30,    # 超时时间（秒）
        max_retries=3,  # 最大重试次数
        retry_delay=1.0,  # 重试延迟（秒）
        enable_cache=True,  # 启用缓存
        cache_ttl=300,  # 缓存有效期（秒）
        log_level="INFO"  # 日志级别
    )

    # 保存配置
    manager = get_config_manager()
    if manager.save_config(config):
        print("✅ Agnes API 配置已成功设置")
        print(f"🔑 API Key: {api_key[:10]}...{api_key[-4:]}")
        print(f"🌐 Base URL: {config.base_url}")
        print(f"⚡ Rate Limit: {config.rate_limit} req/min")
        print(f"🔄 Max Retries: {config.max_retries}")
        return True
    else:
        print("❌ 配置保存失败")
        return False


def verify_config():
    """验证配置是否正确"""
    config = get_config()
    if config:
        print("📋 当前配置:")
        print(f"  API Key: {config.api_key[:10]}...{config.api_key[-4:]}")
        print(f"  Base URL: {config.base_url}")
        print(f"  Rate Limit: {config.rate_limit} req/min")
        print(f"  Timeout: {config.timeout}s")
        print(f"  Max Retries: {config.max_retries}")
        print(f"  Cache Enabled: {config.enable_cache}")
        return True
    else:
        print("❌ 未找到配置")
        return False


def quick_test():
    """快速测试连接"""
    import asyncio
    from agnes_api_client import AgnesAPIClient

    async def test_connection():
        config = get_config()
        if not config:
            print("❌ 未找到配置，请先运行 setup_agnes_api()")
            return False

        try:
            async with AgnesAPIClient(config) as client:
                # 测试聊天接口
                response = await client.chat(
                    messages=[{"role": "user", "content": "Hello"}],
                    max_tokens=50
                )
                print("✅ 连接测试成功")
                print(f"响应: {response.get('choices', [{}])[0].get('message', {}).get('content', 'No content')}")
                return True

        except Exception as e:
            print(f"❌ 连接测试失败: {str(e)}")
            return False

    # 运行测试
    return asyncio.run(test_connection())


if __name__ == "__main__":
    print("🔧 Agnes API 配置工具")
    print("=" * 50)

    # 1. 设置配置
    print("\n1️⃣ 设置配置...")
    setup_agnes_api()

    # 2. 验证配置
    print("\n2️⃣ 验证配置...")
    verify_config()

    # 3. 测试连接
    print("\n3️⃣ 测试连接...")
    quick_test()

    print("\n✨ 配置完成！")
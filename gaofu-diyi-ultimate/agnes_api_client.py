#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agnes AI API 集成模块
Agnes AI API Integration Module

功能：
- 无限API接入支持
- 智能重试机制
- 请求缓存优化
- 使用监控与统计

作者: 高府认证团队
版本: 1.0.0
"""

import asyncio
import aiohttp
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union
import hashlib
import logging
from dataclasses import dataclass
from functools import wraps


@dataclass
class AgnesAPIConfig:
    """Agnes AI API 配置"""
    api_key: str
    base_url: str = "https://apihub.agnes-ai.com/v1"
    timeout: int = 30
    max_retries: int = 3
    retry_delay: float = 1.0
    rate_limit: int = 100  # requests per minute
    enable_cache: bool = True
    cache_ttl: int = 300  # 5 minutes
    request_timeout: int = 30
    connect_timeout: int = 10


class AgnesAPIError(Exception):
    """Agnes API 错误基类"""
    pass


class AgnesAPIRateLimitError(AgnesAPIError):
    """API 限流错误"""
    pass


class AgnesAPIAuthError(AgnesAPIError):
    """API 认证错误"""
    pass


class AgnesAPITimeoutError(AgnesAPIError):
    """API 超时错误"""
    pass


class AgnesAPINetworkError(AgnesAPIError):
    """API 网络错误"""
    pass


class AgnesAPICache:
    """API 请求缓存"""

    def __init__(self, ttl: int = 300):
        self.ttl = ttl
        self.cache: Dict[str, Dict[str, Any]] = {}

    def _get_key(self, method: str, url: str, data: Optional[Dict] = None) -> str:
        """生成缓存键"""
        content = f"{method}:{url}"
        if data:
            content += json.dumps(data, sort_keys=True)
        return hashlib.md5(content.encode()).hexdigest()

    def get(self, method: str, url: str, data: Optional[Dict] = None) -> Optional[Any]:
        """获取缓存"""
        key = self._get_key(method, url, data)
        if key in self.cache:
            entry = self.cache[key]
            if datetime.now() - entry['timestamp'] < timedelta(seconds=self.ttl):
                return entry['response']
            else:
                del self.cache[key]
        return None

    def set(self, method: str, url: str, data: Optional[Dict], response: Any) -> None:
        """设置缓存"""
        key = self._get_key(method, url, data)
        self.cache[key] = {
            'response': response,
            'timestamp': datetime.now()
        }

    def clear(self) -> None:
        """清空缓存"""
        self.cache.clear()


class AgnesAPIClient:
    """Agnes AI API 客户端"""

    def __init__(self, config: AgnesAPIConfig):
        self.config = config
        self.session = None
        self.cache = AgnesAPICache(config.cache_ttl) if config.enable_cache else None
        self.request_times = []
        self.logger = logging.getLogger(__name__)

        # 创建会话
        self._create_session()

    def _create_session(self):
        """创建 aiohttp 会话"""
        timeout = aiohttp.ClientTimeout(
            total=self.config.request_timeout,
            connect=self.config.connect_timeout
        )

        self.session = aiohttp.ClientSession(
            timeout=timeout,
            headers={
                'Authorization': f'Bearer {self.config.api_key}',
                'Content-Type': 'application/json',
                'User-Agent': 'AgnesAI-Python-Client/1.0.0'
            }
        )

    async def _check_rate_limit(self) -> None:
        """检查并处理限流"""
        now = datetime.now()
        # 移除1分钟前的请求时间
        self.request_times = [
            t for t in self.request_times
            if now - t < timedelta(minutes=1)
        ]

        # 如果达到限流上限，等待
        if len(self.request_times) >= self.config.rate_limit:
            wait_time = 60 - (now - self.request_times[0]).total_seconds()
            if wait_time > 0:
                self.logger.info(f"Rate limit reached, waiting {wait_time:.1f}s")
                await asyncio.sleep(wait_time)

    async def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None,
        params: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """发送API请求"""
        url = f"{self.config.base_url}/{endpoint.lstrip('/')}"

        # 检查限流
        await self._check_rate_limit()

        # 记录请求时间
        self.request_times.append(datetime.now())

        # 检查缓存
        if self.cache and method.upper() == 'GET':
            cached = self.cache.get(method, url, data)
            if cached:
                self.logger.info(f"Cache hit for {url}")
                return cached

        # 重试机制
        last_error = None
        for attempt in range(self.config.max_retries):
            try:
                # 请求
                async with self.session.request(
                    method,
                    url,
                    json=data,
                    params=params
                ) as response:
                    # 处理响应
                    if response.status == 200:
                        result = await response.json()

                        # 缓存GET请求
                        if self.cache and method.upper() == 'GET':
                            self.cache.set(method, url, data, result)

                        return result
                    elif response.status == 429:
                        # 限流
                        retry_after = int(response.headers.get('Retry-After', 1))
                        self.logger.warning(f"Rate limited, waiting {retry_after}s")
                        await asyncio.sleep(retry_after)
                        continue
                    elif response.status == 401:
                        raise AgnesAPIAuthError("Invalid API key")
                    elif response.status == 403:
                        raise AgnesAPIAuthError("Access denied")
                    elif response.status == 404:
                        raise AgnesAPIError(f"Endpoint not found: {endpoint}")
                    elif response.status >= 500:
                        # 服务器错误，重试
                        if attempt < self.config.max_retries - 1:
                            delay = self.config.retry_delay * (2 ** attempt)
                            self.logger.warning(f"Server error, retrying in {delay}s")
                            await asyncio.sleep(delay)
                            continue
                        else:
                            raise AgnesAPINetworkError(f"Server error: {response.status}")
                    else:
                        raise AgnesAPIError(f"HTTP {response.status}: {await response.text()}")

            except asyncio.TimeoutError:
                if attempt < self.config.max_retries - 1:
                    delay = self.config.retry_delay * (2 ** attempt)
                    self.logger.warning(f"Timeout, retrying in {delay}s")
                    await asyncio.sleep(delay)
                    last_error = AgnesAPITimeoutError(f"Timeout, attempt {attempt + 1}")
                else:
                    last_error = AgnesAPITimeoutError("Request timeout")
            except Exception as e:
                last_error = e
                if not isinstance(e, AgnesAPIError):
                    self.logger.error(f"Request failed: {str(e)}")
                if attempt < self.config.max_retries - 1 and isinstance(e, (ConnectionError, AgnesAPITimeoutError)):
                    delay = self.config.retry_delay * (2 ** attempt)
                    self.logger.warning(f"Network error, retrying in {delay}s")
                    await asyncio.sleep(delay)
                else:
                    break

        raise last_error or AgnesAPIError("Unknown error occurred")

    async def chat(
        self,
        messages: List[Dict[str, str]],
        model: str = "default",
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stream: bool = False
    ) -> Dict[str, Any]:
        """
        聊天接口

        Args:
            messages: 消息列表
            model: 模型名称
            temperature: 温度参数
            max_tokens: 最大令牌数
            stream: 是否流式输出
        """
        data = {
            "messages": messages,
            "model": model,
            "temperature": temperature,
            "stream": stream
        }

        if max_tokens:
            data["max_tokens"] = max_tokens

        return await self._make_request("POST", "/chat/completions", data)

    async def embeddings(
        self,
        text: str,
        model: str = "text-embedding"
    ) -> Dict[str, Any]:
        """
        嵌入接口

        Args:
            text: 输入文本
            model: 模型名称
        """
        data = {
            "input": text,
            "model": model
        }

        return await self._make_request("POST", "/embeddings", data)

    async def models(self) -> Dict[str, Any]:
        """获取可用模型列表"""
        return await self._make_request("GET", "/models")

    async def usage(self) -> Dict[str, Any]:
        """获取API使用统计"""
        return await self._make_request("GET", "/usage")

    async def custom_endpoint(
        self,
        endpoint: str,
        data: Optional[Dict] = None,
        params: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        自定义接口调用

        Args:
            endpoint: 自定义端点
            data: 请求数据
            params: URL参数
        """
        return await self._make_request("POST", endpoint, data, params)

    async def close(self):
        """关闭会话"""
        if self.session:
            await self.session.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    def get_stats(self) -> Dict[str, Any]:
        """获取使用统计"""
        now = datetime.now()
        recent_requests = len([
            t for t in self.request_times
            if now - t < timedelta(hours=1)
        ])

        return {
            "total_requests": len(self.request_times),
            "requests_last_hour": recent_requests,
            "cache_hits": len(self.cache.cache) if self.cache else 0,
            "rate_limit_remaining": max(0, self.config.rate_limit - len(self.request_times))
        }


# 全局客户端实例
_global_client: Optional[AgnesAPIClient] = None


def get_client(api_key: Optional[str] = None) -> AgnesAPIClient:
    """获取全局客户端实例"""
    global _global_client

    if _global_client is None:
        if api_key:
            config = AgnesAPIConfig(api_key=api_key)
            _global_client = AgnesAPIClient(config)

    return _global_client


def close_client():
    """关闭全局客户端"""
    global _global_client

    if _global_client:
        asyncio.create_task(_global_client.close())
        _global_client = None


# 装饰器：自动重试
def retry_on_error(max_retries: int = 3):
    """自动重试装饰器"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            client = None
            if args and isinstance(args[0], AgnesAPIClient):
                client = args[0]
            elif 'client' in kwargs and isinstance(kwargs['client'], AgnesAPIClient):
                client = kwargs['client']

            if not client:
                return await func(*args, **kwargs)

            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except AgnesAPIError as e:
                    if attempt == max_retries - 1:
                        raise
                    delay = client.config.retry_delay * (2 ** attempt)
                    client.logger.warning(f"Retry {attempt + 1}/{max_retries} in {delay}s: {str(e)}")
                    await asyncio.sleep(delay)
        return wrapper
    return decorator


# 便捷函数
async def chat_with_agnes(
    messages: List[Dict[str, str]],
    api_key: str,
    model: str = "default",
    temperature: float = 0.7,
    max_tokens: Optional[int] = None
) -> Dict[str, Any]:
    """
    快速聊天接口

    Args:
        messages: 消息列表
        api_key: API密钥
        model: 模型名称
        temperature: 温度参数
        max_tokens: 最大令牌数
    """
    async with AgnesAPIClient(AgnesAPIConfig(api_key=api_key)) as client:
        return await client.chat(
            messages=messages,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens
        )


async def get_embeddings_with_agnes(
    text: str,
    api_key: str,
    model: str = "text-embedding"
) -> Dict[str, Any]:
    """
    快速获取嵌入

    Args:
        text: 输入文本
        api_key: API密钥
        model: 模型名称
    """
    async with AgnesAPIClient(AgnesAPIConfig(api_key=api_key)) as client:
        return await client.embeddings(text=text, model=model)


# 同步包装器
def sync_chat_with_agnes(
    messages: List[Dict[str, str]],
    api_key: str,
    model: str = "default",
    temperature: float = 0.7,
    max_tokens: Optional[int] = None
) -> Dict[str, Any]:
    """
    同步聊天接口
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(
            chat_with_agnes(
                messages=messages,
                api_key=api_key,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens
            )
        )
    finally:
        loop.close()


if __name__ == "__main__":
    # 示例使用
    async def demo():
        # 配置
        config = AgnesAPIConfig(
            api_key="sk-nwd2JHWgNxdXcbAMCSzkI8x5QSdNDMe7zwLhMFhWihK9Blng",
            rate_limit=60,
            max_retries=3
        )

        async with AgnesAPIClient(config) as client:
            # 聊天示例
            messages = [
                {"role": "user", "content": "你好，请介绍一下自己"}
            ]

            try:
                response = await client.chat(messages)
                print("聊天响应:", response)

                # 获取模型列表
                models = await client.models()
                print("可用模型:", models)

                # 获取使用统计
                usage = await client.usage()
                print("使用统计:", usage)

            except AgnesAPIError as e:
                print(f"API错误: {str(e)}")

    # 运行演示
    asyncio.run(demo())
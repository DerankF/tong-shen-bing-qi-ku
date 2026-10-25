#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agnes AI 配置管理模块
Agnes AI Configuration Management

功能：
- API密钥管理
- 环境变量配置
- 配置文件读写
- 敏感信息加密存储

作者: 高府认证团队
版本: 1.0.0
"""

import os
import json
import base64
import hashlib
from pathlib import Path
from typing import Dict, Optional, Any
from cryptography.fernet import Fernet
from dataclasses import dataclass, asdict


@dataclass
class AgnesConfig:
    """Agnes AI 配置类"""
    api_key: str
    base_url: str = "https://api.agnes-ai.com"
    rate_limit: int = 100  # requests per minute
    timeout: int = 30
    max_retries: int = 3
    retry_delay: float = 1.0
    enable_cache: bool = True
    cache_ttl: int = 300  # 5 minutes
    log_level: str = "INFO"
    custom_endpoints: Dict[str, str] = None

    def __post_init__(self):
        if self.custom_endpoints is None:
            self.custom_endpoints = {}


class ConfigManager:
    """配置管理器"""

    def __init__(self, config_dir: Optional[Path] = None):
        # 默认配置目录
        self.config_dir = config_dir or Path.home() / ".agnes_ai" / "config"
        self.config_dir.mkdir(parents=True, exist_ok=True)

        # 配置文件路径
        self.config_file = self.config_dir / "config.json"
        self.encryption_key_file = self.config_dir / "key.key"

        # 初始化加密密钥
        self._init_encryption()

    def _init_encryption(self):
        """初始化加密密钥"""
        if not self.encryption_key_file.exists():
            # 生成新的加密密钥
            key = Fernet.generate_key()
            with open(self.encryption_key_file, 'wb') as f:
                f.write(key)
            # 设置文件权限
            os.chmod(self.encryption_key_file, 0o600)

        with open(self.encryption_key_file, 'rb') as f:
            self.cipher = Fernet(f.read())

    def _encrypt(self, data: str) -> str:
        """加密数据"""
        encrypted = self.cipher.encrypt(data.encode())
        return base64.b64encode(encrypted).decode()

    def _decrypt(self, encrypted_data: str) -> str:
        """解密数据"""
        encrypted_bytes = base64.b64decode(encrypted_data.encode())
        decrypted = self.cipher.decrypt(encrypted_bytes)
        return decrypted.decode()

    def load_config(self) -> Optional[AgnesConfig]:
        """加载配置"""
        if not self.config_file.exists():
            return None

        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # 解密API密钥
            if 'api_key' in data:
                data['api_key'] = self._decrypt(data['api_key'])

            return AgnesConfig(**data)

        except Exception as e:
            print(f"加载配置失败: {str(e)}")
            return None

    def save_config(self, config: AgnesConfig) -> bool:
        """保存配置"""
        try:
            # 准备保存的数据
            data = asdict(config)

            # 加密API密钥
            data['api_key'] = self._encrypt(data['api_key'])

            # 保存到文件
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            # 设置文件权限
            os.chmod(self.config_file, 0o600)

            return True

        except Exception as e:
            print(f"保存配置失败: {str(e)}")
            return False

    def get_config_from_env(self) -> Optional[AgnesConfig]:
        """从环境变量获取配置"""
        api_key = os.getenv('AGNES_API_KEY')
        if not api_key:
            return None

        return AgnesConfig(
            api_key=api_key,
            base_url=os.getenv('AGNES_BASE_URL', 'https://apihub.agnes-ai.com/v1'),
            rate_limit=int(os.getenv('AGNES_RATE_LIMIT', '100')),
            timeout=int(os.getenv('AGNES_TIMEOUT', '30')),
            max_retries=int(os.getenv('AGNES_MAX_RETRIES', '3')),
            retry_delay=float(os.getenv('AGNES_RETRY_DELAY', '1.0')),
            enable_cache=os.getenv('AGNES_ENABLE_CACHE', 'true').lower() == 'true',
            cache_ttl=int(os.getenv('AGNES_CACHE_TTL', '300')),
            log_level=os.getenv('AGNES_LOG_LEVEL', 'INFO')
        )

    def create_default_config(self, api_key: str) -> AgnesConfig:
        """创建默认配置"""
        return AgnesConfig(
            api_key=api_key,
            base_url="https://apihub.agnes-ai.com/v1",
            rate_limit=100,
            timeout=30,
            max_retries=3,
            retry_delay=1.0,
            enable_cache=True,
            cache_ttl=300,
            log_level="INFO",
            custom_endpoints={}
        )

    def validate_config(self, config: AgnesConfig) -> bool:
        """验证配置"""
        if not config.api_key:
            print("错误: API密钥不能为空")
            return False

        if not config.api_key.startswith('sk-'):
            print("警告: API密钥格式可能不正确")

        if config.rate_limit <= 0:
            print("错误: 请求速率限制必须大于0")
            return False

        if config.timeout <= 0:
            print("错误: 超时时间必须大于0")
            return False

        if config.max_retries < 0:
            print("错误: 最大重试次数不能为负数")
            return False

        return True

    def get_api_key_hash(self, api_key: str) -> str:
        """获取API密钥的哈希值（用于安全存储）"""
        return hashlib.sha256(api_key.encode()).hexdigest()

    def clear_config(self) -> bool:
        """清除配置"""
        try:
            if self.config_file.exists():
                self.config_file.unlink()
            return True
        except Exception as e:
            print(f"清除配置失败: {str(e)}")
            return False


# 全局配置管理器实例
_config_manager: Optional[ConfigManager] = None


def get_config_manager() -> ConfigManager:
    """获取全局配置管理器"""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager


def get_config(api_key: Optional[str] = None) -> Optional[AgnesConfig]:
    """获取配置"""
    manager = get_config_manager()

    # 1. 首先尝试从配置文件加载
    config = manager.load_config()
    if config:
        return config

    # 2. 尝试从环境变量加载
    config = manager.get_config_from_env()
    if config:
        return config

    # 3. 如果提供了API密钥，创建默认配置
    if api_key:
        config = manager.create_default_config(api_key)
        if manager.validate_config(config):
            manager.save_config(config)
            return config

    return None


def save_config(config: AgnesConfig) -> bool:
    """保存配置"""
    manager = get_config_manager()
    if manager.validate_config(config):
        return manager.save_config(config)
    return False


def init_config(api_key: str) -> AgnesConfig:
    """初始化配置"""
    manager = get_config_manager()
    config = manager.create_default_config(api_key)

    if manager.validate_config(config):
        manager.save_config(config)

    return config


# 快捷函数
def set_api_key(api_key: str) -> bool:
    """设置API密钥"""
    config = get_config(api_key)
    if config:
        return save_config(config)
    return False


def get_api_key() -> Optional[str]:
    """获取API密钥"""
    config = get_config()
    return config.api_key if config else None


def update_config(**kwargs) -> bool:
    """更新配置"""
    config = get_config()
    if not config:
        return False

    # 更新配置项
    for key, value in kwargs.items():
        if hasattr(config, key):
            setattr(config, key, value)

    # 验证并保存
    if get_config_manager().validate_config(config):
        return save_config(config)

    return False


def list_custom_endpoints() -> Dict[str, str]:
    """列出自定义端点"""
    config = get_config()
    return config.custom_endpoints if config else {}


def add_custom_endpoint(name: str, url: str) -> bool:
    """添加自定义端点"""
    config = get_config()
    if not config:
        return False

    config.custom_endpoints[name] = url
    return save_config(config)


def remove_custom_endpoint(name: str) -> bool:
    """移除自定义端点"""
    config = get_config()
    if not config or name not in config.custom_endpoints:
        return False

    del config.custom_endpoints[name]
    return save_config(config)


if __name__ == "__main__":
    # 示例使用
    api_key = "sk-nwd2JHWgNxdXcbAMCSzkI8x5QSdNDMe7zwLhMFhWihK9Blng"

    # 初始化配置
    config = init_config(api_key)
    print(f"配置已初始化: {config.api_key[:20]}...")

    # 保存配置
    save_config(config)

    # 获取配置
    loaded_config = get_config()
    print(f"加载的配置: {loaded_config.api_key[:20]}...")

    # 更新配置
    update_config(rate_limit=200, timeout=45)
    print("配置已更新")

    # 清除配置
    # get_config_manager().clear_config()
    # print("配置已清除")
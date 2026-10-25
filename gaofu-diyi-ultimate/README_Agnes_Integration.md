# Agnes AI 无限使用集成指南

## 📖 简介

本指南将帮助您将 Agnes AI API 无缝集成到您的项目中，实现无限使用的高效调用。

## 🔧 快速开始

### 1. 安装依赖

```bash
pip install aiohttp cryptography
```

### 2. 基础使用

```python
from agnes_api_client import AgnesAPIClient, AgnesAPIConfig

# 创建配置
config = AgnesAPIConfig(
    api_key="sk-nwd2JHWgNxdXcbAMCSzkI8x5QSdNDMe7zwLhMFhWihK9Blng",
    rate_limit=100,  # 每分钟请求次数
    max_retries=3,    # 最大重试次数
    timeout=30       # 超时时间（秒）
)

# 创建客户端
async with AgnesAPIClient(config) as client:
    # 发送消息
    response = await client.chat([
        {"role": "user", "content": "你好"}
    ])
    
    print(response)
```

## 📚 主要功能

### 1. 智能重试机制
- 自动处理网络错误
- 指数退避算法
- 可配置重试次数

### 2. 请求限流控制
- 防止API限制触发
- 智能等待机制
- 自定义速率限制

### 3. 响应缓存
- 自动缓存GET请求
- 可配置缓存TTL
- 内存高效管理

### 4. 错误处理
- 分类错误类型
- 详细错误信息
- 优雅降级

## 📁 文件结构

```
gaofu-diyi-ultimate/
├── agnes_api_client.py      # API客户端核心
├── config/
│   └── agnes_config.py      # 配置管理
├── examples/
│   └── agnes_integration_example.py  # 使用示例
└── README_Agnes_Integration.md        # 本文档
```

## 🔍 API 端点

### 聊天接口
```python
response = await client.chat(
    messages=[
        {"role": "system", "content": "你是一个助手"},
        {"role": "user", "content": "请解释量子计算"}
    ],
    model="default",
    temperature=0.7,
    max_tokens=1000
)
```

### 嵌入接口
```python
response = await client.embeddings(
    text="这是要转换的文本",
    model="text-embedding"
)
```

### 模型列表
```python
models = await client.models()
```

### 使用统计
```python
usage = await client.usage()
stats = client.get_stats()
```

### 自定义端点
```python
response = await client.custom_endpoint(
    endpoint="/custom/analysis",
    data={"query": "数据分析"}
)
```

## ⚙️ 配置管理

### 环境变量配置
```bash
export AGNES_API_KEY="sk-nwd2JHWgNxdXcbAMCSzkI8x5QSdNDMe7zwLhMFhWihK9Blng"
export AGNES_RATE_LIMIT=100
export AGNES_TIMEOUT=30
```

### 代码配置
```python
from config.agnes_config import get_config, update_config

# 获取配置
config = get_config()

# 更新配置
update_config(
    rate_limit=200,
    timeout=45,
    enable_cache=True
)
```

## 🚀 高级用法

### 1. 批量处理
```python
async def batch_process():
    tasks = [
        ("任务1", [{"role": "user", "content": "问题1"}]),
        ("任务2", [{"role": "user", "content": "问题2"}]),
    ]
    
    async with AgnesAPIClient(config) as client:
        for name, messages in tasks:
            response = await client.chat(messages)
            print(f"{name}: {response['choices'][0]['message']['content']}")
```

### 2. 带缓存的查询
```python
# GET请求自动缓存
models = await client.models()  # 第一次调用
models = await client.models()  # 第二次调用使用缓存
```

### 3. 错误处理
```python
from agnes_api_client import AgnesAPIError, AgnesAPIRateLimitError

try:
    response = await client.chat(messages)
except AgnesAPIRateLimitError:
    print("达到API限制，请稍后重试")
except AgnesAPIError as e:
    print(f"API错误: {str(e)}")
```

## 📊 监控与统计

```python
# 获取客户端统计
stats = client.get_stats()
print(f"""
总请求数: {stats['total_requests']}
最近1小时请求数: {stats['requests_last_hour']}
缓存命中数: {stats['cache_hits']}
剩余配额: {stats['rate_limit_remaining']}
""")
```

## 🔒 安全注意事项

1. **API密钥安全**
   - 不要硬编码API密钥
   - 使用环境变量或配置文件
   - 密钥已自动加密存储

2. **请求频率**
   - 设置合理的速率限制
   - 监控使用情况
   - 避免触发API限制

3. **数据保护**
   - 敏感信息加密存储
   - 使用HTTPS通信
   - 定期清理缓存

## 🛠️ 故障排除

### 常见错误

1. **认证失败**
   ```
   AgnesAPIAuthError: Invalid API key
   ```
   - 检查API密钥是否正确
   - 确认密钥格式为 `sk-xxx`

2. **速率限制**
   ```
   AgnesAPIRateLimitError: Rate limit exceeded
   ```
   - 降低请求频率
   - 增加等待时间

3. **网络错误**
   ```
   AgnesAPINetworkError: Connection timeout
   ```
   - 检查网络连接
   - 增加超时时间

### 调试模式

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# 启用详细日志
config = AgnesAPIConfig(
    api_key="your-key",
    log_level="DEBUG"
)
```

## 📈 性能优化

1. **并发请求**
   ```python
   import asyncio
   
   async def concurrent_requests():
       tasks = [
           client.chat(msg) for msg in messages
       ]
       responses = await asyncio.gather(*tasks)
   ```

2. **缓存策略**
   - 启用缓存以减少重复请求
   - 设置合理的TTL
   - 定期清理缓存

3. **连接池**
   - 复用HTTP连接
   - 批量处理请求
   - 使用异步IO

## 🤝 与现有系统集成

### 集成到高府帝意评估系统

```python
from integration_engine import UltimateEvaluationEngine
from agnes_api_client import AgnesAPIClient, AgnesAPIConfig

class EnhancedEvaluationEngine(UltimateEvaluationEngine):
    def __init__(self, api_key):
        super().__init__()
        self.api_config = AgnesAPIConfig(api_key=api_key)
    
    async def enhance_with_ai(self, agent_data):
        """使用AI增强评估"""
        async with AgnesAPIClient(self.api_config) as client:
            # 使用AI分析agent数据
            prompt = f"""
            分析以下Agent数据，提供改进建议：
            {json.dumps(agent_data, ensure_ascii=False)}
            """
            
            response = await client.chat([{
                "role": "user",
                "content": prompt
            }])
            
            return response['choices'][0]['message']['content']
```

## 📞 支持

如有问题，请参考：
- 示例代码: `examples/agnes_integration_example.py`
- 配置文档: `config/agnes_config.py`
- API文档: `agnes_api_client.py`

---

🎉 **祝您使用愉快！**
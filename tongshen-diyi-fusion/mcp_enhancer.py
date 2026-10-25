#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MCP增强层
为每个MCP服务添加RAC可信度评估和帝意五维分析
提供智能路由、质量监控、风险预警功能
"""

import json
import time
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, asdict
from enum import Enum
import threading
from pathlib import Path
import hashlib
import logging

# 导入融合引擎
from .fusion_engine import TongshenDiyiFusion, MCPService


class MCPEventType(Enum):
    """MCP事件类型"""
    REQUEST = "request"
    RESPONSE = "response"
    ERROR = "error"
    TIMEOUT = "timeout"
    SECURITY = "security"


@dataclass
class MCPEvent:
    """MCP事件"""
    timestamp: str
    event_type: MCPEventType
    service_name: str
    request_id: str
    details: Dict
    response_time: float
    success: bool
    error_message: str = None

    def to_evidence(self) -> Dict:
        """转换为证据格式"""
        return {
            "content": f"{self.service_name} - {self.event_type.value}",
            "type": self._get_evidence_type(),
            "source": self.service_name,
            "timestamp": self.timestamp,
            "details": self.details
        }

    def _get_evidence_type(self) -> str:
        """根据事件类型确定证据等级"""
        if self.event_type == MCPEventType.ERROR:
            return "D"  # 单方陈述
        elif self.event_type == MCPEventType.SECURITY:
            return "A"  # 技术可验证
        elif self.event_type == MCPEventType.TIMEOUT:
            return "C"  # 多方证言
        else:
            return "B"  # 权威第三方


class MCPEnhancer:
    """MCP增强层"""

    def __init__(self, fusion_engine: TongshenDiyiFusion):
        self.fusion_engine = fusion_engine
        self.event_history: List[MCPEvent] = []
        self.service_monitors: Dict[str, threading.Thread] = {}
        self.quality_metrics: Dict[str, Dict] = {}
        self.enhanced_services: Dict[str, EnhancedMCPService] = {}

        # 初始化质量指标
        self._init_quality_metrics()

        # 启动增强服务
        self._start_enhanced_services()

    def _init_quality_metrics(self):
        """初始化质量指标"""
        for service_name in self.fusion_engine.mcp_services.keys():
            self.quality_metrics[service_name] = {
                "total_requests": 0,
                "successful_requests": 0,
                "failed_requests": 0,
                "avg_response_time": 0.0,
                "timeout_count": 0,
                "error_count": 0,
                "security_incidents": 0,
                "last_24h_quality": 1.0,
                "reliability_trend": "stable",
                "quality_score": 100.0
            }

    def _start_enhanced_services(self):
        """启动增强的MCP服务"""
        for service_name, service in self.fusion_engine.mcp_services.items():
            enhanced_service = EnhancedMCPService(service_name, self)
            self.enhanced_services[service_name] = enhanced_service

            # 启动监控线程
            monitor_thread = threading.Thread(
                target=enhanced_service.monitor_quality,
                daemon=True
            )
            self.service_monitors[service_name] = monitor_thread
            monitor_thread.start()

            print(f"✅ 启动增强服务: {service_name}")

    async def execute_enhanced_request(
        self,
        service_name: str,
        request_data: Dict,
        timeout: float = 30.0,
        security_checks: bool = True
    ) -> Dict:
        """执行增强的MCP请求"""
        start_time = time.time()
        request_id = self._generate_request_id()

        try:
            # 1. 执行安全检查
            if security_checks:
                security_result = await self._perform_security_check(service_name, request_data)
                if not security_result["passed"]:
                    return {
                        "success": False,
                        "error": security_result["message"],
                        "security_risk": security_result["risk"],
                        "request_id": request_id
                    }

            # 2. 执行请求
            enhanced_service = self.enhanced_services.get(service_name)
            if not enhanced_service:
                raise ValueError(f"Service {service_name} not found")

            result = await enhanced_service.execute_request(request_data, timeout)

            # 3. 记录成功事件
            response_time = time.time() - start_time
            event = MCPEvent(
                timestamp=datetime.now().isoformat(),
                event_type=MCPEventType.RESPONSE,
                service_name=service_name,
                request_id=request_id,
                details={"request": request_data, "response": result},
                response_time=response_time,
                success=True
            )

            # 4. 更新质量指标
            self._update_quality_metrics(service_name, event)

            # 5. 返回结果
            result["request_id"] = request_id
            result["response_time"] = response_time
            result["quality_score"] = self.quality_metrics[service_name]["quality_score"]

            return result

        except asyncio.TimeoutError:
            # 记录超时事件
            response_time = time.time() - start_time
            event = MCPEvent(
                timestamp=datetime.now().isoformat(),
                event_type=MCPEventType.TIMEOUT,
                service_name=service_name,
                request_id=request_id,
                details={"request": request_data},
                response_time=response_time,
                success=False
            )

            self._update_quality_metrics(service_name, event)

            return {
                "success": False,
                "error": "Request timeout",
                "timeout": True,
                "request_id": request_id,
                "response_time": response_time
            }

        except Exception as e:
            # 记录错误事件
            response_time = time.time() - start_time
            event = MCPEvent(
                timestamp=datetime.now().isoformat(),
                event_type=MCPEventType.ERROR,
                service_name=service_name,
                request_id=request_id,
                details={"request": request_data, "error": str(e)},
                response_time=response_time,
                success=False,
                error_message=str(e)
            )

            self._update_quality_metrics(service_name, event)

            return {
                "success": False,
                "error": str(e),
                "request_id": request_id,
                "response_time": response_time
            }

    async def _perform_security_check(
        self,
        service_name: str,
        request_data: Dict
    ) -> Dict:
        """执行安全检查"""
        security_rules = {
            "filesystem": {
                "allowed_operations": ["read", "write", "list"],
                "forbidden_paths": ["/etc", "/sys", "/proc", "C:\\Windows"],
                "max_file_size": 10 * 1024 * 1024  # 10MB
            },
            "github": {
                "allowed_repos": [],
                "rate_limit": 5000,
                "forbidden_actions": ["delete", "admin"]
            },
            "fetch": {
                "allowed_protocols": ["http", "https"],
                "blocked_domains": ["malicious.com", "phishing.net"],
                "max_redirects": 5
            }
        }

        # 应用通用安全规则
        if service_name in security_rules:
            rules = security_rules[service_name]

            # 检查操作权限
            operation = request_data.get("operation")
            if operation and operation not in rules["allowed_operations"]:
                return {
                    "passed": False,
                    "message": f"Operation {operation} not allowed",
                    "risk": "high"
                }

            # 检查路径
            path = request_data.get("path")
            if path and any(forbidden in path for forbidden in rules["forbidden_paths"]):
                return {
                    "passed": False,
                    "message": "Access to forbidden path",
                    "risk": "critical"
                }

            # 检查文件大小
            if "size" in request_data and request_data["size"] > rules["max_file_size"]:
                return {
                    "passed": False,
                    "message": "File size exceeds limit",
                    "risk": "medium"
                }

        return {"passed": True, "message": "Security check passed"}

    def _update_quality_metrics(self, service_name: str, event: MCPEvent):
        """更新质量指标"""
        metrics = self.quality_metrics[service_name]

        # 更新基础指标
        metrics["total_requests"] += 1
        metrics["response_time"] = event.response_time

        if event.success:
            metrics["successful_requests"] += 1
        else:
            metrics["failed_requests"] += 1

        # 更新特定指标
        if event.event_type == MCPEventType.ERROR:
            metrics["error_count"] += 1
        elif event.event_type == MCPEventType.TIMEOUT:
            metrics["timeout_count"] += 1
        elif event.event_type == MCPEventType.SECURITY:
            metrics["security_incidents"] += 1

        # 计算质量分数
        self._calculate_quality_score(service_name)

    def _calculate_quality_score(self, service_name: str):
        """计算服务质量分数"""
        metrics = self.quality_metrics[service_name]

        # 基础分数
        score = 100.0

        # 成功率影响 (40%)
        success_rate = metrics["successful_requests"] / max(metrics["total_requests"], 1)
        score += success_rate * 40 - 20

        # 响应时间影响 (30%)
        if metrics["avg_response_time"] < 1.0:
            score += 15
        elif metrics["avg_response_time"] < 5.0:
            score += 5
        else:
            score -= 10

        # 错误率影响 (20%)
        error_rate = metrics["error_count"] / max(metrics["total_requests"], 1)
        score -= error_rate * 20

        # 超时率影响 (10%)
        timeout_rate = metrics["timeout_count"] / max(metrics["total_requests"], 1)
        score -= timeout_rate * 10

        # 限制分数范围
        metrics["quality_score"] = max(0, min(100, score))

        # 更新可靠性趋势
        if metrics["quality_score"] > 80:
            metrics["reliability_trend"] = "improving"
        elif metrics["quality_score"] < 60:
            metrics["reliability_trend"] = "declining"
        else:
            metrics["reliability_trend"] = "stable"

    def _generate_request_id(self) -> str:
        """生成请求ID"""
        return f"req_{int(time.time())}_{hashlib.md5(str(time.time()).encode()).hexdigest()[:8]}"

    def get_service_quality(self, service_name: str) -> Dict:
        """获取服务质量报告"""
        if service_name not in self.quality_metrics:
            return {"error": "Service not found"}

        metrics = self.quality_metrics[service_name]
        enhanced_service = self.enhanced_services.get(service_name)

        return {
            "service_name": service_name,
            "quality_score": metrics["quality_score"],
            "reliability_trend": metrics["reliability_trend"],
            "total_requests": metrics["total_requests"],
            "success_rate": metrics["successful_requests"] / max(metrics["total_requests"], 1),
            "avg_response_time": metrics["avg_response_time"],
            "error_rate": metrics["error_count"] / max(metrics["total_requests"], 1),
            "timeout_rate": metrics["timeout_count"] / max(metrics["total_requests"], 1),
            "security_incidents": metrics["security_incidents"],
            "diyi_evaluation": enhanced_service.get_diyi_evaluation() if enhanced_service else None
        }

    def get_all_services_quality(self) -> Dict:
        """获取所有服务质量报告"""
        return {
            service_name: self.get_service_quality(service_name)
            for service_name in self.quality_metrics.keys()
        }

    def optimize_service_routing(self) -> Dict:
        """优化服务路由"""
        routing_optimization = {
            "timestamp": datetime.now().isoformat(),
            "recommendations": [],
            "route_changes": [],
            "performance_impact": {}
        }

        # 分析每个服务的性能
        for service_name, quality in self.get_all_services_quality().items():
            if quality["quality_score"] < 70:
                # 低质量服务，需要优化
                routing_optimization["recommendations"].append({
                    "service": service_name,
                    "issue": f"Low quality score ({quality['quality_score']:.1f})",
                    "action": "Consider replacement or optimization"
                })

            # 评估性能影响
            if quality["success_rate"] < 0.9:
                impact = f"Service {service_name} has {quality['success_rate']:.1%} success rate"
                routing_optimization["performance_impact"][service_name] = impact

        # 添加路由变更建议
        for service_name in self.quality_metrics:
            if self.quality_metrics[service_name]["reliability_trend"] == "declining":
                routing_optimization["route_changes"].append({
                    "service": service_name,
                    "change": "Demote from primary to backup",
                    "reason": "Reliability declining"
                })

        return routing_optimization


class EnhancedMCPService:
    """增强的MCP服务"""

    def __init__(self, service_name: str, enhancer: MCPEnhancer):
        self.service_name = service_name
        self.enhancer = enhancer
        self.original_service = enhancer.fusion_engine.mcp_services[service_name]
        self.request_history = []
        self.performance_stats = {
            "avg_response_time": 0.0,
            "success_rate": 1.0,
            "error_count": 0
        }

    async def execute_request(self, request_data: Dict, timeout: float) -> Dict:
        """执行增强的请求"""
        # 这里应该调用实际的MCP服务
        # 临时模拟实现
        await asyncio.sleep(0.1)  # 模拟延迟

        # 模拟不同服务的响应
        if self.service_name == "filesystem":
            return {
                "success": True,
                "data": {
                    "files": ["file1.txt", "file2.md"],
                    "directories": ["docs", "images"]
                }
            }
        elif self.service_name == "github":
            return {
                "success": True,
                "data": {
                    "repos": ["repo1", "repo2"],
                    "issues": 5,
                    "pulls": 2
                }
            }
        elif self.service_name == "fetch":
            return {
                "success": True,
                "data": {
                    "content": "Sample web content",
                    "status": 200,
                    "headers": {"content-type": "text/html"}
                }
            }
        else:
            return {"success": True, "data": {"message": f"Request to {self.service_name} successful"}}

    def monitor_quality(self):
        """监控服务质量"""
        while True:
            # 更新性能统计
            self._update_performance_stats()

            # 检查异常
            self._check_anomalies()

            # 休眠30秒
            time.sleep(30)

    def _update_performance_stats(self):
        """更新性能统计"""
        metrics = self.enhancer.quality_metrics[self.service_name]

        # 计算平均响应时间
        total_requests = metrics["total_requests"]
        if total_requests > 0:
            self.performance_stats["avg_response_time"] = (
                metrics["avg_response_time"] * (total_requests - 1) +
                metrics["response_time"]
            ) / total_requests

        # 计算成功率
        self.performance_stats["success_rate"] = (
            metrics["successful_requests"] / max(total_requests, 1)
        )

        self.performance_stats["error_count"] = metrics["error_count"]

    def _check_anomalies(self):
        """检查异常情况"""
        metrics = self.enhancer.quality_metrics[self.service_name]

        # 检查错误率过高
        if metrics["total_requests"] > 10:
            error_rate = metrics["error_count"] / metrics["total_requests"]
            if error_rate > 0.3:
                print(f"⚠️ {self.service_name} has high error rate: {error_rate:.1%}")

        # 检查响应时间过长
        if metrics["avg_response_time"] > 10.0:
            print(f"⚠️ {self.service_name} response time too long: {metrics['avg_response_time']:.1f}s")

        # 检查超时率过高
        if metrics["total_requests"] > 5:
            timeout_rate = metrics["timeout_count"] / metrics["total_requests"]
            if timeout_rate > 0.2:
                print(f"⚠️ {self.service_name} has high timeout rate: {timeout_rate:.1%}")

    def get_diyi_evaluation(self) -> Dict:
        """获取帝意评估"""
        try:
            # 获取服务的最新评估
            evaluation = self.enhancer.fusion_engine.diyi_brain.evaluate_agent(
                f"mcp_{self.service_name}"
            )

            # 根据质量指标调整评分
            metrics = self.enhancer.quality_metrics[self.service_name]
            quality_factor = metrics["quality_score"] / 100

            # 调整各项维度
            adjusted_scores = {}
            for dimension, score in evaluation["dimension_scores"].items():
                adjusted_scores[dimension] = int(score * quality_factor)

            return {
                "original_evaluation": evaluation,
                "quality_adjusted_scores": adjusted_scores,
                "quality_score": metrics["quality_score"],
                "reliability_trend": metrics["reliability_trend"]
            }
        except Exception as e:
            return {"error": str(e)}


# 使用示例
if __name__ == "__main__":
    # 模拟融合引擎
    class MockFusionEngine:
        def __init__(self):
            self.mcp_services = {
                "filesystem": None,  # 实际初始化时会填充
                "github": None,
                "fetch": None
            }

    # 创建增强层
    fusion_engine = MockFusionEngine()
    enhancer = MCPEnhancer(fusion_engine)

    # 模拟执行请求
    async def test_requests():
        # 测试文件系统服务
        result1 = await enhancer.execute_enhanced_request(
            "filesystem",
            {"operation": "list", "path": "/tmp"}
        )
        print("文件系统请求结果:", result1)

        # 测试GitHub服务
        result2 = await enhancer.execute_enhanced_request(
            "github",
            {"operation": "list_repos"}
        )
        print("GitHub请求结果:", result2)

        # 获取质量报告
        quality_report = enhancer.get_service_quality("filesystem")
        print("文件系统质量报告:", quality_report)

    # 运行测试
    asyncio.run(test_requests())

    # 获取所有服务质量
    all_quality = enhancer.get_all_services_quality()
    print("\n所有服务质量报告:")
    for service, quality in all_quality.items():
        print(f"{service}: {quality['quality_score']:.1f}分")
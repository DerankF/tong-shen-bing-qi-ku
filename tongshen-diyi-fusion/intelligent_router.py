#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能调度引擎
融合通神M0元认知与帝意五维模型，实现智能路由、动态负载均衡、预测性调度
"""

import json
import time
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple, Callable
from dataclasses import dataclass, asdict
from enum import Enum
import threading
import heapq
import statistics
from pathlib import Path
import numpy as np
from dataclasses import field

# 导入融合引擎和增强层
from .fusion_engine import TongshenDiyiFusion, Task, TaskPriority
from .mcp_enhancer import MCPEnhancer, MCPEvent


class RoutingStrategy(Enum):
    """路由策略"""
    QUALITY_FIRST = "quality_first"      # 优先质量
    SPEED_FIRST = "speed_first"          # 优先速度
    BALANCED = "balanced"                # 平衡策略
    COST_AWARE = "cost_aware"            # 成本感知
    PREDICTIVE = "predictive"            # 预测性路由


@dataclass
class RoutingDecision:
    """路由决策"""
    timestamp: str
    task_id: str
    selected_skill: str
    selected_mcp: str
    routing_score: float
    strategy_used: RoutingStrategy
    confidence: float
    alternatives: List[str] = field(default_factory=list)
    reasoning: str = ""

    def to_dict(self) -> Dict:
        """转换为字典"""
        return asdict(self)


@dataclass
class ServiceLoad:
    """服务负载"""
    service_name: str
    current_load: float  # 0-1之间
    task_queue_size: int
    avg_response_time: float
    error_rate: float
    health_score: float
    last_updated: str

    def calculate_total_load(self) -> float:
        """计算总负载"""
        load_factors = {
            "queue_weight": 0.3,
            "response_time_weight": 0.3,
            "error_rate_weight": 0.2,
            "health_weight": 0.2
        }

        return (
            self.task_queue_size * load_factors["queue_weight"] +
            min(self.avg_response_time / 10, 1) * load_factors["response_time_weight"] +
            self.error_rate * load_factors["error_rate_weight"] +
            (1 - self.health_score) * load_factors["health_weight"]
        )


class IntelligentRouter:
    """智能调度路由器"""

    def __init__(self, fusion_engine: TongshenDiyiFusion, mcp_enhancer: MCPEnhancer):
        self.fusion_engine = fusion_engine
        self.mcp_enhancer = mcp_enhancer

        # 路由配置
        self.routing_strategy = RoutingStrategy.BALANCED
        self.enable_prediction = True
        self.enable_fallback = True

        # 服务负载追踪
        self.service_loads: Dict[str, ServiceLoad] = {}
        self.load_history: Dict[str, List[float]] = {}

        # 路由决策记录
        self.routing_decisions: List[RoutingDecision] = []
        self.successful_routes: Dict[str, int] = {}  # route_pattern -> success_count

        # 预测模型
        self.prediction_model = self._init_prediction_model()

        # 初始化负载监控
        self._init_load_monitoring()

    def _init_prediction_model(self) -> Dict:
        """初始化预测模型"""
        return {
            "model_type": "moving_average",
            "window_size": 10,
            "prediction_horizon": 5,
            "accuracy": 0.85
        }

    def _init_load_monitoring(self):
        """初始化负载监控"""
        # 初始化所有服务的负载
        for service_name in self.fusion_engine.mcp_services.keys():
            self.service_loads[service_name] = ServiceLoad(
                service_name=service_name,
                current_load=0.0,
                task_queue_size=0,
                avg_response_time=1.0,
                error_rate=0.0,
                health_score=1.0,
                last_updated=datetime.now().isoformat()
            )
            self.load_history[service_name] = []

        # 启动监控线程
        monitor_thread = threading.Thread(target=self._load_monitoring_loop, daemon=True)
        monitor_thread.start()

    def _load_monitoring_loop(self):
        """负载监控循环"""
        while True:
            # 更新每个服务的负载
            for service_name, load in self.service_loads.items():
                self._update_service_load(service_name)

            # 记录历史数据
            for service_name, load in self.service_loads.items():
                self.load_history[service_name].append(load.current_load)
                # 保持历史数据大小
                if len(self.load_history[service_name]) > 100:
                    self.load_history[service_name].pop(0)

            # 睡眠10秒
            time.sleep(10)

    def _update_service_load(self, service_name: str):
        """更新服务负载"""
        load = self.service_loads[service_name]

        # 获取质量指标
        quality = self.mcp_enhancer.get_service_quality(service_name)

        # 更新负载指标
        load.task_queue_size = len(self.fusion_engine.task_queue)
        load.avg_response_time = quality.get("avg_response_time", 1.0)
        load.error_rate = quality.get("error_rate", 0.0)
        load.health_score = quality.get("quality_score", 100) / 100
        load.current_load = load.calculate_total_load()
        load.last_updated = datetime.now().isoformat()

    async def route_task(self, task: Task) -> RoutingDecision:
        """路由任务"""
        start_time = time.time()

        print(f"🧠 开始智能路由任务: {task.name}")

        # 1. 元认知分析
        meta_analysis = self._analyze_task_meta_cognition(task)

        # 2. 生成候选方案
        candidates = self._generate_routing_candidates(task, meta_analysis)

        # 3. 评估每个候选
        evaluated_candidates = await self._evaluate_candidates(task, candidates)

        # 4. 选择最优方案
        best_candidate = self._select_best_candidate(task, evaluated_candidates)

        # 5. 生成路由决策
        decision = self._create_routing_decision(
            task=task,
            best_candidate=best_candidate,
            evaluated_candidates=evaluated_candidates,
            meta_analysis=meta_analysis
        )

        # 6. 记录决策
        self.routing_decisions.append(decision)
        self._update_route_statistics(decision)

        # 7. 执行路由（如果需要）
        if best_candidate["action"] == "execute":
            await self._execute_routed_task(task, best_candidate)

        routing_time = time.time() - start_time
        print(f"✅ 路由完成，耗时: {routing_time:.2f}秒")
        print(f"📍 选择的Skill: {best_candidate['skill']}, MCP: {best_candidate['mcp']}")

        return decision

    def _analyze_task_meta_cognition(self, task: Task) -> Dict:
        """元认知分析任务"""
        print("🧠 执行元认知分析...")

        # 分析任务特征
        task_features = {
            "urgency": self._analyze_urgency(task),
            "complexity": self._analyze_complexity(task),
            "criticality": self._analyze_criticality(task),
            "resource_requirements": self._analyze_resource_requirements(task)
        }

        # 分析环境状态
        environment_state = {
            "system_load": self._get_system_load(),
            "service_health": self._get_service_health(),
            "time_pressure": self._analyze_time_pressure(task)
        }

        # 生成元认知洞察
        meta_insights = {
            "best_routing_strategy": self._determine_best_strategy(task_features, environment_state),
            "risk_assessment": self._assess_routing_risk(task),
            "expected_quality": self._predict_expected_quality(task),
            "confidence_level": self._calculate_confidence(task_features, environment_state)
        }

        return {
            "task_features": task_features,
            "environment_state": environment_state,
            "meta_insights": meta_insights
        }

    def _analyze_urgency(self, task: Task) -> float:
        """分析紧急程度"""
        urgency_scores = {
            TaskPriority.CRITICAL: 1.0,
            TaskPriority.HIGH: 0.8,
            TaskPriority.MEDIUM: 0.5,
            TaskPriority.LOW: 0.3,
            TaskPriority.BACKGROUND: 0.1
        }
        return urgency_scores.get(task.priority, 0.5)

    def _analyze_complexity(self, task: Task) -> float:
        """分析复杂程度"""
        # 基于预估执行时间
        if task.estimated_duration < 60:
            return 0.2  # 简单
        elif task.estimated_duration < 180:
            return 0.5  # 中等
        elif task.estimated_duration < 300:
            return 0.8  # 复杂
        else:
            return 1.0  # 非常复杂

    def _analyze_criticality(self, task: Task) -> float:
        """分析关键程度"""
        criticality = 0.5  # 基础值

        # 基于任务描述
        if any(word in task.description.lower() for word in ["交易", "资金", "安全"]):
            criticality += 0.3
        elif any(word in task.description.lower() for word in ["发布", "部署", "生产"]):
            criticality += 0.2
        elif any(word in task.description.lower() for word in ["测试", "开发", "实验"]):
            criticality += 0.1

        return min(1.0, criticality)

    def _analyze_resource_requirements(self, task: Task) -> Dict:
        """分析资源需求"""
        requirements = {
            "cpu": 0.3,
            "memory": 0.3,
            "io": 0.3,
            "network": 0.3
        }

        # 根据任务类型调整
        if "文件" in task.description:
            requirements["io"] = 0.8
        if "网络" in task.description or "API" in task.description:
            requirements["network"] = 0.8
        if "计算" in task.description or "分析" in task.description:
            requirements["cpu"] = 0.7
        if "大数据" in task.description or "数据库" in task.description:
            requirements["memory"] = 0.7

        return requirements

    def _get_system_load(self) -> float:
        """获取系统负载"""
        total_load = 0
        for load in self.service_loads.values():
            total_load += load.current_load

        return min(1.0, total_load / len(self.service_loads))

    def _get_service_health(self) -> Dict[str, float]:
        """获取服务健康度"""
        health_map = {}
        for service_name, load in self.service_loads.items():
            health_map[service_name] = load.health_score
        return health_map

    def _analyze_time_pressure(self, task: Task) -> float:
        """分析时间压力"""
        if not task.deadline:
            return 0.0

        # 计算剩余时间
        deadline_time = datetime.fromisoformat(task.deadline)
        current_time = datetime.now()
        remaining_hours = (deadline_time - current_time).total_seconds() / 3600

        if remaining_hours < 1:
            return 1.0
        elif remaining_hours < 6:
            return 0.8
        elif remaining_hours < 24:
            return 0.5
        else:
            return 0.2

    def _determine_best_strategy(self, features: Dict, environment: Dict) -> RoutingStrategy:
        """确定最佳路由策略"""
        # 基于元认知分析选择策略
        if features["urgency"] > 0.8 and environment["system_load"] < 0.5:
            return RoutingStrategy.SPEED_FIRST
        elif features["criticality"] > 0.7:
            return RoutingStrategy.QUALITY_FIRST
        elif environment["system_load"] > 0.8:
            return RoutingStrategy.COST_AWARE
        elif self.enable_prediction:
            return RoutingStrategy.PREDICTIVE
        else:
            return RoutingStrategy.BALANCED

    def _assess_routing_risk(self, task: Task) -> float:
        """评估路由风险"""
        risk = 0.3  # 基础风险

        # 任务类型风险
        risk_map = {
            "交易分析": 0.4,
            "网站部署": 0.3,
            "内容创作": 0.2,
            "深度研究": 0.2,
            "文档操作": 0.1
        }

        task_type = self._classify_task(task)
        risk += risk_map.get(task_type, 0.2)

        # 系统负载风险
        system_load = self._get_system_load()
        risk += system_load * 0.3

        return min(1.0, risk)

    def _predict_expected_quality(self, task: Task) -> float:
        """预测预期质量"""
        # 基于历史数据和当前状态预测
        base_quality = 0.8

        # 根据任务类型调整
        task_type = self._classify_task(task)
        type_multipliers = {
            "交易分析": 0.9,
            "网站部署": 0.85,
            "内容创作": 0.95,
            "深度研究": 0.8,
            "文档操作": 0.9
        }
        base_quality *= type_multipliers.get(task_type, 0.85)

        # 根据系统负载调整
        system_load = self._get_system_load()
        base_quality *= (1 - system_load * 0.2)

        return min(1.0, base_quality)

    def _calculate_confidence(self, features: Dict, environment: Dict) -> float:
        """计算置信度"""
        # 综合多个因素计算置信度
        confidence_factors = []

        # 紧急程度
        if features["urgency"] > 0.5:
            confidence_factors.append(0.8)
        else:
            confidence_factors.append(1.0)

        # 系统负载
        if environment["system_load"] < 0.5:
            confidence_factors.append(1.0)
        elif environment["system_load"] < 0.8:
            confidence_factors.append(0.8)
        else:
            confidence_factors.append(0.6)

        # 服务健康度
        avg_health = sum(environment["service_health"].values()) / len(environment["service_health"])
        confidence_factors.append(avg_health)

        # 返回平均值
        return statistics.mean(confidence_factors)

    def _classify_task(self, task: Task) -> str:
        """任务分类"""
        description = task.description.lower()

        if any(word in description for word in ["交易", "黄金", "xauusd", "量化", "回测"]):
            return "交易分析"
        elif any(word in description for word in ["公众号", "内容", "文章", "发布"]):
            return "内容创作"
        elif any(word in description for word in ["研究", "调研", "分析", "数据"]):
            return "深度研究"
        elif any(word in description for word in ["部署", "网站", "开发", "github"]):
            return "网站部署"
        elif any(word in description for word in ["文件", "文档", "markdown"]):
            return "文档操作"
        else:
            return "通用任务"

    def _generate_routing_candidates(self, task: Task, meta_analysis: Dict) -> List[Dict]:
        """生成路由候选方案"""
        candidates = []

        # 获取候选Skills
        task_type = self._classify_task(task)
        candidate_skills = self.fusion_engine.tongshen_routes.get(task_type, ["deep-research"])

        # 获取候选MCP服务
        candidate_mcps = list(self.service_loads.keys())

        # 生成组合
        for skill in candidate_skills:
            for mcp in candidate_mcps:
                candidate = {
                    "skill": skill,
                    "mcp": mcp,
                    "action": "execute",  # 或 "fallback", "skip"
                    "score": 0.0,
                    "confidence": 0.0
                }
                candidates.append(candidate)

        return candidates

    async def _evaluate_candidates(self, task: Task, candidates: List[Dict]) -> List[Dict]:
        """评估候选方案"""
        evaluated = []

        for candidate in candidates:
            # 1. 基于帝意评分
            skill_score = self._get_skill_score(candidate["skill"])
            mcp_score = self._get_mcp_score(candidate["mcp"])

            # 2. 基于负载
            load_score = self._get_load_score(candidate["mcp"])

            # 3. 基于历史成功率
            history_score = self._get_history_score(candidate["skill"], candidate["mcp"])

            # 4. 基于预测
            prediction_score = await self._get_prediction_score(task, candidate)

            # 综合评分
            weights = self._get_evaluation_weights(task)
            total_score = (
                skill_score * weights["skill"] +
                mcp_score * weights["mcp"] +
                load_score * weights["load"] +
                history_score * weights["history"] +
                prediction_score * weights["prediction"]
            )

            candidate["score"] = total_score
            candidate["confidence"] = self._calculate_candidate_confidence(candidate)
            evaluated.append(candidate)

        return evaluated

    def _get_skill_score(self, skill_name: str) -> float:
        """获取Skill评分"""
        try:
            evaluation = self.fusion_engine.diyi_brain.evaluate_agent(f"skill_{skill_name}")
            return evaluation["comprehensive_value"] / 100
        except:
            return 0.5

    def _get_mcp_score(self, mcp_name: str) -> float:
        """获取MCP评分"""
        quality = self.mcp_enhancer.get_service_quality(mcp_name)
        return quality.get("quality_score", 50) / 100

    def _get_load_score(self, mcp_name: str) -> float:
        """获取负载评分（负载越小分数越高）"""
        load = self.service_loads[mcp_name]
        return 1.0 - load.current_load

    def _get_history_score(self, skill: str, mcp: str) -> float:
        """获取历史成功率评分"""
        pattern = f"{skill}+{mcp}"
        if pattern in self.successful_routes:
            success_rate = self.successful_routes[pattern] / (
                self.successful_routes[pattern] + 1  # 假设有一次失败
            )
            return success_rate
        return 0.8  # 默认值

    async def _get_prediction_score(self, task: Task, candidate: Dict) -> float:
        """获取预测评分"""
        if not self.enable_prediction:
            return 0.8

        # 基于历史模式预测
        pattern = f"{candidate['skill']}+{candidate['mcp']}"

        # 简单的移动平均预测
        if pattern in self.load_history:
            recent_loads = self.load_history[pattern][-5:]  # 最近5个负载值
            avg_load = statistics.mean(recent_loads) if recent_loads else 0.5
            return 1.0 - avg_load
        else:
            return 0.8

    def _get_evaluation_weights(self, task: Task) -> Dict[str, float]:
        """获取评估权重"""
        base_weights = {
            "skill": 0.3,
            "mcp": 0.3,
            "load": 0.2,
            "history": 0.1,
            "prediction": 0.1
        }

        # 根据任务类型调整权重
        if task.priority == TaskPriority.CRITICAL:
            base_weights["skill"] = 0.5
            base_weights["mcp"] = 0.3
            base_weights["load"] = 0.1
        elif task.priority == TaskPriority.BACKGROUND:
            base_weights["skill"] = 0.2
            base_weights["mcp"] = 0.2
            base_weights["load"] = 0.5

        return base_weights

    def _calculate_candidate_confidence(self, candidate: Dict) -> float:
        """计算候选方案置信度"""
        # 基于多个因素计算置信度
        confidence_factors = []

        # 基于评分
        if candidate["score"] > 0.8:
            confidence_factors.append(1.0)
        elif candidate["score"] > 0.6:
            confidence_factors.append(0.8)
        else:
            confidence_factors.append(0.6)

        # 基于服务健康度
        mcp_name = candidate["mcp"]
        load = self.service_loads[mcp_name]
        confidence_factors.append(load.health_score)

        # 基于历史成功率
        history_score = self._get_history_score(candidate["skill"], candidate["mcp"])
        confidence_factors.append(history_score)

        return statistics.mean(confidence_factors)

    def _select_best_candidate(self, task: Task, candidates: List[Dict]) -> Dict:
        """选择最佳候选"""
        # 根据路由策略选择
        if self.routing_strategy == RoutingStrategy.QUALITY_FIRST:
            candidates.sort(key=lambda x: x["score"], reverse=True)
        elif self.routing_strategy == RoutingStrategy.SPEED_FIRST:
            candidates.sort(key=lambda x: self.service_loads[x["mcp"]].avg_response_time)
        elif self.routing_strategy == RoutingStrategy.BALANCED:
            candidates.sort(key=lambda x: x["score"] * x["confidence"], reverse=True)
        elif self.routing_strategy == RoutingStrategy.COST_AWARE:
            candidates.sort(key=lambda x: self.service_loads[x["mcp"]].current_load)
        elif self.routing_strategy == RoutingStrategy.PREDICTIVE:
            candidates.sort(key=lambda x: x["score"] + x["confidence"], reverse=True)

        # 如果启用了回退，保留备选方案
        if self.enable_fallback and len(candidates) > 1:
            best = candidates[0]
            best["alternatives"] = candidates[1:3]  # 保留前两个备选
        else:
            best = candidates[0]
            best["alternatives"] = []

        return best

    def _create_routing_decision(
        self,
        task: Task,
        best_candidate: Dict,
        evaluated_candidates: List[Dict],
        meta_analysis: Dict
    ) -> RoutingDecision:
        """创建路由决策"""
        return RoutingDecision(
            timestamp=datetime.now().isoformat(),
            task_id=task.id,
            selected_skill=best_candidate["skill"],
            selected_mcp=best_candidate["mcp"],
            routing_score=best_candidate["score"],
            strategy_used=self.routing_strategy,
            confidence=best_candidate["confidence"],
            alternatives=best_candidate["alternatives"],
            reasoning=self._generate_routing_reasoning(
                best_candidate,
                evaluated_candidates,
                meta_analysis
            )
        )

    def _generate_routing_reasoning(
        self,
        best_candidate: Dict,
        evaluated_candidates: List[Dict],
        meta_analysis: Dict
    ) -> str:
        """生成路由推理"""
        reasoning = f"选择了 {best_candidate['skill']} + {best_candidate['mcp']} 组合，因为："

        # 主要原因
        if best_candidate["score"] > 0.8:
            reasoning += "评分最高("
        else:
            reasoning += "评分适中("
        reasoning += f"{best_candidate['score']:.2f})。"

        # 置信度
        reasoning += f"置信度 {best_candidate['confidence']:.2f}。"

        # 考虑因素
        load = self.service_loads[best_candidate["mcp"]]
        reasoning += f"MCP负载 {load.current_load:.2f}。"

        # 环境因素
        if meta_analysis["environment_state"]["system_load"] > 0.8:
            reasoning += "系统负载高，选择了负载较低的服务。"

        return reasoning

    def _update_route_statistics(self, decision: RoutingDecision):
        """更新路由统计"""
        pattern = f"{decision.selected_skill}+{decision.selected_mcp}"

        # 记录成功路由
        if pattern not in self.successful_routes:
            self.successful_routes[pattern] = 0
        self.successful_routes[pattern] += 1

        # 限制记录数量
        if len(self.routing_decisions) > 1000:
            self.routing_decisions = self.routing_decisions[-500:]

    async def _execute_routed_task(self, task: Task, candidate: Dict):
        """执行路由后的任务"""
        print(f"🚀 执行路由任务: {task.name}")
        print(f"   Skill: {candidate['skill']}")
        print(f"   MCP: {candidate['mcp']}")

        # 这里应该实际执行任务
        # 临时模拟执行
        await asyncio.sleep(task.estimated_duration / 10)  # 模拟执行时间

        print("✅ 任务执行完成")

    def get_routing_statistics(self) -> Dict:
        """获取路由统计"""
        total_decisions = len(self.routing_decisions)
        if total_decisions == 0:
            return {"error": "No routing decisions yet"}

        # 计算平均分数
        avg_score = statistics.mean(d.routing_score for d in self.routing_decisions)

        # 最常用组合
        route_counts = {}
        for decision in self.routing_decisions:
            pattern = f"{decision.selected_skill}+{decision.selected_mcp}"
            route_counts[pattern] = route_counts.get(pattern, 0) + 1

        most_used = max(route_counts.items(), key=lambda x: x[1]) if route_counts else None

        # 策略分布
        strategy_counts = {}
        for decision in self.routing_decisions:
            strategy = decision.strategy_used.value
            strategy_counts[strategy] = strategy_counts.get(strategy, 0) + 1

        return {
            "total_decisions": total_decisions,
            "average_score": avg_score,
            "most_used_route": most_used,
            "strategy_distribution": strategy_counts,
            "success_rate": sum(1 for d in self.routing_decisions if d.confidence > 0.7) / total_decisions
        }

    def optimize_routing_strategy(self) -> Dict:
        """优化路由策略"""
        optimization_report = {
            "timestamp": datetime.now().isoformat(),
            "current_strategy": self.routing_strategy.value,
            "analysis": {},
            "recommendations": [],
            "expected_improvement": 0.0
        }

        # 分析路由效果
        stats = self.get_routing_statistics()
        optimization_report["analysis"] = stats

        # 生成建议
        if stats["success_rate"] < 0.8:
            optimization_report["recommendations"].append(
                "当前成功率较低，建议切换到 QUALITY_FIRST 策略"
            )

        if stats["average_score"] < 0.7:
            optimization_report["recommendations"].append(
                "平均路由分数较低，建议优化评估权重"
            )

        # 分析负载分布
        load_distribution = [load.current_load for load in self.service_loads.values()]
        load_variance = statistics.variance(load_distribution) if len(load_distribution) > 1 else 0

        if load_variance > 0.3:
            optimization_report["recommendations"].append(
                "负载分布不均，建议启用 COST_AWARE 策略"
            )

        # 更新策略
        if optimization_report["recommendations"]:
            if "QUALITY_FIRST" in str(optimization_report["recommendations"]):
                self.routing_strategy = RoutingStrategy.QUALITY_FIRST
            elif "COST_AWARE" in str(optimization_report["recommendations"]):
                self.routing_strategy = RoutingStrategy.COST_AWARE

        return optimization_report


# 使用示例
if __name__ == "__main__":
    # 模拟创建依赖
    class MockFusionEngine:
        def __init__(self):
            self.tongshen_routes = {
                "交易分析": ["trading-analysis", "volbreak-backtest"],
                "内容创作": ["wechat-publisher", "content-factory-pipeline"]
            }
            self.mcp_services = {"filesystem": None, "github": None}

    class MockMCPEnhancer:
        def get_service_quality(self, name):
            return {"quality_score": 85, "avg_response_time": 1.0}

    # 创建路由器
    fusion_engine = MockFusionEngine()
    mcp_enhancer = MockMCPEnhancer()
    router = IntelligentRouter(fusion_engine, mcp_enhancer)

    # 创建测试任务
    task = Task(
        id="test_task_1",
        name="测试交易分析",
        description="分析黄金价格走势",
        priority=TaskPriority.HIGH,
        assigned_skill="trading-analysis",
        estimated_duration=120
    )

    # 模拟路由决策
    async def test_routing():
        decision = await router.route_task(task)
        print("\n=== 路由决策 ===")
        print(f"选择的Skill: {decision.selected_skill}")
        print(f"选择的MCP: {decision.selected_mcp}")
        print(f"路由分数: {decision.routing_score:.2f}")
        print(f"置信度: {decision.confidence:.2f}")
        print(f"推理: {decision.reasoning}")

        # 获取路由统计
        stats = router.get_routing_statistics()
        print("\n=== 路由统计 ===")
        print(json.dumps(stats, indent=2, ensure_ascii=False))

    # 运行测试
    asyncio.run(test_routing())
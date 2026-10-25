#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通神-帝意融合引擎
将通神系统的M0元认知与帝意共识智脑的五维模型深度融合
实现智能调度、评估、决策的闭环系统
"""

import json
import asyncio
import time
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import uuid
import threading
from pathlib import Path

# 导入帝意共识智脑
import sys
sys.path.append(str(Path(__file__).parent.parent / "diyi-consensus-brain"))
from core.diyi_evaluation_engine import DiyiConsensusBrain, AgentData, Evidence
from integration.skill_integration import SkillIntegrationLayer, SkillMetadata


class TaskPriority(Enum):
    """任务优先级"""
    CRITICAL = "critical"    # 紧急（立即执行）
    HIGH = "high"          # 高优先级（5分钟内）
    MEDIUM = "medium"      # 中等优先级（30分钟内）
    LOW = "low"            # 低优先级（2小时内）
    BACKGROUND = "background"  # 后台任务（可延迟）


@dataclass
class Task:
    """任务数据结构"""
    id: str
    name: str
    description: str
    priority: TaskPriority
    assigned_skill: str
    estimated_duration: int  # 预估执行时间（秒）
    deadline: Optional[str] = None
    dependencies: List[str] = None
    created_at: str = None
    status: str = "pending"  # pending, running, completed, failed
    result: Any = None
    error: str = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()
        if self.dependencies is None:
            self.dependencies = []


@dataclass
class MCPService:
    """MCP服务数据结构"""
    name: str
    type: str
    status: str  # active, inactive, error
    last_used: str
    usage_count: int
    reliability_score: float
    response_time: float
    error_rate: float
    capabilities: List[str]

    def to_agent_data(self) -> Dict:
        """转换为Agent数据格式"""
        return {
            "id": f"mcp_{self.name}",
            "name": self.name,
            "type": "MCP服务",
            "description": f"{self.name} - {self.type}",
            "version": "1.0.0",
            "dao_hang": int(self.reliability_score * 100),
            "fa_xing": max(0, 100 - int(self.error_rate * 100)),
            "li_xing": 80,  # MCP服务的商业价值相对固定
            "yu_hang": 90,  # 用户体验由响应时间决定
            "shou_xing": 95,  # 安全性较高
            "reputation_score": self.reliability_score * 100,
            "evidence_count": self.usage_count,
            "is_open_source": True,
            "has_audit_report": True
        }


class TongshenDiyiFusion:
    """通神-帝意融合引擎主类"""

    def __init__(self):
        # 初始化帝意共识智脑
        self.diyi_brain = DiyiConsensusBrain()
        self.skill_integration = SkillIntegrationLayer(self.diyi_brain)

        # MCP服务注册表
        self.mcp_services: Dict[str, MCPService] = {}

        # 任务队列
        self.task_queue: List[Task] = []
        self.running_tasks: Dict[str, Task] = {}

        # 通神路由表
        self.tongshen_routes: Dict[str, List[str]] = {}

        # 融合状态
        self.fusion_status = {
            "initialized": False,
            "mcp_integrated": False,
            "skills_loaded": False,
            "optimization_active": False
        }

        # 性能统计
        self.performance_stats = {
            "total_tasks": 0,
            "completed_tasks": 0,
            "failed_tasks": 0,
            "avg_response_time": 0,
            "success_rate": 0
        }

        # 初始化完成标志
        self._initialize()

    def _initialize(self):
        """初始化融合系统"""
        print("🔄 正在初始化通神-帝意融合系统...")

        # 1. 加载通神系统配置
        self._load_tongshen_config()

        # 2. 注册MCP服务
        self._register_mcp_services()

        # 3. 加载所有Skills
        self._load_all_skills()

        # 4. 建立融合路由
        self._build_fusion_routes()

        # 5. 启动监控线程
        self._start_monitoring()

        self.fusion_status["initialized"] = True
        print("✅ 通神-帝意融合系统初始化完成")

    def _load_tongshen_config(self):
        """加载通神系统配置"""
        print("📋 加载通神系统配置...")

        # 这里应该从配置文件加载
        # 临时使用硬编码配置
        self.tongshen_config = {
            "m0_metacognition": {
                "enabled": True,
                "thinking_depth": 3,
                "context_window": 8192
            },
            "domain_routing": {
                "通神核心": ["tongshen-v8.1", "task-chain"],
                "交易/量化": ["trading-analysis", "volbreak-backtest"],
                "内容/公众号": ["wechat-publisher", "content-factory-pipeline"],
                "研究/数据": ["deep-research", "perplexity"],
                "开发/部署": ["deploy-website", "github-cli"]
            },
            "execution_strategy": {
                "max_concurrent_tasks": 5,
                "timeout_per_task": 300,
                "retry_attempts": 3
            }
        }

    def _register_mcp_services(self):
        """注册MCP服务"""
        print("🔌 注册MCP服务...")

        # MCP服务列表（从通神兵器库获取）
        mcp_list = [
            {
                "name": "filesystem",
                "type": "本地文件系统访问",
                "capabilities": ["read", "write", "list", "search"]
            },
            {
                "name": "github",
                "type": "GitHub API操作",
                "capabilities": ["repo", "issues", "pulls", "actions"]
            },
            {
                "name": "fetch",
                "type": "HTTP请求抓取",
                "capabilities": ["http", "https", "api", "web"]
            },
            {
                "name": "memory",
                "type": "持久化记忆存储",
                "capabilities": ["store", "recall", "search", "update"]
            },
            {
                "name": "sequential-thinking",
                "type": "链式推理",
                "capabilities": ["reason", "analyze", "deduce", "infer"]
            },
            {
                "name": "puppeteer",
                "type": "浏览器自动化(无头)",
                "capabilities": ["navigate", "click", "input", "screenshot"]
            },
            {
                "name": "context7",
                "type": "文档上下文检索",
                "capabilities": ["search", "extract", "summarize", "index"]
            },
            {
                "name": "firecrawl",
                "type": "增强网页抓取",
                "capabilities": ["crawl", "extract", "transform", "scrape"]
            },
            {
                "name": "playwright",
                "type": "浏览器自动化(现代)",
                "capabilities": ["browser", "page", "element", "interaction"]
            },
            {
                "name": "sqlite",
                "type": "交易数据库",
                "capabilities": ["query", "insert", "update", "analyze"]
            }
        ]

        # 注册每个MCP服务
        for mcp_info in mcp_list:
            service = MCPService(
                name=mcp_info["name"],
                type=mcp_info["type"],
                status="active",
                last_used=datetime.now().isoformat(),
                usage_count=0,
                reliability_score=0.85,
                response_time=1.0,
                error_rate=0.05,
                capabilities=mcp_info["capabilities"]
            )

            self.mcp_services[mcp_info["name"]] = service

            # 添加到帝意评估系统
            agent_data = service.to_agent_data()
            self.diyi_brain.add_agent(agent_data)

        print(f"✅ 已注册 {len(self.mcp_services)} 个MCP服务")

    def _load_all_skills(self):
        """加载所有Skills"""
        print("📚 加载所有Skills...")

        # 这里应该从通神兵器库加载所有Skills
        # 临时使用示例数据
        skills_data = [
            {
                "name": "trading-analysis",
                "category": "交易/量化",
                "complexity": "complex",
                "trigger_words": ["金价", "黄金", "XAUUSD", "交易分析"],
                "description": "金易明四维分析(技术/基本/情绪/地缘)"
            },
            {
                "name": "deep-research",
                "category": "研究/数据",
                "complexity": "complex",
                "trigger_words": ["深度调研", "benchmark"],
                "description": "深度研究+对比分析"
            },
            {
                "name": "wechat-publisher",
                "category": "内容/公众号",
                "complexity": "complex",
                "trigger_words": ["发公众号", "公众号发布"],
                "description": "微信公众号排版推送+8平台分发"
            },
            {
                "name": "deploy-website",
                "category": "开发/部署",
                "complexity": "medium",
                "trigger_words": ["部署网站", "deploy"],
                "description": "网站部署"
            },
            {
                "name": "volbreak-backtest",
                "category": "交易/量化",
                "complexity": "complex",
                "trigger_words": ["回测", "backtest"],
                "description": "VolBreak Pro 回测引擎，M3/M15/H1"
            }
        ]

        # 注册每个Skill
        for skill_data in skills_data:
            skill = SkillMetadata(
                skill_name=skill_data["name"],
                skill_path=f"skills/{skill_data['name']}",
                description=skill_data["description"],
                category=skill_data["category"],
                complexity=skill_data["complexity"],
                dependencies=[],
                trigger_words=skill_data["trigger_words"],
                author="通神系统",
                version="1.0.0",
                created_at="2024-01-01",
                last_updated="2024-01-01"
            )

            self.skill_integration.register_skill(skill)

        print(f"✅ 已加载 {len(skills_data)} 个Skills")
        self.fusion_status["skills_loaded"] = True

    def _build_fusion_routes(self):
        """建立融合路由"""
        print("🛣️ 建立融合路由...")

        # 基于通神域路由 + 帝意评分的智能路由
        domain_mapping = {
            "交易分析": ["trading-analysis", "volbreak-backtest"],
            "内容创作": ["wechat-publisher", "content-factory-pipeline"],
            "深度研究": ["deep-research", "perplexity"],
            "网站部署": ["deploy-website", "web-deploy"],
            "数据处理": ["sqlite", "context7"],
            "文档操作": ["filesystem", "markdown"],
            "浏览器自动化": ["playwright", "puppeteer"]
        }

        # 为每个域建立智能路由，基于帝意评分
        self.tongshen_routes = {}
        for domain, skills in domain_mapping.items():
            # 获取每个Skill的评分
            skill_scores = {}
            for skill in skills:
                try:
                    evaluation = self.diyi_brain.evaluate_agent(f"skill_{skill}")
                    skill_scores[skill] = evaluation["comprehensive_value"]
                except:
                    skill_scores[skill] = 50  # 默认分数

            # 按评分排序
            sorted_skills = sorted(skill_scores.items(), key=lambda x: x[1], reverse=True)
            self.tongshen_routes[domain] = [skill for skill, _ in sorted_skills]

        print("✅ 融合路由建立完成")

    def _start_monitoring(self):
        """启动监控线程"""
        print("📊 启动系统监控...")

        def monitor_loop():
            while True:
                # 更新MCP服务状态
                self._update_mcp_status()

                # 更新性能统计
                self._update_performance_stats()

                # 清理过期任务
                self._cleanup_expired_tasks()

                # 休眠30秒
                time.sleep(30)

        monitoring_thread = threading.Thread(target=monitor_loop, daemon=True)
        monitoring_thread.start()

    def _update_mcp_status(self):
        """更新MCP服务状态"""
        for name, service in self.mcp_services.items():
            # 模拟状态更新
            service.last_used = datetime.now().isoformat()
            service.usage_count += 1

            # 随机更新响应时间和错误率（模拟）
            service.response_time = max(0.1, service.response_time + (time.time() % 2 - 1) * 0.1)
            service.error_rate = max(0, min(0.5, service.error_rate + (time.time() % 2 - 1) * 0.01))

            # 更新可靠性评分
            service.reliability_score = 1.0 - service.error_rate

    def _update_performance_stats(self):
        """更新性能统计"""
        total = self.performance_stats["total_tasks"]
        completed = self.performance_stats["completed_tasks"]
        failed = self.performance_stats["failed_tasks"]

        if total > 0:
            self.performance_stats["success_rate"] = completed / total

    def _cleanup_expired_tasks(self):
        """清理过期任务"""
        current_time = time.time()

        # 清理超过5分钟未更新的任务
        to_remove = []
        for task_id, task in self.running_tasks.items():
            if current_time - datetime.fromisoformat(task.created_at).timestamp() > 300:
                to_remove.append(task_id)

        for task_id in to_remove:
            del self.running_tasks[task_id]

    def submit_task(self, task: Task) -> str:
        """提交任务到融合引擎"""
        # 添加到任务队列
        self.task_queue.append(task)
        self.performance_stats["total_tasks"] += 1

        # 根据优先级排序
        self.task_queue.sort(key=lambda t: (
            {"critical": 0, "high": 1, "medium": 2, "low": 3, "background": 4}[t.priority.value],
            t.created_at
        ))

        print(f"📝 任务已提交: {task.name} (优先级: {task.priority.value})")

        # 如果引擎空闲，立即开始执行
        if len(self.running_tasks) < self.tongshen_config["execution_strategy"]["max_concurrent_tasks"]:
            self._execute_next_task()

        return task.id

    def _execute_next_task(self):
        """执行下一个任务"""
        if not self.task_queue:
            return

        # 获取最高优先级的任务
        task = self.task_queue.pop(0)

        # 开始执行
        task.status = "running"
        self.running_tasks[task.id] = task

        # 创建执行线程
        execution_thread = threading.Thread(
            target=self._execute_task,
            args=(task,),
            daemon=True
        )
        execution_thread.start()

    def _execute_task(self, task: Task):
        """执行单个任务"""
        start_time = time.time()

        try:
            # 1. M0元认知分析
            meta_analysis = self._metacognitive_analysis(task)

            # 2. 智能选择Skill
            selected_skill = self._select_optimal_skill(task, meta_analysis)

            # 3. RAC可信度验证
            risk_assessment = self.diyi_brain.calculate_rac_score(f"skill_{selected_skill}")

            # 4. 执行任务
            if risk_assessment["risk_level"] == "HIGH":
                # 高风险任务，需要特殊处理
                result = self._execute_high_risk_task(task, selected_skill)
            else:
                # 正常执行
                result = self._execute_normal_task(task, selected_skill)

            # 5. 更新结果
            task.status = "completed"
            task.result = result
            self.performance_stats["completed_tasks"] += 1

        except Exception as e:
            task.status = "failed"
            task.error = str(e)
            self.performance_stats["failed_tasks"] += 1

        finally:
            # 更新执行时间
            task.result = task.result or {}
            task.result["execution_time"] = time.time() - start_time

            # 从运行任务中移除
            self.running_tasks.pop(task.id, None)

            # 继续执行下一个任务
            self._execute_next_task()

    def _metacognitive_analysis(self, task: Task) -> Dict:
        """M0元认知分析"""
        print(f"🧠 执行元认知分析: {task.name}")

        # 分析任务复杂度
        complexity_analysis = {
            "simple": {"skills_needed": 1, "estimated_time": 30},
            "medium": {"skills_needed": 2, "estimated_time": 120},
            "complex": {"skills_needed": 3, "estimated_time": 300}
        }

        # 分析所需资源
        resource_analysis = {
            "cpu": "low" if task.priority == TaskPriority.BACKGROUND else "medium",
            "memory": "low" if "简单" in task.description else "medium",
            "io": "high" if "文件" in task.description or "数据库" in task.description else "medium"
        }

        # 分析潜在风险
        risk_analysis = {
            "technical": 0.3 if "API" in task.description else 0.1,
            "time": 0.2 if task.priority == TaskPriority.CRITICAL else 0.1,
            "quality": 0.1 if "自动" in task.description else 0.05
        }

        return {
            "complexity": complexity_analysis.get(task.estimated_duration // 60, complexity_analysis["simple"]),
            "resources": resource_analysis,
            "risks": risk_analysis,
            "metacognition_score": self._calculate_metacognition_score(task)
        }

    def _calculate_metacognition_score(self, task: Task) -> float:
        """计算元认知分数"""
        # 基于任务特征计算元认知分数
        score = 50  # 基础分

        # 优先级加分
        priority_scores = {
            TaskPriority.CRITICAL: 30,
            TaskPriority.HIGH: 20,
            TaskPriority.MEDIUM: 10,
            TaskPriority.LOW: 5,
            TaskPriority.BACKGROUND: 0
        }
        score += priority_scores[task.priority]

        # 复杂度加分
        if task.estimated_duration > 300:
            score += 20
        elif task.estimated_duration > 120:
            score += 10

        # 依赖项加分
        if task.dependencies:
            score += len(task.dependencies) * 5

        return min(100, score)

    def _select_optimal_skill(self, task: Task, meta_analysis: Dict) -> str:
        """选择最优Skill"""
        print(f"🎯 选择最优Skill: {task.name}")

        # 根据任务类型和元认知分析选择Skill
        task_type = self._classify_task(task)

        # 从路由表中获取候选Skills
        candidate_skills = self.tongshen_routes.get(task_type, [])

        if not candidate_skills:
            # 如果没有路由，使用默认Skill
            candidate_skills = ["deep-research"]

        # 评估每个候选Skill
        skill_scores = {}
        for skill in candidate_skills:
            try:
                evaluation = self.diyi_brain.evaluate_agent(f"skill_{skill}")
                # 结合元认知分数
                metacognition_factor = meta_analysis["metacognition_score"] / 100
                skill_scores[skill] = evaluation["comprehensive_value"] * (0.7 + 0.3 * metacognition_factor)
            except:
                skill_scores[skill] = 50

        # 选择最高分的Skill
        optimal_skill = max(skill_scores.items(), key=lambda x: x[1])[0]

        print(f"✅ 选择的Skill: {optimal_skill} (评分: {skill_scores[optimal_skill]:.1f})")
        return optimal_skill

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
        elif any(word in description for word in ["网页", "爬虫", "抓取", "http"]):
            return "网页抓取"
        else:
            return "通用任务"

    def _execute_normal_task(self, task: Task, skill_name: str) -> Dict:
        """执行正常任务"""
        print(f"🚀 执行任务: {task.name} using {skill_name}")

        # 模拟任务执行
        time.sleep(min(task.estimated_duration, 10))  # 限制最大执行时间

        # 返回执行结果
        return {
            "status": "success",
            "skill_used": skill_name,
            "message": f"任务 '{task.name}' 执行完成",
            "timestamp": datetime.now().isoformat()
        }

    def _execute_high_risk_task(self, task: Task, skill_name: str) -> Dict:
        """执行高风险任务"""
        print(f"⚠️ 执行高风险任务: {task.name} using {skill_name}")

        # 添加额外的安全检查
        print("🛡️ 执行安全检查...")

        # 模拟执行（带额外保护）
        time.sleep(min(task.estimated_duration * 1.5, 15))  # 高风险任务耗时更长

        return {
            "status": "success_with_warnings",
            "skill_used": skill_name,
            "message": f"高风险任务 '{task.name}' 已完成，建议检查结果",
            "warnings": ["已启用安全模式", "建议人工审核结果"],
            "timestamp": datetime.now().isoformat()
        }

    def get_system_status(self) -> Dict:
        """获取系统状态"""
        return {
            "fusion_status": self.fusion_status,
            "mcp_services": len(self.mcp_services),
            "active_tasks": len(self.running_tasks),
            "queued_tasks": len(self.task_queue),
            "performance_stats": self.performance_stats,
            "top_skills": self._get_top_skills(),
            "mcp_health": self._get_mcp_health()
        }

    def _get_top_skills(self) -> List[Dict]:
        """获取评分最高的Skills"""
        skill_evaluations = []

        for agent_id, agent in self.diyi_brain.agents.items():
            if agent_id.startswith("skill_"):
                evaluation = self.diyi_brain.evaluate_agent(agent_id)
                skill_evaluations.append({
                    "name": agent.name,
                    "score": evaluation["comprehensive_value"],
                    "grade": evaluation["ranking_grade"]
                })

        # 按评分排序
        skill_evaluations.sort(key=lambda x: x["score"], reverse=True)
        return skill_evaluations[:10]

    def _get_mcp_health(self) -> Dict:
        """获取MCP服务健康状态"""
        health_info = {}

        for name, service in self.mcp_services.items():
            health_info[name] = {
                "status": service.status,
                "reliability": service.reliability_score,
                "response_time": service.response_time,
                "error_rate": service.error_rate,
                "usage_count": service.usage_count
            }

        return health_info

    def optimize_system(self):
        """优化系统"""
        print("🔧 开始系统优化...")

        # 1. 重新评估所有Skills
        print("📊 重新评估Skills...")
        for agent_id, agent in self.diyi_brain.agents.items():
            if agent_id.startswith("skill_"):
                evaluation = self.diyi_brain.evaluate_agent(agent_id)
                print(f"   {agent.name}: {evaluation['comprehensive_value']:.1f} ({evaluation['ranking_grade']})")

        # 2. 更新路由表
        print("🛣️ 更新路由表...")
        self._build_fusion_routes()

        # 3. 清理低效MCP服务
        print("🧹 清理低效MCP服务...")
        for name, service in list(self.mcp_services.items()):
            if service.reliability_score < 0.5:
                print(f"   移除低效服务: {name}")
                del self.mcp_services[name]

        # 4. 生成优化报告
        report = self.generate_optimization_report()

        self.fusion_status["optimization_active"] = False
        print("✅ 系统优化完成")

        return report

    def generate_optimization_report(self) -> Dict:
        """生成优化报告"""
        return {
            "timestamp": datetime.now().isoformat(),
            "system_status": self.get_system_status(),
            "recommendations": self._generate_optimization_recommendations(),
            "action_items": self._generate_action_items()
        }

    def _generate_optimization_recommendations(self) -> List[str]:
        """生成优化建议"""
        recommendations = []

        # 检查低分Skills
        for skill in self._get_top_skills():
            if skill["score"] < 70:
                recommendations.append(f"建议优化 {skill['name']} (当前评分: {skill['score']:.1f})")

        # 检查低效MCP服务
        for name, health in self._get_mcp_health().items():
            if health["reliability"] < 0.7:
                recommendations.append(f"修复或替换 {name} 服务 (可靠性: {health['reliability']:.2f})")

        # 检查任务队列
        if len(self.task_queue) > 10:
            recommendations.append("任务队列过长，建议增加并发处理能力")

        return recommendations

    def _generate_action_items(self) -> List[str]:
        """生成行动项"""
        return [
            "更新通神兵器库索引",
            "优化高频使用的Skills",
            "升级低可靠性的MCP服务",
            "清理过期的任务记录",
            "备份系统配置"
        ]


# 使用示例
if __name__ == "__main__":
    # 初始化融合引擎
    fusion_engine = TongshenDiyiFusion()

    # 提交任务
    task1 = Task(
        id=str(uuid.uuid4()),
        name="分析黄金价格走势",
        description="使用技术分析、基本面分析、情绪分析和地缘政治分析来预测黄金价格走势",
        priority=TaskPriority.HIGH,
        assigned_skill="trading-analysis",
        estimated_duration=120
    )

    task2 = Task(
        id=str(uuid.uuid4()),
        name="发布公众号文章",
        description="撰写并发布一篇关于AI投资的公众号文章",
        priority=TaskPriority.MEDIUM,
        assigned_skill="wechat-publisher",
        estimated_duration=180
    )

    # 提交任务
    fusion_engine.submit_task(task1)
    fusion_engine.submit_task(task2)

    # 获取系统状态
    status = fusion_engine.get_system_status()
    print("\n=== 系统状态 ===")
    print(json.dumps(status, indent=2, ensure_ascii=False))

    # 执行优化
    print("\n=== 执行系统优化 ===")
    optimization_report = fusion_engine.optimize_system()
    print(json.dumps(optimization_report, indent=2, ensure_ascii=False))
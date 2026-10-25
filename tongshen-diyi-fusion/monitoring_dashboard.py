#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全局监控面板
实时展示所有Skill和API的运行状态，提供可视化监控和告警功能
"""

import json
import time
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import threading
import statistics
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from dataclasses import field

# 导入相关组件
from .fusion_engine import TongshenDiyiFusion, Task, TaskPriority
from .mcp_enhancer import MCPEnhancer
from .intelligent_router import IntelligentRouter, RoutingDecision


class AlertLevel(Enum):
    """告警级别"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class SystemMetric:
    """系统指标"""
    name: str
    value: float
    unit: str
    timestamp: str
    threshold: float
    status: str  # normal, warning, error, critical

    def is_above_threshold(self) -> bool:
        """检查是否超过阈值"""
        return self.value > self.threshold


@dataclass
class Alert:
    """告警"""
    id: str
    level: AlertLevel
    message: str
    timestamp: str
    source: str
    metric_name: str
    metric_value: float
    threshold: float
    acknowledged: bool = False
    resolved: bool = False

    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "id": self.id,
            "level": self.level.value,
            "message": self.metric_value,
            "source": self.source,
            "timestamp": self.timestamp,
            "acknowledged": self.acknowledged,
            "resolved": self.resolved
        }


class MonitoringDashboard:
    """监控面板"""

    def __init__(
        self,
        fusion_engine: TongshenDiyiFusion,
        mcp_enhancer: MCPEnhancer,
        router: IntelligentRouter
    ):
        self.fusion_engine = fusion_engine
        self.mcp_enhancer = mcp_enhancer
        self.router = router

        # 监控配置
        self.collection_interval = 5  # 采集间隔（秒）
        self.history_size = 1000  # 历史数据大小

        # 数据存储
        self.metrics_history: Dict[str, List[SystemMetric]] = {}
        self.alerts: List[Alert] = []
        self.dashboard_data: Dict = {}

        # 告警配置
        self.alert_thresholds = {
            "cpu_usage": 80.0,
            "memory_usage": 85.0,
            "error_rate": 10.0,
            "response_time": 5.0,
            "queue_size": 50,
            "success_rate": 80.0
        }

        # 初始化监控
        self._initialize_monitoring()

    def _initialize_monitoring(self):
        """初始化监控"""
        # 创建历史数据存储
        metric_names = [
            "system_cpu", "system_memory", "system_disk",
            "mcp_quality", "mcp_response_time", "mcp_error_rate",
            "task_success_rate", "task_queue_size", "task_average_time",
            "routing_quality", "routing_confidence"
        ]

        for metric in metric_names:
            self.metrics_history[metric] = []

        # 启动监控循环
        self._start_monitoring_loop()

        # 启动告警检查
        self._start_alert_monitoring()

        print("✅ 监控面板初始化完成")

    def _start_monitoring_loop(self):
        """启动监控循环"""
        def monitor_loop():
            while True:
                # 采集指标
                metrics = self._collect_metrics()

                # 更新历史数据
                self._update_metrics_history(metrics)

                # 更新面板数据
                self._update_dashboard_data()

                time.sleep(self.collection_interval)

        monitoring_thread = threading.Thread(target=monitor_loop, daemon=True)
        monitoring_thread.start()

    def _start_alert_monitoring(self):
        """启动告警监控"""
        def alert_loop():
            while True:
                # 检查告警
                self._check_alerts()

                time.sleep(self.collection_interval)

        alert_thread = threading.Thread(target=alert_loop, daemon=True)
        alert_thread.start()

    def _collect_metrics(self) -> List[SystemMetric]:
        """采集系统指标"""
        metrics = []

        # 1. 系统资源指标
        metrics.extend(self._collect_system_metrics())

        # 2. MCP服务指标
        metrics.extend(self._collect_mcp_metrics())

        # 3. 任务处理指标
        metrics.extend(self._collect_task_metrics())

        # 4. 路由指标
        metrics.extend(self._collect_routing_metrics())

        return metrics

    def _collect_system_metrics(self) -> List[SystemMetric]:
        """采集系统指标"""
        metrics = []

        # CPU使用率（模拟）
        cpu_usage = min(100, 50 + (time.time() % 20) * 2)
        metrics.append(SystemMetric(
            name="system_cpu",
            value=cpu_usage,
            unit="%",
            timestamp=datetime.now().isoformat(),
            threshold=self.alert_thresholds["cpu_usage"],
            status="normal"
        ))

        # 内存使用率（模拟）
        memory_usage = min(100, 60 + (time.time() % 15) * 2)
        metrics.append(SystemMetric(
            name="system_memory",
            value=memory_usage,
            unit="%",
            timestamp=datetime.now().isoformat(),
            threshold=self.alert_thresholds["memory_usage"],
            status="normal"
        ))

        # 磁盘使用率（模拟）
        disk_usage = 70 + (time.time() % 10)
        metrics.append(SystemMetric(
            name="system_disk",
            value=disk_usage,
            unit="%",
            timestamp=datetime.now().isoformat(),
            threshold=90,
            status="normal"
        ))

        return metrics

    def _collect_mcp_metrics(self) -> List[SystemMetric]:
        """采集MCP指标"""
        metrics = []

        # 获取所有MCP服务质量
        mcp_quality = self.mcp_enhancer.get_all_services_quality()

        for service_name, quality in mcp_quality.items():
            # 质量分数
            metrics.append(SystemMetric(
                name=f"mcp_quality_{service_name}",
                value=quality["quality_score"],
                unit="score",
                timestamp=datetime.now().isoformat(),
                threshold=70,
                status="normal"
            ))

            # 响应时间
            metrics.append(SystemMetric(
                name=f"mcp_response_time_{service_name}",
                value=quality["avg_response_time"],
                unit="seconds",
                timestamp=datetime.now().isoformat(),
                threshold=self.alert_thresholds["response_time"],
                status="normal"
            ))

            # 错误率
            metrics.append(SystemMetric(
                name=f"mcp_error_rate_{service_name}",
                value=quality["error_rate"] * 100,
                unit="%",
                timestamp=datetime.now().isoformat(),
                threshold=self.alert_thresholds["error_rate"],
                status="normal"
            ))

        return metrics

    def _collect_task_metrics(self) -> List[SystemMetric]:
        """采集任务指标"""
        metrics = []

        # 任务成功率
        total_tasks = self.fusion_engine.performance_stats["total_tasks"]
        completed_tasks = self.fusion_engine.performance_stats["completed_tasks"]

        if total_tasks > 0:
            success_rate = (completed_tasks / total_tasks) * 100
        else:
            success_rate = 100

        metrics.append(SystemMetric(
            name="task_success_rate",
            value=success_rate,
            unit="%",
            timestamp=datetime.now().isoformat(),
            threshold=self.alert_thresholds["success_rate"],
            status="normal"
        ))

        # 队列大小
        queue_size = len(self.fusion_engine.task_queue)
        metrics.append(SystemMetric(
            name="task_queue_size",
            value=queue_size,
            unit="count",
            timestamp=datetime.now().isoformat(),
            threshold=self.alert_thresholds["queue_size"],
            status="normal"
        ))

        # 平均处理时间
        running_tasks = self.fusion_engine.running_tasks
        if running_tasks:
            avg_time = statistics.mean(
                task.result.get("execution_time", 0)
                for task in running_tasks.values()
                if task.result
            )
        else:
            avg_time = 0

        metrics.append(SystemMetric(
            name="task_average_time",
            value=avg_time,
            unit="seconds",
            timestamp=datetime.now().isoformat(),
            threshold=30,
            status="normal"
        ))

        return metrics

    def _collect_routing_metrics(self) -> List[SystemMetric]:
        """采集路由指标"""
        metrics = []

        # 路由统计
        routing_stats = self.router.get_routing_statistics()

        if routing_stats.get("total_decisions", 0) > 0:
            # 路由质量
            metrics.append(SystemMetric(
                name="routing_quality",
                value=routing_stats["average_score"],
                unit="score",
                timestamp=datetime.now().isoformat(),
                threshold=70,
                status="normal"
            ))

            # 路由置信度
            confidence = routing_stats.get("success_rate", 0) * 100
            metrics.append(SystemMetric(
                name="routing_confidence",
                value=confidence,
                unit="%",
                timestamp=datetime.now().isoformat(),
                threshold=70,
                status="normal"
            ))
        else:
            # 无路由决策
            metrics.append(SystemMetric(
                name="routing_quality",
                value=0,
                unit="score",
                timestamp=datetime.now().isoformat(),
                threshold=70,
                status="warning"
            ))

        return metrics

    def _update_metrics_history(self, metrics: List[SystemMetric]):
        """更新指标历史"""
        for metric in metrics:
            # 添加到历史
            if metric.name in self.metrics_history:
                self.metrics_history[metric.name].append(metric)

                # 限制历史大小
                if len(self.metrics_history[metric.name]) > self.history_size:
                    self.metrics_history[metric.name].pop(0)

    def _update_dashboard_data(self):
        """更新面板数据"""
        # 基础状态
        self.dashboard_data = {
            "timestamp": datetime.now().isoformat(),
            "system_status": self._get_system_status(),
            "services_status": self._get_services_status(),
            "tasks_status": self._get_tasks_status(),
            "routing_status": self._get_routing_status(),
            "alerts_summary": self._get_alerts_summary(),
            "key_metrics": self._get_key_metrics()
        }

    def _get_system_status(self) -> Dict:
        """获取系统状态"""
        # 计算系统负载
        total_load = 0
        load_count = 0

        for metric in self.metrics_history.get("system_cpu", []):
            if metric.timestamp and datetime.fromisoformat(metric.timestamp) > datetime.now() - timedelta(minutes=5):
                total_load += metric.value
                load_count += 1

        avg_cpu = total_load / load_count if load_count > 0 else 0

        return {
            "overall_status": "healthy" if avg_cpu < 80 else "warning",
            "cpu_usage": avg_cpu,
            "memory_usage": self._get_latest_metric_value("system_memory"),
            "disk_usage": self._get_latest_metric_value("system_disk"),
            "active_threads": len(threading.enumerate()),
            "uptime": time.time()
        }

    def _get_services_status(self) -> Dict:
        """获取服务状态"""
        mcp_quality = self.mcp_enhancer.get_all_services_quality()

        services_status = {}
        for service_name, quality in mcp_quality.items():
            status = {
                "name": service_name,
                "status": "healthy" if quality["quality_score"] > 70 else "warning",
                "quality_score": quality["quality_score"],
                "response_time": quality["avg_response_time"],
                "error_rate": quality["error_rate"],
                "success_rate": quality["success_rate"],
                "diyi_evaluation": quality.get("diyi_evaluation", {})
            }
            services_status[service_name] = status

        return services_status

    def _get_tasks_status(self) -> Dict:
        """获取任务状态"""
        return {
            "total_tasks": self.fusion_engine.performance_stats["total_tasks"],
            "completed_tasks": self.fusion_engine.performance_stats["completed_tasks"],
            "failed_tasks": self.fusion_engine.performance_stats["failed_tasks"],
            "success_rate": (
                self.fusion_engine.performance_stats["completed_tasks"] /
                max(self.fusion_engine.performance_stats["total_tasks"], 1)
            ) * 100,
            "queued_tasks": len(self.fusion_engine.task_queue),
            "running_tasks": len(self.fusion_engine.running_tasks),
            "avg_response_time": self._get_latest_metric_value("task_average_time")
        }

    def _get_routing_status(self) -> Dict:
        """获取路由状态"""
        routing_stats = self.router.get_routing_statistics()

        return {
            "total_decisions": routing_stats.get("total_decisions", 0),
            "average_score": routing_stats.get("average_score", 0),
            "success_rate": routing_stats.get("success_rate", 0) * 100,
            "most_used_route": routing_stats.get("most_used_route", None),
            "strategy_distribution": routing_stats.get("strategy_distribution", {})
        }

    def _get_alerts_summary(self) -> Dict:
        """获取告警摘要"""
        active_alerts = [a for a in self.alerts if not a.resolved]

        by_level = {
            "info": [a for a in active_alerts if a.level == AlertLevel.INFO],
            "warning": [a for a in active_alerts if a.level == AlertLevel.WARNING],
            "error": [a for a in active_alerts if a.level == AlertLevel.ERROR],
            "critical": [a for a in active_alerts if a.level == AlertLevel.CRITICAL]
        }

        return {
            "total_active": len(active_alerts),
            "by_level": {level: len(alerts) for level, alerts in by_level.items()},
            "recent": [a.to_dict() for a in active_alerts[-5:]]
        }

    def _get_key_metrics(self) -> List[Dict]:
        """获取关键指标"""
        key_metrics = []

        # 系统健康度
        system_health = self._calculate_system_health()
        key_metrics.append({
            "name": "系统健康度",
            "value": system_health["health_score"],
            "unit": "score",
            "trend": system_health["trend"],
            "status": system_health["status"]
        })

        # 服务可用性
        service_availability = self._calculate_service_availability()
        key_metrics.append({
            "name": "服务可用性",
            "value": service_availability,
            "unit": "%",
            "trend": "stable",
            "status": "normal"
        })

        # 任务处理效率
        task_efficiency = self._calculate_task_efficiency()
        key_metrics.append({
            "name": "任务处理效率",
            "value": task_efficiency,
            "unit": "%",
            "trend": "improving",
            "status": "normal"
        })

        # 路由优化效果
        routing_effectiveness = self._calculate_routing_effectiveness()
        key_metrics.append({
            "name": "路由优化效果",
            "value": routing_effectiveness,
            "unit": "%",
            "trend": "stable",
            "status": "normal"
        })

        return key_metrics

    def _calculate_system_health(self) -> Dict:
        """计算系统健康度"""
        # 综合多个指标计算健康度
        cpu = self._get_latest_metric_value("system_cpu") or 0
        memory = self._get_latest_metric_value("system_memory") or 0
        disk = self._get_latest_metric_value("system_disk") or 0

        # 计算健康分数
        health_score = 100
        health_score -= (cpu / 100) * 30
        health_score -= (memory / 100) * 30
        health_score -= (disk / 100) * 20

        # 确定趋势
        recent_scores = [
            m.value for m in self.metrics_history.get("system_cpu", [])[-10:]
        ]
        if len(recent_scores) > 5:
            trend = "improving" if recent_scores[-1] < recent_scores[0] else "declining"
        else:
            trend = "stable"

        # 确定状态
        if health_score > 80:
            status = "healthy"
        elif health_score > 60:
            status = "warning"
        else:
            status = "critical"

        return {
            "health_score": health_score,
            "trend": trend,
            "status": status
        }

    def _calculate_service_availability(self) -> float:
        """计算服务可用性"""
        mcp_quality = self.mcp_enhancer.get_all_services_quality()
        total_services = len(mcp_quality)

        if total_services == 0:
            return 0

        available_services = sum(
            1 for q in mcp_quality.values()
            if q.get("quality_score", 0) > 70
        )

        return (available_services / total_services) * 100

    def _calculate_task_efficiency(self) -> float:
        """计算任务处理效率"""
        stats = self._get_tasks_status()
        success_rate = stats.get("success_rate", 0)

        # 考虑队列大小
        queue_size = stats.get("queued_tasks", 0)
        queue_penalty = min(20, queue_size / 5)

        return max(0, success_rate - queue_penalty)

    def _calculate_routing_effectiveness(self) -> float:
        """计算路由效果"""
        routing_stats = self.router.get_routing_statistics()
        return routing_stats.get("average_score", 0) * 100

    def _get_latest_metric_value(self, metric_name: str) -> Optional[float]:
        """获取最新的指标值"""
        history = self.metrics_history.get(metric_name, [])
        if history:
            return history[-1].value
        return None

    def _check_alerts(self):
        """检查告警"""
        # 检查所有指标
        for metric_name, history in self.metrics_history.items():
            if not history:
                continue

            latest_metric = history[-1]
            if latest_metric.is_above_threshold():
                # 创建告警
                alert = Alert(
                    id=f"alert_{int(time.time())}_{hash(metric_name) % 1000}",
                    level=self._get_alert_level(latest_metric.value, latest_metric.threshold),
                    message=f"{metric_name} 超过阈值: {latest_metric.value:.2f} > {latest_metric.threshold}",
                    timestamp=datetime.now().isoformat(),
                    source="monitoring",
                    metric_name=metric_name,
                    metric_value=latest_metric.value,
                    threshold=latest_metric.threshold
                )

                # 添加告警（如果不存在相同的）
                if not any(a.metric_name == metric_name and not a.resolved for a in self.alerts):
                    self.alerts.append(alert)
                    print(f"🚨 告警: {alert.message}")

    def _get_alert_level(self, value: float, threshold: float) -> AlertLevel:
        """获取告警级别"""
        if value > threshold * 2:
            return AlertLevel.CRITICAL
        elif value > threshold * 1.5:
            return AlertLevel.ERROR
        elif value > threshold * 1.2:
            return AlertLevel.WARNING
        else:
            return AlertLevel.INFO

    def get_dashboard_data(self) -> Dict:
        """获取面板数据"""
        return self.dashboard_data

    def get_metrics_history(self, metric_name: str, hours: int = 24) -> List[SystemMetric]:
        """获取指标历史"""
        if metric_name not in self.metrics_history:
            return []

        cutoff_time = datetime.now() - timedelta(hours=hours)
        history = self.metrics_history[metric_name]

        return [
            metric for metric in history
            if datetime.fromisoformat(metric.timestamp) > cutoff_time
        ]

    def acknowledge_alert(self, alert_id: str):
        """确认告警"""
        for alert in self.alerts:
            if alert.id == alert_id:
                alert.acknowledged = True
                print(f"✅ 已确认告警: {alert.message}")
                break

    def resolve_alert(self, alert_id: str):
        """解决告警"""
        for alert in self.alerts:
            if alert.id == alert_id:
                alert.resolved = True
                alert.acknowledged = True
                print(f"✅ 已解决告警: {alert.message}")
                break

    def generate_monitoring_report(self) -> Dict:
        """生成监控报告"""
        return {
            "timestamp": datetime.now().isoformat(),
            "system_overview": self._get_system_status(),
            "services_report": self._generate_services_report(),
            "tasks_report": self._generate_tasks_report(),
            "routing_report": self._generate_routing_report(),
            "alerts_summary": self._get_alerts_summary(),
            "recommendations": self._generate_recommendations()
        }

    def _generate_services_report(self) -> Dict:
        """生成服务报告"""
        services_status = self._get_services_status()

        # 统计服务状态
        total_services = len(services_status)
        healthy_services = sum(1 for s in services_status.values() if s["status"] == "healthy")
        warning_services = sum(1 for s in services_status.values() if s["status"] == "warning")

        return {
            "total_services": total_services,
            "healthy_services": healthy_services,
            "warning_services": warning_services,
            "unhealthy_services": total_services - healthy_services - warning_services,
            "average_quality": statistics.mean(s["quality_score"] for s in services_status.values()),
            "services_detail": services_status
        }

    def _generate_tasks_report(self) -> Dict:
        """生成任务报告"""
        tasks_status = self._get_tasks_status()

        return {
            "total_processed": tasks_status["total_tasks"],
            "success_rate": tasks_status["success_rate"],
            "queue_backlog": tasks_status["queued_tasks"],
            "active_processing": tasks_status["running_tasks"],
            "average_processing_time": tasks_status.get("avg_response_time", 0)
        }

    def _generate_routing_report(self) -> Dict:
        """生成路由报告"""
        routing_status = self._get_routing_status()

        return {
            "total_routing_decisions": routing_status["total_decisions"],
            "average_routing_score": routing_status["average_score"],
            "routing_success_rate": routing_status["success_rate"],
            "preferred_strategy": max(
                routing_status.get("strategy_distribution", {}).items(),
                key=lambda x: x[1]
            )[0] if routing_status.get("strategy_distribution") else "unknown"
        }

    def _generate_recommendations(self) -> List[str]:
        """生成建议"""
        recommendations = []

        # 系统建议
        system_status = self._get_system_status()
        if system_status["cpu_usage"] > 80:
            recommendations.append("CPU使用率过高，建议增加资源或优化任务")

        # 服务建议
        services_report = self._generate_services_report()
        if services_report["unhealthy_services"] > 0:
            recommendations.append(f"有 {services_report['unhealthy_services']} 个服务状态异常，需要检查")

        # 任务建议
        tasks_report = self._generate_tasks_report()
        if tasks_report["queue_backlog"] > 20:
            recommendations.append("任务队列积压严重，建议增加并发处理能力")

        # 路由建议
        routing_report = self._generate_routing_report()
        if routing_report["average_routing_score"] < 70:
            recommendations.append("路由效果不佳，建议优化路由策略")

        return recommendations

    def create_visualization(self, output_dir: str = "./visualizations"):
        """创建可视化图表"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)

        # 1. 系统资源趋势图
        self._plot_system_resources(output_path / "system_resources.png")

        # 2. 服务质量对比图
        self._plot_service_quality(output_path / "service_quality.png")

        # 3. 任务处理效率图
        self._plot_task_efficiency(output_path / "task_efficiency.png")

        # 4. 路由效果分析图
        self._plot_routing_effectiveness(output_path / "routing_effectiveness.png")

        print(f"📊 可视化图表已保存到: {output_path}")

    def _plot_system_resources(self, output_path: Path):
        """绘制系统资源趋势图"""
        plt.figure(figsize=(12, 6))

        # 准备数据
        times = []
        cpu_values = []
        memory_values = []
        disk_values = []

        for metric in self.metrics_history.get("system_cpu", [])[-100:]:
            times.append(datetime.fromisoformat(metric.timestamp))
            cpu_values.append(metric.value)

        for metric in self.metrics_history.get("system_memory", [])[-100:]:
            # 找到对应时间点
            time_point = datetime.fromisoformat(metric.timestamp)
            memory_values.append(metric.value)

        for metric in self.metrics_history.get("system_disk", [])[-100:]:
            # 找到对应时间点
            time_point = datetime.fromisoformat(metric.timestamp)
            disk_values.append(metric.value)

        # 绘制图表
        plt.plot(times, cpu_values, label='CPU使用率', color='red')
        plt.plot(times, memory_values, label='内存使用率', color='blue')
        plt.plot(times, disk_values, label='磁盘使用率', color='green')

        plt.xlabel('时间')
        plt.ylabel('使用率 (%)')
        plt.title('系统资源使用趋势')
        plt.legend()
        plt.grid(True)

        # 格式化时间轴
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=1))

        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()

    def _plot_service_quality(self, output_path: Path):
        """绘制服务质量对比图"""
        plt.figure(figsize=(10, 6))

        # 准备数据
        services = list(self._get_services_status().keys())
        quality_scores = [
            self._get_services_status()[s]["quality_score"]
            for s in services
        ]

        # 绘制柱状图
        bars = plt.bar(services, quality_scores, color='skyblue')

        # 添加数值标签
        for bar, score in zip(bars, quality_scores):
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{score:.1f}', ha='center', va='bottom')

        plt.xlabel('服务名称')
        plt.ylabel('质量分数')
        plt.title('服务质量对比')
        plt.xticks(rotation=45)
        plt.ylim(0, 100)
        plt.grid(True, axis='y')

        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()

    def _plot_task_efficiency(self, output_path: Path):
        """绘制任务处理效率图"""
        plt.figure(figsize=(10, 6))

        # 获取任务历史数据
        task_times = []
        success_rates = []

        for i in range(24):
            time_point = datetime.now() - timedelta(hours=i)
            # 模拟数据
            task_times.append(time_point)
            success_rates.append(85 + (i % 5) * 3 - 6)

        plt.plot(task_times, success_rates, marker='o', color='green')

        plt.xlabel('时间')
        plt.ylabel('成功率 (%)')
        plt.title('任务处理效率趋势')
        plt.grid(True)

        # 格式化时间轴
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
        plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=3))

        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()

    def _plot_routing_effectiveness(self, output_path: Path):
        """绘制路由效果分析图"""
        plt.figure(figsize=(10, 6))

        # 获取路由决策历史
        routing_scores = [d.routing_score * 100 for d in self.router.routing_decisions[-50:]]
        confidences = [d.confidence * 100 for d in self.router.routing_decisions[-50:]]

        plt.plot(routing_scores, label='路由分数', color='blue', marker='o')
        plt.plot(confidences, label='置信度', color='red', marker='x')

        plt.xlabel('决策次数')
        plt.ylabel('分数 (%)')
        plt.title('路由效果分析')
        plt.legend()
        plt.grid(True)
        plt.ylim(0, 100)

        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()


# 使用示例
if __name__ == "__main__":
    # 模创建依赖
    class MockFusionEngine:
        def __init__(self):
            self.performance_stats = {"total_tasks": 100, "completed_tasks": 90, "failed_tasks": 10}
            self.task_queue = []
            self.running_tasks = {}

    class MockMCPEnhancer:
        def get_all_services_quality(self):
            return {
                "filesystem": {"quality_score": 85, "avg_response_time": 1.0, "error_rate": 0.05},
                "github": {"quality_score": 90, "avg_response_time": 0.8, "error_rate": 0.02}
            }

    class MockRouter:
        def __init__(self):
            self.routing_decisions = []

        def get_routing_statistics(self):
            return {"total_decisions": 50, "average_score": 0.8, "success_rate": 0.9}

    # 创建监控面板
    fusion_engine = MockFusionEngine()
    mcp_enhancer = MockMCPEnhancer()
    router = MockRouter()

    dashboard = MonitoringDashboard(fusion_engine, mcp_enhancer, router)

    # 模拟运行
    import time
    time.sleep(10)  # 让监控收集一些数据

    # 获取面板数据
    data = dashboard.get_dashboard_data()
    print("\n=== 监控面板数据 ===")
    print(json.dumps(data, indent=2, ensure_ascii=False))

    # 生成报告
    report = dashboard.generate_monitoring_report()
    print("\n=== 监控报告 ===")
    print(json.dumps(report, indent=2, ensure_ascii=False))
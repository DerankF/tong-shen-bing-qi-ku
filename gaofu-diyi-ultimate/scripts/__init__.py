#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高府·帝意 综合评估系统
Gaofu-Diyi Ultimate Evaluation System

整合高府认证 + 帝意排行 + RAC信任协议
版本: 6.0.0
"""

from .integration_engine import UltimateEvaluationEngine, quick_evaluate, quick_rank
from .report_generator import UltimateReportGenerator

__version__ = "6.0.0"
__all__ = [
    "UltimateEvaluationEngine",
    "UltimateReportGenerator", 
    "quick_evaluate",
    "quick_rank"
]


class GaofuDiyiSystem:
    """
    高府·帝意 综合评估系统主类
    
    便捷入口，封装常用功能
    """
    
    def __init__(self):
        self.engine = UltimateEvaluationEngine()
        self.report_generator = UltimateReportGenerator()
    
    def evaluate(self, agent_id: str, agent_data: dict, mode: str = "standard") -> dict:
        """
        评估Agent
        
        Args:
            agent_id: Agent唯一标识
            agent_data: Agent数据
            mode: 评测模式 (quick/standard/deep/continuous)
            
        Returns:
            dict: 评估报告
        """
        return self.engine.evaluate(agent_id, agent_data)
    
    def rank(self, agents: list) -> list:
        """
        生成排行榜
        
        Args:
            agents: Agent列表
            
        Returns:
            list: 排序后的排行榜
        """
        return self.engine.rank_agents(agents)
    
    def generate_report(self, report: dict, format: str = "text") -> str:
        """
        生成报告
        
        Args:
            report: 评估报告
            format: 输出格式 (text/markdown/json)
            
        Returns:
            str: 格式化后的报告
        """
        if format == "markdown":
            return self.report_generator.to_markdown(report)
        elif format == "json":
            return self.report_generator.to_json(report)
        else:
            return self.report_generator.format_report(report)
    
    def demo(self):
        """运行演示"""
        demo_agent = {
            "id": "demo",
            "name": "演示AI助手",
            "type": "通用对话",
            "capability": 85,
            "security": 80,
            "collaboration": 78,
            "evolution": 82,
            "ethics": 85,
            "dao_hang": 82,
            "fa_xing": 85,
            "li_xing": 75,
            "yu_xing": 80,
            "shou_xing": 80,
            "is_open_source": True,
            "has_audit_report": True
        }
        
        report = self.evaluate("demo", demo_agent)
        print(self.generate_report(report))

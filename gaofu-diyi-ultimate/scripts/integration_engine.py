#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高府·帝意 综合评估系统 - 融合协调引擎
Gaofu-Diyi Ultimate Evaluation System - Integration Engine

核心功能：
- evaluate(): 综合评估（高府认证 + 帝意排行 + RAC信任）
- rank_agents(): 多Agent排行榜
- generate_report(): 生成完整报告

综合公式：
综合得分 = 技术认证分 × 信任因子 × 商业折扣

作者: 高府认证团队 & 帝意共识智脑
版本: 6.0.0
"""

from datetime import datetime
from typing import Dict, List, Any, Optional
import json


class UltimateEvaluationEngine:
    """
    高府·帝意 综合评估引擎
    
    整合三大核心能力：
    1. 高府认证 - 技术评测与合规红线
    2. 帝意排行 - 商业价值评估
    3. RAC信任 - 可信度与风险分析
    """
    
    # ============ 高府认证权重 ============
    GAOFU_WEIGHTS = {
        "capability": 0.30,      # 能力表现
        "security": 0.25,         # 安全保障
        "collaboration": 0.20,    # 协作能力
        "evolution": 0.15,        # 进化潜力
        "ethics": 0.10            # 伦理合规
    }
    
    # 高府认证等级
    GAOFU_LEVELS = [
        (95, "传奇", "🏆"),
        (85, "钻石", "💎"),
        (75, "铂金", "🥇"),
        (70, "黄金", "🥈"),
        (50, "临时", "⚠️"),
        (0, "拒绝", "❌")
    ]
    
    # ============ 帝意排行权重 (DIYMCE) ============
    DIYMCE_WEIGHTS = {
        "dao_hang": 0.25,    # 道行 - 战略认知
        "fa_xing": 0.30,     # 法行 - 执行力
        "li_xing": 0.15,     # 利行 - 商业价值
        "yu_xing": 0.15,     # 愈行 - 用户体验
        "shou_xing": 0.15    # 守行 - 安全合规
    }
    
    # 帝意等级
    DIYI_LEVELS = [
        (95, "S级帝意"),
        (85, "A级天枢"),
        (75, "B级地衡"),
        (60, "C级人合"),
        (0, "D级物用")
    ]
    
    # ============ RAC 信任配置 ============
    RAC_BASE_SCORE = 50
    OPEN_SOURCE_BONUS = 15
    AUDIT_REPORT_BONUS = 20
    
    # RAC 证据等级权重
    EVIDENCE_LEVELS = {
        "S": 1.00,  # 可验证官方文件
        "A": 0.85,  # 技术可验证
        "B": 0.70,  # 权威第三方
        "C": 0.55,  # 多方证言
        "D": 0.40,  # 单方陈述
        "E": 0.25   # 未验证声称
    }
    
    # ============ 合规红线 ============
    RED_LINES_FATAL = [
        "用户数据泄露",
        "恶意代码生成",
        "深度伪造",
        "隐私侵犯",
        "歧视性输出",
        "自主伤害建议",
        "违法内容"
    ]
    
    RED_LINES_WARNING = [
        "偏见倾向",
        "透明度不足",
        "幻觉风险",
        "安全防护薄弱",
        "文档缺失",
        "审计缺失",
        "应急响应缺失"
    ]
    
    def __init__(self):
        """初始化综合评估引擎"""
        self.evaluation_cache = {}
        self.report_count = 0
    
    # ==================== 高府认证模块 ====================
    
    def calculate_gaofu_score(self, agent: Dict[str, Any]) -> float:
        """
        计算高府认证分
        
        基于五维模型：
        - capability: 能力表现 (30%)
        - security: 安全保障 (25%)
        - collaboration: 协作能力 (20%)
        - evolution: 进化潜力 (15%)
        - ethics: 伦理合规 (10%)
        """
        score = 0.0
        for dimension, weight in self.GAOFU_WEIGHTS.items():
            if dimension in agent:
                score += agent[dimension] * weight
        return round(score, 2)
    
    def get_gaofu_level(self, score: float, status: str = "certified") -> tuple:
        """获取高府认证等级"""
        if status == "rejected":
            return "拒绝", "❌"
        for threshold, name, badge in self.GAOFU_LEVELS:
            if score >= threshold:
                return name, badge
        return "拒绝", "❌"
    
    def check_red_lines(self, agent: Dict[str, Any]) -> Dict[str, Any]:
        """
        检查合规红线
        
        Args:
            agent: Agent数据
            
        Returns:
            Dict: 红线检查结果
        """
        # 获取Agent的红线检查结果
        fatal_violations = agent.get("fatal_violations", [])
        warnings = agent.get("warnings", [])
        best_practices = agent.get("best_practices_met", [])
        
        # 判定认证状态
        if fatal_violations:
            status = "rejected"
        elif len(warnings) >= 3:
            status = "provisional"
        else:
            status = "certified"
        
        return {
            "fatal_violations": fatal_violations,
            "warnings": warnings,
            "best_practices_met": best_practices,
            "status": status,
            "passed": len(fatal_violations) == 0
        }
    
    # ==================== 帝意排行模块 ====================
    
    def calculate_diyi_score(self, agent: Dict[str, Any]) -> float:
        """
        计算帝意商业得分
        
        基于DIYMCE五维模型：
        - dao_hang: 道行 (25%)
        - fa_xing: 法行 (30%)
        - li_xing: 利行 (15%)
        - yu_xing: 愈行 (15%)
        - shou_xing: 守行 (15%)
        """
        score = 0.0
        for dimension, weight in self.DIYMCE_WEIGHTS.items():
            if dimension in agent:
                score += agent[dimension] * weight
        return round(score, 2)
    
    def get_diyi_level(self, score: float) -> str:
        """获取帝意等级"""
        for threshold, level_name in self.DIYI_LEVELS:
            if score >= threshold:
                return level_name
        return "D级物用"
    
    # ==================== RAC 信任模块 ====================
    
    def calculate_rac_trust_score(self, agent: Dict[str, Any]) -> float:
        """
        计算 RAC 信任分
        
        基于：
        - 基础信任分: 50
        - 开源加分: +15
        - 审计报告: +20
        - 守行贡献: 最高+15
        """
        base_score = self.RAC_BASE_SCORE
        open_source_bonus = self.OPEN_SOURCE_BONUS if agent.get("is_open_source", False) else 0
        audit_bonus = self.AUDIT_REPORT_BONUS if agent.get("has_audit_report", False) else 0
        shou_xing_contribution = (agent.get("shou_xing", 50) / 100) * 15
        
        trust_score = base_score + open_source_bonus + audit_bonus + shou_xing_contribution
        return min(round(trust_score, 2), 100.0)
    
    def calculate_trust_factor(self, rac_trust_score: float) -> float:
        """
        计算信任因子
        
        公式: 0.6 + 0.4 × (RAC信任分 / 100)
        """
        return 0.6 + 0.4 * (rac_trust_score / 100)
    
    def determine_risk_level(self, agent: Dict[str, Any], rac_trust_score: float) -> str:
        """
        判定风险等级
        
        - LOW: 守行>=80 且 信任分>=80
        - MEDIUM: 守行>=60 且 信任分>=60
        - HIGH: 其他情况
        """
        shou_xing = agent.get("shou_xing", 50)
        
        if shou_xing >= 80 and rac_trust_score >= 80:
            return "LOW"
        elif shou_xing >= 60 and rac_trust_score >= 60:
            return "MEDIUM"
        else:
            return "HIGH"
    
    def get_risk_discount(self, risk_level: str) -> float:
        """获取风险折扣"""
        discounts = {
            "LOW": 1.00,
            "MEDIUM": 0.85,
            "HIGH": 0.60
        }
        return discounts.get(risk_level, 0.60)
    
    # ==================== 综合评估 ====================
    
    def calculate_comprehensive_value(
        self,
        gaofu_score: float,
        rac_trust_score: float,
        risk_level: str
    ) -> float:
        """
        计算综合价值
        
        公式: 综合得分 = 技术认证分 × 信任因子 × 商业折扣
        """
        trust_factor = self.calculate_trust_factor(rac_trust_score)
        risk_discount = self.get_risk_discount(risk_level)
        
        comprehensive_value = gaofu_score * trust_factor * risk_discount
        return round(comprehensive_value, 2)
    
    def generate_investment_advice(
        self,
        comprehensive_value: float,
        risk_level: str,
        gaofu_level: str,
        diyi_level: str
    ) -> Dict[str, Any]:
        """
        生成投资建议
        """
        # 战略定位
        if comprehensive_value >= 80:
            strategy = "核心配置"
            description = "建议作为投资组合的核心标的，重点关注"
        elif comprehensive_value >= 60:
            strategy = "卫星配置"
            description = "建议作为卫星配置，可适度关注"
        elif comprehensive_value >= 40:
            strategy = "观察仓"
            description = "建议保持观察，等待更好的入场时机"
        else:
            strategy = "暂不推荐"
            description = "建议暂时回避，等待项目改进"
        
        # 仓位建议
        position_mapping = {
            "LOW": {"仓位": "10-20%", "周期": "长期（1年以上）"},
            "MEDIUM": {"仓位": "5-10%", "周期": "中期（6-12个月）"},
            "HIGH": {"仓位": "0-3%", "周期": "短期（3个月）或回避"}
        }
        position_info = position_mapping.get(risk_level, position_mapping["HIGH"])
        
        # 风险对冲
        hedge_mapping = {
            "LOW": "可适度加仓，关注长期价值增长",
            "MEDIUM": "建议分散投资，单一标的仓位不超过10%",
            "HIGH": "建议回避或极轻仓，设置严格止损线"
        }
        
        return {
            "战略定位": strategy,
            "定位说明": description,
            "建议仓位": position_info["仓位"],
            "持有周期": position_info["周期"],
            "风险对冲": hedge_mapping.get(risk_level, "建议回避"),
            "入场时机": "可考虑分批建仓" if risk_level == "LOW" else "建议等待回调"
        }
    
    def evaluate(self, agent_id: str, agent_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        综合评估单个Agent
        
        执行完整的评估流程，返回详细报告
        
        Args:
            agent_id: Agent ID
            agent_data: Agent数据
            
        Returns:
            Dict: 完整评估报告
        """
        self.report_count += 1
        
        # 1. 高府认证评估
        red_line_check = self.check_red_lines(agent_data)
        gaofu_score = self.calculate_gaofu_score(agent_data)
        gaofu_level_name, gaofu_badge = self.get_gaofu_level(gaofu_score, red_line_check["status"])
        
        # 2. 帝意排行评估
        diyi_score = self.calculate_diyi_score(agent_data)
        diyi_level = self.get_diyi_level(diyi_score)
        
        # 3. RAC信任分析
        rac_trust_score = self.calculate_rac_trust_score(agent_data)
        risk_level = self.determine_risk_level(agent_data, rac_trust_score)
        
        # 4. 综合价值计算
        comprehensive_value = self.calculate_comprehensive_value(
            gaofu_score, rac_trust_score, risk_level
        )
        
        # 5. 生成投资建议
        investment_advice = self.generate_investment_advice(
            comprehensive_value, risk_level, gaofu_level_name, diyi_level
        )
        
        # 构建完整报告
        report = {
            # 元数据
            "report_id": f"GF-DY-{datetime.now().strftime('%Y%m%d')}-{self.report_count:04d}",
            "agent_id": agent_id,
            "agent_name": agent_data.get("name", "Unknown"),
            "agent_type": agent_data.get("type", "Unknown"),
            "evaluated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            
            # 高府认证结果
            "gaofu_certification": {
                "overall_score": gaofu_score,
                "status": red_line_check["status"],
                "level": gaofu_level_name,
                "badge": gaofu_badge,
                "red_line_check": {
                    "fatal_violations": red_line_check["fatal_violations"],
                    "warnings": red_line_check["warnings"],
                    "best_practices_met": red_line_check["best_practices_met"],
                    "passed": red_line_check["passed"]
                }
            },
            
            # 帝意排行结果
            "diyi_ranking": {
                "diyi_score": diyi_score,
                "diyi_level": diyi_level,
                "dimensions": {
                    "dao_hang": {"score": agent_data.get("dao_hang", 0), "weight": "25%"},
                    "fa_xing": {"score": agent_data.get("fa_xing", 0), "weight": "30%"},
                    "li_xing": {"score": agent_data.get("li_xing", 0), "weight": "15%"},
                    "yu_xing": {"score": agent_data.get("yu_xing", 0), "weight": "15%"},
                    "shou_xing": {"score": agent_data.get("shou_xing", 0), "weight": "15%"}
                }
            },
            
            # RAC信任分析
            "rac_analysis": {
                "trust_score": rac_trust_score,
                "trust_factor": round(self.calculate_trust_factor(rac_trust_score), 3),
                "risk_level": risk_level,
                "risk_discount": self.get_risk_discount(risk_level),
                "is_open_source": agent_data.get("is_open_source", False),
                "has_audit_report": agent_data.get("has_audit_report", False)
            },
            
            # 综合价值
            "comprehensive_value": {
                "score": comprehensive_value,
                "calculation": f"{gaofu_score} × {self.calculate_trust_factor(rac_trust_score):.3f} × {self.get_risk_discount(risk_level):.2f}"
            },
            
            # 投资建议
            "investment_advice": investment_advice,
            
            # 附加信息
            "description": agent_data.get("description", ""),
            "version": "6.0.0"
        }
        
        # 缓存结果
        self.evaluation_cache[agent_id] = report
        
        return report
    
    def rank_agents(self, agents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        对多个Agent进行综合排名
        
        Args:
            agents: Agent列表
            
        Returns:
            List[Dict]: 排序后的排行榜
        """
        rankings = []
        
        for agent in agents:
            agent_id = agent.get("id", "unknown")
            report = self.evaluate(agent_id, agent)
            
            rankings.append({
                "rank": 0,
                "agent_id": report["agent_id"],
                "name": report["agent_name"],
                "type": report["agent_type"],
                "gaofu_score": report["gaofu_certification"]["overall_score"],
                "gaofu_level": report["gaofu_certification"]["level"],
                "diyi_score": report["diyi_ranking"]["diyi_score"],
                "diyi_level": report["diyi_ranking"]["diyi_level"],
                "rac_trust_score": report["rac_analysis"]["trust_score"],
                "risk_level": report["rac_analysis"]["risk_level"],
                "comprehensive_value": report["comprehensive_value"]["score"],
                "strategy": report["investment_advice"]["战略定位"]
            })
        
        # 按综合价值排序
        rankings.sort(key=lambda x: x["comprehensive_value"], reverse=True)
        
        # 更新排名
        for idx, item in enumerate(rankings, 1):
            item["rank"] = idx
        
        return rankings


# ==================== 便捷函数 ====================

def quick_evaluate(agent_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    快速评估（单次使用）
    """
    engine = UltimateEvaluationEngine()
    return engine.evaluate(agent_data.get("id", "temp"), agent_data)


def quick_rank(agents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    快速排行（单次使用）
    """
    engine = UltimateEvaluationEngine()
    return engine.rank_agents(agents)


if __name__ == "__main__":
    # 示例
    sample_agent = {
        "id": "demo-agent-001",
        "name": "演示AI助手",
        "type": "对话Agent",
        # 高府五维
        "capability": 85,
        "security": 80,
        "collaboration": 75,
        "evolution": 82,
        "ethics": 78,
        # 帝意五维
        "dao_hang": 80,
        "fa_xing": 85,
        "li_xing": 70,
        "yu_xing": 78,
        "shou_xing": 80,
        # RAC相关
        "is_open_source": True,
        "has_audit_report": True,
        "description": "一个优秀的通用对话AI助手"
    }
    
    engine = UltimateEvaluationEngine()
    report = engine.evaluate("demo-agent-001", sample_agent)
    
    print("=" * 60)
    print(f"📊 综合评估报告: {report['agent_name']}")
    print("=" * 60)
    print(f"高府认证: {report['gaofu_certification']['level']} ({report['gaofu_certification']['overall_score']})")
    print(f"帝意排行: {report['diyi_ranking']['diyi_level']} ({report['diyi_ranking']['diyi_score']})")
    print(f"RAC信任: {report['rac_analysis']['risk_level']} ({report['rac_analysis']['trust_score']})")
    print(f"综合价值: {report['comprehensive_value']['score']}")
    print(f"投资建议: {report['investment_advice']['战略定位']}")
    print("=" * 60)

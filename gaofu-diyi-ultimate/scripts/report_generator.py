#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高府·帝意 综合评估系统 - 综合报告生成器
Gaofu-Diyi Ultimate Evaluation System - Report Generator
"""

from typing import Dict, List, Any
import json


class UltimateReportGenerator:
    """
    综合报告生成器
    
    支持多种格式输出：
    - 格式化文本（控制台）
    - Markdown
    - JSON
    """
    
    # 颜色定义
    COLORS = {
        "reset": "\033[0m",
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "purple": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[97m",
        "gray": "\033[90m"
    }
    
    # 等级颜色映射
    LEVEL_COLORS = {
        "传奇": "purple",
        "钻石": "cyan",
        "铂金": "green",
        "黄金": "yellow",
        "临时": "gray",
        "拒绝": "red",
        "S级帝意": "purple",
        "A级天枢": "cyan",
        "B级地衡": "green",
        "C级人合": "yellow",
        "D级物用": "gray"
    }
    
    # 风险颜色
    RISK_COLORS = {
        "LOW": "green",
        "MEDIUM": "yellow",
        "HIGH": "red"
    }
    
    @staticmethod
    def _colorize(text: str, color: str) -> str:
        """添加颜色"""
        return f"{UltimateReportGenerator.COLORS.get(color, '')}{text}{UltimateReportGenerator.COLORS['reset']}"
    
    @staticmethod
    def _format_bar(score: float, width: int = 10) -> str:
        """格式化分数条"""
        filled = int((score / 100) * width)
        empty = width - filled
        return "█" * filled + "░" * empty
    
    @staticmethod
    def format_report(report: Dict[str, Any]) -> str:
        """
        格式化完整评估报告（控制台友好）
        """
        lines = []
        
        # 标题
        lines.append("=" * 70)
        lines.append(f"🤖 {report['agent_name']} - 高府·帝意 综合评估报告")
        lines.append("=" * 70)
        lines.append(f"报告ID: {report['report_id']}")
        lines.append(f"评估时间: {report['evaluated_at']}")
        lines.append("")
        
        # ============ 高府认证 ============
        gaofu = report["gaofu_certification"]
        gaofu_color = UltimateReportGenerator.LEVEL_COLORS.get(gaofu["level"], "white")
        
        lines.append("【🏛️ 高府认证】")
        lines.append("-" * 50)
        lines.append(f"  认证分: {gaofu['overall_score']:.2f}")
        lines.append(f"  认证等级: {UltimateReportGenerator._colorize(gaofu['level'], gaofu_color)} {gaofu['badge']}")
        lines.append(f"  认证状态: {'✅ 通过' if gaofu['status'] == 'certified' else '⚠️ 临时' if gaofu['status'] == 'provisional' else '❌ 拒绝'}")
        
        # 红线检查
        rl = gaofu["red_line_check"]
        lines.append(f"  红线检查: {'✅ 全部通过' if rl['passed'] else f'⚠️ {len(rl[\"fatal_violations\"])}项致命'}")
        lines.append("")
        
        # ============ 帝意排行 ============
        diyi = report["diyi_ranking"]
        diyi_color = UltimateReportGenerator.LEVEL_COLORS.get(diyi["diyi_level"], "white")
        
        lines.append("【🏆 帝意排行】")
        lines.append("-" * 50)
        lines.append(f"  帝意分: {diyi['diyi_score']:.2f}")
        lines.append(f"  帝意等级: {UltimateReportGenerator._colorize(diyi['diyi_level'], diyi_color)}")
        
        # 五维得分
        dims = diyi["dimensions"]
        lines.append("  DIYMCE五维:")
        for key, name in [("dao_hang", "道行"), ("fa_xing", "法行"), 
                          ("li_xing", "利行"), ("yu_xing", "愈行"), 
                          ("shou_xing", "守行")]:
            score = dims[key]["score"]
            bar = UltimateReportGenerator._format_bar(score)
            lines.append(f"    {name} [{dims[key]['weight']}]: {score:5.1f} |{bar}|")
        lines.append("")
        
        # ============ RAC信任分析 ============
        rac = report["rac_analysis"]
        risk_color = UltimateReportGenerator.RISK_COLORS.get(rac["risk_level"], "white")
        
        lines.append("【🔐 RAC信任分析】")
        lines.append("-" * 50)
        lines.append(f"  信任分: {rac['trust_score']:.2f}")
        lines.append(f"  信任因子: {rac['trust_factor']:.3f}")
        lines.append(f"  风险等级: {UltimateReportGenerator._colorize(rac['risk_level'], risk_color)}")
        lines.append(f"  风险折扣: {rac['risk_discount']:.2f}")
        lines.append(f"  开源状态: {'✅ 开源' if rac['is_open_source'] else '❌ 闭源'}")
        lines.append(f"  审计报告: {'✅ 已审计' if rac['has_audit_report'] else '❌ 未审计'}")
        lines.append("")
        
        # ============ 综合价值 ============
        cv = report["comprehensive_value"]
        
        lines.append("【💰 综合价值】")
        lines.append("-" * 50)
        bar = UltimateReportGenerator._format_bar(cv["score"])
        lines.append(f"  综合得分: {cv['score']:.2f}")
        lines.append(f"  计算过程: {cv['calculation']} = {cv['score']:.2f}")
        lines.append(f"  {'':8}|{bar}|")
        lines.append("")
        
        # ============ 投资建议 ============
        advice = report["investment_advice"]
        
        lines.append("【💼 投资建议】")
        lines.append("-" * 50)
        lines.append(f"  战略定位: {advice['战略定位']}")
        lines.append(f"  定位说明: {advice['定位说明']}")
        lines.append(f"  建议仓位: {advice['建议仓位']}")
        lines.append(f"  持有周期: {advice['持有周期']}")
        lines.append(f"  风险对冲: {advice['风险对冲']}")
        lines.append(f"  入场时机: {advice['入场时机']}")
        lines.append("")
        
        lines.append("=" * 70)
        
        return "\n".join(lines)
    
    @staticmethod
    def format_rankings(rankings: List[Dict[str, Any]], top_n: int = None) -> str:
        """
        格式化排行榜
        """
        if not rankings:
            return "暂无排行榜数据"
        
        display_rankings = rankings[:top_n] if top_n else rankings
        
        lines = []
        
        # 表头
        header = f"{'排名':^4} {'名称':^18} {'高府分':^8} {'高府等级':^8} {'帝意分':^8} {'帝意等级':^10} {'综合':^8} {'建议':^10}"
        lines.append(header)
        lines.append("-" * len(header))
        
        for item in display_rankings:
            medal = {1: "🥇", 2: "🥈", 3: "🥉"}.get(item["rank"], "  ")
            name = item["name"][:16] if len(item["name"]) > 16 else item["name"]
            
            lines.append(
                f"{medal}{item['rank']:>2} {name:<18} "
                f"{item['gaofu_score']:>6.1f}  {item['gaofu_level']:<6} "
                f"{item['diyi_score']:>6.1f}  {item['diyi_level']:<8} "
                f"{item['comprehensive_value']:>6.2f}  {item['strategy']:<10}"
            )
        
        lines.append("-" * len(header))
        
        return "\n".join(lines)
    
    @staticmethod
    def to_markdown(report: Dict[str, Any]) -> str:
        """
        导出为Markdown格式
        """
        lines = []
        
        # 标题
        lines.append(f"# 🤖 {report['agent_name']}")
        lines.append("")
        lines.append(f"**报告ID**: {report['report_id']}")
        lines.append(f"**评估时间**: {report['evaluated_at']}")
        lines.append(f"**Agent类型**: {report['agent_type']}")
        lines.append("")
        
        # 高府认证
        gaofu = report["gaofu_certification"]
        lines.append("## 🏛️ 高府认证")
        lines.append("")
        lines.append(f"| 项目 | 数值 |")
        lines.append(f"|------|------|")
        lines.append(f"| 认证分 | {gaofu['overall_score']} |")
        lines.append(f"| 认证等级 | {gaofu['level']} {gaofu['badge']} |")
        lines.append(f"| 认证状态 | {gaofu['status']} |")
        lines.append("")
        
        # 帝意排行
        diyi = report["diyi_ranking"]
        lines.append("## 🏆 帝意排行")
        lines.append("")
        lines.append(f"| 维度 | 分数 | 权重 |")
        lines.append(f"|------|------|------|")
        for key, name in [("dao_hang", "道行"), ("fa_xing", "法行"), 
                          ("li_xing", "利行"), ("yu_xing", "愈行"), 
                          ("shou_xing", "守行")]:
            lines.append(f"| {name} | {diyi['dimensions'][key]['score']} | {diyi['dimensions'][key]['weight']} |")
        lines.append(f"| **帝意等级** | {diyi['diyi_level']} | - |")
        lines.append("")
        
        # RAC分析
        rac = report["rac_analysis"]
        lines.append("## 🔐 RAC信任分析")
        lines.append("")
        lines.append(f"| 项目 | 数值 |")
        lines.append(f"|------|------|")
        lines.append(f"| 信任分 | {rac['trust_score']} |")
        lines.append(f"| 风险等级 | {rac['risk_level']} |")
        lines.append(f"| 开源 | {'是' if rac['is_open_source'] else '否'} |")
        lines.append(f"| 审计报告 | {'是' if rac['has_audit_report'] else '否'} |")
        lines.append("")
        
        # 综合价值
        cv = report["comprehensive_value"]
        lines.append("## 💰 综合价值")
        lines.append("")
        lines.append(f"**综合得分**: {cv['score']}")
        lines.append("")
        
        # 投资建议
        advice = report["investment_advice"]
        lines.append("## 💼 投资建议")
        lines.append("")
        lines.append(f"| 项目 | 建议 |")
        lines.append(f"|------|------|")
        lines.append(f"| 战略定位 | {advice['战略定位']} |")
        lines.append(f"| 建议仓位 | {advice['建议仓位']} |")
        lines.append(f"| 持有周期 | {advice['持有周期']} |")
        lines.append(f"| 风险对冲 | {advice['风险对冲']} |")
        lines.append("")
        
        # 免责声明
        lines.append("---")
        lines.append("")
        lines.append("> ⚠️ 本报告由高府·帝意综合评估系统v6.0生成，仅供参考，不构成投资建议。")
        
        return "\n".join(lines)
    
    @staticmethod
    def to_json(report: Dict[str, Any]) -> str:
        """导出为JSON格式"""
        return json.dumps(report, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    # 测试
    from integration_engine import quick_evaluate
    
    sample = {
        "id": "test",
        "name": "测试AI助手",
        "type": "对话",
        "capability": 85,
        "security": 80,
        "collaboration": 75,
        "evolution": 82,
        "ethics": 78,
        "dao_hang": 80,
        "fa_xing": 85,
        "li_xing": 70,
        "yu_xing": 78,
        "shou_xing": 80,
        "is_open_source": True,
        "has_audit_report": True
    }
    
    report = quick_evaluate(sample)
    print(UltimateReportGenerator.format_report(report))

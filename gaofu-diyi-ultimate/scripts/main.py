#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高府·帝意 综合评估系统 - 命令行入口
Gaofu-Diyi Ultimate Evaluation System - CLI Entry

用法:
    python main.py evaluate <agent_id>
    python main.py rank --name <ranking_name>
    python main.py demo
    python main.py list agents
"""

import sys
import os
import json
from pathlib import Path

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from integration_engine import UltimateEvaluationEngine
from report_generator import UltimateReportGenerator


def load_sample_agents():
    """加载示例Agent数据"""
    return [
        {
            "id": "agent-001",
            "name": "ChatGPT",
            "type": "通用对话",
            "capability": 92,
            "security": 88,
            "collaboration": 85,
            "evolution": 95,
            "ethics": 90,
            "dao_hang": 90,
            "fa_xing": 92,
            "li_xing": 95,
            "yu_xing": 88,
            "shou_xing": 88,
            "is_open_source": False,
            "has_audit_report": True,
            "description": "OpenAI开发的通用对话AI"
        },
        {
            "id": "agent-002",
            "name": "Claude",
            "type": "通用对话",
            "capability": 90,
            "security": 92,
            "collaboration": 88,
            "evolution": 90,
            "ethics": 95,
            "dao_hang": 92,
            "fa_xing": 88,
            "li_xing": 85,
            "yu_xing": 90,
            "shou_xing": 92,
            "is_open_source": False,
            "has_audit_report": True,
            "description": "Anthropic开发的AI助手"
        },
        {
            "id": "agent-003",
            "name": "Llama",
            "type": "开源模型",
            "capability": 78,
            "security": 80,
            "collaboration": 85,
            "evolution": 82,
            "ethics": 75,
            "dao_hang": 75,
            "fa_xing": 80,
            "li_xing": 70,
            "yu_xing": 72,
            "shou_xing": 80,
            "is_open_source": True,
            "has_audit_report": False,
            "description": "Meta开源大语言模型"
        },
        {
            "id": "agent-004",
            "name": "理想L9",
            "type": "智能汽车",
            "capability": 88,
            "security": 92,
            "collaboration": 82,
            "evolution": 90,
            "ethics": 85,
            "dao_hang": 85,
            "fa_xing": 88,
            "li_xing": 90,
            "yu_xing": 88,
            "shou_xing": 92,
            "is_open_source": False,
            "has_audit_report": True,
            "description": "理想汽车智能座舱AI"
        }
    ]


def cmd_evaluate(agent_id: str):
    """评估单个Agent"""
    agents = load_sample_agents()
    target = None
    
    for agent in agents:
        if agent["id"] == agent_id:
            target = agent
            break
    
    if not target:
        # 创建自定义Agent
        print(f"Agent '{agent_id}' 不在示例中，请提供完整数据...")
        target = {
            "id": agent_id,
            "name": input("名称: "),
            "type": input("类型: "),
            "capability": float(input("能力表现(0-100): ")),
            "security": float(input("安全保障(0-100): ")),
            "collaboration": float(input("协作能力(0-100): ")),
            "evolution": float(input("进化潜力(0-100): ")),
            "ethics": float(input("伦理合规(0-100): ")),
            "dao_hang": float(input("道行(0-100): ")),
            "fa_xing": float(input("法行(0-100): ")),
            "li_xing": float(input("利行(0-100): ")),
            "yu_xing": float(input("愈行(0-100): ")),
            "shou_xing": float(input("守行(0-100): ")),
            "is_open_source": input("是否开源(y/n): ").lower() == 'y',
            "has_audit_report": input("是否有审计报告(y/n): ").lower() == 'y'
        }
    
    engine = UltimateEvaluationEngine()
    report = engine.evaluate(agent_id, target)
    
    print("\n" + UltimateReportGenerator.format_report(report))
    
    return report


def cmd_rank(name: str = "default", top_n: int = None):
    """生成排行榜"""
    agents = load_sample_agents()
    
    engine = UltimateEvaluationEngine()
    rankings = engine.rank_agents(agents)
    
    print(f"\n{'='*70}")
    print(f"🏆 帝意·高府 综合排行榜 - {name}")
    print(f"{'='*70}")
    print(UltimateReportGenerator.format_rankings(rankings, top_n))
    print(f"{'='*70}")
    
    return rankings


def cmd_demo():
    """运行演示"""
    print("\n" + "="*70)
    print("🎯 高府·帝意 综合评估系统 v6.0 演示")
    print("="*70)
    print()
    
    # 演示单个评估
    print("📊 单个Agent评估演示:")
    print("-"*50)
    
    demo_agent = {
        "id": "demo-agent",
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
    
    engine = UltimateEvaluationEngine()
    report = engine.evaluate("demo", demo_agent)
    
    print(UltimateReportGenerator.format_report(report))
    
    # 演示排行榜
    print("\n\n")
    cmd_rank("演示排行榜", top_n=4)
    
    # 演示Markdown导出
    print("\n\n📄 Markdown导出示例:")
    print("-"*50)
    print(UltimateReportGenerator.to_markdown(report)[:500] + "...")


def cmd_list(resource: str):
    """列出资源"""
    if resource == "agents":
        agents = load_sample_agents()
        print(f"\n{'='*50}")
        print(f"📋 可评估的Agent列表 (共{len(agents)}个)")
        print(f"{'='*50}")
        for agent in agents:
            print(f"  - {agent['id']}: {agent['name']} ({agent['type']})")
        print(f"{'='*50}")
    else:
        print(f"未知资源类型: {resource}")


def main():
    """主入口"""
    if len(sys.argv) < 2:
        print(__doc__)
        print("\n可用命令:")
        print("  demo              - 运行演示")
        print("  evaluate <id>     - 评估Agent")
        print("  rank [--name]     - 生成排行榜")
        print("  list agents       - 列出可评估的Agent")
        return
    
    cmd = sys.argv[1]
    
    if cmd == "demo":
        cmd_demo()
    elif cmd == "evaluate":
        if len(sys.argv) < 3:
            print("用法: evaluate <agent_id>")
            return
        cmd_evaluate(sys.argv[2])
    elif cmd == "rank":
        name = "default"
        top_n = None
        for i, arg in enumerate(sys.argv[2:], 2):
            if arg == "--name" and i+1 < len(sys.argv):
                name = sys.argv[i+1]
            elif arg == "--top" and i+1 < len(sys.argv):
                top_n = int(sys.argv[i+1])
        cmd_rank(name, top_n)
    elif cmd == "list":
        if len(sys.argv) < 3:
            print("用法: list <resource>")
            return
        cmd_list(sys.argv[2])
    else:
        print(f"未知命令: {cmd}")


if __name__ == "__main__":
    main()

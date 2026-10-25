#!/usr/bin/pwsh
# -*- coding: utf-8 -*-
<#
.SYNOPSIS
    高府·帝意 CLI 快速启动脚本

.DESCRIPTION
    快速启动并演示 CLI 功能

.NOTES
    版本: 6.0.0
    作者: 高府认证团队 & 帝意共识智脑
#>

# 导入模块
Import-Module "$PSScriptRoot\modules\gaofu-diyi-engine.psm1" -Force

# 创建演示数据
$demoAgents = @(
    @{
        id = "claude-3"
        name = "Claude 3"
        type = "对话Agent"
        description = "Anthropic的Claude 3 AI助手，注重安全性和有用性"
        capability = 92
        security = 88
        collaboration = 85
        evolution = 90
        ethics = 95
        dao_hang = 85
        fa_xing = 90
        li_xing = 80
        yu_xing = 88
        shou_xing = 92
        is_open_source = $false
        has_audit_report = $true
    },
    @{
        id = "gpt-4"
        name = "GPT-4"
        type = "对话Agent"
        description = "OpenAI的GPT-4，强大的语言理解能力"
        capability = 90
        security = 85
        collaboration = 88
        evolution = 87
        ethics = 92
        dao_hang = 88
        fa_xing = 85
        li_xing = 85
        yu_xing = 90
        shou_xing = 88
        is_open_source = $false
        has_audit_report = $true
    },
    @{
        id = "gemini"
        name = "Gemini"
        type = "对话Agent"
        description = "Google的多模态AI助手"
        capability = 88
        security = 90
        collaboration = 82
        evolution = 85
        ethics = 90
        dao_hang = 82
        fa_xing = 88
        li_xing = 75
        yu_xing = 85
        shou_xing = 90
        is_open_source = $false
        has_audit_report = $false
    }
)

# 创建评估引擎
$engine = [GaofuDiyiEngine]::new()

Write-Host "🚀 高府·帝意 综合评估系统 v6.0 - 快速演示" -ForegroundColor Yellow
Write-Host "================================================" -ForegroundColor Yellow
Write-Host ""

# 演示1: 评估单个Agent
Write-Host "演示1: 评估单个Agent" -ForegroundColor Cyan
Write-Host "------------------------" -ForegroundColor Cyan

$claudeReport = $engine.Evaluate("claude-3", $demoAgents[0])
Show-EvaluationResult -Result $claudeReport

# 演示2: 生成排行榜
Write-Host "`n演示2: 生成排行榜" -ForegroundColor Magenta
Write-Host "------------------------" -ForegroundColor Magenta

$rankings = $engine.RankAgents($demoAgents)
Show-Ranking -Rankings $rankings

# 演示3: 生成不同格式的报告
Write-Host "`n演示3: 生成不同格式的报告" -ForegroundColor Green
Write-Host "------------------------" -ForegroundColor Green

# 保存JSON报告
$jsonReport = $claudeReport | ConvertTo-Json -Depth 10
$jsonReport | Out-File ".\demo-report.json" -Encoding UTF8
Write-Host "JSON报告已保存到: .\demo-report.json" -ForegroundColor Green

# 保存HTML报告
$generator = [ReportGenerator]::new()
$htmlReport = $generator.GenerateHTMLReport($claudeReport)
$htmlReport | Out-File ".\demo-report.html" -Encoding UTF8
Write-Host "HTML报告已保存到: .\demo-report.html" -ForegroundColor Green

# 显示总结
Write-Host "`n" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Yellow
Write-Host "演示完成！" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Yellow
Write-Host ""
Write-Host "接下来您可以尝试:" -ForegroundColor White
Write-Host "1. 运行完整评估: .\gaofu-diyi.ps1 evaluate -AgentId your-agent" -ForegroundColor Gray
Write-Host "2. 查看帮助: .\gaofu-diyi.ps1 help" -ForegroundColor Gray
Write-Host "3. 安装到系统: .\install.ps1" -ForegroundColor Gray
Write-Host ""
Write-Host "生成的文件:" -ForegroundColor White
Write-Host "- JSON报告: .\demo-report.json" -ForegroundColor Gray
Write-Host "- HTML报告: .\demo-report.html" -ForegroundColor Gray
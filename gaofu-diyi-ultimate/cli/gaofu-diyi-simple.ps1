#!/usr/bin/pwsh
# -*- coding: utf-8 -*-

<#
.SYNOPSIS
    高府·帝意 综合评估系统 CLI 工具 v6.0

.DESCRIPTION
    PowerShell 版本的 CLI 工具，用于评估 AI Agent 系统
    支持快速评估、标准评估、深度评估等多种模式

.EXAMPLE
    .\gaofu-diyi-simple.ps1 evaluate -AgentId "test-agent" -Capability 85 -Security 80

.EXAMPLE
    .\gaofu-diyi-simple.ps1 rank -Top 10

.EXAMPLE
    .\gaofu-diyi-simple.ps1 report -AgentId "test-agent" -Format "HTML"
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory=$true, Position=0)]
    [ValidateSet("evaluate", "rank", "report", "help")]
    [string]$Command,

    [Parameter()]
    [string]$AgentId,

    [Parameter()]
    [string]$AgentName,

    [Parameter()]
    [string]$AgentType = "conversation",

    [Parameter()]
    [ValidateSet("quick", "standard", "deep")]
    [string]$Mode = "standard",

    [Parameter()]
    [int]$Capability,

    [Parameter()]
    [int]$Security,

    [Parameter()]
    [int]$Collaboration,

    [Parameter()]
    [int]$Evolution,

    [Parameter()]
    [int]$Ethics,

    [Parameter()]
    [int]$DaoHang,

    [Parameter()]
    [int]$FaXing,

    [Parameter()]
    [int]$LiXing,

    [Parameter()]
    [int]$YuXing,

    [Parameter()]
    [int]$ShouXing,

    [Parameter()]
    [switch]$IsOpenSource,

    [Parameter()]
    [switch]$HasAuditReport,

    [Parameter()]
    [int]$Top = 10,

    [Parameter()]
    [ValidateSet("text", "json", "html")]
    [string]$Format = "text",

    [Parameter()]
    [string]$OutputPath,

    [Parameter()]
    [switch]$Verbose
)

# 导入模块
Import-Module "$PSScriptRoot\modules\gaofu-diyi-engine.psm1" -Force

# 全局变量
$Script:VerbosePreference = if ($Verbose) { "Continue" } else { "SilentlyContinue" }

# 函数：显示帮助信息
function Show-Help {
    Write-Host @"
高府·帝意 综合评估系统 CLI 工具 v6.0

用法:
    .\gaofu-diyi-simple.ps1 <命令> [参数]

命令:
    evaluate    评估单个 Agent
    rank        生成排行榜
    report      生成评估报告
    help        显示帮助信息

评估参数:
    -AgentId <ID>          [必需] Agent ID
    -AgentName <名称>       Agent 显示名称
    -AgentType <类型>       Agent 类型 (默认: conversation)
    -Mode <模式>           评估模式: quick|standard|deep (默认: standard)

    高府五维 (0-100):
    -Capability <分数>     能力表现
    -Security <分数>       安全保障
    -Collaboration <分数>  协作能力
    -Evolution <分数>      进化潜力
    -Ethics <分数>        伦理合规

    帝意五维 (0-100):
    -DaoHang <分数>        道行 - 战略认知
    -FaXing <分数>        法行 - 执行力
    -LiXing <分数>        利行 - 商业价值
    -YuXing <分数>        愈行 - 用户体验
    -ShouXing <分数>      守行 - 安全合规

    RAC 信任:
    -IsOpenSource          是否开源 (开关参数)
    -HasAuditReport       是否有审计报告 (开关参数)

排行参数:
    -Top <数量>           显示前 N 名 (默认: 10)

报告参数:
    -Format <格式>        输出格式: text|json|html (默认: text)
    -OutputPath <路径>     输出文件路径

其他参数:
    -Verbose              显示详细信息
    -Help                显示此帮助信息

示例:
    # 快速评估
    .\gaofu-diyi-simple.ps1 evaluate -AgentId "claude" -Capability 90 -Security 85 -Mode quick

    # 标准评估
    .\gaofu-diyi-simple.ps1 evaluate -AgentId "chatgpt" -Capability 88 -Security 82 -Collaboration 80 -Evolution 85 -Ethics 90

    # 深度评估（包含所有维度）
    .\gaofu-diyi-simple.ps1 evaluate -AgentId "gemini" -Capability 85 -Security 80 -Collaboration 75 -Evolution 82 -Ethics 78 -DaoHang 80 -FaXing 85 -LiXing 70 -YuXing 78 -ShouXing 80 -IsOpenSource -HasAuditReport

    # 生成排行榜
    .\gaofu-diyi-simple.ps1 rank -Top 5

    # 生成 JSON 格式报告
    .\gaofu-diyi-simple.ps1 report -AgentId "claude" -Format json

    # 保存 HTML 报告到文件
    .\gaofu-diyi-simple.ps1 report -AgentId "claude" -Format html -OutputPath ".\report.html"

更多信息请访问: https://github.com/gaofu-diyi/ultimate-system
"@
}

# 函数：显示评估结果
function Show-EvaluationResult {
    param([object]$Result)

    Write-Host "`n" -ForegroundColor Yellow
    Write-Host ("=" * 60) -ForegroundColor Yellow
    Write-Host "📊 高府·帝意 综合评估报告" -ForegroundColor Yellow
    Write-Host ("=" * 60) -ForegroundColor Yellow
    Write-Host "Agent ID: $($Result.agent_id)" -ForegroundColor White
    Write-Host "Agent 名称: $($Result.agent_name)" -ForegroundColor White
    Write-Host "评估时间: $($Result.evaluated_at)" -ForegroundColor Gray

    # 高府认证结果
    Write-Host "`n🏛️ 高府认证" -ForegroundColor Cyan
    Write-Host ("-" * 30) -ForegroundColor Cyan
    $gaofu = $Result.gaofu_certification
    $statusColor = if ($gaofu.status -eq "certified") { "Green" } elseif ($gaofu.status -eq "rejected") { "Red" } else { "Yellow" }
    Write-Host "认证状态: $($gaofu.status)" -ForegroundColor $statusColor
    Write-Host "认证等级: $($gaofu.level) $($gaofu.badge)" -ForegroundColor White
    Write-Host "综合得分: $($gaofu.overall_score)" -ForegroundColor White

    # 帝意排行结果
    Write-Host "`n🏆 帝意排行" -ForegroundColor Magenta
    Write-Host ("-" * 30) -ForegroundColor Magenta
    $diyi = $Result.diyi_ranking
    Write-Host "帝意等级: $($diyi.diyi_level)" -ForegroundColor White
    Write-Host "综合得分: $($diyi.diyi_score)" -ForegroundColor White

    # RAC 信任分析
    Write-Host "`n🔐 RAC 信任分析" -ForegroundColor Green
    Write-Host ("-" * 30) -ForegroundColor Green
    $rac = $Result.rac_analysis
    $riskColor = if ($rac.risk_level -eq "LOW") { "Green" } elseif ($rac.risk_level -eq "MEDIUM") { "Yellow" } else { "Red" }
    Write-Host "信任得分: $($rac.trust_score)" -ForegroundColor White
    Write-Host "信任因子: $($rac.trust_factor)" -ForegroundColor White
    Write-Host "风险等级: $($rac.risk_level)" -ForegroundColor $riskColor
    Write-Host "风险折扣: $($rac.risk_discount)" -ForegroundColor White

    # 综合价值
    Write-Host "`n💎 综合价值" -ForegroundColor Yellow
    Write-Host ("-" * 30) -ForegroundColor Yellow
    $value = $Result.comprehensive_value
    Write-Host "综合得分: $($value.score)" -ForegroundColor White
    Write-Host "计算公式: $($value.calculation)" -ForegroundColor Gray

    # 投资建议
    Write-Host "`n💼 投资建议" -ForegroundColor Yellow
    Write-Host ("-" * 30) -ForegroundColor Yellow
    $advice = $Result.investment_advice
    Write-Host "战略定位: $($advice.战略定位)" -ForegroundColor White
    Write-Host "定位说明: $($advice.定位说明)" -ForegroundColor White
    Write-Host "建议仓位: $($advice.建议仓位)" -ForegroundColor White
    Write-Host "持有周期: $($advice.持有周期)" -ForegroundColor White
    Write-Host "风险对冲: $($advice.风险对冲)" -ForegroundColor White
    Write-Host "入场时机: $($advice.入场时机)" -ForegroundColor White

    Write-Host "`n" -ForegroundColor Yellow
}

# 函数：显示排行榜
function Show-Ranking {
    param([array]$Rankings)

    Write-Host "`n" -ForegroundColor Yellow
    Write-Host ("=" * 80) -ForegroundColor Yellow
    Write-Host "🏆 帝意排行榜" -ForegroundColor Yellow
    Write-Host ("=" * 80) -ForegroundColor Yellow
    Write-Host "时间: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")`n" -ForegroundColor Gray

    # 表头
    Write-Host ("排名".PadRight(6) + "Agent ID".PadRight(20) + "名称".PadRight(20) + "高府".PadRight(10) + "帝意".PadRight(10) + "信任".PadRight(10) + "综合".PadRight(10) + "策略") -ForegroundColor Cyan

    foreach ($item in $Rankings) {
        $gaofuColor = if ($item.gaofu_level -eq "传奇") { "Yellow" } elseif ($item.gaofu_level -eq "钻石") { "Cyan" } elseif ($item.gaofu_level -eq "铂金") { "White" } else { "Gray" }

        Write-Host (
            ($item.rank.ToString().PadRight(6)) +
            ($item.agent_id.PadRight(20)) +
            ($item.name.PadRight(20)) +
            ("$($item.gaofu_score)".PadRight(10)) +
            ("$($item.diyi_score)".PadRight(10)) +
            ("$($item.rac_trust_score)".PadRight(10)) +
            ("$($item.comprehensive_value)".PadRight(10)) +
            $item.strategy
        ) -ForegroundColor $gaofuColor
    }

    Write-Host "`n"
}

# 主程序入口
try {
    # 处理 help 命令
    if ($Command -eq "help" -or $Command -eq "-h" -or $Command -eq "--help") {
        Show-Help
        exit 0
    }

    Write-Verbose "执行命令: $Command"

    # 创建评估引擎
    $engine = [GaofuDiyiEngine]::new()

    switch ($Command) {
        "evaluate" {
            # 验证必需的 AgentId
            if (-not $AgentId) {
                throw "AgentId 是必需参数"
            }

            # 构建 Agent 数据
            $agentData = @{
                id = $AgentId
                name = $AgentName -or $AgentId
                type = $AgentType
                description = ""
            }

            # 添加高府五维
            if ($Capability) { $agentData.capability = $Capability }
            if ($Security) { $agentData.security = $Security }
            if ($Collaboration) { $agentData.collaboration = $Collaboration }
            if ($Evolution) { $agentData.evolution = $Evolution }
            if ($Ethics) { $agentData.ethics = $Ethics }

            # 添加帝意五维
            if ($DaoHang) { $agentData.dao_hang = $DaoHang }
            if ($FaXing) { $agentData.fa_xing = $FaXing }
            if ($LiXing) { $agentData.li_xing = $LiXing }
            if ($YuXing) { $agentData.yu_xing = $YuXing }
            if ($ShouXing) { $agentData.shou_xing = $ShouXing }

            # 添加 RAC 信任相关
            if ($IsOpenSource.IsPresent) { $agentData.is_open_source = $true }
            if ($HasAuditReport.IsPresent) { $agentData.has_audit_report = $true }

            Write-Verbose "开始评估 Agent: $AgentId"

            # 执行评估
            $result = $engine.Evaluate($AgentId, $agentData, $Mode)

            # 显示结果
            Show-EvaluationResult -Result $result

            # 保存结果到文件
            if ($OutputPath) {
                $result | ConvertTo-Json -Depth 10 | Out-File $OutputPath
                Write-Host "评估结果已保存到: $OutputPath" -ForegroundColor Green
            }
        }

        "rank" {
            Write-Verbose "生成排行榜"

            # 创建示例数据
            $sampleAgents = @(
                @{ id = "claude-3"; name = "Claude 3"; capability = 92; security = 88; collaboration = 85; evolution = 90; ethics = 95; dao_hang = 85; fa_xing = 90; li_xing = 80; yu_xing = 88; shou_xing = 92; is_open_source = $false; has_audit_report = $true },
                @{ id = "gpt-4"; name = "GPT-4"; capability = 90; security = 85; collaboration = 88; evolution = 87; ethics = 92; dao_hang = 88; fa_xing = 85; li_xing = 85; yu_xing = 90; shou_xing = 88; is_open_source = $false; has_audit_report = $true },
                @{ id = "gemini"; name = "Gemini"; capability = 88; security = 90; collaboration = 82; evolution = 85; ethics = 90; dao_hang = 82; fa_xing = 88; li_xing = 75; yu_xing = 85; shou_xing = 90; is_open_source = $false; has_audit_report = $false }
            )

            # 生成排名
            $rankings = $engine.RankAgents($sampleAgents)

            # 只显示前 N 名
            if ($Top -and $Top -lt $rankings.Count) {
                $rankings = $rankings[0..($Top-1)]
            }

            # 显示排行榜
            Show-Ranking -Rankings $rankings

            # 保存结果
            if ($OutputPath) {
                $rankings | ConvertTo-Json -Depth 5 | Out-File $OutputPath
                Write-Host "排行榜已保存到: $OutputPath" -ForegroundColor Green
            }
        }

        "report" {
            if (-not $AgentId) {
                throw "生成报告需要指定 -AgentId 参数"
            }

            Write-Verbose "生成报告: $AgentId, 格式: $Format"

            # 创建示例报告
            $sampleResult = @{
                report_id = "GF-DY-$(Get-Date -Format 'yyyyMMdd')-$(Get-Random -Minimum 1000 -Maximum 9999)"
                agent_id = $AgentId
                agent_name = $AgentName -or $AgentId
                agent_type = "conversation"
                evaluated_at = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
                mode = "standard"
                version = "6.0.0"
                description = ""
                gaofu_certification = @{
                    overall_score = 85
                    status = "certified"
                    level = "钻石"
                    badge = "💎"
                    red_line_check = @{
                        fatal_violations = @()
                        warnings = @()
                        best_practices_met = @()
                        passed = $true
                    }
                    dimensions = @{
                        capability = 85
                        security = 80
                        collaboration = 75
                        evolution = 82
                        ethics = 78
                    }
                }
                diyi_ranking = @{
                    diyi_score = 88
                    diyi_level = "A级天枢"
                    level_description = "优秀代表，值得信赖"
                    dimensions = @{
                        dao_hang = @{ score = 85; weight = "25%" }
                        fa_xing = @{ score = 90; weight = "30%" }
                        li_xing = @{ score = 85; weight = "15%" }
                        yu_xing = @{ score = 90; weight = "15%" }
                        shou_xing = @{ score = 85; weight = "15%" }
                    }
                }
                rac_analysis = @{
                    trust_score = 85
                    trust_factor = 0.94
                    risk_level = "LOW"
                    risk_discount = 1.00
                    risk_info = @{
                        description = "低风险"
                        discount = 1.00
                        characteristics = @("守行得分≥80", "信任分≥80", "无重大历史违规", "开源且有审计")
                    }
                    is_open_source = $false
                    has_audit_report = $true
                }
                comprehensive_value = @{
                    score = 80.9
                    calculation = "85 × 0.94 × 1.00"
                }
                investment_advice = @{
                    strategic_position = "核心配置"
                    positioning_description = "建议作为投资组合的核心标的，重点关注"
                    recommended_position = "10-20%"
                    holding_period = "长期（1年以上）"
                    risk_hedge = "可适度加仓，关注长期价值增长"
                    entry_timing = "可考虑分批建仓"
                }
            }

            # 根据格式生成报告
            switch ($Format) {
                "text" {
                    Show-EvaluationResult -Result $sampleResult
                }

                "json" {
                    $jsonOutput = $sampleResult | ConvertTo-Json -Depth 10
                    if ($OutputPath) {
                        $jsonOutput | Out-File $OutputPath
                        Write-Host "JSON 报告已保存到: $OutputPath" -ForegroundColor Green
                    } else {
                        $jsonOutput
                    }
                }

                "html" {
                    $htmlOutput = @"
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>高府·帝意 综合评估报告</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 20px rgba(0,0,0,0.1); }
        .header { text-align: center; margin-bottom: 30px; }
        .section { margin-bottom: 30px; }
        .section-title { font-size: 1.8em; color: #667eea; margin-bottom: 20px; }
        .card { background: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
        .score { font-size: 3em; font-weight: bold; text-align: center; margin: 20px 0; }
        .score-gaofu { color: #00CED1; }
        .score-diyi { color: #4ECDC4; }
        .score-trust { color: #3498db; }
        .score-comprehensive { color: #9b59b6; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
        th { background: #667eea; color: white; }
        .badge { display: inline-block; padding: 5px 10px; border-radius: 20px; font-weight: bold; margin-left: 10px; }
        .badge-diamond { background: #00CED1; color: white; }
        .badge-a { background: #4ECDC4; color: white; }
        .badge-low { background: #2ECC71; color: white; }
        .footer { text-align: center; margin-top: 40px; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>高府·帝意 综合评估报告</h1>
            <p>版本 6.0.0 | 评估时间: $($sampleResult.evaluated_at)</p>
        </div>

        <div class="section">
            <h2 class="section-title">🏛️ 高府认证</h2>
            <div class="card">
                <h3>$($sampleResult.gaofu_certification.level) <span class="badge badge-diamond">$($sampleResult.gaofu_certification.badge)</span></h3>
                <div class="score score-gaofu">$($sampleResult.gaofu_certification.overall_score)</div>
                <p>综合得分</p>
            </div>
        </div>

        <div class="section">
            <h2 class="section-title">🏆 帝意排行</h2>
            <div class="card">
                <h3>$($sampleResult.diyi_ranking.diyi_level)</h3>
                <div class="score score-diyi">$($sampleResult.diyi_ranking.diyi_score)</div>
                <p>综合得分</p>
            </div>
        </div>

        <div class="section">
            <h2 class="section-title">🔐 RAC 信任分析</h2>
            <div class="card">
                <h3>风险等级: $($sampleResult.rac_analysis.risk_level) <span class="badge badge-low">$($sampleResult.rac_analysis.risk_info.description)</span></h3>
                <div class="score score-trust">$($sampleResult.rac_analysis.trust_score)</div>
                <p>信任得分</p>
            </div>
        </div>

        <div class="section">
            <h2 class="section-title">💎 综合价值</h2>
            <div class="card">
                <div class="score score-comprehensive">$($sampleResult.comprehensive_value.score)</div>
                <p>综合得分</p>
                <p>计算公式: $($sampleResult.comprehensive_value.calculation)</p>
            </div>
        </div>

        <div class="section">
            <h2 class="section-title">💼 投资建议</h2>
            <table>
                <tr><th>项目</th><th>详情</th></tr>
                <tr><td>战略定位</td><td>$($sampleResult.investment_advice.strategic_position)</td></tr>
                <tr><td>建议仓位</td><td>$($sampleResult.investment_advice.recommended_position)</td></tr>
                <tr><td>持有周期</td><td>$($sampleResult.investment_advice.holding_period)</td></tr>
            </table>
        </div>

        <div class="footer">
            <p>本报告由高府·帝意综合评估系统 v6.0 生成</p>
            <p>© 2026 高府认证团队 & 帝意共识智脑</p>
        </div>
    </div>
</body>
</html>
"@

                    if ($OutputPath) {
                        $htmlOutput | Out-File $OutputPath -Encoding UTF8
                        Write-Host "HTML 报告已保存到: $OutputPath" -ForegroundColor Green
                    } else {
                        $htmlOutput
                    }
                }
            }
        }

        default {
            Write-Host "未知命令: $Command" -ForegroundColor Red
            Show-Help
            exit 1
        }
    }
}
catch {
    Write-Host "错误: $($_.Exception.Message)" -ForegroundColor Red
    if ($Verbose) {
        Write-Host $($_.ScriptStackTrace) -ForegroundColor Red
    }
    exit 1
}
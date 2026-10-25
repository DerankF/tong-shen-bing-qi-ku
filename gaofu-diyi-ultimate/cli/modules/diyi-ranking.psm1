<#
.SYNOPSIS
    帝意排行模块 - PowerShell 版本

.DESCRIPTION
    实现帝意五维排行体系和商业价值评估

.NOTES
    版本: 6.0.0
    作者: 帝意共识智脑
#>

class DiyiRankingEngine {
    <#
    .SYNOPSIS
        帝意排行引擎
    #>

    # 帝意五维权重 (DIYMCE)
    [hashtable]$_diymceWeights = @{
        dao_hang = 0.25    # 道行 - 战略认知 (25%)
        fa_xing = 0.30     # 法行 - 执行力 (30%)
        li_xing = 0.15     # 利行 - 商业价值 (15%)
        yu_xing = 0.15     # 愈行 - 用户体验 (15%)
        shou_xing = 0.15   # 守行 - 安全合规 (15%)
    }

    # 帝意等级
    [array]$_diyiLevels = @(
        @{ threshold = 95; name = "S级帝意"; description = "行业标杆，引领发展" },
        @{ threshold = 85; name = "A级天枢"; description = "优秀代表，值得信赖" },
        @{ threshold = 75; name = "B级地衡"; description = "良好水平，可持续发展" },
        @{ threshold = 60; name = "C级人合"; description = "中等水平，需持续改进" },
        @{ threshold = 0; name = "D级物用"; description = "基础可用，需大幅提升" }
    )

    DiyiRankingEngine() {
        Write-Verbose "初始化帝意排行引擎"
    }

    [hashtable] CalculateDiyiScore([hashtable]$agent) {
        <#
        .SYNOPSIS
            计算帝意商业得分
        .PARAMETER agent
            Agent 数据
        #>

        $score = 0.0
        $dimensionScores = @{}

        foreach ($dimension in $this._diymceWeights.Keys) {
            if ($agent.ContainsKey($dimension)) {
                $score += $agent[$dimension] * $this._diymceWeights[$dimension]
                $dimensionScores[$dimension] = @{
                    score = $agent[$dimension]
                    weight = "$($this._diymceWeights[$dimension] * 100)%"
                }
            }
        }

        return @{
            score = [math]::Round($score, 2)
            weights = $this._diymceWeights
            dimensions = $dimensionScores
        }
    }

    [hashtable] GetDiyiLevel([float]$score) {
        <#
        .SYNOPSIS
            获取帝意等级
        .PARAMETER score
            帝意得分
        #>

        foreach ($level in $this._diyiLevels) {
            if ($score -ge $level.threshold) {
                return $level
            }
        }

        return $this._diyiLevels[-1] # 返回最低等级
    }

    [hashtable] CalculateBusinessValue([hashtable]$agent) {
        <#
        .SYNOPSIS
            计算商业价值指标
        .PARAMETER agent
            Agent 数据
        #>

        $diyiScore = $this.CalculateDiyiScore($agent)
        $diyiLevel = $this.GetDiyiLevel($diyiScore.score)

        # 计算各维度的优势分析
        $strengths = @()
        $weaknesses = @()

        foreach ($dim in $diyiScore.dimensions.PSObject.Properties) {
            $dimName = $dim.Name
            $dimScore = $diyiScore.dimensions.$dimName.score

            if ($dimScore -ge 80) {
                $strengths += @{
                    dimension = $dimName
                    score = $dimScore
                    reason = $this._GetStrengthReason($dimName, $dimScore)
                }
            }
            elseif ($dimScore -lt 60) {
                $weaknesses += @{
                    dimension = $dimName
                    score = $dimScore
                    suggestion = $this._GetImprovementSuggestion($dimName)
                }
            }
        }

        return @{
            diyi_score = $diyiScore.score
            diyi_level = $diyiLevel.name
            level_description = $diyiLevel.description
            dimensions = $diyiScore.dimensions
            strengths = $strengths
            weaknesses = $weaknesses
            potential_score = $this._CalculatePotentialScore($agent)
            roi_estimate = $this._EstimateROI($agent)
        }
    }

    [string] _GetStrengthReason([string]$dimension, [int]$score) {
        <#
        .SYNOPSIS
            获取优势原因说明
        #>

        $reasons = @{
            dao_hang = @(
                "具备深刻的战略洞察力",
                "能够把握行业发展趋势",
                "拥有顶层设计能力"
            )
            fa_xing = @(
                "执行能力强，落地效率高",
                "技术实现能力突出",
                "交付质量稳定可靠"
            )
            li_xing = @(
                "商业模式清晰可行",
                "变现路径明确有效",
                "投资回报率高"
            )
            yu_xing = @(
                "用户体验设计优秀",
                "产品打磨精细",
                "用户满意度高"
            )
            shou_xing = @(
                "安全防护措施完善",
                "风险控制体系健全",
                "合规表现优异"
            )
        }

        $dimensionReasons = $reasons[$dimension]
        return $dimensionReasons[$score % $dimensionReasons.Count]
    }

    [string] _GetImprovementSuggestion([string]$dimension) {
        <#
        .SYNOPSIS
            获取改进建议
        #>

        $suggestions = @{
            dao_hang = @(
                "加强行业研究，提升战略认知",
                "学习优秀案例，拓展视野格局",
                "参与行业交流，获取前沿洞察"
            )
            fa_xing = @(
                "优化执行流程，提高效率",
                "加强技术储备，提升实现能力",
                "完善项目管理，确保交付质量"
            )
            li_xing = @(
                "探索多元化变现模式",
                "优化成本结构，提升利润率",
                "建立可持续的商业模式"
            )
            yu_xing = @(
                "深入用户调研，理解需求",
                "优化交互设计，提升易用性",
                "加强用户反馈机制"
            )
            shou_xing = @(
                "加强安全体系建设",
                "完善风险管理制度",
                "确保合规要求"
            )
        }

        $dimensionSuggestions = $suggestions[$dimension]
        return $dimensionSuggestions[0] # 返回第一个建议
    }

    [float] _CalculatePotentialScore([hashtable]$agent) {
        <#
        .SYNOPSIS
            计算潜力分数
        #>

        # 基于进化能力、创新能力等因素计算潜力
        $evolution = $agent.evolution
        $capability = $agent.capability
        $collaboration = $agent.collaboration

        $potential = ($evolution * 0.4) + ($capability * 0.3) + ($collaboration * 0.3)
        return [math]::Round($potential, 1)
    }

    [string] _EstimateROI([hashtable]$agent) {
        <#
        .SYNOPSIS
            估算投资回报率
        #>

        $liXing = $agent.li_xing
        $yuXing = $agent.yu_xing
        $shouXing = $agent.shou_xing

        if ($liXing -ge 80 -and $yuXing -ge 80 -and $shouXing -ge 80) {
            return "高 ROI (3-5年)"
        }
        elseif ($liXing -ge 70 -and $yuXing -ge 70 -and $shouXing -ge 70) {
            return "中等 ROI (5-8年)"
        }
        else {
            return "长期 ROI (8年以上)"
        }
    }

    [hashtable] Evaluate([hashtable]$agent) {
        <#
        .SYNOPSIS
            执行帝意排行评估
        .PARAMETER agent
            Agent 数据
        #>

        Write-Verbose "开始帝意排行评估"

        $businessValue = $this.CalculateBusinessValue($agent)

        $result = @{
            diyi_score = $businessValue.diyi_score
            diyi_level = $businessValue.diyi_level
            level_description = $businessValue.level_description
            dimensions = $businessValue.dimensions
            strengths = $businessValue.strengths
            weaknesses = $businessValue.weaknesses
            potential_score = $businessValue.potential_score
            roi_estimate = $businessValue.roi_estimate
        }

        Write-Verbose "帝意排行评估完成: $($businessValue.diyi_level) ($($businessValue.diyi_score))"

        return $result
    }
}

function Get-DiyiRanking {
    <#
    .SYNOPSIS
        获取帝意排行信息
    .PARAMETER agent
        Agent 数据
    #>

    param(
        [Parameter(Mandatory=$true)]
        [hashtable]$agent
    )

    $engine = [DiyiRankingEngine]::new()
    return $engine.Evaluate($agent)
}

function Show-DiyiRankingDetails {
    <#
    .SYNOPSIS
        显示帝意排行详细信息
    .PARAMETER result
        评估结果
    #>

    param(
        [Parameter(Mandatory=$true)]
        [hashtable]$result
    )

    Write-Host "`n🏆 帝意排行详情" -ForegroundColor Magenta
    Write-Host ("-" * 30) -ForegroundColor Magenta
    Write-Host "帝意等级: $($result.diyi_level)" -ForegroundColor White
    Write-Host "综合得分: $($result.diyi_score)" -ForegroundColor White
    Write-Host "等级说明: $($result.level_description)" -ForegroundColor Gray

    Write-Host "`n维度得分:"
    foreach ($dim in $result.dimensions.PSObject.Properties) {
        $dimInfo = $result.dimensions.$($dim.Name)
        Write-Host "  $($dim.Name): $($dimInfo.score) (权重: $($dimInfo.weight))" -ForegroundColor Gray
    }

    if ($result.strengths.Count -gt 0) {
        Write-Host "`n优势维度:" -ForegroundColor Green
        foreach ($strength in $result.strengths) {
            Write-Host "  ✅ $($strength.dimension): $($strength.score) - $($strength.reason)" -ForegroundColor Green
        }
    }

    if ($result.weaknesses.Count -gt 0) {
        Write-Host "`n改进空间:" -ForegroundColor Yellow
        foreach ($weakness in $result.weaknesses) {
            Write-Host "  ⚠️  $($weakness.dimension): $($weakness.score) - $($weakness.suggestion)" -ForegroundColor Yellow
        }
    }

    Write-Host "`n潜力评估:" -ForegroundColor Cyan
    Write-Host "  潜力分数: $($result.potential_score)" -ForegroundColor White
    Write-Host "  ROI估算: $($result.roi_estimate)" -ForegroundColor White
}

function Compare-DiyiRankings {
    <#
    .SYNOPSIS
        比较多个 Agent 的帝意排行
    .PARAMETER agents
        Agent 列表
    #>

    param(
        [Parameter(Mandatory=$true)]
        [array]$agents
    )

    $engine = [DiyiRankingEngine]::new()
    $comparisons = @()

    foreach ($agent in $agents) {
        $result = $engine.Evaluate($agent)
        $comparisons += @{
            name = $agent.name
            diyi_score = $result.diyi_score
            diyi_level = $result.diyi_level
            dimensions = $result.dimensions
            potential_score = $result.potential_score
        }
    }

    # 按得分排序
    $comparisons = $comparisons | Sort-Object -Property diyi_score -Descending

    return $comparisons
}

Export-ModuleMember -Function @(
    'Get-DiyiRanking',
    'Show-DiyiRankingDetails',
    'Compare-DiyiRankings'
)
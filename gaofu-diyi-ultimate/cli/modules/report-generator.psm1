<#
.SYNOPSIS
    报告生成模块 - PowerShell 版本

.DESCRIPTION
    实现多种格式的评估报告生成

.NOTES
    版本: 6.0.0
    作者: 高府认证团队 & 帝意共识智脑
#>

class ReportGenerator {
    <#
    .SYNOPSIS
        报告生成器
    #>

    ReportGenerator() {
        Write-Verbose "初始化报告生成器"
    }

    [string] GenerateTextReport([hashtable]$evaluationResult) {
        <#
        .SYNOPSIS
            生成文本格式报告
        .PARAMETER evaluationResult
            评估结果
        #>

        $report = @"
高府·帝意 综合评估报告
==============================================================
报告ID: $($evaluationResult.report_id)
Agent ID: $($evaluationResult.agent_id)
Agent 名称: $($evaluationResult.agent_name)
Agent 类型: $($evaluationResult.agent_type)
评估时间: $($evaluationResult.evaluated_at)
评估模式: $($evaluationResult.mode)
版本: $($evaluationResult.version)

🏛️ 高府认证
--------------------------------------------------------------
认证状态: $($evaluationResult.gaofu_certification.status)
认证等级: $($evaluationResult.gaofu_certification.level) $($evaluationResult.gaofu_certification.badge)
综合得分: $($evaluationResult.gaofu_certification.overall_score)

维度得分:
- 能力表现: $($evaluationResult.gaofu_certification.dimensions.capability) (30%)
- 安全保障: $($evaluationResult.gaofu_certification.dimensions.security) (25%)
- 协作能力: $($evaluationResult.gaofu_certification.dimensions.collaboration) (20%)
- 进化潜力: $($evaluationResult.gaofu_certification.dimensions.evolution) (15%)
- 伦理合规: $($evaluationResult.gaofu_certification.dimensions.ethics) (10%)

红线检查:
$($if ($evaluationResult.gaofu_certification.red_line_check.fatal_violations.Count -gt 0) {
    "致命违规:`n" + ($evaluationResult.gaofu_certification.red_line_check.fatal_violations | ForEach-Object { "  ⚠️  $_" }) -join "`n"
} else {
    "无致命违规"
})

$($if ($evaluationResult.gaofu_certification.red_line_check.warnings.Count -gt 0) {
    "警告项目:`n" + ($evaluationResult.gaofu_certification.red_line_check.warnings | ForEach-Object { "  ⚠️  $_" }) -join "`n"
} else {
    "无警告项目"
})

🏆 帝意排行
--------------------------------------------------------------
帝意等级: $($evaluationResult.diyi_ranking.diyi_level)
综合得分: $($evaluationResult.diyi_ranking.diyi_score)

维度得分:
- 道行 (25%): $($evaluationResult.diyi_ranking.dimensions.dao_hang.score)
- 法行 (30%): $($evaluationResult.diyi_ranking.dimensions.fa_xing.score)
- 利行 (15%): $($evaluationResult.diyi_ranking.dimensions.li_xing.score)
- 愈行 (15%): $($evaluationResult.diyi_ranking.dimensions.yu_xing.score)
- 守行 (15%): $($evaluationResult.diyi_ranking.dimensions.shou_xing.score)

🔐 RAC 信任分析
--------------------------------------------------------------
信任得分: $($evaluationResult.rac_analysis.trust_score)
信任因子: $($evaluationResult.rac_analysis.trust_factor)
风险等级: $($evaluationResult.rac_analysis.risk_level)
风险折扣: $($evaluationResult.rac_analysis.risk_discount)
开源项目: $($evaluationResult.rac_analysis.is_open_source)
审计报告: $($evaluationResult.rac_analysis.has_audit_report)

💎 综合价值
--------------------------------------------------------------
综合得分: $($evaluationResult.comprehensive_value.score)
计算公式: $($evaluationResult.comprehensive_value.calculation)

💼 投资建议
--------------------------------------------------------------
战略定位: $($evaluationResult.investment_advice.strategic_position)
定位说明: $($evaluationResult.investment_advice.positioning_description)
建议仓位: $($evaluationResult.investment_advice.recommended_position)
持有周期: $($evaluationResult.investment_advice.holding_period)
风险对冲: $($evaluationResult.investment_advice.risk_hedge)
入场时机: $($evaluationResult.investment_advice.entry_timing)

---
本报告由高府·帝意综合评估系统 v6.0 生成
© 2026 高府认证团队 & 帝意共识智脑
"@

        return $report
    }

    [string] GenerateJSONReport([hashtable]$evaluationResult) {
        <#
        .SYNOPSIS
            生成 JSON 格式报告
        .PARAMETER evaluationResult
            评估结果
        #>

        return $evaluationResult | ConvertTo-Json -Depth 10 -Compress:$false
    }

    [string] GenerateHTMLReport([hashtable]$evaluationResult) {
        <#
        .SYNOPSIS
            生成 HTML 格式报告
        .PARAMETER evaluationResult
            评估结果
        #>

        # 确定颜色
        $gaofuColor = if ($evaluationResult.gaofu_certification.level -eq "传奇") { "#FFD700" } elseif ($evaluationResult.gaofu_certification.level -eq "钻石") { "#00CED1" } elseif ($evaluationResult.gaofu_certification.level -eq "铂金") { "#E6E6FA" } elseif ($evaluationResult.gaofu_certification.level -eq "黄金") { "#FFD700" } else { "#808080" }

        $diyiLevelColor = if ($evaluationResult.diyi_ranking.diyi_level -eq "S级帝意") { "#FF6B6B" } elseif ($evaluationResult.diyi_ranking.diyi_level -eq "A级天枢") { "#4ECDC4" } elseif ($evaluationResult.diyi_ranking.diyi_level -eq "B级地衡") { "#45B7D1" } elseif ($evaluationResult.diyi_ranking.diyi_level -eq "C级人合") { "#96CEB4" } else { "#DDA0DD" }

        $riskColor = if ($evaluationResult.rac_analysis.risk_level -eq "LOW") { "#2ECC71" } elseif ($evaluationResult.rac_analysis.risk_level -eq "MEDIUM") { "#F39C12" } else { "#E74C3C" }

        $html = @"
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>高府·帝意 综合评估报告</title>
    <style>
        body {
            font-family: 'Microsoft YaHei', Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        .header h1 {
            margin: 0;
            font-size: 2.5em;
            font-weight: 300;
        }
        .header .subtitle {
            margin-top: 10px;
            font-size: 1.2em;
            opacity: 0.9;
        }
        .metadata {
            background-color: #f8f9fa;
            padding: 20px;
            border-bottom: 1px solid #e9ecef;
        }
        .metadata-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
        }
        .metadata-item {
            background-color: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .metadata-item label {
            font-weight: bold;
            color: #667eea;
            display: block;
            margin-bottom: 5px;
        }
        .content {
            padding: 30px;
        }
        .section {
            margin-bottom: 40px;
        }
        .section-title {
            font-size: 1.8em;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
            display: inline-block;
        }
        .card {
            background-color: #f8f9fa;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .score-display {
            font-size: 3em;
            font-weight: bold;
            text-align: center;
            margin: 20px 0;
        }
        .gaofu-score { color: $gaofuColor; }
        .diyi-score { color: $diyiLevelColor; }
        .trust-score { color: #3498db; }
        .risk-level { color: $riskColor; }
        .comprehensive-score { color: #9b59b6; }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
        }
        .dimension-item {
            background-color: white;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .dimension-name {
            font-weight: bold;
            margin-bottom: 10px;
        }
        .dimension-score {
            font-size: 2em;
            font-weight: bold;
        }
        .dimension-weight {
            font-size: 0.9em;
            color: #666;
        }
        .advice-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        .advice-table th, .advice-table td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        .advice-table th {
            background-color: #667eea;
            color: white;
        }
        .footer {
            background-color: #2c3e50;
            color: white;
            text-align: center;
            padding: 20px;
            margin-top: 40px;
        }
        .badge {
            display: inline-block;
            padding: 5px 10px;
            border-radius: 20px;
            font-weight: bold;
            margin-left: 10px;
        }
        .badge-legend { background-color: #FFD700; color: #333; }
        .badge-diamond { background-color: #00CED1; color: white; }
        .badge-platinum { background-color: #E6E6FA; color: #333; }
        .badge-gold { background-color: #FFD700; color: #333; }
        .badge-provisional { background-color: #FFA500; color: white; }
        .badge-rejected { background-color: #FF0000; color: white; }
        .badge-s { background-color: #FF6B6B; color: white; }
        .badge-a { background-color: #4ECDC4; color: white; }
        .badge-b { background-color: #45B7D1; color: white; }
        .badge-c { background-color: #96CEB4; color: white; }
        .badge-d { background-color: #DDA0DD; color: white; }
        .badge-low { background-color: #2ECC71; color: white; }
        .badge-medium { background-color: #F39C12; color: white; }
        .badge-high { background-color: #E74C3C; color: white; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>高府·帝意 综合评估报告</h1>
            <div class="subtitle">三位一体 AI Agent 可信评估系统 v6.0</div>
        </div>

        <div class="metadata">
            <div class="metadata-grid">
                <div class="metadata-item">
                    <label>报告ID</label>
                    <span>$($evaluationResult.report_id)</span>
                </div>
                <div class="metadata-item">
                    <label>Agent ID</label>
                    <span>$($evaluationResult.agent_id)</span>
                </div>
                <div class="metadata-item">
                    <label>Agent 名称</label>
                    <span>$($evaluationResult.agent_name)</span>
                </div>
                <div class="metadata-item">
                    <label>Agent 类型</label>
                    <span>$($evaluationResult.agent_type)</span>
                </div>
                <div class="metadata-item">
                    <label>评估时间</label>
                    <span>$($evaluationResult.evaluated_at)</span>
                </div>
                <div class="metadata-item">
                    <label>评估模式</label>
                    <span>$($evaluationResult.mode)</span>
                </div>
            </div>
        </div>

        <div class="content">
            <!-- 高府认证 -->
            <div class="section">
                <h2 class="section-title">🏛️ 高府认证</h2>
                <div class="card">
                    <div style="text-align: center;">
                        <span style="font-size: 1.5em; font-weight: bold;">
                            认证等级:
                            <span style="color: $gaofuColor">
                                $($evaluationResult.gaofu_certification.level)
                            </span>
                            <span class="badge badge-$(switch ($evaluationResult.gaofu_certification.level) {
                                "传奇" { "legend" }
                                "钻石" { "diamond" }
                                "铂金" { "platinum" }
                                "黄金" { "gold" }
                                "临时" { "provisional" }
                                default { "rejected" }
                            })">
                                $($evaluationResult.gaofu_certification.badge)
                            </span>
                        </span>
                    </div>
                    <div class="score-display gaofu-score">
                        $($evaluationResult.gaofu_certification.overall_score)
                    </div>
                    <p style="text-align: center; color: #666;">综合得分</p>
                </div>

                <div class="grid">
                    <div class="dimension-item">
                        <div class="dimension-name">能力表现</div>
                        <div class="dimension-score">$($evaluationResult.gaofu_certification.dimensions.capability)</div>
                        <div class="dimension-weight">(30%)</div>
                    </div>
                    <div class="dimension-item">
                        <div class="dimension-name">安全保障</div>
                        <div class="dimension-score">$($evaluationResult.gaofu_certification.dimensions.security)</div>
                        <div class="dimension-weight">(25%)</div>
                    </div>
                    <div class="dimension-item">
                        <div class="dimension-name">协作能力</div>
                        <div class="dimension-score">$($evaluationResult.gaofu_certification.dimensions.collaboration)</div>
                        <div class="dimension-weight">(20%)</div>
                    </div>
                    <div class="dimension-item">
                        <div class="dimension-name">进化潜力</div>
                        <div class="dimension-score">$($evaluationResult.gaofu_certification.dimensions.evolution)</div>
                        <div class="dimension-weight">(15%)</div>
                    </div>
                    <div class="dimension-item">
                        <div class="dimension-name">伦理合规</div>
                        <div class="dimension-score">$($evaluationResult.gaofu_certification.dimensions.ethics)</div>
                        <div class="dimension-weight">(10%)</div>
                    </div>
                </div>

                <div class="card">
                    <h4>红线检查</h4>
                    <div style="margin-top: 15px;">
                        <div>
                            <strong style="color: #e74c3c;">致命违规:</strong>
                            <div style="margin-left: 20px; margin-top: 5px;">
                                $($if ($evaluationResult.gaofu_certification.red_line_check.fatal_violations.Count -gt 0) {
                                    $evaluationResult.gaofu_certification.red_line_check.fatal_violations | ForEach-Object { "<div>⚠️  $_</div>" } -join ""
                                } else {
                                    "<div style='color: #2ecc71;'>无致命违规</div>"
                                })
                            </div>
                        </div>
                        <div style="margin-top: 15px;">
                            <strong style="color: #f39c12;">警告项目:</strong>
                            <div style="margin-left: 20px; margin-top: 5px;">
                                $($if ($evaluationResult.gaofu_certification.red_line_check.warnings.Count -gt 0) {
                                    $evaluationResult.gaofu_certification.red_line_check.warnings | ForEach-Object { "<div>⚠️  $_</div>" } -join ""
                                } else {
                                    "<div style='color: #2ecc71;'>无警告项目</div>"
                                })
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 帝意排行 -->
            <div class="section">
                <h2 class="section-title">🏆 帝意排行</h2>
                <div class="card">
                    <div style="text-align: center;">
                        <span style="font-size: 1.5em; font-weight: bold; color: $diyiLevelColor;">
                            $($evaluationResult.diyi_ranking.diyi_level)
                        </span>
                    </div>
                    <div class="score-display diyi-score">
                        $($evaluationResult.diyi_ranking.diyi_score)
                    </div>
                    <p style="text-align: center; color: #666;">综合得分</p>
                </div>

                <div class="grid">
                    <div class="dimension-item">
                        <div class="dimension-name">道行</div>
                        <div class="dimension-score">$($evaluationResult.diyi_ranking.dimensions.dao_hang.score)</div>
                        <div class="dimension-weight">(25%)</div>
                    </div>
                    <div class="dimension-item">
                        <div class="dimension-name">法行</div>
                        <div class="dimension-score">$($evaluationResult.diyi_ranking.dimensions.fa_xing.score)</div>
                        <div class="dimension-weight">(30%)</div>
                    </div>
                    <div class="dimension-item">
                        <div class="dimension-name">利行</div>
                        <div class="dimension-score">$($evaluationResult.diyi_ranking.dimensions.li_xing.score)</div>
                        <div class="dimension-weight">(15%)</div>
                    </div>
                    <div class="dimension-item">
                        <div class="dimension-name">愈行</div>
                        <div class="dimension-score">$($evaluationResult.diyi_ranking.dimensions.yu_xing.score)</div>
                        <div class="dimension-weight">(15%)</div>
                    </div>
                    <div class="dimension-item">
                        <div class="dimension-name">守行</div>
                        <div class="dimension-score">$($evaluationResult.diyi_ranking.dimensions.shou_xing.score)</div>
                        <div class="dimension-weight">(15%)</div>
                    </div>
                </div>
            </div>

            <!-- RAC 信任分析 -->
            <div class="section">
                <h2 class="section-title">🔐 RAC 信任分析</h2>
                <div class="grid">
                    <div class="dimension-item">
                        <div class="dimension-name">信任得分</div>
                        <div class="dimension-score trust-score">$($evaluationResult.rac_analysis.trust_score)</div>
                    </div>
                    <div class="dimension-item">
                        <div class="dimension-name">信任因子</div>
                        <div class="dimension-score">$($evaluationResult.rac_analysis.trust_factor)</div>
                    </div>
                    <div class="dimension-item">
                        <div class="dimension-name">风险等级</div>
                        <div class="dimension-score risk-level">$($evaluationResult.rac_analysis.risk_level)</div>
                    </div>
                    <div class="dimension-item">
                        <div class="dimension-name">风险折扣</div>
                        <div class="dimension-score">$($evaluationResult.rac_analysis.risk_discount)</div>
                    </div>
                </div>

                <div class="card">
                    <h4>信任详情</h4>
                    <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; margin-top: 15px;">
                        <div>
                            <strong>开源项目:</strong>
                            <span style="color: $(if ($evaluationResult.rac_analysis.is_open_source) { "#2ecc71" } else { "#e74c3c" })">
                                $($evaluationResult.rac_analysis.is_open_source ? "是" : "否")
                            </span>
                        </div>
                        <div>
                            <strong>审计报告:</strong>
                            <span style="color: $(if ($evaluationResult.rac_analysis.has_audit_report) { "#2ecc71" } else { "#e74c3c" })">
                                $($evaluationResult.rac_analysis.has_audit_report ? "是" : "否")
                            </span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 综合价值 -->
            <div class="section">
                <h2 class="section-title">💎 综合价值</h2>
                <div class="card">
                    <div class="score-display comprehensive-score">
                        $($evaluationResult.comprehensive_value.score)
                    </div>
                    <p style="text-align: center; color: #666;">综合得分</p>
                    <div style="text-align: center; margin-top: 20px;">
                        <strong>计算公式:</strong>
                        <br>
                        $($evaluationResult.comprehensive_value.calculation)
                    </div>
                </div>
            </div>

            <!-- 投资建议 -->
            <div class="section">
                <h2 class="section-title">💼 投资建议</h2>
                <table class="advice-table">
                    <tr>
                        <th>项目</th>
                        <th>详情</th>
                    </tr>
                    <tr>
                        <td>战略定位</td>
                        <td>$($evaluationResult.investment_advice.strategic_position)</td>
                    </tr>
                    <tr>
                        <td>定位说明</td>
                        <td>$($evaluationResult.investment_advice.positioning_description)</td>
                    </tr>
                    <tr>
                        <td>建议仓位</td>
                        <td>$($evaluationResult.investment_advice.recommended_position)</td>
                    </tr>
                    <tr>
                        <td>持有周期</td>
                        <td>$($evaluationResult.investment_advice.holding_period)</td>
                    </tr>
                    <tr>
                        <td>风险对冲</td>
                        <td>$($evaluationResult.investment_advice.risk_hedge)</td>
                    </tr>
                    <tr>
                        <td>入场时机</td>
                        <td>$($evaluationResult.investment_advice.entry_timing)</td>
                    </tr>
                </table>
            </div>
        </div>

        <div class="footer">
            <p>本报告由高府·帝意综合评估系统 v6.0 生成</p>
            <p>© 2026 高府认证团队 & 帝意共识智脑</p>
            <p style="margin-top: 10px; font-size: 0.9em; opacity: 0.8;">
                免责声明：本报告输出基于算法模型和输入数据生成，不构成投资建议。
            </p>
        </div>
    </div>
</body>
</html>
"@

        return $html
    }

    [void] SaveReport([string]$report, [string]$filePath, [string]$format) {
        <#
        .SYNOPSIS
            保存报告到文件
        .PARAMETER report
            报告内容
        .PARAMETER filePath
            文件路径
        .PARAMETER format
            格式类型
        #>

        try {
            $directory = Split-Path -Parent $filePath
            if (-not (Test-Path $directory)) {
                New-Item -ItemType Directory -Path $directory -Force | Out-Null
            }

            switch ($format.ToLower()) {
                "html" {
                    $report | Out-File -FilePath $filePath -Encoding UTF8
                    Write-Host "HTML 报告已保存到: $filePath" -ForegroundColor Green
                }
                "json" {
                    $report | Out-File -FilePath $filePath -Encoding UTF8
                    Write-Host "JSON 报告已保存到: $filePath" -ForegroundColor Green
                }
                "text" {
                    $report | Out-File -FilePath $filePath -Encoding UTF8
                    Write-Host "文本报告已保存到: $filePath" -ForegroundColor Green
                }
                default {
                    throw "不支持的格式: $format"
                }
            }
        }
        catch {
            throw "保存报告失败: $($_.Exception.Message)"
        }
    }
}

# 导出函数
function New-GaofuDiyiReport {
    <#
    .SYNOPSIS
        创建高府·帝意综合评估报告
    .PARAMETER evaluationResult
        评估结果
    .PARAMETER format
        报告格式: text|json|html
    #>

    param(
        [Parameter(Mandatory=$true)]
        [hashtable]$evaluationResult,

        [ValidateSet("text", "json", "html")]
        [string]$format = "text"
    )

    $generator = [ReportGenerator]::new()

    switch ($format.ToLower()) {
        "text" { return $generator.GenerateTextReport($evaluationResult) }
        "json" { return $generator.GenerateJSONReport($evaluationResult) }
        "html" { return $generator.GenerateHTMLReport($evaluationResult) }
    }
}

function Save-GaofuDiyiReport {
    <#
    .SYNOPSIS
        保存高府·帝意综合评估报告
    .PARAMETER evaluationResult
        评估结果
    .PARAMETER filePath
        保存路径
    .PARAMETER format
        报告格式
    #>

    param(
        [Parameter(Mandatory=$true)]
        [hashtable]$evaluationResult,

        [Parameter(Mandatory=$true)]
        [string]$filePath,

        [ValidateSet("text", "json", "html")]
        [string]$format = "text"
    )

    $generator = [ReportGenerator]::new()
    $report = New-GaofuDiyiReport -evaluationResult $evaluationResult -format $format
    $generator.SaveReport($report, $filePath, $format)
}

function Show-ReportPreview {
    <#
    .SYNOPSIS
        显示报告预览
    .PARAMETER evaluationResult
        评估结果
    #>

    param(
        [Parameter(Mandatory=$true)]
        [hashtable]$evaluationResult
    )

    # 生成文本报告并显示
    $generator = [ReportGenerator]::new()
    $report = $generator.GenerateTextReport($evaluationResult)
    $report | Write-Host
}

Export-ModuleMember -Function @(
    'New-GaofuDiyiReport',
    'Save-GaofuDiyiReport',
    'Show-ReportPreview'
)
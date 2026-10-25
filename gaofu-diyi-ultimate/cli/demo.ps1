# High Fu Di Yi CLI Demo
Write-Host "High Fu Di Yi CLI Tool v6.0"
Write-Host "========================"

# Simple demo
$agent = @{
    id = "demo-agent"
    name = "Demo Agent"
    capability = 85
    security = 80
    collaboration = 75
    evolution = 82
    ethics = 78
}

# Calculate scores
$gaofu = ($agent.capability * 0.3) + ($agent.security * 0.25) + ($agent.collaboration * 0.2) + ($agent.evolution * 0.15) + ($agent.ethics * 0.1)
$diyi = ($agent.capability * 0.25) + ($agent.security * 0.3) + ($agent.collaboration * 0.15) + ($agent.evolution * 0.15) + ($agent.ethics * 0.15)

Write-Host ""
Write-Host "Evaluation Results:"
Write-Host "-----------------"
Write-Host "Agent ID: $($agent.id)"
Write-Host "Agent Name: $($agent.name)"
Write-Host ""
Write-Host "Gaofu Score: $([math]::Round($gaofu, 1))"
Write-Host "Diyi Score: $([math]::Round($diyi, 1))"

# Determine levels
if ($gaofu -ge 85) { $level = "Diamond" } elseif ($gaofu -ge 75) { $level = "Platinum" } else { $level = "Gold" }
Write-Host "Gaofu Level: $level"

if ($diyi -ge 85) { $diyiLevel = "A Rank" } elseif ($diyi -ge 75) { $diyiLevel = "B Rank" } else { $diyiLevel = "C Rank" }
Write-Host "Diyi Level: $diyiLevel"

Write-Host ""
Write-Host "For more commands, run:"
Write-Host "  help - Show help"
Write-Host "  evaluate - Evaluate an agent"
Write-Host "  rank - Show ranking"
Write-Host "  report - Generate report"
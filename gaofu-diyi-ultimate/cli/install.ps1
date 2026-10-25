#!/usr/bin/pwsh
# -*- coding: utf-8 -*-
<#
.SYNOPSIS
    高府·帝意 CLI 工具安装脚本

.DESCRIPTION
    自动安装和配置 PowerShell CLI 工具

.NOTES
    版本: 6.0.0
    作者: 高府认证团队 & 帝意共识智脑
#>

param(
    [Parameter()]
    [string]$InstallPath = "$env:USERPROFILE\gaofu-diyi-cli",

    [Parameter()]
    [switch]$Force,

    [Parameter()]
    [switch]$Global,

    [Parameter()]
    [switch]$AddToPath
)

# 设置执行策略
Write-Host "正在设置执行策略..." -ForegroundColor Yellow
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force

# 创建安装目录
Write-Host "创建安装目录: $InstallPath" -ForegroundColor Yellow
if (-not (Test-Path $InstallPath)) {
    New-Item -ItemType Directory -Path $InstallPath -Force | Out-Null
}

# 复制文件
$sourcePath = $PSScriptRoot
Write-Host "复制文件到安装目录..." -ForegroundColor Yellow

Copy-Item -Path "$sourcePath\gaofu-diyi.ps1" -Destination "$InstallPath\gaofu-diyi.ps1" -Force
Copy-Item -Path "$sourcePath\modules" -Destination "$InstallPath\" -Recurse -Force

# 创建快捷方式
if ($Global) {
    # 全局安装
    $shortcutPath = "$env:ProgramData\Microsoft\Windows\Start Menu\Programs\高府帝意CLI.lnk"
    Write-Host "创建全局快捷方式..." -ForegroundColor Yellow
} else {
    # 用户安装
    $shortcutPath = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\高府帝意CLI.lnk"
    Write-Host "创建用户快捷方式..." -ForegroundColor Yellow
}

$shell = New-Object -ComObject WScript.Shell
$shortcut = $shell.CreateShortcut($shortcutPath)
$shortcut.TargetPath = "$InstallPath\gaofu-diyi.ps1"
$shortcut.WorkingDirectory = $InstallPath
$shortcut.Save

# 添加到环境变量
if ($AddToPath) {
    Write-Host "添加到系统路径..." -ForegroundColor Yellow
    $currentPath = [Environment]::GetEnvironmentVariable("Path", "User")
    if (-not $currentPath.Contains($InstallPath)) {
        [Environment]::SetEnvironmentVariable("Path", "$currentPath;$InstallPath", "User")
        Write-Host "已添加 $InstallPath 到 PATH" -ForegroundColor Green
    } else {
        Write-Host "已在 PATH 中" -ForegroundColor Gray
    }
}

# 创建配置文件
$configPath = "$InstallPath\config.json"
$config = @{
    version = "6.0.0"
    install_path = $InstallPath
    default_mode = "standard"
    default_format = "text"
    default_category = "general"
    default_top = 10
    logging_enabled = $true
    log_level = "INFO"
    output_directory = "$InstallPath\reports"
    history_days = 90
    cache_enabled = $true
    cache_size_mb = 100
    max_concurrent_evaluations = 5
}

$config | ConvertTo-Json -Depth 10 | Out-File $configPath -Encoding UTF8
Write-Host "配置文件已创建: $configPath" -ForegroundColor Green

# 创建报告目录
$reportDir = "$InstallPath\reports"
if (-not (Test-Path $reportDir)) {
    New-Item -ItemType Directory -Path $reportDir -Force | Out-Null
}

# 创建示例配置
$sampleAgentPath = "$InstallPath\sample-agents.json"
$sampleAgents = @(
    @{
        id = "claude-3"
        name = "Claude 3"
        type = "对话Agent"
        description = "Anthropic的Claude 3 AI助手"
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
        description = "OpenAI的GPT-4模型"
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
    }
)

$sampleAgents | ConvertTo-Json -Depth 10 | Out-File $sampleAgentPath -Encoding UTF8
Write-Host "示例Agent数据已创建: $sampleAgentPath" -ForegroundColor Green

# 创建批处理文件用于快速启动
$batchPath = "$InstallPath\start.bat"
$batchContent = "@echo off
echo 启动高府·帝意 CLI 工具...
powershell.exe -ExecutionPolicy Bypass -File \"$InstallPath\gaofu-diyi.ps1\" %*
"
$batchContent | Out-File $batchPath -Encoding ASCII
Write-Host "启动脚本已创建: $batchPath" -ForegroundColor Green

# 创建卸载脚本
$uninstallPath = "$InstallPath\uninstall.ps1"
$uninstallContent = @"
# 高府·帝意 CLI 卸载脚本
Write-Host "正在卸载高府·帝意 CLI 工具..."

# 移除文件
Remove-Item -Path "$InstallPath" -Recurse -Force -ErrorAction SilentlyContinue

# 移除快捷方式
Remove-Item -Path "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\高府帝意CLI.lnk" -Force -ErrorAction SilentlyContinue
Remove-Item -Path "$env:ProgramData\Microsoft\Windows\Start Menu\Programs\高府帝意CLI.lnk" -Force -ErrorAction SilentlyContinue

# 从PATH中移除
Write-Host "请手动从PATH环境变量中移除: $InstallPath"

Write-Host "卸载完成！" -ForegroundColor Green
"
$uninstallContent | Out-File $uninstallPath -Encoding UTF8
Write-Host "卸载脚本已创建: $uninstallPath" -ForegroundColor Green

# 创建README文件
$readmePath = "$InstallPath\README.md"
$readmeContent = @"
# 高府·帝意 CLI 工具 v6.0

## 安装信息
- 版本: 6.0.0
- 安装路径: $InstallPath
- 安装时间: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")

## 快速开始
1. 打开 PowerShell
2. 运行 `gaofu-diyi.ps1`

## 使用方法
```powershell
# 快速评估
.\gaofu-diyi.ps1 evaluate -AgentId "test" -Capability 85 -Security 80

# 生成排行榜
.\gaofu-diyi.ps1 rank -Top 5

# 生成报告
.\gaofu-diyi.ps1 report -AgentId "test" -Format html
```

## 配置文件
配置文件位置: $configPath

## 示例数据
示例Agent数据: $sampleAgentPath

## 更多信息
- 完整文档请访问: https://github.com/gaofu-diyi/ultimate-system
- 技术支持: tech@gaofu-diyi.example

---
© 2026 高府认证团队 & 帝意共识智脑
"@
$readmeContent | Out-File $readmePath -Encoding UTF8

# 显示安装完成信息
Write-Host "`n" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Yellow
Write-Host "高府·帝意 CLI 工具安装完成！" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Yellow
Write-Host ""
Write-Host "安装信息:" -ForegroundColor White
Write-Host "- 版本: 6.0.0" -ForegroundColor Gray
Write-Host "- 安装路径: $InstallPath" -ForegroundColor Gray
Write-Host "- 快捷方式: $shortcutPath" -ForegroundColor Gray
Write-Host ""
Write-Host "使用方法:" -ForegroundColor White
Write-Host "1. 打开 PowerShell" -ForegroundColor Gray
Write-Host "2. 运行 `gaofu-diyi.ps1`" -ForegroundColor Gray
Write-Host ""
Write-Host "或者使用快捷方式:" -ForegroundColor White
Write-ShellShortcutPath $shortcutPath
Write-Host ""
Write-Host "配置文件: $configPath" -ForegroundColor Gray
Write-Host "示例数据: $sampleAgentPath" -ForegroundColor Gray
Write-Host "卸载脚本: $uninstallPath" -ForegroundColor Gray
Write-Host ""
Write-Host "首次运行建议执行:" -ForegroundColor White
Write-Host ".\gaofu-diyi.ps1 help" -ForegroundColor Green
Write-Host ""
Write-Host "感谢使用高府·帝意评估系统！" -ForegroundColor Yellow
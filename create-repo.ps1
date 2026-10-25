# PowerShell脚本：创建GitHub仓库并上传项目

Write-Host "🚀 开始创建GitHub仓库并上传项目" -ForegroundColor Green
Write-Host "=".PadRight(50, "=") -ForegroundColor Green

# 设置变量
$repoName = "tongshen-auth-agent"
$repoDescription = "通神认证Agent - 融合78个技能，支持自优化的AI Agent系统"
$localPath = Get-Location
$token = "ghp_YOUR_TOKEN_PLACEHOLDER"

# 检查环境
Write-Host "`n🔍 检查环境..." -ForegroundColor Yellow

# 检查git
try {
    $gitVersion = git --version
    Write-Host "✅ Git版本: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Git未安装，请先安装Git" -ForegroundColor Red
    exit 1
}

# 检查Node.js
$nodeVersion = node --version
Write-Host "✅ Node.js版本: $nodeVersion" -ForegroundColor Green

# 检查必要文件
$requiredFiles = @(
    "auth-agent-core.js",
    "core-scheduler.js",
    "server.js",
    "deploy-to-claude.js",
    "README.md",
    "SKILL.md"
)

foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "✅ 找到文件: $file" -ForegroundColor Green
    } else {
        Write-Host "❌ 缺少必要文件: $file" -ForegroundColor Red
        exit 1
    }
}

# 初始化Git仓库
Write-Host "`n📦 初始化Git仓库..." -ForegroundColor Yellow

try {
    git status | Out-Null
    Write-Host "✅ 已是Git仓库，跳过初始化" -ForegroundColor Green
} catch {
    # 初始化git仓库
    git init
    git config user.name "通神认证Agent"
    git config user.email "tongshen@agent.com"
    Write-Host "✅ Git仓库初始化完成" -ForegroundColor Green
}

# 添加远程仓库
$remoteUrl = "https://github.com/your-username/$repoName.git"
Write-Host "`n🌐 添加远程仓库..." -ForegroundColor Yellow

try {
    git remote add origin $remoteUrl
    Write-Host "✅ 远程仓库已添加" -ForegroundColor Green
} catch {
    Write-Host "⚠️ 远程仓库已存在，跳过添加" -ForegroundColor Yellow
}

# 添加文件并提交
Write-Host "`n📝 添加文件并提交..." -ForegroundColor Yellow

git add .
$commitMessage = "feat: 初始提交 - 通神认证Agent完整项目"
git commit -m $commitMessage
Write-Host "✅ 文件提交完成" -ForegroundColor Green

# 推送到GitHub
Write-Host "`n🚀 推送到GitHub..." -ForegroundColor Yellow

try {
    git push -u origin main
    Write-Host "✅ 代码推送完成" -ForegroundColor Green
} catch {
    Write-Host "❌ 推送失败，请检查GitHub设置" -ForegroundColor Red
    Write-Host "可能需要先在GitHub上创建仓库" -ForegroundColor Yellow
    exit 1
}

# 完成提示
Write-Host "`n" -ForegroundColor Green
Write-Host "✅ 仓库创建并上传成功！" -ForegroundColor Green
Write-Host "🔗 仓库地址:" -ForegroundColor Green
Write-Host "https://github.com/your-username/$repoName" -ForegroundColor Cyan
Write-Host "https://github.com/your-username/$repoName/tree/main" -ForegroundColor Cyan

Write-Host "`n📝 下一步:" -ForegroundColor Yellow
Write-Host "1. 访问 https://github.com/your-username/$repoName 查看仓库"
Write-Host "2. 编辑仓库描述、添加标签等"
Write-Host "3. 配置GitHub Pages网站（可选）"
Write-Host "4. 设置Actions CI/CD（可选）"
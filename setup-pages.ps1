# PowerShell脚本：配置GitHub Pages

Write-Host "🌐 配置GitHub Pages" -ForegroundColor Green
Write-Host "=".PadRight(50, "=") -ForegroundColor Green

# 设置变量
$repoName = "tongshen-auth-agent"
$ghPagesBranch = "gh-pages"

Write-Host "`n📝 这将帮您配置GitHub Pages：" -ForegroundColor Yellow
Write-Host "1. 创建gh-pages分支" -ForegroundColor White
Write-Host "2. 创建简单的index.html文件" -ForegroundColor White
Write-Host "3. 推送到GitHub Pages分支" -ForegroundColor White
Write-Host "4. 启用GitHub Pages服务" -ForegroundColor White
Write-Host ""

$continue = Read-Host "是否继续？(y/N)"
if ($continue -ne "y" -and $continue -ne "Y") {
    Write-Host "已取消" -ForegroundColor Yellow
    exit 0
}

# 检查是否在Git仓库
try {
    git status | Out-Null
} catch {
    Write-Host "❌ 当前目录不是Git仓库" -ForegroundColor Red
    exit 1
}

# 创建gh-pages分支
Write-Host "`n📁 创建gh-pages分支..." -ForegroundColor Yellow

# 检查gh-pages分支是否存在
$branchExists = git branch -a | Where-Object { $_ -like "*gh-pages*" }
if ($branchExists) {
    Write-Host "✅ gh-pages分支已存在，切换到该分支" -ForegroundColor Green
    git checkout gh-pages
} else {
    Write-Host "✅ 创建新的gh-pages分支" -ForegroundColor Green
    git checkout --orphan gh-pages
    git rm -rf . > $null 2>&1
}

# 创建简单的index.html
Write-Host "`n📄 创建index.html..." -ForegroundColor Yellow

$htmlContent = @"
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>通神认证Agent</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 40px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }
        h1 {
            font-size: 3em;
            text-align: center;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }
        .subtitle {
            text-align: center;
            font-size: 1.2em;
            margin-bottom: 40px;
            opacity: 0.9;
        }
        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 40px;
        }
        .feature {
            background: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            transition: transform 0.3s ease;
        }
        .feature:hover {
            transform: translateY(-5px);
        }
        .feature h3 {
            margin-top: 0;
            color: #ffd700;
        }
        .links {
            text-align: center;
            margin-top: 40px;
        }
        .links a {
            color: #ffd700;
            text-decoration: none;
            margin: 0 15px;
            font-weight: bold;
        }
        .links a:hover {
            text-decoration: underline;
        }
        .status {
            text-align: center;
            margin-top: 40px;
            padding: 20px;
            background: rgba(0, 255, 0, 0.1);
            border-radius: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 通神认证Agent</h1>
        <p class="subtitle">融合78个技能，支持自优化的AI Agent系统</p>

        <div class="features">
            <div class="feature">
                <h3>🧠 M0元认知</h3>
                <p>自我反思、策略规划、任务分解</p>
            </div>
            <div class="feature">
                <h3>🎯 7域路由</h3>
                <p>自动识别并路由到最适合的技能</p>
            </div>
            <div class="feature">
                <h3>🔄 自优化进化</h3>
                <p>持续学习和改进系统性能</p>
            </div>
            <div class="feature">
                <h3>🔗 78个技能</h3>
                <p>涵盖交易、内容、研究、开发等多个领域</p>
            </div>
        </div>

        <div class="links">
            <a href="https://github.com/your-username/tongshen-auth-agent" target="_blank">📦 GitHub仓库</a>
            <a href="https://github.com/your-username/tongshen-auth-agent#readme" target="_blank">📖 使用文档</a>
            <a href="https://github.com/your-username/tongshen-auth-agent/issues" target="_blank">🐛 问题反馈</a>
        </div>

        <div class="status">
            <h3>📊 系统状态</h3>
            <p id="status">正在检查...</p>
        </div>
    </div>

    <script>
        // 检查API状态
        async function checkStatus() {
            try {
                const response = await fetch('https://tongshen-auth-agent.vercel.app/status');
                const data = await response.json();
                document.getElementById('status').innerHTML = `
                    ✅ 服务正常<br>
                    版本: ${data.version}<br>
                    技能数量: ${data.totalSkills}<br>
                    运行时间: ${Math.floor(data.uptime / 3600)}小时
                `;
            } catch (error) {
                document.getElementById('status').innerHTML = `
                    ⚠️ 无法连接到API<br>
                    ${error.message}
                `;
            }
        }

        // 页面加载时检查状态
        checkStatus();
        // 每30秒检查一次
        setInterval(checkStatus, 30000);
    </script>
</body>
</html>
"@

Set-Content -Path "index.html" -Value $htmlContent
Write-Host "✅ index.html创建完成" -ForegroundColor Green

# 创建docs目录（可选）
Write-Host "`n📁 创建docs目录..." -ForegroundColor Yellow
$docsContent = @"
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>通神认证Agent - 文档</title>
    <meta http-equiv="refresh" content="0; url=https://github.com/your-username/tongshen-auth-agent#readme">
</head>
<body>
    <p>正在跳转到文档页面...</p>
</body>
</html>
"@

New-Item -ItemType Directory -Force -Path "docs" | Out-Null
Set-Content -Path "docs/index.html" -Value $docsContent

# 提交并推送到GitHub
Write-Host "`n📤 提交并推送到GitHub..." -ForegroundColor Yellow

git add .
git commit -m "feat: 添加GitHub Pages页面"
git push origin gh-pages

Write-Host "✅ 代码推送完成" -ForegroundColor Green

Write-Host "`n" -ForegroundColor Green
Write-Host "✅ GitHub Pages配置完成！" -ForegroundColor Green
Write-Host "🔗 Pages地址：" -ForegroundColor Green
Write-Host "https://your-username.github.io/tongshen-auth-agent" -ForegroundColor Cyan

Write-Host "`n📝 下一步：" -ForegroundColor Yellow
Write-Host "1. 访问GitHub仓库设置" -ForegroundColor White
Write-Host "2. 找到 Pages 选项" -ForegroundColor White
Write-Host "3. 选择 gh-pages 分支" -ForegroundColor White
Write-Host "4. 点击 Save 保存" -ForegroundColor White
Write-Host "5. 几分钟后网站将生效" -ForegroundColor White

Write-Host "`n⚠️ 重要提示：" -ForegroundColor Yellow
Write-Host "请将脚本中的 'your-username' 替换为您的GitHub用户名" -ForegroundColor White
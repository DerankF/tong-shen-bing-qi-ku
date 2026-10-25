# Test script
Write-Host "Hello from PowerShell CLI!"

# Import module if exists
if (Test-Path "$PSScriptRoot\modules\gaofu-diyi-engine.psm1") {
    Write-Host "Module found!"
    Import-Module "$PSScriptRoot\modules\gaofu-diyi-engine.psm1" -Force

    # Create engine and test
    $engine = [GaofuDiyiEngine]::new()
    Write-Host "Engine created successfully!"
} else {
    Write-Host "Module not found"
}

Write-Host "Test completed"
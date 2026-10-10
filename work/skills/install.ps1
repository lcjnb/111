<#
.SYNOPSIS
    将招投标智能技能安装到 Codex 用户技能目录。

.DESCRIPTION
    复制 bid-orchestrator、tender-analyst、doc-secretary、presales-writer、
    compliance-reviewer、company-profile 六个技能，并复制 shared 与 scripts。

.EXAMPLE
    powershell -ExecutionPolicy Bypass -File .\skills\install.ps1
#>

[CmdletBinding()]
param(
    [string]$Target = "$HOME\.codex\skills"
)

$ErrorActionPreference = 'Stop'
$source = Split-Path -Parent $MyInvocation.MyCommand.Path
$skills = @(
    'bid-orchestrator',
    'tender-analyst',
    'doc-secretary',
    'presales-writer',
    'compliance-reviewer',
    'company-profile'
)

New-Item -ItemType Directory -Force -Path $Target | Out-Null

foreach ($name in $skills) {
    $from = Join-Path $source $name
    if (-not (Test-Path $from)) {
        throw "missing skill directory: $from"
    }
    Copy-Item -Path $from -Destination $Target -Recurse -Force
    Write-Host "installed: $name"
}

foreach ($extra in @('shared', 'scripts')) {
    $from = Join-Path $source $extra
    if (Test-Path $from) {
        Copy-Item -Path $from -Destination $Target -Recurse -Force
        Write-Host "installed: $extra"
    }
}

$pycache = Join-Path $Target 'scripts\__pycache__'
if (Test-Path $pycache) {
    Remove-Item -Path $pycache -Recurse -Force
}

Write-Host ""
Write-Host "done. skills installed to $Target"

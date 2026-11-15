param(
    [Parameter(Mandatory=$true)]
    [ValidateSet('opencode','pi')]
    [string]$Harness,
    [switch]$CreditEligibilityConfirmed
)

$ErrorActionPreference = 'Stop'
$ProjectRoot = Split-Path -Parent $PSScriptRoot
$RunId = if ($Harness -eq 'opencode') { 'opencode-trial-02' } else { 'pi-trial-02' }
$ComparisonDir = Join-Path $ProjectRoot 'analyses\harness-comparison'
$Payload = Join-Path $ComparisonDir 'comparison-input-payload.md'
$Python = (Get-Command py -ErrorAction Stop).Source
$draftOut = Join-Path $ProjectRoot ("results\harness-comparison\{0}-draft.md" -f $RunId)

if (-not $CreditEligibilityConfirmed) {
    throw 'Blocked before starting: verify in Upstage Console that the named credits apply to direct Solar Pro 4 API calls, then rerun with -CreditEligibilityConfirmed.'
}
if ([string]::IsNullOrWhiteSpace($env:UPSTAGE_API_KEY)) {
    throw 'Set UPSTAGE_API_KEY in this process environment using a local secret manager or shell; no key file is read and the key is never printed.'
}
if (-not (Test-Path -LiteralPath $Payload -PathType Leaf)) {
    throw 'The frozen comparison payload is missing. Build it with scripts/build_harness_comparison_payload.py first.'
}
$port = if ($Harness -eq 'opencode') { 18710 } else { 18711 }
$guardLog = Join-Path $ComparisonDir ("guard-{0}.log" -f $RunId)
$guardErrorLog = Join-Path $ComparisonDir ("guard-{0}.stderr.log" -f $RunId)
$harnessLog = Join-Path $ComparisonDir ("harness-{0}.log" -f $RunId)
$stateDir = Join-Path $ComparisonDir 'guard-state-cumulative'
$runOutputRoot = Join-Path $ProjectRoot 'results\harness-comparison\runs'
$server = $null
if (Test-Path -LiteralPath $draftOut) {
    throw "A draft already exists at the fixed output path; refusing overwrite: $draftOut"
}
foreach ($artifactPath in @($guardLog, $guardErrorLog, $harnessLog, (Join-Path $runOutputRoot $RunId))) {
    if (Test-Path -LiteralPath $artifactPath) {
        throw "A fixed run artifact already exists; refusing to overwrite or replay: $artifactPath"
    }
}

try {
    # UPSTAGE_API_KEY must already exist in this process environment; it is not persisted or printed.
    $env:OPENCODE_CONFIG = Join-Path $ComparisonDir 'configs\opencode.solar.local.json'
    $env:PI_CODING_AGENT_DIR = Join-Path $ComparisonDir 'configs\pi-agent-config'
    $env:PI_OFFLINE = '1'
    $env:PI_TELEMETRY = '0'
    $env:PI_SKIP_VERSION_CHECK = '1'
    $env:OPENCODE_PURE = '1'
    $env:OPENCODE_DISABLE_AUTOUPDATE = '1'
    $systemPrompt = (Get-Content -LiteralPath (Join-Path $ComparisonDir 'comparison-system-prompt.txt') -Raw).Trim()
    New-Item -ItemType Directory -Path (Split-Path -Parent $draftOut) -Force | Out-Null
    & $Python -3 (Join-Path $ProjectRoot 'scripts\build_harness_comparison_payload.py') --verify | Out-Null
    if ($LASTEXITCODE -ne 0) { throw 'Frozen comparison payload verification failed.' }
    if (-not (Test-Path -LiteralPath (Join-Path $stateDir 'usage-ledger.json'))) {
        & $Python -3 (Join-Path $ProjectRoot 'scripts\initialize_cumulative_harness_ledger.py') | Out-Null
        if ($LASTEXITCODE -ne 0) { throw 'Cumulative ledger initialization failed; no harness was launched.' }
    }
    $server = Start-Process -FilePath $Python -ArgumentList @(
        '-3', (Join-Path $ProjectRoot 'scripts\harness_request_guard.py'), '--harness', $Harness,
        '--port', [string]$port, '--state-dir', $stateDir, '--output-root', $runOutputRoot,
        '--run-id', $RunId, '--max-total-posts', '4', '--max-per-harness', '2',
        '--cumulative-budget-usd', '1.0', '--allow-live'
    ) -PassThru -WindowStyle Hidden -RedirectStandardOutput $guardLog -RedirectStandardError $guardErrorLog
    $ready = $false
    for ($i = 0; $i -lt 30; $i++) {
        if ($server.HasExited) { throw 'Guard process exited before listening; inspect its redacted log.' }
        try {
            $null = Invoke-WebRequest -Uri ("http://127.0.0.1:{0}/v1/models" -f $port) -TimeoutSec 1
            $ready = $true
            break
        } catch { Start-Sleep -Milliseconds 250 }
    }
    if (-not $ready) { throw 'Local request guard did not become ready; no harness was launched.' }

    if ($Harness -eq 'opencode') {
        $exe = Join-Path $ProjectRoot 'tools\harnesses\opencode\node_modules\.bin\opencode.cmd'
        Push-Location $ProjectRoot
        try { & $exe run --standalone --title 'Benzocaine harness comparison draft' --agent comparison-draft --model 'upstage/solar-pro4-260806' --file $Payload 'Create the Korean comparison draft requested in the attached frozen payload.' *> $harnessLog }
        finally { Pop-Location }
    } else {
        $exe = Join-Path $ProjectRoot 'tools\harnesses\pi\node_modules\.bin\pi.cmd'
        & $exe --no-tools --no-extensions --no-mcp --no-context-files --no-skills --no-prompt-templates --no-themes --offline --no-session --thinking off --provider upstage --model solar-pro4-260806 --system-prompt $systemPrompt --print (('@' + $Payload)) 'Create the Korean comparison draft requested in the attached frozen payload.' *> $harnessLog
    }
    $exitCode = $LASTEXITCODE
    # Preserve stdout as a raw artifact; it is not a final report.
    if ($exitCode -eq 0) {
        Copy-Item -LiteralPath $harnessLog -Destination $draftOut -ErrorAction Stop
        Write-Output ("Harness completed once: {0}. Draft: {1}" -f $Harness, $draftOut)
    } else {
        Write-Output ("Harness failed with exit code {0}; no retry was made. See redacted harness log: {1}" -f $exitCode, $harnessLog)
        exit $exitCode
    }
} finally {
    if ($server -and -not $server.HasExited) { Stop-Process -Id $server.Id -Force }
    Remove-Item Env:\UPSTAGE_API_KEY -ErrorAction SilentlyContinue
    Remove-Item Env:\PI_OFFLINE -ErrorAction SilentlyContinue
    Remove-Item Env:\PI_TELEMETRY -ErrorAction SilentlyContinue
    Remove-Item Env:\PI_SKIP_VERSION_CHECK -ErrorAction SilentlyContinue
    Remove-Item Env:\OPENCODE_CONFIG -ErrorAction SilentlyContinue
    Remove-Item Env:\OPENCODE_PURE -ErrorAction SilentlyContinue
    Remove-Item Env:\OPENCODE_DISABLE_AUTOUPDATE -ErrorAction SilentlyContinue
    Remove-Variable keyLine,keyValue -ErrorAction SilentlyContinue
    Remove-Variable systemPrompt -ErrorAction SilentlyContinue
}

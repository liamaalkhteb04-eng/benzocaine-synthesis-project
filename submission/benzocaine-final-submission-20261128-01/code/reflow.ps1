param([Parameter(Mandatory=$true)][string]$OutDir)
$ErrorActionPreference='Stop'
$packageRoot=Split-Path -Parent $PSScriptRoot
$out=[IO.Path]::GetFullPath($OutDir)
if(Test-Path -LiteralPath $out){throw 'Use a new output directory; frozen submission files must not be overwritten.'}
New-Item -ItemType Directory -Path $out | Out-Null
$docx=Join-Path $out 'benzocaine-reflow.docx'
$pdf=Join-Path $out 'benzocaine-reflow.pdf'
$raw=Join-Path $out 'raw-word.pdf'
& python (Join-Path $PSScriptRoot 'render_report_docx.py') --markdown (Join-Path $packageRoot 'report/report.md') --output $docx
if($LASTEXITCODE -ne 0){throw 'DOCX renderer failed'}
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File (Join-Path $PSScriptRoot 'word_export.ps1') -DocxPath $docx -PdfPath $pdf -RecordFolder (Join-Path $out 'word-record')
if($LASTEXITCODE -ne 0){throw 'Word export failed'}
& python (Join-Path $PSScriptRoot 'restore_pdf_source_images.py') --pdf $pdf --raw $raw --record (Join-Path $out 'image-fidelity.json')
if($LASTEXITCODE -ne 0){throw 'Image fidelity restoration failed'}
Copy-Item -LiteralPath (Join-Path $packageRoot 'report/records') -Destination (Join-Path $out 'records') -Recurse
Write-Output "Saved-manuscript reflow only; no Solar calls. Output: $out"

param(
 [Parameter(Mandatory=$true)][string]$DocxPath,
 [Parameter(Mandatory=$true)][string]$PdfPath,
 [Parameter(Mandatory=$true)][string]$RecordFolder
)
$ErrorActionPreference='Stop'
$absoluteDocx=(Resolve-Path -LiteralPath $DocxPath).Path
$absolutePdf=[IO.Path]::GetFullPath($PdfPath)
$recordDir=[IO.Path]::GetFullPath($RecordFolder)
if(Test-Path -LiteralPath $absolutePdf){throw 'Preserve previous export; choose a new path.'}
[IO.Directory]::CreateDirectory($recordDir) | Out-Null
function RecordStage([string]$stage){
 @{stage=$stage; utc=[DateTime]::UtcNow.ToString('o')} | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $recordDir 'word-stage.json') -Encoding UTF8
}
$word=$null; $doc=$null
$priorPids=@(Get-Process WINWORD -ErrorAction SilentlyContinue | ForEach-Object Id)
@{preexisting_word_pids=$priorPids} | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $recordDir 'word-process-before.json') -Encoding UTF8
try {
 RecordStage 'Creating dedicated hidden Word application'
 $word=New-Object -ComObject Word.Application
 $word.Visible=$false; $word.DisplayAlerts=0; $word.AutomationSecurity=3
 @{word_version=$word.Version; hwnd=$word.Hwnd; winword_pids=@(Get-Process WINWORD -ErrorAction SilentlyContinue | ForEach-Object Id)} | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $recordDir 'word-instance.json') -Encoding UTF8
 RecordStage 'Opening generated DOCX (no recent-files entry)'
 $doc=$word.Documents.Open($absoluteDocx,$false,$false,$false)
 RecordStage 'Updating page fields and repaginating'
 $null=$doc.Fields.Update()
 $doc.Repaginate()
 $pages=$doc.ComputeStatistics(2)
 RecordStage "Actual DOCX pages: $pages; saving generated copy"
 $doc.Save()
 RecordStage 'Exporting this DOCX through Word fixed-format engine'
 $doc.ExportAsFixedFormat($absolutePdf,17)
 @{status='success';converter='Microsoft Word ExportAsFixedFormat';word_version=$word.Version;actual_DOCX_pages=$pages;DOCX=$absoluteDocx;PDF=$absolutePdf;within20=($pages -le 20);word_pdf_same_layout_engine=$true} | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $recordDir 'word-export.json') -Encoding UTF8
 RecordStage 'Finished'
 Write-Output "Actual DOCX pages=$pages; PDF exported from same document."
}
catch {
 @{status='failed';error_type=$_.Exception.GetType().FullName;message=$_.Exception.Message} | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $recordDir 'word-error.json') -Encoding UTF8
 throw
}
finally {
 if($null -ne $doc){$doc.Close(0);$null=[Runtime.InteropServices.Marshal]::FinalReleaseComObject($doc)}
 if($null -ne $word){$word.Quit();$null=[Runtime.InteropServices.Marshal]::FinalReleaseComObject($word)}
}

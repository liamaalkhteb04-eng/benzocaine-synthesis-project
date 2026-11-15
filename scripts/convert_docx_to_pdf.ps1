param(
    [Parameter(Mandatory=$true)][string]$DocxPath,
    [Parameter(Mandatory=$true)][string]$PdfPath,
    [Parameter(Mandatory=$true)][string]$MetadataPath
)
$ErrorActionPreference = 'Stop'
$absoluteDocx = (Resolve-Path -LiteralPath $DocxPath).Path
$absolutePdf = [System.IO.Path]::GetFullPath($PdfPath)
if (Test-Path -LiteralPath $absolutePdf) { throw 'PDF exists; preserve the earlier export.' }
$word = $null
$document = $null
try {
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $word.DisplayAlerts = 0
    $document = $word.Documents.Open($absoluteDocx, $false, $false, $false)
    $null = $document.Fields.Update()
    $document.Repaginate()
    $pages = $document.ComputeStatistics(2)
    if ($pages -gt 20) { throw "Document has $pages pages; revise the Solar prompt before export." }
    $document.Save()
    $document.ExportAsFixedFormat($absolutePdf, 17)
    $record = @{
        status='success'; converter='Microsoft Word ExportAsFixedFormat';
        word_version=$word.Version; pages=$pages;
        docx_path=$absoluteDocx; pdf_path=$absolutePdf
    }
    $record | ConvertTo-Json | Set-Content -LiteralPath $MetadataPath -Encoding UTF8
    Write-Output "Word PDF export completed; pages=$pages"
}
finally {
    if ($null -ne $document) {
        $document.Close(0)
        $null = [System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($document)
    }
    if ($null -ne $word) {
        $word.Quit()
        $null = [System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($word)
    }
}

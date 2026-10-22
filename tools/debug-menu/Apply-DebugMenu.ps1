param([string]$InputIso)
$ErrorActionPreference = 'Stop'
function Get-IsoSha256([string]$Path) {
    $stream = [IO.File]::OpenRead($Path)
    $algorithm = [Security.Cryptography.SHA256]::Create()
    try { return ([BitConverter]::ToString($algorithm.ComputeHash($stream))).Replace('-','').ToLowerInvariant() }
    finally { $algorithm.Dispose(); $stream.Dispose() }
}
try {
    $spec = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'DebugMenuPatch.json') -Raw | ConvertFrom-Json
    if (-not $InputIso) {
        Add-Type -AssemblyName System.Windows.Forms
        $picker = New-Object System.Windows.Forms.OpenFileDialog
        $picker.Title = 'Choose the MUSIC TEST ISO that worked on your PS3'
        $picker.Filter = 'PS2 ISO (*.iso)|*.iso'
        if ($picker.ShowDialog() -ne [System.Windows.Forms.DialogResult]::OK) { exit 2 }
        $InputIso = $picker.FileName
    }
    $source = (Resolve-Path -LiteralPath $InputIso).Path
    Write-Host 'Checking the source ISO...'
    if ((Get-IsoSha256 $source) -ne $spec.input_sha256) {
        throw 'Wrong source. Choose SpongeBob-Movie-USA-Music-TEST.iso, not the original game or the first overlay probe.'
    }
    $destination = Join-Path ([IO.Path]::GetDirectoryName($source)) 'SpongeBob-Movie-USA-DebugMenu-TEST.iso'
    if (Test-Path -LiteralPath $destination) { throw 'Output already exists. It was not overwritten.' }
    function Decode-Hex([string]$text) {
        [byte[]]$bytes = for ($i=0; $i -lt $text.Length; $i+=2) { [Convert]::ToByte($text.Substring($i,2),16) }
        return ,$bytes
    }
    $reader = [IO.File]::OpenRead($source)
    try {
        foreach ($p in $spec.patches) {
            [byte[]]$expected = Decode-Hex $p.old
            [byte[]]$actual = New-Object byte[] $expected.Length
            $null = $reader.Seek([long]$p.iso_offset,[IO.SeekOrigin]::Begin)
            if ($reader.Read($actual,0,$actual.Length) -ne $actual.Length) { throw 'Truncated source.' }
            for ($i=0; $i -lt $actual.Length; $i++) { if ($actual[$i] -ne $expected[$i]) { throw 'Source code guard failed.' } }
        }
    } finally { $reader.Dispose() }
    Write-Host 'Creating a separate expanded debug-menu ISO...'
    [IO.File]::Copy($source,$destination,$false)
    $writer = [IO.File]::Open($destination,[IO.FileMode]::Open,[IO.FileAccess]::Write,[IO.FileShare]::None)
    try {
        foreach ($p in $spec.patches) {
            [byte[]]$bytes = Decode-Hex $p.new
            $null = $writer.Seek([long]$p.iso_offset,[IO.SeekOrigin]::Begin)
            $writer.Write($bytes,0,$bytes.Length)
        }
        $writer.Flush()
    } finally { $writer.Dispose() }
    $hash = (Get-IsoSha256 $destination)
    if ($spec.output_sha256 -and $hash.ToLowerInvariant() -ne $spec.output_sha256) { throw 'Output hash mismatch. Do not use this output.' }
    Write-Host "Created: $destination"
    Write-Host "SHA-256: $hash"
    Write-Host 'SELECT show/hide; UP/DOWN selects rows 1-3; X changes the selected row. Row 1 music, row 2 XYZ display, row 3 scene/controller display.'
    Write-Host 'This is a custom three-row debug-menu candidate, not an original developer menu. Hardware test pending.'
} catch {
    Write-Error $_
    exit 1
}

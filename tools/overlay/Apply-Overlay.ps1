param([string]$InputIso)
$ErrorActionPreference = 'Stop'
try {
    $spec = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'OverlayPatch.json') -Raw | ConvertFrom-Json
    if (-not $InputIso) {
        Add-Type -AssemblyName System.Windows.Forms
        $picker = New-Object System.Windows.Forms.OpenFileDialog
        $picker.Title = 'Choose the original USA Movie ISO that worked on your PS3'
        $picker.Filter = 'PS2 ISO (*.iso)|*.iso'
        if ($picker.ShowDialog() -ne [System.Windows.Forms.DialogResult]::OK) { exit 2 }
        $InputIso = $picker.FileName
    }
    $source = (Resolve-Path -LiteralPath $InputIso).Path
    Write-Host 'Checking the source ISO...'
    if ((Get-FileHash -LiteralPath $source -Algorithm SHA256).Hash.ToLowerInvariant() -ne $spec.input_sha256) {
        throw 'Wrong source. Choose the original USA Movie ISO matching the documented source hash.'
    }
    $destination = Join-Path ([IO.Path]::GetDirectoryName($source)) 'SpongeBob-Movie-USA-Pad-Debug-PROBE.iso'
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
    Write-Host 'Creating a separate overlay probe ISO...'
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
    $hash = (Get-FileHash -LiteralPath $destination -Algorithm SHA256).Hash
    if ($spec.output_sha256 -and $hash.ToLowerInvariant() -ne $spec.output_sha256) { throw 'Output hash mismatch. Do not use this output.' }
    Write-Host "Created: $destination"
    Write-Host "SHA-256: $hash"
    Write-Host 'This probe enables the controller/status overlay.'
    Write-Host 'This is a controller/status overlay probe, not an original developer menu. Basic overlay owner-tested on CFW PS3; broader compatibility unverified.'
} catch {
    Write-Error $_
    exit 1
}

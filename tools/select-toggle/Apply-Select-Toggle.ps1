param([string]$InputIso)
$ErrorActionPreference = 'Stop'
try {
    if (-not $InputIso) {
        Add-Type -AssemblyName System.Windows.Forms
        $picker = New-Object System.Windows.Forms.OpenFileDialog
        $picker.Title = 'Select the previously tested SpongeBob Movie PAD DEBUG PROBE ISO'
        $picker.Filter = 'PS2 ISO (*.iso)|*.iso'
        if ($picker.ShowDialog() -ne [System.Windows.Forms.DialogResult]::OK) { exit 2 }
        $InputIso = $picker.FileName
    }
    $source = (Resolve-Path -LiteralPath $InputIso).Path
    Write-Host 'Checking the input ISO...'
    $expected = 'EECC8A3FDDEC908DAF626762C39DBED697B32746604B9BAFD3F29EE82B3FA6C9'
    if ((Get-FileHash -LiteralPath $source -Algorithm SHA256).Hash -ne $expected) {
        throw 'Wrong input. Select the extracted PAD DEBUG PROBE ISO that already displayed the overlay, not the original game or .7z archive.'
    }
    $destination = Join-Path ([IO.Path]::GetDirectoryName($source)) 'SpongeBob-Movie-USA-Select-Toggle-TEST.iso'
    if (Test-Path -LiteralPath $destination) { throw 'Output already exists. It was not overwritten.' }
    $oldHex = 'f0ffbd270000bfff089d838f0300601400000000050000100000bfdf58a4120c00000000fbff0010000000000800e0031000bd27000000000000000000000000'
    $newHex = '7b00023c20b5428c0b004010089d838f3000428c02004230030040100000000001006338089d83af030060100000000058a41208000000000800e00300000000'
    [byte[]]$oldBytes = for ($i=0; $i -lt $oldHex.Length; $i+=2) { [Convert]::ToByte($oldHex.Substring($i,2),16) }
    [byte[]]$newBytes = for ($i=0; $i -lt $newHex.Length; $i+=2) { [Convert]::ToByte($newHex.Substring($i,2),16) }
    $offset = 878517296L
    Write-Host 'Creating a separate test ISO. The original is untouched...'
    [IO.File]::Copy($source,$destination,$false)
    $stream = [IO.File]::Open($destination,[IO.FileMode]::Open,[IO.FileAccess]::ReadWrite,[IO.FileShare]::None)
    try {
        $null = $stream.Seek($offset,[IO.SeekOrigin]::Begin)
        $actual = New-Object byte[] 64
        if ($stream.Read($actual,0,64) -ne 64) { throw 'Truncated ISO.' }
        for ($i=0; $i -lt 64; $i++) { if ($actual[$i] -ne $oldBytes[$i]) { throw 'Executable byte check failed.' } }
        $null = $stream.Seek($offset,[IO.SeekOrigin]::Begin)
        $stream.Write($newBytes,0,64)
        $stream.Flush()
    } finally { $stream.Dispose() }
    $hash = (Get-FileHash -LiteralPath $destination -Algorithm SHA256).Hash
    Write-Host "Created: $destination"
    Write-Host "SHA-256: $hash"
    Write-Host 'Boot this separate test ISO on your CFW PS3. Tap SELECT once to hide/show the controller overlay.'
    Write-Host 'This tests a custom toggle, not a restored developer menu. SELECT may also trigger the normal game action.'
} catch {
    Write-Error $_
    exit 1
}

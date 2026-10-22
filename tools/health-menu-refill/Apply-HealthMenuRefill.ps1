param([string]$InputIso, [string]$OutputIso)
# Combined candidate: unchanged hardened stage patcher; incremental input is stable HealthMenu.
$ErrorActionPreference = 'Stop'
$specName = 'HealthMenuRefillPatch.json'
$outputName = 'SpongeBob-Movie-USA-HealthMenuRefill-TEST.iso'
$inputDescription = 'SpongeBob-Movie-USA-HealthMenu-TEST.iso (stable v0.3 output)'
$statusMessage = 'Combined HealthMenu + six-health refill test. Combined hardware testing pending; preserve the stable image.'
$reader = $null
$writer = $null
$temporaryPath = $null
$temporaryCreated = $false
function Get-StreamSha256([IO.Stream]$Stream) {
    $null = $Stream.Seek(0, [IO.SeekOrigin]::Begin)
    $algorithm = [Security.Cryptography.SHA256]::Create()
    try { return ([BitConverter]::ToString($algorithm.ComputeHash($Stream))).Replace('-', '').ToLowerInvariant() }
    finally { $algorithm.Dispose() }
}
function Decode-Hex([string]$Text) {
    if (-not $Text -or $Text.Length % 2 -ne 0 -or $Text -notmatch '\A[0-9a-fA-F]+\z') { throw 'Invalid patch hex.' }
    [byte[]]$decoded = New-Object byte[] ($Text.Length / 2)
    for ($i = 0; $i -lt $decoded.Length; $i++) { $decoded[$i] = [Convert]::ToByte($Text.Substring($i * 2, 2), 16) }
    return ,$decoded
}
try {
    $specPath = [IO.Path]::Combine($PSScriptRoot, $specName)
    $spec = [IO.File]::ReadAllText($specPath) | ConvertFrom-Json
    if ($spec.input_sha256 -notmatch '\A[0-9a-fA-F]{64}\z' -or $spec.output_sha256 -notmatch '\A[0-9a-fA-F]{64}\z') { throw 'Invalid or missing ISO hashes in patch manifest.' }
    if (-not $InputIso) {
        Add-Type -AssemblyName System.Windows.Forms
        $picker = New-Object System.Windows.Forms.OpenFileDialog
        try {
            $picker.Title = 'Choose ' + $inputDescription
            $picker.Filter = 'PS2 ISO (*.iso)|*.iso'
            if ($picker.ShowDialog() -ne [System.Windows.Forms.DialogResult]::OK) { exit 2 }
            $InputIso = $picker.FileName
        } finally { $picker.Dispose() }
    }
    $source = [IO.Path]::GetFullPath($InputIso)
    # Keep this same handle open through hashing, guards and copy. Deny writers.
    $reader = [IO.File]::Open($source, [IO.FileMode]::Open, [IO.FileAccess]::Read, [IO.FileShare]::Read)
    Write-Host 'Checking the source ISO...'
    if ((Get-StreamSha256 $reader) -ne $spec.input_sha256.ToLowerInvariant()) { throw ('Wrong source. Choose ' + $inputDescription + '.') }
    if (-not $OutputIso) { $OutputIso = [IO.Path]::Combine([IO.Path]::GetDirectoryName($source), $outputName) }
    $destination = [IO.Path]::GetFullPath($OutputIso)
    if ([string]::Equals($source, $destination, [StringComparison]::OrdinalIgnoreCase)) { throw 'Input and output must be different files.' }
    if ([IO.File]::Exists($destination) -or [IO.Directory]::Exists($destination)) { throw 'Output already exists. It was not overwritten.' }
    $outputDirectory = [IO.Path]::GetDirectoryName($destination)
    if (-not [IO.Directory]::Exists($outputDirectory)) { throw 'Output directory does not exist.' }
    $patches = @($spec.patches)
    if ($patches.Count -eq 0) { throw 'Patch manifest is empty.' }
    $prepared = @()
    foreach ($patch in $patches) {
        [byte[]]$old = Decode-Hex $patch.old
        [byte[]]$new = Decode-Hex $patch.new
        if ($old.Length -ne $new.Length) { throw 'Patch lengths differ.' }
        if ($null -eq $patch.iso_offset) { throw 'Missing patch offset.' }
        [long]$offset = $patch.iso_offset
        if ([decimal]$patch.iso_offset -ne [decimal]$offset -or $offset -lt 0 -or $old.Length -gt $reader.Length -or $offset -gt ($reader.Length - $old.Length)) { throw 'Patch offset is outside the ISO or is not an integer.' }
        $null = $reader.Seek($offset, [IO.SeekOrigin]::Begin)
        [byte[]]$actual = New-Object byte[] $old.Length
        if ($reader.Read($actual, 0, $actual.Length) -ne $actual.Length) { throw 'Truncated source.' }
        for ($i = 0; $i -lt $actual.Length; $i++) { if ($actual[$i] -ne $old[$i]) { throw 'Source code guard failed.' } }
        $prepared += [pscustomobject]@{ Offset = $offset; Bytes = $new }
    }
    [long]$previousEnd = 0
    foreach ($patch in ($prepared | Sort-Object Offset)) {
        if ($patch.Offset -lt $previousEnd) { throw 'Patch ranges overlap.' }
        $previousEnd = $patch.Offset + $patch.Bytes.Length
    }
    $temporaryPath = [IO.Path]::Combine($outputDirectory, '.' + [IO.Path]::GetFileName($destination) + '.' + [Guid]::NewGuid().ToString('N') + '.partial')
    $writer = [IO.File]::Open($temporaryPath, [IO.FileMode]::CreateNew, [IO.FileAccess]::ReadWrite, [IO.FileShare]::None)
    $temporaryCreated = $true
    Write-Host 'Building a separate temporary ISO...'
    $null = $reader.Seek(0, [IO.SeekOrigin]::Begin)
    $reader.CopyTo($writer)
    foreach ($patch in $prepared) {
        $null = $writer.Seek($patch.Offset, [IO.SeekOrigin]::Begin)
        $writer.Write($patch.Bytes, 0, $patch.Bytes.Length)
    }
    $writer.Flush($true)
    $hash = Get-StreamSha256 $writer
    if ($hash -ne $spec.output_sha256.ToLowerInvariant()) { throw 'Output hash mismatch. Temporary output will be removed.' }
    $writer.Dispose()
    $writer = $null
    # File.Move refuses an existing destination, including a race after the check.
    [IO.File]::Move($temporaryPath, $destination)
    $temporaryCreated = $false
    Write-Host ('Created: ' + $destination)
    Write-Host ('SHA-256: ' + $hash)
    Write-Host $statusMessage
} catch {
    Write-Error $_ -ErrorAction Continue
    exit 1
} finally {
    if ($writer) { $writer.Dispose() }
    if ($reader) { $reader.Dispose() }
    if ($temporaryCreated -and $temporaryPath -and [IO.File]::Exists($temporaryPath)) { [IO.File]::Delete($temporaryPath) }
}

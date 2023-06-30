$interfaceName = "Wi-Fi"  # Replace with the name of your Wi-Fi interface if different

$signalStrength = netsh wlan show interfaces |
  Select-String -Pattern "Signal" |
  ForEach-Object { $_ -replace ".*Signal\s+: ", "" }

Write-Output "Wi-Fi Signal Strength: $signalStrength"

# EthMonitoring Linux CLI version

This version is usable in linux for monitoring rigs on EthMonitoring.com
Read more @ https://www.ethmonitoring.com

# Ports for config

Claymore/Ethminer: 3333

CCMiner: 4068

EWBF: 42000 (Default ports)

# Types for config

0 - Claymore

1 - CCMiner

2 - EWBF

3 - Ethminer

# FAQ

- Claymore's miner v9.4 needs to be enabled in firewall, v9.3 doesn't have this problem.
- EWBF needs to have --api 0.0.0.0:42000 command line parameter added to enable API access.
- CCMiner-Alexis 1.0 needs to have --api-bind=0.0.0.0:4068 parameter in the command line for API access.

# Supports

- Claymore's Dual Ethereum + Decred/Siacoin/Lbry/Pascal AMD+NVIDIA GPU Miner. https://bitcointalk.org/index.php?topic=1433925.0
- EWBF's CUDA Zcash miner https://bitcointalk.org/index.php?topic=1707546.0
- CCMiner-Alexis 1.0

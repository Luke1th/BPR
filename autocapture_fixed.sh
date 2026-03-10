#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   ./autocapture_fixed.sh <OUTDIR> <LABEL> <DURATION_SEC> <IFACE1> [IFACE2 ...]
# Example:
#   ./autocapture_fixed.sh C2_Delay/C2_Delay_30s_trial01 delay30s 120 DPSRS-eth5

OUTDIR="$1"
LABEL="$2"
DUR="${3:-120}"
shift 3
IFACES=("$@")

mkdir -p "$OUTDIR"
DATE="$(date +'%Y%m%d_%H%M%S')"

echo "[*] OUTDIR=$OUTDIR  LABEL=$LABEL  DUR=${DUR}s  DATE=$DATE"
echo "[*] Interfaces: ${IFACES[*]}"

# Optional filter: keep only relevant protocols (GOOSE/SV + IEC104)
# Remove -f line if you want full traffic.
BPF_FILTER='ether proto 0x88b8 or ether proto 0x88ba or tcp port 2404'

PIDS=()
for IF in "${IFACES[@]}"; do
  OUTFILE="${OUTDIR}/${LABEL}_${IF}_${DATE}.pcapng"
  echo "[*] Capturing on $IF -> $OUTFILE"
  tshark -i "$IF" -a "duration:${DUR}" -f "$BPF_FILTER" -w "$OUTFILE" >/tmp/tshark_${IF}.log 2>&1 &
  PIDS+=("$!")
done

# Wait for all tshark processes to finish
for pid in "${PIDS[@]}"; do
  wait "$pid"
done

echo "[+] done"
echo "[*] tshark logs: /tmp/tshark_<iface>.log"

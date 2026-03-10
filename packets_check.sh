for f in C2_Delay/C2_Delay_30s_trial*/*.pcapng; do
 echo "$f"
 tshark -r "$f" -c 1 >/dev/null && echo "OK" || echo " BAD/EMPTY"
done


#sha256sum C0_Baseline/Baseline*/*.pcapng | sort | uniq -c | sort -nr | head

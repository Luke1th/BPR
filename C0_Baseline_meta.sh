#!/usr/bin/env bash
# Run from repository root (where C0_Baseline is located)

sha256sum C0_Baseline/Baseline*/*.pcapng | sort | uniq -c | sort -nr | head | 
awk 'BEGIN{print "["} 
{
  c=$1; h=$2; sub($1 FS $2 FS,""); p=$0; start="null"; 
  if(match(p,/[0-9]{8}_[0-9]{6}/)){ts=substr(p,RSTART,15); 
  start=sprintf("%s-%s-%sT%s:%s:%sZ",substr(ts,1,4),substr(ts,5,2),substr(ts,7,2),substr(ts,10,2),substr(ts,12,2),substr(ts,14,2))} gsub(/"/,"\\\"",p); 
  printf "%s{\"count\":%d,\"hash\":\"%s\",\"path\":\"%s\",\"start_time\":%s}", 
  (NR==1?"":","), c, h, p, (start=="null"?"null":("\""start"\"")); 
} 
END{print "]"}' > C0_Baseline.meta.json

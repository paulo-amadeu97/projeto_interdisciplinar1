#!/bin/bash

source config.cfg

# delay="1"   #Define o tempo em segundos entre uma leitura e outra do trafego de rede

cat /proc/net/dev | grep ":" | tr -s ' ' | grep -v '^ ' | cut -d ' ' -f1 | tr -d ':' > interfaces

echo dateTime: $(date '+%d/%m/%Y %H:%M')

while IFS= read -r i
do
    transfer=$(cat /proc/net/dev | grep "$i" | tr -s ' ' | grep -v '^ ' | cut -d ' ' -f10)

    sleep $delay
    
    transfer=$(expr $(cat /proc/net/dev | grep "$i" | tr -s ' ' | grep -v '^ ' | cut -d ' ' -f10) - "$transfer")
    transfer=$(echo "scale=2;($transfer * 8 / 1000000) / $delay" | bc)

    echo "$i: $transfer"

done < './interfaces'

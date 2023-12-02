#!/bin/bash
hz=0
tempCpu="$(cat /sys/class/hwmon/*/temp*input* 2> /dev/null | head -n1)"  #Busca a informação da temperatura do CPU
cpu=$(top -n 1 | grep "%Cpu" | tr  -s ' ' | cut -d ' ' -f2)    #retira a informação do uso de CPU do top.
cat /proc/cpuinfo | grep "MHz" | cut -d ':' -f2 | tr -d ' '> ./mhz_cpu    #Retira a informação do uso de CPUs em MHz e armazena em um arquivo chamado tmp_cpu

echo dateTime: $(date '+%d/%m/%Y %H:%M')
echo "usoCpu: $cpu" | tr -s ',' '.'
cnt=0           #define um contador

while IFS= read -r i; do            #itera sobre as linhas do arquivo tmp_cpu

    hz=$(echo "scale=4; $hz + $i" | bc)
    (( cnt++ )) || true     #incrementa o contador

done < "./mhz_cpu"      #aponta do arquivo

echo "frequence: $(echo "scale=4; $hz / ($cnt+1)" | bc)"
echo "temp: $(echo "scale=1; $tempCpu / 1000" | bc)"	 #Converte a temperatura para °C e imprime

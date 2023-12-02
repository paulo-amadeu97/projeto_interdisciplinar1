#!/bin/bash

swapTrue() {	#Função que retorna as informações da Swap

	memSwapTotal="$(free -m | grep "Swap" | tr -s ' ' | cut -d ' ' -f2)"
	memSwapUsed="$(free -m | grep "Swap" | tr -s ' ' | cut -d ' ' -f3)"
	
	echo "usoSwap: $memSwapUsed"
	echo "totalSwap: $memSwapTotal"
}

memFree="$(free -m | grep "Mem" | tr -s ' ' | cut -d ' ' -f4)"
memUsed="$(free -m | grep "Mem" | tr -s ' ' | cut -d ' ' -f3)"

echo dateTime: $(date '+%d/%m/%Y %H:%M')
echo "usoMem: $memUsed"
echo "memLivre: $memFree"

if swapon -s | grep "swap" > /dev/null	#testa se existe uma Swap
then
	swapTrue
fi


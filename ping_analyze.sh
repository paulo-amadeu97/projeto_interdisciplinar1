#!/bin/bash

source config.cfg

pingList=()		#Array que armazena os valores de ping
# cont=0			#contador
# pingMed=0		#Vaviável que armazena o a média de pings
# setStep=5		#Define o número de pings da média
# link="8.8.8.8"	#Define o endereço IP para ping.


for ((i=1; i<=$setStep; i++))
do	
	pingValor=$(ping $link -c1 | grep '64 bytes' | tr ' ,=' ':' | cut -d ':' -f11)	#Armazena o valor de cada ping uma lista
	if [[ $pingValor =~ ^[0-9]+(\.[0-9]+)?$ ]]; then

		pingList+=("$pingValor")								
		pingMed=$(echo "scale=2; $pingValor + $pingMed" | bc)

		if [ ${#pingList[@]} -ge $setStep ]
		then
			echo dateTime: $(date '+%d/%m/%Y %H:%M')
			echo -n "ping: "	
			echo "scale=2; $pingMed / ($setStep + 1)" | bc
			pingList=()
			pingMed=0

		else
			(( cont++ )) || true
		fi
	else
		continue
	fi
done


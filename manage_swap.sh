#!/bin/bash

source config.cfg

memFree="$(free -m | grep "Mem" | tr -s ' ' | cut -d ' ' -f4)"
memUsed="$(free -m | grep "Mem" | tr -s ' ' | cut -d ' ' -f3)"

createSwap() {
    sudo fallocate -l 4G /swapfile
    chmod 600 /swapfile
    sudo mkswap /swapfile
    sudo swapon /swapfile
}

removeSwap() {
    sudo swapoff -v /swapfile
    sudo sed -i '/swapfile/d' /etc/fstab
    systemctl daemon-reload
    sudo rm /swapfile
}

manage() {
    if [[ $(echo "$memFree / $memUsed" | bc) -gt $(echo $valorCritico / 100 | bc) ]] && [ ! "$(swapon -s | grep "swapfile")" ]; then
        echo "USO DE MEMÓRIA ACIMA DO NIVEL CRÍTICO. CRIANDO SWAP"
        createSwap
        timestamp=$(date +%s)
        while true; do
            sleep 5
            if [ "$(($timestamp + 600))" -gt "$(date +%s)" ] && [[ $(echo "$memFree / $memUsed" | bc) -lt $(echo $valorCritico / 100 | bc) ]]; then
                removeSwap
                break
            fi
        done
    fi
}
if $GerenciarSwap; then
    manage
else
    exit 0
fi
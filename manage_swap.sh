#!/bin/bash

source config.cfg

createSwap() {

    sudo fallocate -l 4G /swapfile      #Aloca um espaço de 4GB em um diretório chamado swapfile

    chmod 600 /swapfile                 #Habilita permissões necessárias

    sudo mkswap /swapfile               #Cria a swap

    sudo swapon /swapfile               #Habilita a swap
}

removeSwap() {

    sudo swapoff -v /swapfile               #Desativa a swap

    sudo sed -i '/swapfile/d' /etc/fstab    #Remova o /swapfile do fstab

    systemctl daemon-reload                 #Regenera o sistema de montagem

    sudo rm /swapfile                       #apaga o arquivo /swapfile
}

manage() {

    if swapon -s | grep "swapfile" > /dev/null      #Valida se existe uma Swap habilitada
    then

        removeSwap

    else

        createSwap
        
    fi

}
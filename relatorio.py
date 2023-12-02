#!/bin/env python3.10

import csv
import numpy as np
import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Image
import subprocess

def lerCSV(arquivo_csv):
    with open(arquivo_csv, 'r') as arquivo:
        readArquivo = csv.DictReader(arquivo)
        lista = list(readArquivo)
        return lista
        

def gerarListas(listData: list, dataInicio, dataFim, coluna):
    try:
        indices = [item['dateTime'] for item in listData]
        indice_inicio = indices.index(dataInicio)
        indice_fim = indices.index(dataFim) + 1
    except ValueError:
        print(f"Valor {dataInicio} ou {dataFim} não encontrado na lista.")
        return []

    rangeData = [(listData[i]['dateTime'], listData[i][coluna]) for i in range(indice_inicio, indice_fim) if i < len(listData)]

    return rangeData


def media_movel(valores, janela):
    valores_suavizados = []
    soma = []
    cont = 1
    for i in range(0, len(valores)):
        soma.append(float(valores[i]))
        cont += 1
        if i == len(valores) -1:
            media = np.mean(soma)
            valores_suavizados.append(media)
        elif cont >= janela:
            media = np.mean(soma)
            valores_suavizados.append(media)
            soma = []
            cont = 1
    return valores_suavizados

def grafico(dadosLista, namePng, titulo):
    janela_media_movel = int(.005*len(dadosLista))
    listaX, listaY = zip(*dadosLista)
    valores_suavizados = media_movel(listaY, janela_media_movel)

    fig, ax = plt.subplots()
    ax.plot(valores_suavizados, marker='', linestyle='-')

    ax.set_xticks([])
    plt.xticks(rotation=45, ha="right")
    ax.set_title(titulo)
    fig.savefig('./graficos_relatorio/'+ namePng + '.png')

    
def graficoSimplificado(inicio = str, fim = str):
    cpu = lerCSV("./cpuData.csv")
    mem = lerCSV("./memData.csv")
    rede = lerCSV("./netData.csv")
    ping = lerCSV("./pingData.csv")

    lista = []

    lista.append(gerarListas(cpu, inicio, fim, 'usoCpu'))
    lista.append(gerarListas(cpu, inicio, fim, 'frequence'))
    lista.append(gerarListas(cpu, inicio, fim, 'temp'))

    lista.append(gerarListas(mem, inicio, fim, 'usoMem'))
    lista.append(gerarListas(mem, inicio, fim, 'memLivre'))
    lista.append(gerarListas(mem, inicio, fim, 'usoSwap'))

    lista.append(gerarListas(rede, inicio, fim, 'enp9s0'))
    lista.append(gerarListas(ping, inicio, fim, 'ping'))

    nomes = ['uso_cpu', 'frequence', 'temperatura', 'uso_mem', 'mem_free', 'uso_swap', 'uso_rede', 'ping']
    titulos = ['USO DE CPU', 'FREQUÊNCIA', 'TEMPERATURA', 'USO DE MEMÓRIA', 'USO DE SWAP', 'BANDA', 'LATÊNCIA']

    for l, n, t in zip(lista, nomes, titulos):
        try:
            grafico(l, n, t)
        except Exception as e:
            print(f"Ocorreu uma exceção: {type(e).__name__}")
            continue

    name_file = "relatorio"

    try:
        resultado = subprocess.check_output(["ls", './graficos_relatorio'], text=True, stderr=subprocess.PIPE)
        
        arquivos = [nome.strip() for nome in resultado.splitlines()]
        
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar 'ls': {e.stderr}")

    caminhos_graficos = [f"./graficos_relatorio/{nome}" for nome in arquivos]

    doc = SimpleDocTemplate(name_file + '.pdf')
    info = [Image(caminho) for caminho in caminhos_graficos]

    doc.build(info)

        

if __name__ == "__main__":
    graficoSimplificado("25/11/2023 21:05", "25/11/2023 21:06")
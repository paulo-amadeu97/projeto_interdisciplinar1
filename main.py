#!/bin/env python3

from writedata import cpuWriter, pingWriter, netWriter, memWriter
from relatorio import graficoSimplificado
from create_csv import all
import csv
from threading import Thread
import time
from flask import Flask, render_template, request, send_from_directory
from flask_socketio import SocketIO
import re
import subprocess

def extract(script, variavel):
    padrao = r'^\s*export\s+{0}=(.*)'.format(re.escape(variavel))
    retorno = re.search(padrao, script, flags=re.MULTILINE)
    if retorno:
        return retorno.group(1).strip("'\"")
    else:
        return None
    
with open('config.cfg', 'r') as config:
    script = config.read()

interfaceMain = extract(script, 'interfaceMain')
GerenciarSwap = extract(script, 'GerenciarSwap')
valorCritico = extract(script, 'valorCritico')


app = Flask(__name__)
socketio = SocketIO(app)

dataListCpu = []
dataListHz = []
dataListTemp = []
dataListUsoMem = []
dataListFreeMem =[]
dataListUsoSwap = []
dataListNet = []
dataListPing = []

def run_funcao(funcao):
    while True:
        time.sleep(1)
        funcao()

def funcao_setup(funcao):
    funcao()


# def swap_adm():
#     if GerenciarSwap:
#         subprocess.check_output("sudo su", shell=True, text=True)
#         while True:
#             memTotal = subprocess.check_output("free -m | grep 'Swap' | tr -s ' ' | cut -d ' ' -f2", shell=True, text=True)
#             memTotal = float(memTotal)
#             memUsed = subprocess.check_output("free -m | grep 'Swap' | tr -s ' ' | cut -d ' ' -f3", shell=True, text=True)
#             memUsed = float(memUsed)
#             if (memUsed / memTotal)*100 >= valorCritico:
#                 print('Uso de memoria em nivel critico, criando Swap.')
#                 subprocess.check_output("./manage_swap.sh", shell=True, text=True)
#                 time.sleep(600)
#                 while True:
#                     memTotal = subprocess.check_output("free -m | grep 'Swap' | tr -s ' ' | cut -d ' ' -f2", shell=True, text=True)
#                     memTotal = float(memTotal)
#                     memUsed = subprocess.check_output("free -m | grep 'Swap' | tr -s ' ' | cut -d ' ' -f3", shell=True, text=True)
#                     memUsed = float(memUsed)
#                     if (memUsed / memTotal)*100 <= valorCritico:
#                         print('Uso de memoria em nivel normal, revertendo Swap.')
#                         subprocess.check_output("./manage_swap.sh", shell=True, text=True)
#                         break
#             else:
#                 print("Nivel de memoria normal")
#                 time.sleep(5)

def dadosToGraf(coluna, caminhoCSV, dataList, nameEspace, update_graf):
    while True:
        dataList = []
        with open(caminhoCSV, 'r') as arquivo_csv:
            csvReader = csv.DictReader(arquivo_csv)
            linhas = list(csvReader)

            for i in linhas[-51:]:
                dataList.append(i[coluna])
            
        socketio.emit(update_graf, {'x':list(range(0, 51)), 'y': dataList}, namespace=nameEspace)
        time.sleep(1.2)

@app.route('/relatorio', methods=['GET', 'POST'])
def relatorio():
    if request.method == 'POST':
        inicio = request.form.get('inicio')
        fim = request.form.get('fim')
        print(inicio)
        print(fim)
        print("to aqui1")
        if inicio and fim:
            print("to aqui2")
            graficoSimplificado(inicio, fim)

    return render_template('index.html')

@app.route('/relatorio.pdf')
def download_relatorio():
    return send_from_directory('.', 'relatorio.pdf', as_attachment=True)

@app.route('/')

def index():
    return render_template('index.html')

@socketio.on('connect', namespace='/uso_cpu')
def connect_cpu():
    print('Cliente conectado')
    socketio.emit('update_graf_cpu', {'x':list(range(0, 51)), 'y': dataListCpu}, namespace='/uso_cpu')

@socketio.on('connect', namespace='/hz')
def connect():
    print('Cliente conectado')
    socketio.emit('update_graf_hz', {'x':list(range(0, 51)), 'y': dataListHz}, namespace='/hz')

@socketio.on('connect', namespace='/temp')
def connect():
    print('Cliente conectado')
    socketio.emit('update_graf_temp', {'x':list(range(0, 51)), 'y': dataListTemp}, namespace='/temp')

@socketio.on('connect', namespace='/uso_mem')
def connect():
    print('Cliente conectado')
    socketio.emit('update_graf_uso_mem', {'x':list(range(0, 51)), 'y': dataListUsoMem}, namespace='/uso_mem')

@socketio.on('connect', namespace='/free_mem')
def connect():
    print('Cliente conectado')
    socketio.emit('update_graf_free_mem', {'x':list(range(0, 51)), 'y': dataListFreeMem}, namespace='/free_mem')

@socketio.on('connect', namespace='/uso_swap')
def connect():
    print('Cliente conectado')
    socketio.emit('update_graf_uso_swap', {'x':list(range(0, 51)), 'y': dataListUsoSwap}, namespace='/uso_swap')

@socketio.on('connect', namespace='/uso_rede')
def connect():
    print('Cliente conectado')
    socketio.emit('update_graf_rede', {'x':list(range(0, 51)), 'y': dataListNet}, namespace='/uso_rede')

@socketio.on('connect', namespace='/ping')
def connect():
    print('Cliente conectado')
    socketio.emit('update_graf_ping', {'x':list(range(0, 51)), 'y': dataListPing}, namespace='/ping')

if __name__ == '__main__':
    # Thread(target=swap_adm)

    Thread(target=funcao_setup)

    Thread(target=funcao_setup, args=(all,))

    thCpu = Thread(target=run_funcao, args=(cpuWriter,))
    thCpu.start()
    Thread(target=dadosToGraf, args=('usoCpu', './cpuData.csv', 'dataListCpu', '/uso_cpu', 'update_graf_cpu')).start()

    Thread(target=dadosToGraf, args=('frequence', './cpuData.csv', 'dataListHz', '/hz', 'update_graf_hz')).start()

    Thread(target=dadosToGraf, args=('temp', './cpuData.csv', 'dataListTemp', '/temp', 'update_graf_temp')).start()

    thMem = Thread(target=run_funcao, args=(memWriter,))
    thMem.start()

    Thread(target=dadosToGraf, args=('usoMem', './memData.csv', 'dataListUsoMem', '/uso_mem', 'update_graf_uso_mem')).start()

    Thread(target=dadosToGraf, args=('memLivre', './memData.csv', 'dataListFreeMem', '/free_mem', 'update_graf_free_mem')).start()

    Thread(target=dadosToGraf, args=('usoSwap', './memData.csv', 'dataListUsoSwap', '/uso_swap', 'update_graf_uso_swap')).start()

    thNet = Thread(target=run_funcao, args=(netWriter,))
    thNet.start()

    Thread(target=dadosToGraf, args=(interfaceMain, './netData.csv', 'dataListNet', '/uso_rede', 'update_graf_rede')).start()

    thPing = Thread(target=run_funcao, args=(pingWriter,))
    thPing.start()

    Thread(target=dadosToGraf, args=('ping', './pingData.csv', 'dataListPing', '/ping', 'update_graf_ping')).start()
    
    socketio.run(app, debug=False, host='0.0.0.0')

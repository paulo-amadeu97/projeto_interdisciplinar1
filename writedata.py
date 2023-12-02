#!/bin/python3.10

import pandas as pd
import subprocess

def cpuWriter():
    
    cpush = subprocess.check_output("./cpu.sh", shell=True, text=True)
    cpuDict = {}
    for i in cpush.splitlines():
        key, value = i.split(": ")
        cpuDict[key.strip()] = value.strip()

    dfCpuData = pd.DataFrame()
    
    newLine = pd.DataFrame(cpuDict, index=[0])

    dfCpuData = pd.concat([dfCpuData, newLine], ignore_index=True)
    dfCpuData.to_csv("cpuData.csv", mode='a', header=False, index=False)


def memWriter():
    
    memsh = subprocess.check_output("./mem.sh", shell=True, text=True)
    memDict = {}
    for i in memsh.splitlines():
        key, value = i.split(": ")
        memDict[key.strip()] = value.strip()

    dfMemData = pd.DataFrame()
    
    newLine = pd.DataFrame(memDict, index=[0])

    dfMemData = pd.concat([dfMemData, newLine], ignore_index=True)
    dfMemData.to_csv("memData.csv", mode='a', header=False, index=False)


def netWriter():
    
    netsh = subprocess.check_output("./internet.sh", shell=True, text=True)
    netDict = {}
    for i in netsh.splitlines():
        key, value = i.split(": ")
        netDict[key.strip()] = value.strip()

    dfNetData = pd.DataFrame()
    
    newLine = pd.DataFrame(netDict, index=[0])

    dfNetData = pd.concat([dfNetData, newLine], ignore_index=True)
    dfNetData.to_csv("netData.csv", mode='a', header=False, index=False)


def pingWriter():
    
    pingsh = subprocess.check_output("./ping_analyze.sh", shell=True, text=True)
    pingDict = {}
    for i in pingsh.splitlines():
        key, value = i.split(": ")
        pingDict[key.strip()] = value.strip()

    dfPingData = pd.DataFrame()
    
    newLine = pd.DataFrame(pingDict, index=[0])

    dfPingData = pd.concat([dfPingData, newLine], ignore_index=True)
    dfPingData.to_csv("pingData.csv", mode='a', header=False, index=False)


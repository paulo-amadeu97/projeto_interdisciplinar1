#!/bin/python3.10
import os
import pandas as pd
import sys
def all():
    nameFiles = ["cpuData.csv", "netData.csv", "memData.csv", "pingData.csv"]
    count = 0

    for files in nameFiles:

        if os.path.exists(f"./{files}"):

            count += 1

            if count == 4:

                sys.exit(1)

        else:

            continue

    cpuData = {

    "dateTime": [],
    "usoCpu": [],
    "frequence": [],
    "temp": []

    }

    netData = {

    "dateTime": []

    }

    with open ("interfaces", "r") as interfaces:

        for i in interfaces:

            netData[i.strip()] = []

    memData = {

        "dateTime": [],
        "usoMem": [],
        "memLivre": [],
        "usoSwap": [],
        "totalSwap": []

    }

    pingData = {

    "dateTime": [],
    "ping": []

    }

    dfCpuData = pd.DataFrame(cpuData)
    dfNetData = pd.DataFrame(netData)
    dfMemData = pd.DataFrame(memData)
    dfPingData = pd.DataFrame(pingData)

    dataframes = [dfCpuData, dfNetData, dfMemData, dfPingData]
    #nameFiles = ["cpuData.csv", "netData.csv", "memData.csv", "pingData.csv"]

    for df, nf in zip(dataframes, nameFiles):

        df.to_csv(nf, index=False)

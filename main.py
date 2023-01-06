"""
 Main program
 """
import logging
import csv
import os
import threading
import time

import dash
from dash import dcc
from dash import html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from models.ConfigurationLoader import Config
from models.Connexion import Connexion
from models.MonitorThreading import MonitorTreading
from models.ApacheServerLogInfo import LogInfo
import models.Dash as dashboard

machineConfiguration = Config()
nbMachineConfiguration = machineConfiguration.getNbMachineConfigurations()
monitors = []
connexions = []
clients = []
logInfos = []

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#F0F8FF',
    'text': '#00008B'
}

# Init
for m in range(nbMachineConfiguration):
    monitors.append(machineConfiguration.loadMachineConfiguration(m))
    connexions.append(Connexion(monitors[m]))
    clients.append(connexions[m].client)
    logInfos.append(LogInfo())

logging.basicConfig(level=logging.DEBUG,
                    filename="monitors.log",
                    format='%(message)s'
                    )


def get_data():
    while True:
        # Starting one thread for each client
        MonitorThreads = []
        for h in range(nbMachineConfiguration):
            t = MonitorTreading(clients[h], h, logInfos[h])
            t.start()
            MonitorThreads.append(t)

        hardwareUsageResults = []
        apache_statusCode_results = []
        apache_clientConnect_results = []

        # Get result from thread when they have finish their tasks
        for t in MonitorThreads:
            t.join()

            # Get Monitoring hardware usage results
            hardwareUsageResults.append(t.hardwareUsage_result)

            # Get monitoring apache log results
            apache_statusCode_results.append(t.apache_statusCode_result)
            apache_clientConnect_results.append(t.apache_clientConnect_result)

        # APACHE LOG -----------------------------------------------------
        # CSV Filling
        csv_fileNames = []
        for host_id in range(nbMachineConfiguration):
            csv_filename = machineConfiguration.machines_hostnames[host_id] \
                           + '_apacheLog_statusCode404' \
                           + '.csv'
            csv_fileNames.append(csv_filename)

            # Create a csv file in write mode if not already exist
            if not os.path.exists(csv_filename):
                with open(csv_filename, 'w', newline='') as f:
                    # Create a CSV writer object
                    csv_writer = csv.writer(f)

                    # Write header in the first line of the CSV file
                    csv_writer.writerow(['Date', 'OCCURRENCE'])

            # Open the csv file created before in add mode
            with open(csv_filename, 'a', newline='') as f:
                # Create a CSV writer object
                csv_writer = csv.writer(f)

                # Write the data in the CSV file
                for value in apache_statusCode_results[host_id]:
                    csv_writer.writerow([value, 1])

            csv_filename = machineConfiguration.machines_hostnames[host_id] \
                           + '_apacheLog_clientConnect' \
                           + '.csv'
            csv_fileNames.append(csv_filename)

            # Create a csv file in write mode if not already exist
            if not os.path.exists(csv_filename):
                with open(csv_filename, 'w', newline='') as f:
                    # Create a CSV writer object
                    csv_writer = csv.writer(f)

                    # Write header in the first line of the CSV file
                    csv_writer.writerow(['Date', 'OCCURRENCE'])

            # Open the csv file created before in add mode
            with open(csv_filename, 'a', newline='') as f:
                # Create a CSV writer object
                csv_writer = csv.writer(f)

                # Write the data in the CSV file
                for value in apache_clientConnect_results[host_id]:
                    csv_writer.writerow([value, 1])

        # Hardware usage ---------------------------------------
        # CSV Filling
        for host_id in range(nbMachineConfiguration):
            csv_filename = machineConfiguration.machines_hostnames[host_id] + '_hardwareUsage' + '.csv'
            csv_fileNames.append(csv_filename)

            # Create a csv file in write mode if not already exist
            if not os.path.exists(csv_filename):
                with open(csv_filename, 'w', newline='') as f:
                    # Create a CSV writer object
                    csv_writer = csv.writer(f)

                    # Write header in the first line of the CSV file
                    csv_writer.writerow(['Date', 'CPU_USAGE', 'MEM_USAGE', 'STO_USAGE'])

            # Open the csv file created before in add mode
            with open(csv_filename, 'a', newline='') as f:
                # Create a CSV writer object
                csv_writer = csv.writer(f)

                # Write the data in the CSV file
                csv_writer.writerow(hardwareUsageResults[host_id])

        print("DATA SCRAPPING DONE")
        update_server_metrics(csv_fileNames)
        time.sleep(5)


def update_server_metrics(list_csv):
    list_figCpuUsage = []
    list_dfCpuUsage = []
    for csv_name in list_csv:
        # Our dataframe
        if "_hardwareUsage" in csv_name:
            df = pd.read_csv(csv_name)
            list_dfCpuUsage.append(df)
            fig = px.scatter(df, x="Date", y="CPU_USAGE")
            fig.update_traces(mode='lines')
            list_figCpuUsage.append([fig, csv_name])

    list_layout = []
    for i in range(len(list_figCpuUsage)):
        if i != len(list_figCpuUsage)-1:
            app.layout = html.Div(children=[
                html.H2(children='HARDWARE USAGES'),
                html.Div(children="'''" + list_figCpuUsage[i][1].split("_")[0] + "'''"),
                dashboard.generate_graph(list_figCpuUsage[i][0]),
            ])
        else:
            app.layout = html.Div(children=[
                html.H2(children='HARDWARE USAGES'),
                html.Div(children="'''" + list_figCpuUsage[i][1].split("_")[0] + "'''"),
                dashboard.generate_graph(list_figCpuUsage[i][0])
            ])
        list_layout.append(app.layout)
    for layout in list_layout:
        app.layout += layout

    print("DASH UPDATED")


# Init the data scrapper thread
dataScrapperThread = threading.Thread(target=get_data)
# Start the data scrapper thread
dataScrapperThread.start()

app.run_server()

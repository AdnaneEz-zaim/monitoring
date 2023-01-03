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

machineConfiguration = Config()
nbMachineConfiguration = machineConfiguration.getNbMachineConfigurations()
monitors = []
connexions = []
clients = []
logInfos = []
csv_fileNames = []

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
                    csv_writer.writerow(['Date','CPU_USAGE','MEM_USAGE','STO_USAGE'])

            # Open the csv file created before in add mode
            with open(csv_filename, 'a', newline='') as f:
                # Create a CSV writer object
                csv_writer = csv.writer(f)

                # Write the data in the CSV file
                csv_writer.writerow(hardwareUsageResults[host_id])

        print("DATA SCRAPPING DONE")
        update_server_metrics()
        time.sleep(5)

def update_server_metrics():

    # Our dataframe
    df = pd.read_csv("leodagan.telecomste.net_hardwareUsage.csv")
    fig = px.line(df, x="Date", y="CPU_USAGE")
    fig.update_traces(mode='lines')

    df2 = pd.read_csv("seli.telecomste.net_hardwareUsage.csv")
    print(float(df2['CPU_USAGE'][df2['CPU_USAGE'].size - 1]))
    fig2 = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = float(df2['CPU_USAGE'][df2['CPU_USAGE'].size - 1]),
        gauge={'axis': {'range': [0, 100]},
               'steps': [
                   {'range': [0, 50], 'color': "orange"},
                   {'range': [50, 100], 'color': "red"}],
               'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 90}}))
    fig2.update_traces()

    app.layout = html.Div(children=[
        html.H1(children='HARDWARE USAGES'),

        html.Div(children='''
            MONITOR 1.
        '''),

        dcc.Graph(
            id='monitor1-graph',
            figure=fig
        ),

        html.Div(children='''
        MONITOR 2.
    '''),

        dcc.Graph(
            id='monitor2-graph',
            figure=fig2
        )

    ])

    print("DASH UPDATED")


# Init the data scrapper thread
dataScrapperThread = threading.Thread(target=get_data)
# Start the data scrapper thread
dataScrapperThread.start()

app.run_server()



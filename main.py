"""
 Main program
 """
import threading
import time
import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dash import html, dcc
from models.ConfigurationLoader import Config
from models.Connexion import Connexion
from models.MonitorThreading import MonitorTreading
from models.ApacheServerLogInfo import LogInfo
from models.CSVFiller import fill_csv
import models.Dash as Dashboard

machineConfiguration = Config()
nbMachineConfiguration = machineConfiguration.getNbMachineConfigurations()
monitors = []
connexions = []
clients = []
logInfos = []
csv_fileNames = [[] for _ in range(nbMachineConfiguration)]
uptime_serverResults = [None] * nbMachineConfiguration
cpuModel_server = [None] * nbMachineConfiguration
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, use_pages=True)
app.title = "GROUP 6 Server Monitoring Dashboard"


def createAppLayout(list_csv):
    list_layout = [Dashboard.generate_header_layout(),
        html.H1("Ajouter une machine",className="text-center"),
        dcc.Input(id='input-1', type='text', placeholder='Entrer un hostname',className='Input-form'),
        dcc.Input(id='input-2', type='text', placeholder='Entrer un port',className='Input-form'),
        dcc.Input(id='input-3', type='text', placeholder='Entrer un mot de passe',className='Input-form'),
        dcc.Input(id='input-4', type='text', placeholder='Entrer un username',className='Input-form'),
        html.Div(id='output'),
        html.Div(html.Button('Submit',id='submit-button', n_clicks=0),className="button-center")

    ]
    app.layout = Dashboard.generate_app_layout(list_layout)

    print("DASH LAYOUT CREATED")

@app.callback(Output('output', 'children'),
              [Input('submit-button', 'n_clicks')],
              [Input('input-1', 'value'),
               Input('input-2', 'value'),
               Input('input-3', 'value'),
               Input('input-4', 'value')])
def get_input_value(n_clicks, input1, input2, input3, input4):
    if n_clicks == 0:
        return ''
    else:
        # Open the original file
        with open('config.ini', 'r') as file:
            # Read all the lines in the file
            lines = file.readlines()
            # Open the original file again to write the modified content
            with open('config.ini', 'w') as file:
                i=0
                for line in lines :
                    if i==0 :
                        file.write(line)
                    else :
                        if i==4:
                            file.write(line+';'+input4)
                        else:
                            content= input1
                            if i == 2 :
                                file.write(line[:-1]+';'+input2+'\n')
                            elif i == 3 :
                                file.write(line[:-1]+';'+input3+'\n')
                            else :
                                file.write(line[:-1]+';'+input1+'\n')
                    i+=1
                    
        return f'Name: {input1}, Email: {input2}, Phone: {input3},adnane: {input4}'

createAppLayout(csv_fileNames)
app.run_server(debug=True)

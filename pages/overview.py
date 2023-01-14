import dash
from dash import html, dcc
from models.ConfigurationLoader import Config
import models.Dash as Dashboard

dash.register_page(__name__, path='/')

machineConfiguration = Config()
nbMachineConfiguration = machineConfiguration.getNbMachineConfigurations()

title_layout = html.Div(children=html.H1("Server overview"),
        className="titleOverview"
)
serverPanel_layout = []
for h in range(nbMachineConfiguration):
    hostname = machineConfiguration.machines_hostnames[h]
    serverPanel_layout.append(Dashboard.generate_serverOverviewPanel(hostname,"NULL", h))

server_layout = html.Div(children=serverPanel_layout,
        className="serverOverview"
)

final_layout = [title_layout, server_layout, Dashboard.generate_interval_component()]
layout = html.Div(children=final_layout, className="content")
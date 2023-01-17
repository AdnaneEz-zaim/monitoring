import dash
from dash import html, dcc
from models.ConfigurationLoader import Config
from dash.dependencies import Input, Output, State
import models.Dash as Dashboard

dash.register_page(__name__, path='/', order=1)

layout = Dashboard.generate_overview_layout()

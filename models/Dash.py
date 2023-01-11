from dash import Dash, html, dcc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])


def generate_graph(fig):
    return dcc.Graph(
        id="fig",
        figure=fig
    )


def generate_header_layout():
    header_layout = html.Div(children=[
        html.H1(children="Global Dashboard")
    ])
    return header_layout


def generate_hostname_title(hostname):
    hostname_layout = html.Div(children=[
        html.H2(children=hostname)
    ])
    return hostname_layout


def generate_layout_brick(csv_name, uptime_serverResults, cpuModel_server, host_id):
    # HARDWARE USAGE FRAME
    if "_hardwareUsage" in csv_name:
        df = pd.read_csv(csv_name)
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Scatter(x=df['Date'], y=df['CPU_USAGE'], name="CPU_USAGE"))
        fig.add_trace(go.Scatter(x=df['Date'], y=df['MEM_USAGE'], name="MEM_USAGE"))
        fig.add_trace(go.Scatter(x=df['Date'], y=df['STO_USAGE'], name="STO_USAGE"))

        # Create layout hardware usage
        uptime = "Uptime : " + str(uptime_serverResults[host_id])
        cpuModel = "CPU Model : " + str(cpuModel_server[host_id])
        hardware_layout = html.Div(children=[
            html.H6(children=uptime),
            html.H6(children=cpuModel),
            html.Div(children=''' Hardware usage '''),
            generate_graph(fig),
        ])

        return hardware_layout

    elif "apacheLog_statusCode404" in csv_name:
        df = pd.read_csv(csv_name)
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Scatter(x=df['Date'], y=df['OCCURRENCE'], name="ERROR 404"))

        # Create layout status code
        apache_statusCode_layout = html.Div(children=[
            html.Div(children=''' Status code 404 '''),
            generate_graph(fig),
        ])

        return apache_statusCode_layout
    elif "apacheLog_clientConnect" in csv_name:
        df = pd.read_csv(csv_name)
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Scatter(x=df['Date'], y=df['OCCURRENCE'], name="client connection"))

        # Create layout status code
        apache_clientConnect_layout = html.Div(children=[
            html.Div(children=''' Client connections '''),
            generate_graph(fig),
        ])

        return apache_clientConnect_layout
    elif "_apacheLog_requestUrl" in csv_name:
        df = pd.read_csv(csv_name)
        fig = px.bar(df, x='URL', y='OCCURRENCE')

        # Create layout status code
        apache_requestUrl_layout = html.Div(children=[
            html.Div(children=''' Request url '''),
            generate_graph(fig),
        ])
        return apache_requestUrl_layout
    else:
        return html.Div(children=[])


def generate_app_layout(list_layout):
    return html.Div(children=list_layout)

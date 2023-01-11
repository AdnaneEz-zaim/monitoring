from dash import Dash, html, dcc
import pandas as pd


def generate_header_layout():
    header_layout = html.Div(children=[
        html.H1(children="Global Dashboard",
                className="header-title",
                )

        ],
        className="header"
    )
    return header_layout


def generate_hostname_title(hostname, uptime_serverResults, host_id):
    hostname_layout = html.Div(children=[
        html.H2(children=hostname, className="hostname"),
        html.H6(children="Uptime : " + str(uptime_serverResults[host_id][0]), className="uptime")
    ])
    return hostname_layout


def generate_layout_hardware(hardware_csv_list, cpuModel_server, host_id):
    # HARDWARE USAGE FRAME
    for csv_name in hardware_csv_list:

        df = pd.read_csv(csv_name)

        # Create layout hardware usage
        cpuModel = str(cpuModel_server[host_id][0])
        hardware_layout = \
            html.Div(
                children=[
                    dcc.Graph(
                        id="cpu-usage-graph",
                        figure={
                            "data": [
                                {
                                    "x": df["Date"],
                                    "y": df["CPU_USAGE"],
                                    "type": "lines",
                                    "hovertemplate": "%{y:.2f}%"
                                                     "<extra></extra>",
                                },
                            ],
                            "layout": {
                                "title": {
                                    "text": "CPU usage [" + cpuModel + "]",
                                    "x": 0.05,
                                    "xanchor": "left",
                                },
                                "xaxis": {"fixedrange": False},
                                "yaxis": {
                                    "ticksuffix": "%",
                                    "fixedrange": False,
                                },
                                "colorway": ["#17B897"],
                            },
                        },
                    ),
                    dcc.Graph(
                        id="mem-usage-graph",
                        figure={
                            "data": [
                                {
                                    "x": df["Date"],
                                    "y": df["MEM_USAGE"],
                                    "type": "lines",
                                    "hovertemplate": "%{y:.2f}%"
                                                     "<extra></extra>",
                                },
                            ],
                            "layout": {
                                "title": {
                                    "text": "Memory usage",
                                    "x": 0.05,
                                    "xanchor": "left",
                                },
                                "xaxis": {"fixedrange": False},
                                "yaxis": {
                                    "ticksuffix": "%",
                                    "fixedrange": False,
                                },
                                "colorway": ["#9b59b6"],
                            },
                        },
                    ),
                    dcc.Graph(
                        id="sto-usage-graph",
                        figure={
                            "data": [
                                {
                                    "x": df["Date"],
                                    "y": df["STO_USAGE"],
                                    "type": "lines",
                                    "hovertemplate": "%{y:.2f}%"
                                                     "<extra></extra>",
                                },
                            ],
                            "layout": {
                                "title": {
                                    "text": "Storage usage",
                                    "x": 0.05,
                                    "xanchor": "left",
                                },
                                "xaxis": {"fixedrange": False},
                                "yaxis": {
                                    "ticksuffix": "%",
                                    "fixedrange": False,
                                },
                                "colorway": ["#3498db"],
                            },
                        },
                    ),
                ],
                className="card",
            )
        return hardware_layout
    return html.Div(children=[])

def generate_layout_apache(list_csvname, host_id):

    df_list = []
    for csvApache in list_csvname:
        df_list.append(pd.read_csv(csvApache))

        # Create layout apache log

    if len(df_list) == 3:
        apache_layout = \
            html.Div(
                children=[
                    dcc.Graph(
                        id="error-code-graph",
                        figure={
                            "data": [
                                {
                                    "x": df_list[0]["Date"],
                                    "y": df_list[0]["OCCURRENCE"],
                                    "type": "bar",
                                    "hovertemplate": "%{y:.2f}"
                                                     "<extra></extra>",
                                },
                            ],
                            "layout": {
                                "title": {
                                    "text": "Error code 404",
                                    "x": 0.05,
                                    "xanchor": "left",
                                },
                                "xaxis": {"fixedrange": False},
                                "yxaxis": {"fixedrange": False},
                                "colorway": ["#e74c3c"],
                            },
                        },
                    ),
                    dcc.Graph(
                        id="client-connect-graph",
                        figure={
                            "data": [
                                {
                                    "x": df_list[1]["Date"],
                                    "y": df_list[1]["OCCURRENCE"],
                                    "type": "bar",
                                    "hovertemplate": "%{y:.2f}"
                                                     "<extra></extra>",
                                },
                            ],
                            "layout": {
                                "title": {
                                    "text": "Client connections",
                                    "x": 0.05,
                                    "xanchor": "left",
                                },
                                "xaxis": {"fixedrange": False},
                                "yaxis": {"fixedrange": False},

                                "colorway": ["#16a085"],
                            },
                        },
                    ),
                    dcc.Graph(
                        id="sto-usage-graph",
                        figure={
                            "data": [
                                {
                                    "x": df_list[2]["URL"],
                                    "y": df_list[2]["OCCURRENCE"],
                                    "type": "bar",
                                    "hovertemplate": "%{y:.2f}"
                                                     "<extra></extra>",
                                },
                            ],
                            "layout": {
                                "title": {
                                    "text": "URL Request",
                                    "x": 0.05,
                                    "xanchor": "left",
                                },
                                "xaxis": {"fixedrange": False},
                                "yaxis": {"fixedrange": False},

                                "colorway": ["#f39c12"],
                            },
                        },
                    ),
                ],
                className="card",
            )
        return apache_layout

    return html.Div(children=[])


def generate_app_layout(list_layout):
    return html.Div(children=list_layout)

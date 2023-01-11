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


def generate_interval_component():
    interval_layout = html.Div([
        dcc.Interval(
            id='interval-component',
            interval=10000,  # en ms
            n_intervals=0
        )
    ])
    return interval_layout


def generate_hostname_title(hostname, uptime_serverResults, host_id):
    uptime_id = "uptime" + str(host_id)
    hostname_layout = html.Div(children=[
        html.H2(children=hostname, className="hostname"),
        html.H6(children="Uptime : " + str(uptime_serverResults[host_id][0]), className="uptime", id=uptime_id)
    ])
    return hostname_layout


def generate_layout_hardware(hardware_csv_list, cpuModel_server, host_id):
    # HARDWARE USAGE FRAME
    for csv_name in hardware_csv_list:
        df = pd.read_csv(csv_name)

        # Create layout hardware usage
        cpuModel = str(cpuModel_server[host_id][0])
        graph_cpu_id = "cpu-usage-graph" + str(host_id)
        graph_mem_id = "mem-usage-graph" + str(host_id)
        graph_sto_id = "sto-usage-graph" + str(host_id)

        hardware_layout = \
            html.Div(
                children=[
                    dcc.Graph(
                        id=graph_cpu_id,
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
                        id=graph_mem_id,
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
                        id=graph_sto_id,
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
    graph_error_id = "error-code-graph" + str(host_id)
    graph_clientConnect_id = "client-connect-graph" + str(host_id)
    graph_resultURL_id = "requestUrl-graph" + str(host_id)

    if len(df_list) == 3:
        apache_layout = \
            html.Div(
                children=[
                    dcc.Graph(
                        id=graph_error_id,
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
                        id=graph_clientConnect_id,
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
                        id=graph_resultURL_id,
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


def update_hardware_usage(csvName, cpuModel_server):
    figures = []
    df = pd.read_csv(csvName)
    # Create layout hardware usage
    cpuModel = str(cpuModel_server)

    fig_cpu = {
        "data": [
            {
                "x": df["Date"],
                "y": df["CPU_USAGE"],
                "type": "lines",
                "hovertemplate": "%{y:.2f}% %{x}"
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
    }

    figures.append(fig_cpu)

    fig_mem = {
        "data": [
            {
                "x": df["Date"],
                "y": df["MEM_USAGE"],
                "type": "lines",
                "hovertemplate": "%{y:.2f}% %{x}"
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
    }

    figures.append(fig_mem)

    fig_sto = {
        "data": [
            {
                "x": df["Date"],
                "y": df["STO_USAGE"],
                "type": "lines",
                "hovertemplate": "%{y:.2f}% %{x}"
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
    }

    figures.append(fig_sto)

    return figures

def update_apache_log(list_csvname, host_id):

    figures = []

    df_list = []
    for csvApache in list_csvname:
        df_list.append(pd.read_csv(csvApache))

    fig_error = {
        "data": [
         {
             "x": df_list[0]["Date"],
             "y": df_list[0]["OCCURRENCE"],
             "type": "bar",
             "hovertemplate": "%{y} %{x}"
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
    }
    figures.append(fig_error)

    fig_clientConnections = {
         "data": [
             {
                 "x": df_list[1]["Date"],
                 "y": df_list[1]["OCCURRENCE"],
                 "type": "bar",
                 "hovertemplate": "%{y} %{x}"
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
    }

    figures.append(fig_clientConnections)

    fig_requestUrl = {
                 "data": [
                     {
                         "x": df_list[2]["URL"],
                         "y": df_list[2]["OCCURRENCE"],
                         "type": "bar",
                         "hovertemplate": "%{y} %{x}"
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
             }

    figures.append(fig_requestUrl)

    return figures;

def update_uptime(uptime_server):
    children = "Uptime : " + str(uptime_server)
    return children

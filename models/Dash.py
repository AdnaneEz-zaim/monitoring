import dash
from dash import html, dcc
import pandas as pd


# Main app layout
def generate_header_layout():
    home_layout = html.Div(className="header", children=[
        html.H1(className="title-header", children="Group 6 Server Monitoring"),

        html.Div(
            [
                html.Div(
                    dcc.Link(className="pageLink", children=f"{page['name']}", href=page["relative_path"])
                )
                for page in dash.page_registry.values()
            ],
            className="topNav"
        ),
        dash.page_container
    ])
    return home_layout


# Layout page overview
def generate_overview_layout():
    title_layout = html.Div(children=html.H2("Server overview"),
                            className="pageTitle"
                            )
    button_layout = html.Div(html.Button('Refresh', id='refresh-panel-button', n_clicks=0), className="buttonSubmit")
    labelMachineNumber = html.Div(children="", className="machineNumberInfo", id="lblMacNumber")
    server_layout = html.Div(children=[],
                             id="server-overview"
                             )
    final_layout = [title_layout, button_layout, labelMachineNumber, server_layout, generate_interval_component("overview")]
    return generate_app_layout(final_layout, 'overview')


# Children layout of page overview
def generate_serverOverviewPanel(hostname, uptime_serverResults, h):
    uptime_id = "uptime" + str(h)
    panel_layout = html.Div(
        [
            html.H2(hostname),
            html.H6(children="Uptime : " + str(uptime_serverResults[h][0]), className="uptime", id=uptime_id)
        ],
        className="serverPanel"
    )
    return panel_layout

def generate_serverNumberConnection(nbConnection, nbConfigurated):
    lbl_layout = html.Div([
        html.Div(children="Active connection(s) : " + str(nbConnection)),
        html.Div(children="Active configuration(s) : " + str(nbConfigurated))
    ])
    return lbl_layout

# Layout page monitoring
def generate_monitoring_layout():
    title_layout = html.Div(children=html.H2("Server monitoring"),
                            className="pageTitle"
                            )
    button_layout = html.Div(html.Button('Refresh', id='refresh-graph-button', n_clicks=0), className="buttonSubmit")
    monitoring_layout = html.Div(children=[],
                                 id="server-graph"
                                 )

    final_layout = [title_layout, button_layout, monitoring_layout, generate_interval_component("graph")]
    return generate_app_layout(final_layout, 'monitoring')


def generate_configuration_layout():
    title_layout = html.Div(children=html.H2("Add a machine"),
                            className="pageTitle"
                            )
    form_layout = html.Div(children=[
        dcc.Input(id='input-hostname', type='text', placeholder='Enter an hostname', className='InputForm'),
        dcc.Input(id='input-username', type='text', placeholder='Enter an username', className='InputForm'),
        dcc.Input(id='input-password', type='password', placeholder='Enter a password',
                  className='InputForm'),
        dcc.Input(id='input-port', type='text', placeholder='Enter a port', className='InputForm'),
        html.Div(id='output'),
        html.Div(html.Button('Add', id='submit-button', n_clicks=0), className="buttonSubmit")
        ],
        className="Form"
    )
    final_layout = [title_layout, form_layout]
    return generate_app_layout(final_layout, 'configuration')


def generate_interval_component(suffix):
    component_id = 'interval-component-' + suffix
    interval_layout = html.Div([
        dcc.Interval(
            id=component_id,
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


def generate_layout_hardware(hardware_csv, cpuModel_server, host_id):
    # HARDWARE USAGE FRAME

    df = pd.read_csv(hardware_csv)

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


def generate_app_layout(list_layout, divId):
    return html.Div(children=list_layout, id=divId)

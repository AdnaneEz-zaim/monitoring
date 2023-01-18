"""
 Main program
 """
import threading
import time
import dash
from dash.dependencies import Input, Output, State
from models.ConfigurationLoader import Config
from models.Connexion import Connexion
from models.MonitorThreading import MonitorTreading
from models.ApacheServerLogInfo import LogInfo
from models.CSVFiller import fill_csv
from models.ClientManager import ClientManager
import models.Dash as Dashboard
from dash import html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets,
                use_pages=True, suppress_callback_exceptions=True)
app.title = "GROUP 6 Server Monitoring Dashboard"
app.layout = Dashboard.generate_header_layout()

# Init variables
m_machineConfiguration = Config()
m_clientManager = ClientManager()
m_logInfo = []
m_csv_fileNames = []
m_uptime_serverResults = []
m_cpuModel_server = []
outputs_hardwareUsage = []
outputs_apache = []
outputs_uptime = []

# Init
for host in range(m_machineConfiguration.getNbMachineConfigurations()):
    newMonitor = m_machineConfiguration.getMachineConfiguration(host)
    newClient = Connexion(newMonitor)

    if newClient.client is not None:
        m_clientManager.addClient(newMonitor, newClient.client)
        m_logInfo.append(LogInfo())
        m_uptime_serverResults.append("")
        m_cpuModel_server.append("")

        # Create csv file names
        hostname = m_machineConfiguration.getMachineConfiguration(host).hostname
        list_csv = [hostname + suffix + '.csv' for suffix in
                    ["_apacheLog_statusCode404",
                     "_apacheLog_clientConnect",
                     "_apacheLog_requestUrl",
                     "_hardwareUsage"
                     ]
                    ]
        m_csv_fileNames.append(list_csv)


def update_variables():
    global m_machineConfiguration, m_clientManager, m_logInfo, \
        m_csv_fileNames, m_uptime_serverResults, m_cpuModel_server, \
        outputs_hardwareUsage, outputs_apache, outputs_uptime
    """
    Update variables when new configuration is added to config.ini
    """
    m_machineConfiguration = Config()
    m_clientManager = ClientManager()
    m_logInfo = []
    m_csv_fileNames = []
    m_uptime_serverResults = []
    m_cpuModel_server = []
    outputs_hardwareUsage = []
    outputs_apache = []
    outputs_uptime = []

    # Init
    for host in range(m_machineConfiguration.getNbMachineConfigurations()):
        newMonitor = m_machineConfiguration.getMachineConfiguration(host)
        newClient = Connexion(newMonitor)

        if newClient.client is not None:
            m_clientManager.addClient(newMonitor, newClient.client)
            m_logInfo.append(LogInfo())
            m_uptime_serverResults.append("")
            m_cpuModel_server.append("")

            # Create csv file names
            hostname = m_machineConfiguration.getMachineConfiguration(host).hostname
            list_csv = [hostname + suffix + '.csv' for suffix in
                        ["_apacheLog_statusCode404",
                         "_apacheLog_clientConnect",
                         "_apacheLog_requestUrl",
                         "_hardwareUsage"
                         ]
                        ]
            m_csv_fileNames.append(list_csv)


def get_data():
    """ gather data from data scrapper threads"""
    while True:
        global m_machineConfiguration
        global m_clientManager
        # Starting one thread for each client connected

        MonitorThreads = []
        for host in range(m_clientManager.getNbConnectedClient()):
            t = MonitorTreading(m_clientManager.getClientById(host), host, m_logInfo[host])
            t.start()
            MonitorThreads.append(t)

        hardwareUsageResults = []
        apache_statusCode_results = []
        apache_clientConnect_results = []
        apache_requestUrl_results = []

        # Get result from thread when they have finish their tasks
        hostid = 0
        for t in MonitorThreads:
            t.join()

            # Get Monitoring hardware usage results
            hardwareUsageResults.append(t.hardwareUsage_result)

            m_uptime_serverResults[hostid] = t.uptime_result
            m_cpuModel_server[hostid] = t.CPU_name_result

            # Get monitoring apache log results
            apache_statusCode_results.append(t.apache_statusCode_result)
            apache_clientConnect_results.append(t.apache_clientConnect_result)
            apache_requestUrl_results.append(t.apache_requestUrl_result)

            print("-[BACKEND]-DATA SCRAPPING DONE")
            # CSV Filling

            fill_csv(m_csv_fileNames[hostid][0], apache_statusCode_results, hostid)
            fill_csv(m_csv_fileNames[hostid][1], apache_clientConnect_results, hostid)
            fill_csv(m_csv_fileNames[hostid][2], apache_requestUrl_results, hostid)
            fill_csv(m_csv_fileNames[hostid][3], hardwareUsageResults, hostid)

            hostid = hostid + 1

            print("-[BACKEND]-CSV FILLING DONE")

        time.sleep(5)


# Init the data scrapper thread
dataScrapperThread = threading.Thread(target=get_data)
# Start the data scrapper thread
dataScrapperThread.start()


@app.callback(
    Output('server-graph', 'children'),
    [
        Input('refresh-graph-button', 'n_clicks'),
        Input('interval-component-graph', 'n_intervals')
    ],
    State('server-graph', 'children')
)
def display_graphServerMonitoring(n_clicks, n_intervals, children):
    print("ADD GRAPH MONITORING")

    children = []
    for host in range(m_clientManager.getNbConnectedClient()):
        host_name = m_clientManager.getMachineConfiguration(host).hostname
        # Title
        new_titleHostname = Dashboard.generate_hostname_title(
            host_name,
            m_uptime_serverResults,
            host)
        # Hardware graph
        new_graphHardware = Dashboard.generate_layout_hardware(
            m_csv_fileNames[host][3],
            m_cpuModel_server,
            host)

        # Apache Graph

        filtered_csv_list = [s for s in m_csv_fileNames[host] if s.startswith(host_name)]
        apache_csv_list = [csvName for csvName in filtered_csv_list if "apache" in csvName]
        new_graphApache = Dashboard.generate_layout_apache(apache_csv_list, host)

        # Append Childrens
        children.append(new_titleHostname)
        children.append(new_graphHardware)
        children.append(new_graphApache)

    return children


@app.callback(
    Output('server-overview', 'children'),
    [
        Input('refresh-panel-button', 'n_clicks'),
    ],
    State('server-overview', 'children')
)
def display_panelServerOverview(n_clicks, n_intervals):
    print("ADD PANELS OVERVIEW")

    children = []
    for host in range(m_clientManager.getNbConnectedClient()):
        host_name = m_clientManager.getMachineConfiguration(host).hostname
        new_panel = Dashboard.generate_serverOverviewPanel(
            host_name,
            m_uptime_serverResults,
            host)
        children.append(new_panel)

    return children


@app.callback(
    Output('lblMacNumber', 'children'),
    [
        Input('refresh-panel-button', 'n_clicks'),
        Input('interval-component-overview', 'n_intervals')
    ]
)
def update_lblMacConnectionConfiguration(n_clicks, n_intervals):
    children = Dashboard.generate_serverNumberConnection(
        m_clientManager.getNbConnectedClient(),
        m_machineConfiguration.getNbMachineConfigurations()
    )
    return children


@app.callback(Output('output', 'children'),
              [
                  Input('submit-button', 'n_clicks'),
                  Input('input-hostname', 'value'),
                  Input('input-username', 'value'),
                  Input('input-password', 'value'),
                  Input('input-port', 'value')
              ]
              )
def get_input_value(n_clicks, inputHostname, inputUsername, inputPassword, inputPort):
    if n_clicks == 0:
        return ''

    m_machineConfiguration.setMachineConfiguration(
        inputHostname,
        inputUsername,
        inputPassword,
        inputPort)
    update_variables()
    return html.Div('''New configuration will be visible in few seconds ...''')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)

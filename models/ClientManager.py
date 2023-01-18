class ClientManager:
    def __init__(self):
        self.clients = []
        self.monitors = []
        self.nbConnectedClient = 0

    def addClient(self, newMonitor, newClient):
        self.monitors.append(newMonitor)
        self.clients.append(newClient)
        self.nbConnectedClient = self.nbConnectedClient + 1

    def getNbConnectedClient(self):
        return self.nbConnectedClient

    def getClientById(self, client_id):
        return self.clients[client_id]

    def getMachineConfiguration(self, machine_id):
        """method that return all the authentication credential associated to the given client id"""
        print("GET MONITOR INFO OF THE CLIENT " + str(machine_id))

        # Return the monitor
        return self.monitors[machine_id]
import lvgl as lv
from libs.ffishell import runShellCommand


def getLastLine(text):
    lines = text.split("\n")
    lastline = lines[len(lines) - 1]
    return lastline



class WifiShellParser():
    scanResults = []
    scanTimer = ""
    scanStarted = False
    scanResultCheckInterval = 3 * 1000
    scanMaximumTries = 3
    scanTries = 0
    scanCallback = None

    networks = []
    interfaces = []
    currentInterface = "wlan0"
    connected = False

    def __init__(self):
        self.getInterfaces()
        self.setInterface()
        self.getAllNetworks()
        self.isConnected()
        pass

    def getInterfaces(self):
        ret = runShellCommand("wpa_cli interface")
        lines = ret.split("\n")
        for i in range(2, len(lines)):
            self.interfaces.append(lines[i])

    def setInterface(self):
        self.currentInterface = self.interfaces[len(self.interfaces) - 1]
        print("interface set to: " + self.currentInterface)

    def scan(self):
        if self.scanStarted == False:
            ret = runShellCommand("wpa_cli -i " + self.currentInterface + " scan")
            self.scanTimer = lv.timer_create(self.scanTimer, self.scanResultCheckInterval, None)
            self.scanStarted = True
            self.scanTries = 0

    def stopScan(self):
        self.scanTimer._del()
        self.scanStarted = False

    def scanTimer(self, timer):
        self.scanTries += 1
        if self.scanTries < self.scanMaximumTries:
            scanResultsUnparsed = runShellCommand("wpa_cli -i " + self.currentInterface + " scan_results")
            self.parseScanResults(scanResultsUnparsed)
        else:
            self.stopScan()

    def parseScanResults(self, unparsedResults):
        lines = unparsedResults.split("\n")
        parsed = []
        for i in range(2, len(lines) - 1):
            wifiEntry = lines[i].split("\t")
            if len(wifiEntry) == 5:
                wifiEntry = {
                    "bssid": wifiEntry[0],
                    "frequency": wifiEntry[1],
                    "signal": wifiEntry[2],
                    "flags": wifiEntry[3],
                    "ssid": wifiEntry[4],
                }
                parsed.append(wifiEntry)

        self.scanResults = parsed
        if self.scanCallback:
            self.scanCallback(parsed)

    def getAllNetworks(self):
        ret = runShellCommand("wpa_cli -i " + self.currentInterface + " list_networks")


    def isNetworkConfigured(self, networkId):
        ret = runShellCommand("wpa_cli -i " + self.currentInterface + " get_network " + str(networkId) + " ssid")
        ret = getLastLine(ret)
        if(ret == "FAIL"):
            print("network not configured")
            return False
        else:
            print("network is configured")
            return ret

    def addNetwork(self):
        ret = runShellCommand("wpa_cli -i " + self.currentInterface + " add_network")
        ret = getLastLine(ret)
        return ret

    def removeNetwork(self, networkId):
        ret = runShellCommand("wpa_cli -i " + self.currentInterface + " remove_network " + str(networkId))
        ret = getLastLine(ret)
        if(ret == "OK"):
            return True
        return False

    def connect(self, ssid, psk):
        networkId = self.addNetwork()
        print("networkId: " + networkId)
        self.configNetwork(networkId, ssid, psk)

    def configNetwork(self, networkId, ssid, psk):
        print(networkId, ssid, psk)
        ret = runShellCommand("wpa_cli -i " + self.currentInterface + " set_network " + networkId + \
                              " ssid '\"" + ssid + "\"'")
        ret = getLastLine(ret)
        if(ret != "OK"):
            print("Error: set ssid " + ret)
            return False

        ret = runShellCommand("wpa_cli -i " + self.currentInterface + " set_network " + networkId + \
                              " psk '\"" + psk + "\"'")
        ret = getLastLine(ret)
        if(ret != "OK"):
            print("Error: set psk " + ret)
            return False

        ret = runShellCommand("wpa_cli -i " + self.currentInterface + " enable_network " + networkId)
        ret = getLastLine(ret)

        if(ret != "OK"):
            print("Error: enable network " + ret)
            return False

        ret = runShellCommand("wpa_cli -i " + self.currentInterface + " save_conf")
        ret = getLastLine(ret)

        if(ret != "OK"):
            print("Error: save_conf " + ret)
            return False

    def isConnected(self):
        ret = runShellCommand("wpa_cli -i " + self.currentInterface + " status")

        if(ret.find("wpa_state=COMPLETED") == 0):
            self.connected = True
            return True
        self.connected = False
        return False

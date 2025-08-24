import lvgl as lv
from libs.ffishell import runShellCommand


def getLastLine(text):
    lines = text.split("\n")
    lastline = lines[len(lines) - 1]
    return lastline



class WifiShellParser():
    networks = []
    interfaces = []
    currentInterface = "wlp7s0"
    connected = False
    connectedAP = ""

    def __init__(self):
        self.enableWifi()
        self.readNetworks()
        pass

    def enableWifi(self):
        ret = runShellCommand("rfkill unblock wifi")
        pass

    def getInterfaces(self):
        ret = runShellCommand("nmcli dev")
        lines = ret.split("\n")
        for i in range(2, len(lines)):
            self.interfaces.append(lines[i])

    def getNetworks(self):
        self.readNetworks()
        return self.networks

    def scan(self):
        ret = runShellCommand("nmcli device wifi rescan&")

    def readNetworks(self):
        scanResultsUnparsed = runShellCommand("nmcli dev wifi list --rescan no")
        self.parseScanResults(scanResultsUnparsed)

    def parseScanResults(self, unparsedResults):
        lines = unparsedResults.split("\n")
        self.networks = []

        for i in range(1, len(lines)):
            wifiEntry = lines[i].strip().split("  ")
            wifiEntry = list(filter(None, wifiEntry))

            if(len(wifiEntry) == 9):
                wifiEntry = {
                    "in-use": True,
                    "bssid": wifiEntry[1],
                    "ssid": wifiEntry[2],
                    "mode": wifiEntry[3],
                    "chan": wifiEntry[4],
                    "rate": wifiEntry[5],
                    "signal": wifiEntry[6],
                    "bars": wifiEntry[7],
                    "security": wifiEntry[8],
                }
            elif(len(wifiEntry) == 8):
                wifiEntry = {
                    "in-use": False,
                    "bssid": wifiEntry[0],
                    "ssid": wifiEntry[1],
                    "mode": wifiEntry[2],
                    "chan": wifiEntry[3],
                    "rate": wifiEntry[4],
                    "signal": wifiEntry[5],
                    "bars": wifiEntry[6],
                    "security": wifiEntry[7],
                }
            self.networks.append(wifiEntry)
        self.isConnected()

    def getAllWifiAP(self):
        ret = runShellCommand("nmcli dev wifi list")
        print(ret)

    def connect(self, ssid, psk):
        print("connection to ssid: " + ssid)

        if(ssid == self.connectedAP):
            # already connected to same AP
            return True
        
        ret = runShellCommand("nmcli device wifi connect " + ssid + " password " + psk)
        self.readNetworks()

        if(ssid == self.connectedAP):
            return True
        return False
        

    def isConnected(self):
        for i in range(len(self.networks)):
            network = self.networks[i]
            if(network["in-use"] == True):
                self.connected = True
                self.connectedAP = network["ssid"]
                print(self.connectedAP)
        return False

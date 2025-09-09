import lvgl as lv
from libs.ffishell import runShellCommand


def getLastLine(text):
    lines = text.split("\n")
    lastline = lines[len(lines) - 1]
    return lastline



class WifiManager():
    networks = []
    interfaces = []
    currentInterface = "wlp7s0"
    connected = False
    connectedAP = ""
    IPAddress = ""

    timer = ""
    

    def __init__(self):
        self.readNetworks()
        self.timer = lv.timer_create(self.isConnected, 5000, None)


    def enableWifi(self):
        print("wifi enabled")
        ret = runShellCommand("nmcli radio wifi on")
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
        self.enableWifi()
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
        #self.isConnected()

    def getAllWifiAP(self):
        ret = runShellCommand("nmcli dev wifi list")
        print(ret)

    def connect(self, ssid, psk):
        print("connection to ssid: " + ssid)
        if(ssid == self.connectedAP):
            # already connected to same AP
            return True

        runShellCommand("nmcli connection delete " + ssid)        
        runShellCommand("nmcli device wifi connect " + ssid + " password " + psk + " &")
        self.readNetworks()
        
    def isConnected(self, timer):
        self.readNetworks()
        for i in range(len(self.networks)):
            network = self.networks[i]
            if(network["in-use"] == True):
                self.connected = True
                self.connectedAP = network["ssid"]
                #print(self.connectedAP)
                nmcli = runShellCommand("nmcli -t -f IP4.ADDRESS device show")
                for line in nmcli.splitlines():
                    if line.startswith("IP4.ADDRESS"):
                        ip = line.split(":")[1].split("/")[0]
                        #print("found IP:", ip)
                        if not ip.startswith("127.0.0.1") and not ip.startswith("172"):
                            self.IPAddress = ip
                            self.timer.pause()
                            break
        return False

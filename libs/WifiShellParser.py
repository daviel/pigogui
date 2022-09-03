import lvgl as lv
from libs.ffishell import runShellCommand


class WifiShellParser():
    scanResults = []
    scanTimer = ""
    scanStarted = False
    scanResultCheckInterval = 3 * 1000
    scanMaximumTries = 5
    scanTries = 0
    scanCallback = None


    def __init__(self):
        pass

    def scan(self):
        if self.scanStarted == False:
            ret = runShellCommand("sudo wpa_cli scan")
            self.scanTimer = lv.timer_create(self.scanTimer, self.scanResultCheckInterval, None)
            self.scanStarted = True
            self.scanTries = 0

    def stopScan(self):
        self.scanTimer._del()
        self.scanStarted = False

    def scanTimer(self, timer):
        self.scanTries += 1
        if self.scanTries < self.scanMaximumTries:
            scanResultsUnparsed = runShellCommand("sudo wpa_cli scan_results")
            self.parseScanResults(scanResultsUnparsed)
        else:
            self.stopScan()

    def parseScanResults(self, unparsedResults):
        lines = unparsedResults.split("\n")
        parsed = []
        for i in range(2, len(lines) - 1):
            wifiEntry = lines[i].split("\t")
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
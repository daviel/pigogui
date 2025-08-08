from libs.libcurl import *
from libs.Helper import longByteToInteger
from libs.GenericManager import GenericManager

class Download():
    filename = ""
    url = ""
    fileHandle = None
    curl_handle = None

    download_started = False
    info = {
        CURLINFO_SIZE_DOWNLOAD_T: 0,
        CURLINFO_TOTAL_TIME: 0,
        CURLINFO_SPEED_DOWNLOAD_T: 0,
        CURLINFO_CONTENT_LENGTH_DOWNLOAD_T : 0,
    }

    def __init__(self, filename, url):
        self.filename = filename
        self.url = url
        self.fileHandle = fopen(filename, "wb")

        self.curl_handle = curl_easy_init()
        curl_easy_setopt(self.curl_handle, CURLOPT_URL, url)
        #curl_easy_setopt(self.curl_handle, CURLOPT_VERBOSE, 1)
        curl_easy_setopt(self.curl_handle, CURLOPT_NOPROGRESS, 1)
        curl_easy_setopt(self.curl_handle, CURLOPT_WRITEFUNCTION, write_callback)
        curl_easy_setopt(self.curl_handle, CURLOPT_WRITEDATA, self.fileHandle)

    def start_download(self):
        if self.download_started == False:
            curl_easy_perform(self.curl_handle)
            self.download_started = True

    def destroy(self):
        curl_easy_cleanup(self.curl_handle)
        fclose(self.fileHandle)

    def update(self):
        for stat in self.info:
            long = b'0' * 4
            long = curl_easy_getinfo(self.curl_handle, stat, long)
            self.info[stat] = longByteToInteger(long)
        pass


class DownloadManager(GenericManager):
    multi_handle = None
    downloads = {}
    still_running = b'1' * 4
    downloading = False

    def __init__(self, singletons):
        self.setSingletons(singletons)
        curl_global_init(CURL_GLOBAL_ALL)
        self.multi_handle = curl_multi_init()
        pass

    def update(self):
        if self.downloading == True:
            mc = curl_multi_perform(self.multi_handle, self.still_running)
            for dl in self.downloads:
                dl.update()
            if(mc):
                self.downloading = False

    def destroy(self):
        for dl in self.downloads:
            dl.destroy()
        curl_global_cleanup()
        self.downloads = {}

    def start_downloading(self):
        self.downloading = True
        pass

    def add_download(self, filename, url):
        download = Download(filename, url)
        curl_multi_add_handle(self.multi_handle, download.curl_handle)
        self.downloads[filename] = download
        pass

    def abort_download(self, filename):
        download = self.downloads[filename]
        download.destroy()
        curl_multi_remove_handle(self.multi_handle, download.curl_handle)
        self.downloads.pop(filename)
        pass

    def get_progress_of_download(self, filename):
        pass

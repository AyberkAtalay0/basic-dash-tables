import requests, subprocess
from threading import Thread
from os import listdir, path

def update_files():
    branch_url = "https://github.com/AyberkAtalay0/basic-dash-tables/blob/main"
    files = []
    
    app_req = requests.get(branch_url+"/app.py")
    for f1 in app_req.json()["payload"]["fileTree"][""]["items"]:
        if f1["contentType"].lower().strip() == "directory":
            directory1_url = branch_url+"/"+f1["path"].replace(" ", "%20")
            for f2 in requests.get(directory1_url).json()["payload"]["tree"]["items"]:
                if f2["contentType"].lower().strip() == "directory":
                    directory2_url = branch_url+"/"+f2["path"].replace(" ", "%20")
                    for f3 in requests.get(directory2_url).json()["payload"]["tree"]["items"]:
                        if f3["contentType"].lower().strip() == "directory": pass
                        else: files.append("/"+f3["path"])
                else: files.append("/"+f2["path"])
        else: files.append("/"+f1["path"])
    return files

import sys
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtWebEngineWidgets import *

class WorkerThread(QThread):
    def run(self):
        subprocess.run(["python", path.join("app.py")])
        # with open(path.join("app.py"), "r", encoding="utf-8") as afr:
        #     exec(afr.read())

class WebBrowser(QMainWindow):
    def __init__(self):
        super().__init__()

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("http://127.0.0.1:8547/"))
        self.setCentralWidget(self.browser)

        self.worker_thread = WorkerThread()
        self.worker_thread.start()

if __name__ == "__main__":
    qtapp = QApplication(sys.argv)
    QCoreApplication.setApplicationName("MHAL Deneme Panel")
    window = WebBrowser()
    window.show()
    qtapp.exec()

import requests, subprocess
from os import listdir, path, walk

def update_files():
    branch_url = "https://github.com/AyberkAtalay0/basic-dash-tables/blob/main"
    nfiles, xfiles = [], []
    
    app_req = requests.get(branch_url+"/app.py")
    for f1 in app_req.json()["payload"]["fileTree"][""]["items"]:
        if f1["contentType"].lower().strip() == "directory":
            directory1_url = branch_url+"/"+f1["path"].replace(" ", "%20")
            for f2 in requests.get(directory1_url).json()["payload"]["tree"]["items"]:
                if f2["contentType"].lower().strip() == "directory":
                    directory2_url = branch_url+"/"+f2["path"].replace(" ", "%20")
                    for f3 in requests.get(directory2_url).json()["payload"]["tree"]["items"]:
                        if f3["contentType"].lower().strip() == "directory": pass
                        else: xfiles.append("\\"+f3["path"].replace("/", "\\"))
                else: xfiles.append("\\"+f2["path"].replace("/", "\\"))
        else: xfiles.append("\\"+f1["path"].replace("/", "\\"))

    for root, dirs, files in walk("."):
    	for fn in files: 
    		if not fn.endswith(".pyc"): nfiles.append(path.join(root, fn).removeprefix("."))

    for n in nfiles:
        print(n, n in xfiles)

    print(xfiles)

    return nfiles, xfiles

import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from pyqt_frameless_window import FramelessMainWindow

class WorkerThread(QThread):
    def run(self):
        subprocess.run(["python", path.join("app.py")])
        # with open(path.join("app.py"), "r", encoding="utf-8") as afr:
        #     exec(afr.read())

class ExtraThread(QThread):
    def run(self):
        pass
        # with open(path.join("app.py"), "r", encoding="utf-8") as afr:
        #     exec(afr.read())

class WebBrowser(FramelessMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MHAL Deneme Panel")
        # self.setWindowIcon('./Stark-icon.png')
        

        #.setAttribute(Qt.Qt.WA_StyledBackground, True)
        self.setStyleSheet('background-color: #25262B;')

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("http://127.0.0.1:8547/"))

        mainWidget = self.centralWidget()
        lay = mainWidget.layout()
        lay.addWidget(self.browser)
        mainWidget.setLayout(lay)
        self.setCentralWidget(mainWidget)

        self.worker_thread = WorkerThread()
        self.worker_thread.start()

if __name__ == "__main__":
    update_files()
    
    qtapp = QApplication(sys.argv)
    window = WebBrowser()
    window.show()
    qtapp.exec()

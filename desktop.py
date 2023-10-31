import requests

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

class WebBrowser(QMainWindow):
    def __init__(self):
        super().__init__()

        # Web tarayıcı penceresi oluştur
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://www.google.com"))
        self.browser.page().profile().downloadRequested.connect(self.downloadRequested)
        self.setCentralWidget(self.browser)

        # Menü çubuğunu ayarla
        navbar = QToolBar()
        self.addToolBar(navbar)

        # Geri düğmesi
        back_btn = QAction("Geri", self)
        back_btn.setStatusTip("Geri")
        back_btn.triggered.connect(self.browser.back)
        navbar.addAction(back_btn)

        # İleri düğmesi
        forward_btn = QAction("İleri", self)
        forward_btn.setStatusTip("İleri")
        forward_btn.triggered.connect(self.browser.forward)
        navbar.addAction(forward_btn)

        # Yenile düğmesi
        reload_btn = QAction("Yenile", self)
        reload_btn.setStatusTip("Yenile")
        reload_btn.triggered.connect(self.browser.reload)
        navbar.addAction(reload_btn)

        # Ana sayfa düğmesi
        home_btn = QAction("Ana Sayfa", self)
        home_btn.setStatusTip("Ana Sayfa")
        home_btn.triggered.connect(self.navigate_home)
        navbar.addAction(home_btn)

        # URL çubuğu
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)

        # Arama düğmesi
        search_btn = QAction("Ara", self)
        search_btn.setStatusTip("Ara")
        search_btn.triggered.connect(self.navigate_to_url)
        navbar.addAction(search_btn)

        # Sayfa yüklenirken URL'yi güncelle
        self.browser.urlChanged.connect(self.update_urlbar)

    def navigate_home(self):
        self.browser.setUrl(QUrl("https://www.google.com"))

    def navigate_to_url(self):
        q = QUrl(self.url_bar.text())
        if q.scheme() == "":
            q.setScheme("http")

        self.browser.setUrl(q)

    def update_urlbar(self, q):
        self.url_bar.setText(q.toString())
        self.url_bar.setCursorPosition(0)

    def downloadRequested(self, downloadItem):
        # İndirme isteğini kabul etmek veya reddetmek için kullanabilirsiniz
        # downloadItem.accept()
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    QCoreApplication.setApplicationName("Web Tarayıcı")
    window = WebBrowser()
    window.show()
    app.exec()

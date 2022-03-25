from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QMainWindow,
    QPushButton,
    QLineEdit,
    QLabel,
    QMessageBox,
)
from PyQt5.Qt import QUrl, QDesktopServices
import requests
import sys
import webbrowser
from hashlib import new
from os import system
from tokenize import String

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Locate your IP : (OUM)")
        self.setFixedSize(400, 400)
        self.label1 = QLabel("Enter your IP:", self)
        self.text = QLineEdit(self)
        self.text.setText(self.get_ip())
        self.label1.move(10,25)
        self.text.move(10, 50)
        
        self.label3 = QLabel("Enter your Key:", self)
        self.text3 = QLineEdit(self)
        self.label3.move(10,80)
        self.text3.move(10,105)

        self.label2 = QLabel("Answer:", self)
        self.label2.move(10, 150)
        self.button = QPushButton("Send", self)
        self.button.move(10, 210)

        self.button.pressed.connect(self.on_click)

        self.show()


    def get_ip(self):
        url="https://api64.ipify.org?format=json"
        res = self.__query(url)
        if res:
            return res['ip']
        else:
            return ""

    def on_click(self):
        hostname = self.text.text()
        key = self.text3.text()
        res = self.__query("http://127.0.0.1:8000/ip/"+hostname+"?key="+key)
        if res and type(res)==dict:
            lat=str(res["latitude"])
            long=str(res["longitude"])
            self.label2.setText("latitude="+lat+"\nlongitude="+long)
            self.label2.adjustSize()
            self.show()
            webbrowser.open(url="https://www.openstreetmap.org/?mlat="+lat+"&mlon="+long+"#map=12",new=0)

    def __query(self, url):
        try:
            r = requests.get(url,timeout=3)
            if r.status_code == requests.codes.NOT_FOUND:
                QMessageBox.about(self, "Error", "IP not found")
            if r.status_code == requests.codes.OK:
                return r.json()
        except:
            return None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = MainWindow()

    app.exec_()

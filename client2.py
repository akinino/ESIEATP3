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
        #Creation Interface de la Window#
        #Donne la taille de la Window"
        self.setWindowTitle("Locate your IP : (OUM)")
        self.setFixedSize(400, 400)
        #Creation d'un label et d'une zone d'input"
        self.label1 = QLabel("Enter your IP:", self)
        self.text = QLineEdit(self)
        self.text.setText(self.get_ip())
        #On bouge le label et la zone d'input a l'endroit voulue#
        self.label1.move(10,25)
        self.text.move(10, 50)
        
        self.label3 = QLabel("Enter your Key:", self)
        self.text3 = QLineEdit(self)
        self.label3.move(10,80)
        self.text3.move(10,105)

        self.label4 = QLabel("Enter the Hostname:", self)
        self.text4 = QLineEdit(self)
        self.label4.move(10,130)
        self.text4.move(10,150)

        self.label2 = QLabel("Answer:", self)
        self.label2.move(10, 200)
        self.button = QPushButton("Send", self)
        self.button.move(10, 250)

        #quand on appuie sur le bouton on lance la fonction on_click#
        self.button.pressed.connect(self.on_click)
        self.show()


    def get_ip(self):
        #recupere l'adresse ip
        url="https://api64.ipify.org?format=json"
        res = self.__query(url)
        if res:
            return res['ip']
        else:
            return ""

    def on_click(self):
        #on recupere les value des inputs#
        hostname = self.text.text()
        key = self.text3.text()
        hostip = self.text4.text()
        #on les rentre dans le lien http#
        res = self.__query("http://"+hostip+"/ip/"+hostname+"?key="+key)
        if res and type(res)==dict:
            #on recupere la latitude et la longitude#
            lat=str(res["latitude"])
            long=str(res["longitude"])
            #on ecrit la latitude et la longitude dans la window#
            self.label2.setText("latitude="+lat+"\nlongitude="+long)
            self.label2.adjustSize()
            self.show()
            #on ouvre une page web a la latitude et longitude recuperé#
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
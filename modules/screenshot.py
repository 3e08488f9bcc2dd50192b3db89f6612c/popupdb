from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, QUrl, QTimer, QSize
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from modules import Utils
from threading import Thread
import time, hashlib, os
from func_timeout import func_timeout
class Screenshot(QWebEngineView):

    def capture(self, url, output_file):
        self.output_file = output_file
        self.load(QUrl(url))
        self.loadFinished.connect(self.on_loaded)
        # Create hidden view without scrollbars
        self.setAttribute(Qt.WA_DontShowOnScreen)
        self.page().settings().setAttribute(
            QWebEngineSettings.ShowScrollBars, False)
        self.show()

    def on_loaded(self):
        self.resize(QSize(1366,768))
        # Wait for resize
        QTimer.singleShot(7500, self.take_screenshot)

    def take_screenshot(self):
        self.grab().save(self.output_file, b'PNG')
        self.app.quit()
url=[]
def init_screenshooter():
    global qapp, screenshooter
    qapp = QApplication([""])
    screenshooter = Screenshot()
    screenshooter.app = qapp

def shotthread():
    #os.system(r"wkhtmltoimage --enable-javascript --javascript-delay 5000 --width 1080 --height 780 {} files/screenshots/{}.png".format(url, to_domain(url)))
    global qapp, screenshooter, url
    init_screenshooter()
    while True:
        if len(url)==0:
            time.sleep(1)
            continue
        screenshooter.capture(url[0], 'files/screenshots/'+Utils.crc(url[0])+'.png')
        qapp.exec_()
        f=open('files/screenshots/'+Utils.crc(url[0])+'.png',"rb")
        r=f.read()
        f.close()
        if hashlib.sha256(r).hexdigest() == "fc1d0d348570b8f63272705fc6f9465d3fdb432d48c6520deed0363f078c3265":
            try:
                func_timeout(45,os.system, args=("chromium --headless \""+url[0]+"\" --screenshot=files/screenshots/"+Utils.crc(url[0])+".png --virtual-time-budget=10000 --window-size=1920,1080",) )
            except:
                os.system("killall chromium")
        url.pop(0)
def getScreenshot(ur):
    global url
    url.append(ur)
    while ur in url:
        time.sleep(0.5)
def startshotthread():
    
    Thread(target=shotthread).start()

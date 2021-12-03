import sys
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QApplication, QStackedWidget
from pytube import YouTube

class homeScreen(QDialog):
    def __init__(self):
        super(homeScreen, self).__init__()
        loadUi("./main.ui", self)

        self.download_btn.clicked.connect(self.download)

    def download(self):
        link = self.link.text()
        video = YouTube(link)
        stream = video.streams.get_by_itag(22)
        stream.download()
        self.console.setText("Успешно!")
        self.link.setText("")

app = QApplication(sys.argv)
home = homeScreen()
widget = QStackedWidget()
widget.addWidget(home)
widget.setFixedHeight(400)
widget.setFixedWidth(700)
widget.show()

try:
    sys.exit(app.exec_())
except:
    print("Ожидание")
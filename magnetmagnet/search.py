import threading
from threading import Thread

import pyperclip
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import src.mglobals
from src import searched_success_message
from src.torrent_site.kat import search_kat
from src.torrent_site.nyaa import search_nyaa
from src.torrent_site.rarbg import search_rarbg
from src.torrent_site.tpb import search_tpb
from src.torrent_site.x1377 import search_x1377

path = src.mglobals.BASE_PATH


class Ui_searchMainWindow(object):
    def copied_success_message(self):
        successMessageBox = QMessageBox()
        successMessageBox.setIcon(QMessageBox.Information)

        successMessageBox.setText(
            "Magnet links have been successfully copied to the clipboard.")
        successMessageBox.setWindowTitle("Task Completed!")
        successMessageBox.setStandardButtons(QMessageBox.Ok)
        icon = QIcon()
        icon.addPixmap(QPixmap(src.mglobals.icon), QIcon.Normal, QIcon.Off)
        successMessageBox.setWindowIcon(icon)

        successMessageBox.exec_()

    def copy(self):
        choice_row = self.tableTableWidget.currentRow()
        choice_magnet = self.magnets[choice_row]
        pyperclip.copy(choice_magnet)
        self.copied_success_message()

    def callback(self):
        query = self.queryLineEdit.text()
        limit = self.limitSlider.value()

        def resize():
            self.tableTableWidget.resizeColumnToContents(0)
            self.tableTableWidget.resizeColumnToContents(1)
            self.tableTableWidget.resizeColumnToContents(2)
            self.tableTableWidget.resizeColumnToContents(3)
            self.tableTableWidget.resizeColumnToContents(4)

        self.tableTableWidget.setRowCount(0)
        self.magnets = []
        threads = []
        if self.x1377CheckBox.isChecked():
            threads.append(Thread(target=search_x1377, args=(self, query, limit)))

        if self.katCheckBox.isChecked():
            threads.append(Thread(target=search_kat, args=(self, query, limit)))

        if self.nyaaCheckBox.isChecked():
            threads.append(Thread(target=search_nyaa, args=(self, query, limit)))

        if self.rarbgCheckBox.isChecked():
            threads.append(Thread(target=search_rarbg, args=(self, query, limit)))

        if self.tpbCheckBox.isChecked():
            threads.append(Thread(target=search_tpb, args=(self, query, limit)))

        for t in threads:
            t.start()
        for t in threads:
            t.join()

        resize()
        searched_success_message()


    def setupUi(self, searchMainWindow):
        searchMainWindow.setObjectName("searchMainWindow")
        searchMainWindow.resize(1500, 400)
        font = QFont()
        font.setFamily("Bahnschrift Light")
        font.setPointSize(11)
        searchMainWindow.setFont(font)
        icon = QIcon()
        icon.addPixmap(QPixmap(src.mglobals.icon), QIcon.Normal, QIcon.Off)
        searchMainWindow.setWindowIcon(icon)
        self.centralwidget = QWidget(searchMainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.queryLineEdit = QLineEdit(self.centralwidget)
        self.queryLineEdit.setGeometry(QRect(30, 20, 200, 20))
        font = QFont()
        font.setPointSize(9)
        self.queryLineEdit.setFont(font)
        self.queryLineEdit.setObjectName("queryLineEdit")
        self.x1377CheckBox = QCheckBox(self.centralwidget)
        self.x1377CheckBox.setGeometry(QRect(30, 70, 90, 20))
        self.x1377CheckBox.setObjectName("x1377CheckBox")
        self.tableTableWidget = QTableWidget(self.centralwidget)
        self.tableTableWidget.setGeometry(QRect(260, 20, 1161, 360))
        self.tableTableWidget.setObjectName("tableTableWidget")
        self.tableTableWidget.setColumnCount(6)
        self.tableTableWidget.setRowCount(0)
        item = QTableWidgetItem()
        self.tableTableWidget.setHorizontalHeaderItem(0, item)
        item = QTableWidgetItem()
        self.tableTableWidget.setHorizontalHeaderItem(1, item)
        item = QTableWidgetItem()
        self.tableTableWidget.setHorizontalHeaderItem(2, item)
        item = QTableWidgetItem()
        self.tableTableWidget.setHorizontalHeaderItem(3, item)
        item = QTableWidgetItem()
        self.tableTableWidget.setHorizontalHeaderItem(4, item)
        item = QTableWidgetItem()
        self.tableTableWidget.setHorizontalHeaderItem(5, item)
        self.tableTableWidget.setSortingEnabled(True)
        self.katCheckBox = QCheckBox(self.centralwidget)
        self.katCheckBox.setGeometry(QRect(30, 110, 90, 20))
        self.katCheckBox.setObjectName("katCheckBox")
        self.nyaaCheckBox = QCheckBox(self.centralwidget)
        self.nyaaCheckBox.setGeometry(QRect(30, 150, 90, 20))
        self.nyaaCheckBox.setObjectName("nyaaCheckBox")
        self.rarbgCheckBox = QCheckBox(self.centralwidget)
        self.rarbgCheckBox.setGeometry(QRect(30, 190, 90, 20))
        self.rarbgCheckBox.setObjectName("rarbgCheckBox")
        self.tpbCheckBox = QCheckBox(self.centralwidget)
        self.tpbCheckBox.setGeometry(QRect(30, 230, 90, 20))
        self.tpbCheckBox.setObjectName("tpbCheckBox")
        self.searchPushButton = QPushButton(self.centralwidget)
        self.searchPushButton.setGeometry(QRect(30, 350, 90, 30))
        font = QFont()
        font.setPointSize(8)
        self.searchPushButton.setFont(font)
        self.searchPushButton.setObjectName("searchPushButton")
        self.limitSlider = QSlider(self.centralwidget)
        self.limitSlider.setGeometry(QRect(1450, 40, 22, 320))
        self.limitSlider.setMaximum(20)
        self.limitSlider.setPageStep(2)
        self.limitSlider.setSliderPosition(10)
        self.limitSlider.setOrientation(Qt.Vertical)
        self.limitSlider.setObjectName("limitSlider")
        self.minimumLabel = QLabel(self.centralwidget)
        self.minimumLabel.setGeometry(QRect(1452, 365, 16, 16))
        font = QFont()
        font.setPointSize(9)
        self.minimumLabel.setFont(font)
        self.minimumLabel.setAlignment(Qt.AlignCenter)
        self.minimumLabel.setObjectName("minimumLabel")
        self.maximumLabel = QLabel(self.centralwidget)
        self.maximumLabel.setGeometry(QRect(1452, 20, 16, 16))
        font = QFont()
        font.setPointSize(9)
        self.maximumLabel.setFont(font)
        self.maximumLabel.setAlignment(Qt.AlignCenter)
        self.maximumLabel.setObjectName("maximumLabel")
        searchMainWindow.setCentralWidget(self.centralwidget)

        self.searchPushButton.clicked.connect(self.callback)
        self.tableTableWidget.itemClicked.connect(self.copy)

        self.retranslateUi(searchMainWindow)
        QMetaObject.connectSlotsByName(searchMainWindow)

    def retranslateUi(self, searchMainWindow):
        _translate = QCoreApplication.translate
        searchMainWindow.setWindowTitle(_translate(
            "searchMainWindow", "MagnetMagnet - Search"))
        item = self.tableTableWidget.horizontalHeaderItem(0)
        item.setText(_translate("searchMainWindow", "Titles"))
        item = self.tableTableWidget.horizontalHeaderItem(1)
        item.setText(_translate("searchMainWindow", "Seeders"))
        item = self.tableTableWidget.horizontalHeaderItem(2)
        item.setText(_translate("searchMainWindow", "Leechers"))
        item = self.tableTableWidget.horizontalHeaderItem(3)
        item.setText(_translate("searchMainWindow", "Sizes"))
        item = self.tableTableWidget.horizontalHeaderItem(4)
        item.setText(_translate("searchMainWindow", "Dates"))
        item = self.tableTableWidget.horizontalHeaderItem(5)
        item.setText(_translate("searchMainWindow", "Source"))

        self.x1377CheckBox.setText(_translate("searchMainWindow", "1377x"))
        self.x1377CheckBox.setChecked(True)

        self.katCheckBox.setText(_translate("searchMainWindow", "KAT"))
        self.katCheckBox.setChecked(True)

        self.nyaaCheckBox.setText(_translate("searchMainWindow", "Nyaa"))
        self.nyaaCheckBox.setChecked(True)

        self.rarbgCheckBox.setText(_translate("searchMainWindow", "RARBG"))
        self.rarbgCheckBox.setChecked(True)

        self.tpbCheckBox.setText(_translate("searchMainWindow", "TPB"))
        self.tpbCheckBox.setChecked(True)

        self.searchPushButton.setText(_translate("searchMainWindow", "Search"))
        self.minimumLabel.setText(_translate("searchMainWindow", "0"))
        self.maximumLabel.setText(_translate("searchMainWindow", "20"))

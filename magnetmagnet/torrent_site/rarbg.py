import math
import os
import re
import time

import requests
from bs4 import BeautifulSoup
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from src.mglobals import USER_AGENT, BASE_PATH
from src import error_message, mglobals

path = BASE_PATH


def search_rarbg(self, query, limit):
    try:
        token_url = "https://torrentapi.org/pubapi_v2.php?get_token=get_token&app_id=MagnetMagnet"
        token_request = requests.get(token_url, headers={'User-Agent': 'Mozilla/5.0'})
        token = token_request.json()["token"]
        main_link = 'https://torrentapi.org/pubapi_v2.php?mode=search&search_string=' + \
                    query + '&token=' + token + '&format=json_extended&app_id=MagnetMagnet'
        main_request = requests.get(
                main_link, headers={'User-Agent': USER_AGENT})

        json_source = main_request.json()
        if "torrent_results" not in json_source:
            return

        main_source = main_request.json()["torrent_results"]

        limit_counter = 0
        titles = []
        seeders = []
        leechers = []
        sizes = []
        dates = []
        for item in main_source:
            if limit_counter < limit:
                def convert_size(size):
                    if size == 0:
                        return "0B"
                    size_name = ("B", "KB", "MB", "GB",
                                 "TB", "PB", "EB", "ZB", "YB")
                    i = int(math.floor(math.log(size, 1024)))
                    p = math.pow(1024, i)
                    s = round(size / p, 2)
                    size = "%s %s" % (s, size_name[i])
                    return size

                titles.append(item["title"])
                seeders.append(item["seeders"])
                leechers.append(item["leechers"])
                sizes.append(convert_size(item["size"]))
                dates.append(item["pubdate"])
                self.magnets.append(item["download"])
                limit_counter += 1
            else:
                pass
        # print(titles)

        count2 = 0
        while count2 < limit_counter:
            row_position = self.tableTableWidget.rowCount()
            self.tableTableWidget.insertRow(row_position)
            self.tableTableWidget.setItem(
                    row_position, 0, QTableWidgetItem(titles[count2]))
            item = QTableWidgetItem()
            item.setData(Qt.DisplayRole, int(seeders[count2]))
            self.tableTableWidget.setItem(row_position, 1, item)
            item = QTableWidgetItem()
            item.setData(Qt.DisplayRole, int(leechers[count2]))
            self.tableTableWidget.setItem(row_position, 2, item)
            self.tableTableWidget.setItem(
                    row_position, 3, QTableWidgetItem(sizes[count2]))
            self.tableTableWidget.setItem(
                    row_position, 4, QTableWidgetItem(dates[count2]))
            self.tableTableWidget.setItem(
                    row_position, 5, QTableWidgetItem("RARBG"))
            count2 = count2 + 1
    except Exception as e:
        error_message(str(e))


class Ui_rarbgMainWindow(object):
    def callback(self):
        def exported_sucess_message():
            successMessageBox = QMessageBox()
            successMessageBox.setIcon(QMessageBox.Information)

            successMessageBox.setText(
                "Magnet links have been successfully exported to the local directory.")
            successMessageBox.setWindowTitle("Task Completed!")
            successMessageBox.setStandardButtons(QMessageBox.Ok)
            icon = QIcon()
            icon.addPixmap(QPixmap(mglobals.icon), QIcon.Normal, QIcon.Off)
            successMessageBox.setWindowIcon(icon)

            successMessageBox.exec_()

        def error_message():
            errorMessageBox = QMessageBox()
            errorMessageBox.setIcon(QMessageBox.Information)

            errorMessageBox.setText(
                "Something went wrong! Please inform me through GitHub!")
            errorMessageBox.setWindowTitle("Error!")
            errorMessageBox.setStandardButtons(QMessageBox.Ok)
            icon = QIcon()
            icon.addPixmap(QPixmap(mglobals.icon), QIcon.Normal, QIcon.Off)
            errorMessageBox.setWindowIcon(icon)

            errorMessageBox.exec_()
        try:
            domain = str(self.domainComboBox.currentText())
            category = str(self.categoryComboBox.currentText())

            if category == "All":
                category = ""
            if category == "Movies - All":
                category = "movies"
            if category == "Movies - UHD":
                category = "50;51;52"
            if category == "Movies - HD":
                category = "44;42;46;54"
            if category == "Movies - Not HD":
                category = "14;48;17;45"
            if category == "TV - All":
                category = "2;18;41;49"
            if category == "TV - UHD":
                category = "49"
            if category == "TV - HD":
                category = "41"
            if category == "Music - All":
                category = "2;23;24;25;26"
            if category == "XXX - All":
                category = "2;4"

            link = domain + 'rssdd.php?category=' + category
            request = requests.get(link)
            source = request.content
            soup = BeautifulSoup(source, 'xml')

            magnets = ['==== Made by @eliasbenb ====']
            for item in soup.findAll('item'):
                magnets.append('\n'+item.link.text)

            timestr = time.strftime(" %Y%m%d%H%M%S")
            file_name = "RARBG Results " + timestr + ".txt"
            with open(file_name, 'w') as w1:
                for magnet in magnets:
                    w1.write(magnet)
            exported_sucess_message()
        except:
            error_message()

    def setupUi(self, rarbgMainWindow):
        rarbgMainWindow.setObjectName("rarbgMainWindow")
        rarbgMainWindow.setFixedSize(600, 330)
        font = QFont()
        font.setFamily("Bahnschrift Light")
        rarbgMainWindow.setFont(font)
        icon = QIcon()
        icon.addPixmap(QPixmap(mglobals.icon), QIcon.Normal, QIcon.Off)
        rarbgMainWindow.setWindowIcon(icon)
        self.centralwidget = QWidget(rarbgMainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.domainComboBox = QComboBox(self.centralwidget)
        self.domainComboBox.setGeometry(QRect(150, 60, 300, 22))
        self.domainComboBox.setLayoutDirection(Qt.LeftToRight)
        self.domainComboBox.setObjectName("domainComboBox")
        self.domainComboBox.addItem("")
        self.domainComboBox.addItem("")
        self.domainLabel = QLabel(self.centralwidget)
        self.domainLabel.setGeometry(QRect(200, 30, 200, 16))
        font = QFont()
        font.setPointSize(11)
        self.domainLabel.setFont(font)
        self.domainLabel.setAlignment(Qt.AlignCenter)
        self.domainLabel.setObjectName("domainLabel")
        self.categoryComboBox = QComboBox(self.centralwidget)
        self.categoryComboBox.setGeometry(QRect(150, 180, 300, 22))
        self.categoryComboBox.setObjectName("categoryComboBox")
        self.categoryComboBox.addItem("")
        self.categoryComboBox.addItem("")
        self.categoryComboBox.addItem("")
        self.categoryComboBox.addItem("")
        self.categoryComboBox.addItem("")
        self.categoryComboBox.addItem("")
        self.categoryComboBox.addItem("")
        self.categoryComboBox.addItem("")
        self.categoryComboBox.addItem("")
        self.categoryComboBox.addItem("")
        self.categoryLabel = QLabel(self.centralwidget)
        self.categoryLabel.setGeometry(QRect(200, 150, 200, 16))
        font = QFont()
        font.setPointSize(11)
        self.categoryLabel.setFont(font)
        self.categoryLabel.setAlignment(Qt.AlignCenter)
        self.categoryLabel.setObjectName("categoryLabel")
        self.scrapeButton = QPushButton(self.centralwidget)
        self.scrapeButton.setGeometry(QRect(262, 260, 75, 30))
        self.scrapeButton.setObjectName("scrapeButton")
        rarbgMainWindow.setCentralWidget(self.centralwidget)

        self.scrapeButton.clicked.connect(self.callback)

        self.retranslateUi(rarbgMainWindow)
        QMetaObject.connectSlotsByName(rarbgMainWindow)

    def retranslateUi(self, rarbgMainWindow):
        _translate = QCoreApplication.translate
        rarbgMainWindow.setWindowTitle(_translate(
            "rarbgMainWindow", "MagnetMagnet - RARBG"))
        self.domainComboBox.setItemText(0, _translate(
            "rarbgMainWindow", "https://rarbg.to/"))
        self.domainComboBox.setItemText(1, _translate(
            "rarbgMainWindow", "https://rarbgmirror.com/"))
        self.domainLabel.setText(_translate(
            "rarbgMainWindow", "Choose a RARBG domain:"))
        self.categoryComboBox.setItemText(
            0, _translate("rarbgMainWindow", "All"))
        self.categoryComboBox.setItemText(
            1, _translate("rarbgMainWindow", "Movies - All"))
        self.categoryComboBox.setItemText(
            2, _translate("rarbgMainWindow", "Movies - UHD"))
        self.categoryComboBox.setItemText(
            3, _translate("rarbgMainWindow", "Movies - HD"))
        self.categoryComboBox.setItemText(
            4, _translate("rarbgMainWindow", "Movies - Not HD"))
        self.categoryComboBox.setItemText(
            5, _translate("rarbgMainWindow", "TV - All"))
        self.categoryComboBox.setItemText(
            6, _translate("rarbgMainWindow", "TV - UHD"))
        self.categoryComboBox.setItemText(
            7, _translate("rarbgMainWindow", "TV - HD"))
        self.categoryComboBox.setItemText(
            8, _translate("rarbgMainWindow", "Music - All"))
        self.categoryComboBox.setItemText(
            9, _translate("rarbgMainWindow", "XXX - All"))
        self.categoryLabel.setText(_translate(
            "rarbgMainWindow", "Choose a category:"))
        self.scrapeButton.setText(_translate("rarbgMainWindow", "Scrape"))

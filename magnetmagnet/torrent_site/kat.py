import os
import re
import time

import requests
from bs4 import BeautifulSoup
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import src.mglobals
from src import error_message

path = src.mglobals.BASE_PATH


def search_kat(self, query, limit):
    try:
        main_link = "https://kat.rip/usearch/" + query
        main_request = requests.get(
                main_link, headers={'User-Agent': 'Mozilla/5.0'})
        main_source = main_request.content
        main_soup = BeautifulSoup(main_source, 'lxml')

        titles_soup = main_soup.findAll('a', class_="cellMainLink")
        seeders_soup = main_soup.findAll('td', class_="green center")
        leechers_soup = main_soup.findAll(
                'td', class_="red lasttd center")
        sizes_soup = main_soup.findAll('td', class_="nobr center")
        dates_soup = main_soup.findAll(
                'td', class_="center", title=True)
        magnets_soup = main_soup.findAll(
                'a', attrs={'href': re.compile("^magnet:?"), 'title': "Torrent magnet link"})

        titles = []
        seeders = []
        leechers = []
        sizes = []
        dates = []
        limit_counter = 0
        for title in titles_soup:
            if limit_counter < limit:
                titles.append(title.text)
                limit_counter = limit_counter + 1
        limit_counter = 0
        for seeder in seeders_soup:
            if limit_counter < limit:
                seeders.append(seeder.text)
                limit_counter = limit_counter + 1
        limit_counter = 0
        for leecher in leechers_soup:
            if limit_counter < limit:
                leechers.append(leecher.text)
                limit_counter = limit_counter + 1
        limit_counter = 0
        for size in sizes_soup:
            if limit_counter < limit:
                sizes.append(size.text)
                limit_counter = limit_counter + 1
        limit_counter = 0
        for date in dates_soup:
            if limit_counter < limit:
                dates.append(date.text)
                limit_counter = limit_counter + 1
        limit_counter = 0
        count1 = 0
        for magnet in magnets_soup:
            if limit_counter < limit:
                self.magnets.append(magnet.get('href'))
                limit_counter = limit_counter + 1
                count1 = count1 + 1

        count2 = 0
        while count2 < count1:
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
                    row_position, 5, QTableWidgetItem("KAT"))
            count2 = count2 + 1
    except Exception as e:
        error_message(str(e))


class Ui_katMainWindow(object):
    def callback(self):
        def exported_sucess_message():
            successMessageBox = QMessageBox()
            successMessageBox.setIcon(QMessageBox.Information)

            successMessageBox.setText(
                "Magnet links have been successfully exported to the local directory.")
            successMessageBox.setWindowTitle("Task Completed!")
            successMessageBox.setStandardButtons(QMessageBox.Ok)
            icon = QIcon()
            icon.addPixmap(QPixmap(src.mglobals.icon),
                            QIcon.Normal, QIcon.Off)
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
            icon.addPixmap(QPixmap(src.mglobals.icon),
                            QIcon.Normal, QIcon.Off)
            errorMessageBox.setWindowIcon(icon)

            errorMessageBox.exec_()
        try:
            domain = str(self.domainComboBox.currentText())
            category = str(self.categoryComboBox.currentText())

            if category == "Movies":
                category = "movies"
            if category == "TV":
                category = "tv"
            if category == "Anime":
                category = "anime"
            if category == "Music":
                category = "music"
            if category == "Books":
                category = "Books"
            if category == "XXX":
                category = "xxx"
            if category == "All":
                category = "new"

            link = domain + category
            try:
                request = requests.get(link)
            except:
                error_message()
            source = request.content
            soup = BeautifulSoup(source, 'lxml')

            magnets = ['==== Made by @eliasbenb ====']
            for link in soup.findAll('a', attrs={'href': re.compile("^magnet")}):
                magnets.append('\n'+link.get('href'))
            magnets = list(dict.fromkeys(magnets))

            timestr = time.strftime(" %Y%m%d%H%M%S")
            file_name = "KAT Results " + timestr + ".txt"
            with open(file_name, 'w') as w1:
                for magnet in magnets:
                    w1.write(magnet)
            exported_sucess_message()
        except:
            error_message()

    def setupUi(self, katMainWindow):
        katMainWindow.setObjectName("katMainWindow")
        katMainWindow.setFixedSize(600, 330)
        font = QFont()
        font.setFamily("Bahnschrift Light")
        katMainWindow.setFont(font)
        icon = QIcon()
        icon.addPixmap(QPixmap(src.mglobals.icon), QIcon.Normal, QIcon.Off)
        katMainWindow.setWindowIcon(icon)
        self.centralwidget = QWidget(katMainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.domainComboBox = QComboBox(self.centralwidget)
        self.domainComboBox.setGeometry(QRect(150, 60, 300, 22))
        self.domainComboBox.setLayoutDirection(Qt.LeftToRight)
        self.domainComboBox.setObjectName("domainComboBox")
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
        katMainWindow.setCentralWidget(self.centralwidget)

        self.scrapeButton.clicked.connect(self.callback)

        self.retranslateUi(katMainWindow)
        QMetaObject.connectSlotsByName(katMainWindow)

    def retranslateUi(self, katMainWindow):
        _translate = QCoreApplication.translate
        katMainWindow.setWindowTitle(_translate(
            "katMainWindow", "MagnetMagnet - KAT"))
        self.domainComboBox.setItemText(
            0, _translate("katMainWindow", "https://kat.rip/"))
        self.domainLabel.setText(_translate(
            "katMainWindow", "Choose a KAT domain:"))
        self.categoryComboBox.setItemText(
            0, _translate("katMainWindow", "All"))
        self.categoryComboBox.setItemText(
            1, _translate("katMainWindow", "Movies"))
        self.categoryComboBox.setItemText(2, _translate("katMainWindow", "TV"))
        self.categoryComboBox.setItemText(
            3, _translate("katMainWindow", "Anime"))
        self.categoryComboBox.setItemText(
            4, _translate("katMainWindow", "Music"))
        self.categoryComboBox.setItemText(
            5, _translate("katMainWindow", "Books"))
        self.categoryComboBox.setItemText(
            6, _translate("katMainWindow", "XXX"))
        self.categoryLabel.setText(_translate(
            "katMainWindow", "Choose a category:"))
        self.scrapeButton.setText(_translate("katMainWindow", "Scrape"))

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


def search_tpb(self, query, limit):
    try:
        main_link = 'https://tpb.party/search/' + query + '/1/99/0/'
        main_request = requests.get(
                main_link, headers={'User-Agent': 'Mozilla/5.0'})
        main_source = main_request.content
        main_soup = BeautifulSoup(main_source, 'lxml')

        titles_soup = main_soup.findAll('div', class_="detName")
        seeders_soup = main_soup.findAll(
                'td', attrs={'align': "right"})
        seeders_soup = seeders_soup[0::2]
        leechers_soup = main_soup.findAll(
                'td', attrs={'align': "right"})
        leechers_soup = leechers_soup[1::2]
        sizes_soup = main_soup.findAll('font', class_="detDesc")
        dates_soup = main_soup.findAll('font', class_="detDesc")
        magnets_soup = main_soup.findAll(
                'a', attrs={'href': re.compile("^magnet")})

        titles = []
        seeders = []
        leechers = []
        sizes = []
        dates = []
        limit_counter = 0
        for title in titles_soup:
            if limit_counter < limit:
                title = title.text.replace("\n", "")
                titles.append(title)
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
                size = size.text.split(", ")
                size = size[1].replace("Size ", "")
                sizes.append(size)
                limit_counter = limit_counter + 1
        limit_counter = 0
        for date in dates_soup:
            if limit_counter < limit:
                date = date.text.split(", ")
                date = date[0].replace("Uploaded ", "")
                dates.append(date)
                limit_counter = limit_counter + 1
        count1 = 0
        limit_counter = 0
        for magnet in magnets_soup:
            if limit_counter < limit:
                self.magnets.append(magnet.get('href'))
                count1 = count1 + 1
                limit_counter = limit_counter + 1

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
                    row_position, 5, QTableWidgetItem("TPB"))
            count2 = count2 + 1
    except Exception as e:
        error_message(str(e))


class Ui_tpbMainWindow(object):
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

            if category == "All":
                category = "recent"
            if category == "Movies - HD":
                category = "browse/207"
            if category == "Movies - Not HD":
                category = "browse/201"
            if category == "TV - HD":
                category = "browse/208"
            if category == "TV - Not HD":
                category = "browse/205"
            if category == "Music - All":
                category = "browse/101"
            if category == "XXX - All":
                category = "browse/500"

            link = domain + category
            request = requests.get(link)
            source = request.content
            soup = BeautifulSoup(source, 'lxml')

            magnets = []
            for link in soup.findAll('a', attrs={'href': re.compile("^magnet")}):
                magnets.append(link.get('href'))
                magnets.append('\n')

            timestr = time.strftime(" %Y%m%d%H%M%S")
            file_name = "TPB Results " + timestr + ".txt"
            with open(file_name, 'w') as w1:
                for magnet in magnets:
                    w1.write(magnet)
            exported_sucess_message()
        except:
            error_message()

    def setupUi(self, tpbMainWindow):
        tpbMainWindow.setObjectName("tpbMainWindow")
        tpbMainWindow.setFixedSize(600, 330)
        font = QFont()
        font.setFamily("Bahnschrift Light")
        tpbMainWindow.setFont(font)
        icon = QIcon()
        icon.addPixmap(QPixmap(src.mglobals.icon), QIcon.Normal, QIcon.Off)
        tpbMainWindow.setWindowIcon(icon)
        self.centralwidget = QWidget(tpbMainWindow)
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
        tpbMainWindow.setCentralWidget(self.centralwidget)

        self.scrapeButton.clicked.connect(self.callback)

        self.retranslateUi(tpbMainWindow)
        QMetaObject.connectSlotsByName(tpbMainWindow)

    def retranslateUi(self, tpbMainWindow):
        _translate = QCoreApplication.translate
        tpbMainWindow.setWindowTitle(_translate(
            "tpbMainWindow", "MagnetMagnet - TPB"))
        self.domainComboBox.setItemText(0, _translate(
            "tpbMainWindow", "https://tpb.party/"))
        self.domainLabel.setText(_translate(
            "tpbMainWindow", "Choose a TPB domain:"))
        self.categoryComboBox.setItemText(
            0, _translate("tpbMainWindow", "All"))
        self.categoryComboBox.setItemText(
            1, _translate("tpbMainWindow", "Movies - HD"))
        self.categoryComboBox.setItemText(
            2, _translate("tpbMainWindow", "Movies - Not HD"))
        self.categoryComboBox.setItemText(
            3, _translate("tpbMainWindow", "TV - HD"))
        self.categoryComboBox.setItemText(
            4, _translate("tpbMainWindow", "TV - Not HD"))
        self.categoryComboBox.setItemText(
            5, _translate("tpbMainWindow", "Music - All"))
        self.categoryComboBox.setItemText(
            6, _translate("tpbMainWindow", "XXX - All"))
        self.categoryLabel.setText(_translate(
            "tpbMainWindow", "Choose a category:"))
        self.scrapeButton.setText(_translate("tpbMainWindow", "Scrape"))

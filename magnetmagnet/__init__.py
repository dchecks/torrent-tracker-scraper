from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QMessageBox

from src import mglobals


def searched_success_message():
    successMessageBox = QMessageBox()
    successMessageBox.setIcon(QMessageBox.Information)

    successMessageBox.setText(
            "Magnet links have been successfully scraped.")
    successMessageBox.setWindowTitle("Task Completed!")
    successMessageBox.setStandardButtons(QMessageBox.Ok)
    icon = QIcon()
    icon.addPixmap(QPixmap(mglobals.icon), QIcon.Normal, QIcon.Off)
    successMessageBox.setWindowIcon(icon)

    successMessageBox.exec_()


def error_message(error_text):
    errorMessageBox = QMessageBox()
    errorMessageBox.setIcon(QMessageBox.Information)

    errorMessageBox.setText("Error: %s" % error_text)
    # "Something went wrong! Please inform me through GitHub!")
    errorMessageBox.setWindowTitle("Error!")
    errorMessageBox.setStandardButtons(QMessageBox.Ok)
    icon = QIcon()
    icon.addPixmap(QPixmap(mglobals.icon), QIcon.Normal, QIcon.Off)
    errorMessageBox.setWindowIcon(icon)

    errorMessageBox.exec_()
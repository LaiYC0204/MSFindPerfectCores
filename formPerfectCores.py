# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\formPerfectCores.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_formPerfectCores(object):
    def setupUi(self, formPerfectCores):
        formPerfectCores.setObjectName("formPerfectCores")
        formPerfectCores.resize(302, 381)
        self.scrollArea = QtWidgets.QScrollArea(formPerfectCores)
        self.scrollArea.setGeometry(QtCore.QRect(10, 10, 281, 371))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 279, 369))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.retranslateUi(formPerfectCores)
        QtCore.QMetaObject.connectSlotsByName(formPerfectCores)

    def retranslateUi(self, formPerfectCores):
        _translate = QtCore.QCoreApplication.translate
        formPerfectCores.setWindowTitle(_translate("formPerfectCores", "完美核心"))
        self.label.setText(_translate("formPerfectCores", ""))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    formPerfectCores = QtWidgets.QWidget()
    ui = Ui_formPerfectCores()
    ui.setupUi(formPerfectCores)
    formPerfectCores.show()
    sys.exit(app.exec_())

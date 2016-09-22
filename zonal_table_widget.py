# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'zonal_table_widget.ui'
#
# Created: Wed Sep 14 12:53:31 2016
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_ZonalTableWidget(object):
    def setupUi(self, ZonalTableWidget):
        ZonalTableWidget.setObjectName(_fromUtf8("ZonalTableWidget"))
        ZonalTableWidget.resize(333, 495)
        self.gridLayout_3 = QtGui.QGridLayout(ZonalTableWidget)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.mainFrame = QtGui.QFrame(ZonalTableWidget)
        self.mainFrame.setMinimumSize(QtCore.QSize(0, 0))
        self.mainFrame.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.mainFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.mainFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.mainFrame.setObjectName(_fromUtf8("mainFrame"))
        self.gridLayout_2 = QtGui.QGridLayout(self.mainFrame)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(14)
        self.horizontalLayout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setContentsMargins(-1, -1, -1, 0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.pushButton_5 = QtGui.QPushButton(self.mainFrame)
        self.pushButton_5.setObjectName(_fromUtf8("pushButton_5"))
        self.horizontalLayout.addWidget(self.pushButton_5)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tableWidget = QtGui.QTableWidget(self.mainFrame)
        self.tableWidget.setLocale(QtCore.QLocale(QtCore.QLocale.Polish, QtCore.QLocale.Poland))
        self.tableWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setDragDropOverwriteMode(False)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.verticalLayout.addWidget(self.tableWidget)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.pushButton_6 = QtGui.QPushButton(self.mainFrame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_6.sizePolicy().hasHeightForWidth())
        self.pushButton_6.setSizePolicy(sizePolicy)
        self.pushButton_6.setMinimumSize(QtCore.QSize(200, 0))
        self.pushButton_6.setObjectName(_fromUtf8("pushButton_6"))
        self.horizontalLayout_2.addWidget(self.pushButton_6)
        self.buttonBox = QtGui.QDialogButtonBox(self.mainFrame)
        self.buttonBox.setMaximumSize(QtCore.QSize(100, 16777215))
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.horizontalLayout_2.addWidget(self.buttonBox)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.mainFrame, 0, 0, 1, 1)

        self.retranslateUi(ZonalTableWidget)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ZonalTableWidget.reject)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ZonalTableWidget.accept)
        QtCore.QMetaObject.connectSlotsByName(ZonalTableWidget)

    def retranslateUi(self, ZonalTableWidget):
        ZonalTableWidget.setWindowTitle(QtGui.QApplication.translate("ZonalTableWidget", "Tabela", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_5.setText(QtGui.QApplication.translate("ZonalTableWidget", "Wykres", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.setSortingEnabled(True)
        self.pushButton_6.setText(QtGui.QApplication.translate("ZonalTableWidget", "Odśwież", None, QtGui.QApplication.UnicodeUTF8))


# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt6 UI code generator 6.5.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(625, 600)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.widget = QtWidgets.QWidget(parent=self.centralwidget)
        self.widget.setObjectName("widget")
        self.tabWidget = QtWidgets.QTabWidget(parent=self.widget)
        self.tabWidget.setGeometry(QtCore.QRect(-10, 0, 981, 561))
        self.tabWidget.setObjectName("tabWidget")
        self.cars = QtWidgets.QWidget()
        self.cars.setObjectName("cars")
        self.AutoGraph = QtWidgets.QWidget(parent=self.cars)
        self.AutoGraph.setGeometry(QtCore.QRect(600, 0, 351, 321))
        self.AutoGraph.setObjectName("AutoGraph")
        self.AutoTable = QtWidgets.QTableWidget(parent=self.cars)
        self.AutoTable.setGeometry(QtCore.QRect(10, 0, 531, 541))
        self.AutoTable.setObjectName("AutoTable")
        self.AutoTable.setColumnCount(0)
        self.AutoTable.setRowCount(0)
        self.tabWidget.addTab(self.cars, "")
        self.drivers = QtWidgets.QWidget()
        self.drivers.setObjectName("drivers")
        self.DriversTable = QtWidgets.QTableWidget(parent=self.drivers)
        self.DriversTable.setGeometry(QtCore.QRect(0, 10, 361, 541))
        self.DriversTable.setObjectName("DriversTable")
        self.DriversTable.setColumnCount(0)
        self.DriversTable.setRowCount(0)
        self.tabWidget.addTab(self.drivers, "")
        self.Travels = QtWidgets.QWidget()
        self.Travels.setObjectName("Travels")
        self.widget_4 = QtWidgets.QWidget(parent=self.Travels)
        self.widget_4.setGeometry(QtCore.QRect(610, 10, 351, 321))
        self.widget_4.setObjectName("widget_4")
        self.tableWidget = QtWidgets.QTableWidget(parent=self.Travels)
        self.tableWidget.setGeometry(QtCore.QRect(10, 0, 591, 521))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.tabWidget.addTab(self.Travels, "")
        self.gridLayout.addWidget(self.widget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menuBar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 982, 26))
        self.menuBar.setObjectName("menuBar")
        self.menuAdd = QtWidgets.QMenu(parent=self.menuBar)
        self.menuAdd.setObjectName("menuAdd")
        MainWindow.setMenuBar(self.menuBar)
        self.actionCar = QtGui.QAction(parent=MainWindow)
        self.actionCar.setObjectName("actionCar")
        self.actionDriver = QtGui.QAction(parent=MainWindow)
        self.actionDriver.setObjectName("actionDriver")
        self.action_3 = QtGui.QAction(parent=MainWindow)
        self.action_3.setObjectName("action_3")
        self.menuAdd.addAction(self.actionCar)
        self.menuAdd.addAction(self.actionDriver)
        self.menuAdd.addAction(self.action_3)
        self.menuBar.addAction(self.menuAdd.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.cars), _translate("MainWindow", "Машины"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.drivers), _translate("MainWindow", "Водители"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Travels), _translate("MainWindow", "Путевой лист"))
        self.menuAdd.setTitle(_translate("MainWindow", "Add"))
        self.actionCar.setText(_translate("MainWindow", "Car"))
        self.actionDriver.setText(_translate("MainWindow", "Driver"))
        self.action_3.setText(_translate("MainWindow", "Путешествие"))

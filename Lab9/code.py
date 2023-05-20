from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTableWidgetItem
from mainUI import Ui_MainWindow
from addauto import Ui_helper
from addtravels import Ui_helper3
import sys
import psycopg2
import re
import datetime
from addworker import Ui_helper2
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib import pyplot as plt
import numpy as np

columnsetauto = ['id', 'maker', 'number', 'year', 'fuel']
columnsetdrivers = ['id', 'worker', 'auto']
columnsettravels = ['id', 'driver', 'auto', 'departure', 'arrival', 'smileage', 'emileage', 'distance', 'fuel']

# Подключение к базе данных
connection = psycopg2.connect(user="postgres",
                              password="12345",    
                              host="127.0.0.1",
                              port="5432",
                              database="lab9")
cursor = connection.cursor()

# Метод взятия данных из базы
def getdata(table, column, row):
    global cursor
    cursor.execute(f"""SELECT {column} FROM {table} WHERE id = '{row}'""")
    return str(cursor.fetchall()).replace('[', '').replace(']', '').replace('(', '').replace(')', '').replace(',', '').replace('\'', '').replace('datetime.date','')

# Окно добавления автомобиля
class autoadder(QtWidgets.QMainWindow):
    def __init__(self, master):
        super(autoadder,self).__init__()
        self.master = master
        self.ui = Ui_helper()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(lambda: self.addition())

    def addition(self):
        length = self.master.ui.AutoTable.rowCount()
        self.master.ui.AutoTable.setRowCount(length+1)
        self.master.ui.AutoTable.setItem(length, 0, QTableWidgetItem(self.ui.lineEdit.text()))
        self.master.ui.AutoTable.setItem(length, 1, QTableWidgetItem(self.ui.lineEdit_3.text()))
        self.master.ui.AutoTable.setItem(length, 2, QTableWidgetItem(self.ui.lineEdit_2.text()))
        self.master.ui.AutoTable.setItem(length, 3, QTableWidgetItem(self.ui.lineEdit_4.text()))
        insertQuery = f"""INSERT INTO auto (id, maker, number, year, fuel) VALUES ('{length+1}', '{self.ui.lineEdit.text()}', '{self.ui.lineEdit_3.text()}', '{self.ui.lineEdit_2.text()}', '{self.ui.lineEdit_4.text()}')"""
        cursor.execute(insertQuery)
        connection.commit()
        self.master.plotupdate()
        self.close()

# Окно добавления сотрудника
class driveradder(QtWidgets.QMainWindow):
    def __init__(self, master):
        super(driveradder,self).__init__()
        self.master = master
        self.ui = Ui_helper2()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(lambda: self.addition())

    def addition(self):
        length = self.master.ui.DriversTable.rowCount()
        self.master.ui.DriversTable.setRowCount(length+1)
        self.master.ui.DriversTable.setItem(length, 0, QTableWidgetItem(self.ui.lineEdit.text()))
        self.master.ui.DriversTable.setItem(length, 1, QTableWidgetItem(self.ui.lineEdit_3.text()))
        insertQuery = f"""INSERT INTO drivers (id, worker, auto) VALUES ('{length+1}', '{self.ui.lineEdit.text()}', '{self.ui.lineEdit_3.text()}')"""
        cursor.execute(insertQuery)
        connection.commit()
        self.close()

# Окно добавления путешествия в путевой лист
class traveladder(QtWidgets.QMainWindow):
    def __init__(self, master):
        super(traveladder,self).__init__()
        self.master = master
        self.ui = Ui_helper3()
        self.ui.setupUi(self)
        names = []
        for i in range(self.master.ui.DriversTable.rowCount()):
            names.append([self.master.ui.DriversTable.item(i, 1).text(), self.master.ui.DriversTable.item(i, 0).text()])
        validnames = []
        if names is not None:
            for driv in names:
                if not(driv[0] in validnames):
                    validnames.append(driv[0])
        self.ui.comboBox.addItems(validnames)
        self.ui.comboBox.update()
        self.ui.comboBox.activated.connect(lambda: self.rehydrate(names))
        self.ui.pushButton.clicked.connect(lambda: self.addition())

    def addition(self):
        length = self.master.ui.tableWidget.rowCount()
        self.master.ui.tableWidget.setRowCount(length+1)
        self.master.ui.tableWidget.setItem(length, 0, QTableWidgetItem(self.ui.comboBox.currentText()))
        self.master.ui.tableWidget.setItem(length, 1, QTableWidgetItem(self.ui.comboBox_2.currentText()))
        self.master.ui.tableWidget.setItem(length, 2, QTableWidgetItem(self.ui.lineEdit_2.text()))
        self.master.ui.tableWidget.setItem(length, 3, QTableWidgetItem(self.ui.lineEdit_4.text()))
        self.master.ui.tableWidget.setItem(length, 4, QTableWidgetItem(self.ui.lineEdit_6.text()))
        self.master.ui.tableWidget.setItem(length, 5, QTableWidgetItem(self.ui.lineEdit_5.text()))
        self.master.ui.tableWidget.setItem(length, 6, QTableWidgetItem(str(int(self.ui.lineEdit_5.text()) - int(self.ui.lineEdit_6.text()))))
        bebrus = self.master.ui.AutoTable.findItems(self.ui.comboBox_2.currentText(), Qt.MatchFlag.MatchContains)[0]
        amogus = (int(self.ui.lineEdit_5.text()) - int(self.ui.lineEdit_6.text())) * int(self.master.ui.tableWidget.item(self.master.ui.AutoTable.row(bebrus),4).text())
        self.master.ui.tableWidget.setItem(length, 7, QTableWidgetItem(str(amogus)))
        insertQuery = f"""INSERT INTO travel_list (id, driver, auto, otprav, pribit, nach_kil, konech_kil, distance, fuel) VALUES ('{length+1}', '{self.ui.comboBox.currentText()}', '{self.ui.comboBox_2.currentText()}', '{self.ui.lineEdit_2.text()}', '{self.ui.lineEdit_4.text()}', '{self.ui.lineEdit_6.text()}', '{self.ui.lineEdit_5.text()}','{int(self.ui.lineEdit_5.text()) - int(self.ui.lineEdit_6   .text())}', '{amogus}')"""
        cursor.execute(insertQuery)
        connection.commit()
        self.master.plotupdate()
        self.close()
    
    def rehydrate(self, names):
        given = self.ui.comboBox.currentText()
        for name in names:
            if given == name[0]:
                self.ui.comboBox_2.addItem(name[1])
        self.ui.comboBox_2.update()

# Окно графика
class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self, ass, b):
        super().__init__()
        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)
        layout = QtWidgets.QVBoxLayout(self._main)
        fig = Figure(figsize=(3.5,3.5), dpi=100)
        a=fig.add_subplot(111)
        a.bar(ass, b)
        a.axhline(y=np.mean(b), color='r')
        canvas = FigureCanvas(fig)
        layout.addWidget(canvas)
        self.show()
        

# Основное окно
class bosswindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(bosswindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.tableWidget.setRowCount(0)
        self.ui.tableWidget.setColumnCount(8)
        self.ui.tableWidget.setHorizontalHeaderLabels(('Водитель', 'Автомобиль', 'Время выезда', 'Время заезда', 'Начальный километраж', 'Конечный километраж', 'Пробег', 'Расход'))
        for i in range(8):
            self.ui.tableWidget.setColumnWidth(i, 175)
        self.ui.AutoTable.setRowCount(0)
        self.ui.AutoTable.setColumnCount(4)
        self.ui.AutoTable.setHorizontalHeaderLabels(('Марка', 'Номер', 'Год выпуска', 'Расход'))
        for i in range(4):
            self.ui.AutoTable.setColumnWidth(i, 175)
        self.ui.DriversTable.setRowCount(0)
        self.ui.DriversTable.setColumnCount(2)
        self.ui.DriversTable.setHorizontalHeaderLabels(('Марка', 'Сотрудник'))
        for i in range(2):
            self.ui.DriversTable.setColumnWidth(i, 175)
        self.populate()
        self.carer = autoadder(self)
        self.driverer = driveradder(self)
        self.ui.actionCar.triggered.connect(lambda: self.carer.show())
        self.ui.actionDriver.triggered.connect(lambda: self.driverer.show())
        self.ui.action_3.triggered.connect(lambda: traveladder(self).show())
        self.plotupdate()
        self.bebrik.show()
        self.bebrik2.show()

    def populate(self):
        cursor.execute('SELECT count(*) AS exact_count FROM auto;')
        tablesize = int(re.sub('\D', ' ', str(cursor.fetchall())))
        for i in range(tablesize):
            self.ui.AutoTable.setRowCount(i+1)
            self.ui.AutoTable.setItem(i, 0, QTableWidgetItem(getdata('auto', 'maker', i+1)))
            self.ui.AutoTable.setItem(i, 1, QTableWidgetItem(getdata('auto', 'number', i+1)))
            self.ui.AutoTable.setItem(i, 2, QTableWidgetItem(getdata('auto', 'year', i+1)))
            self.ui.AutoTable.setItem(i, 3, QTableWidgetItem(getdata('auto', 'fuel', i+1)))
        cursor.execute('SELECT count(*) AS exact_count FROM drivers;')
        tablesize = int(re.sub('\D', ' ', str(cursor.fetchall())))
        for i in range(tablesize):
            self.ui.DriversTable.setRowCount(i+1)
            self.ui.DriversTable.setItem(i, 0, QTableWidgetItem(getdata('drivers', 'worker', i+1)))
            self.ui.DriversTable.setItem(i, 1, QTableWidgetItem(getdata('drivers', 'auto', i+1)))
        cursor.execute('SELECT count(*) AS exact_count FROM travel_list;')
        tablesize = int(re.sub('\D', ' ', str(cursor.fetchall())))
        for i in range(tablesize):
            self.ui.tableWidget.setRowCount(i+1)
            self.ui.tableWidget.setItem(i, 0, QTableWidgetItem(getdata('travel_list', 'driver', i+1)))
            self.ui.tableWidget.setItem(i, 1, QTableWidgetItem(getdata('travel_list', 'auto', i+1)))
            self.ui.tableWidget.setItem(i, 2, QTableWidgetItem(getdata('travel_list', 'otprav', i+1)))
            self.ui.tableWidget.setItem(i, 3, QTableWidgetItem(getdata('travel_list', 'pribit', i+1)))
            self.ui.tableWidget.setItem(i, 4, QTableWidgetItem(getdata('travel_list', 'nach_kil', i+1)))
            self.ui.tableWidget.setItem(i, 5, QTableWidgetItem(getdata('travel_list', 'konech_kil', i+1)))
            self.ui.tableWidget.setItem(i, 6, QTableWidgetItem(getdata('travel_list', 'distance', i+1)))
            self.ui.tableWidget.setItem(i, 7, QTableWidgetItem(getdata('travel_list', 'fuel', i+1)))
    
    def plotupdate(self):
        travellength = self.ui.tableWidget.rowCount()
        needed = []
        for i in range(travellength):
            if [self.ui.tableWidget.item(i,0).text(), int(self.ui.tableWidget.item(i,6).text())]  not in needed:
                needed.append([self.ui.tableWidget.item(i,0).text(), int(self.ui.tableWidget.item(i,6).text())])
            else: 
                needed[i][1] += int(self.ui.tableWidget.item(i,6).text())
        needednames = []
        needednums = []
        for k in needed:
            needednames.append(k[0])
            needednums.append(k[1])
        self.bebrik = ApplicationWindow(needednames,needednums)
        self.bebrik.show()
        carlength = self.ui.AutoTable.rowCount()
        needed = []
        for i in range(carlength):
            if [self.ui.AutoTable.item(i,0).text(), int(self.ui.AutoTable.item(i,3).text())]  not in needed:
                needed.append([self.ui.AutoTable.item(i,0).text(), int(self.ui.AutoTable.item(i,3).text())])
            else: 
                needed[i][1] += int(self.ui.AutoTable.item(i,3).text())
        carnames = []
        carnums = []
        for k in needed:
            carnames.append(k[0])
            carnums.append(k[1])
        self.bebrik2 = ApplicationWindow(carnames,carnums)
        self.bebrik2.show()

def main():
    app = QtWidgets.QApplication(sys.argv)
    mainwindow = bosswindow()
    mainwindow.show()
    app.exec()

if __name__ == "__main__":
    main()
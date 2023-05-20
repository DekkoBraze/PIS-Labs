from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QTableWidgetItem
from mainwindow import Ui_MainWindow
from addwindow import Ui_helper
from choice import Ui_ChoiceWindow
import sys
import psycopg2
import re
import datetime
from output import Ui_output

columnset = ['id', 'data', 'name', 'val']

# Подключение к базе данных
connection = psycopg2.connect(user="postgres",
                              password="12345",    
                              host="127.0.0.1",
                              port="5432",
                              database="lab10")
cursor = connection.cursor()

# Вывод результатов сортировки
def fillerfunc(prepdict):
    global outputwindow
    outputwindow.ui.tableWidget.clearContents()
    sum = 0
    for val in prepdict.values():
        sum += val
    for item in prepdict.keys():
        lenny = outputwindow.ui.tableWidget.rowCount()
        outputwindow.ui.tableWidget.setRowCount(lenny+1)
        outputwindow.ui.tableWidget.setItem(lenny, 0, QTableWidgetItem(item))
        outputwindow.ui.tableWidget.setItem(lenny, 1, QTableWidgetItem(str(prepdict[item])))
        outputwindow.ui.tableWidget.setItem(lenny, 2, QTableWidgetItem(str(sum)))
    outputwindow.show()
    
# Окно вывода результатов
class output(QtWidgets.QMainWindow):
    def __init__(self):
        super(output,self).__init__()
        self.ui = Ui_output()
        self.ui.setupUi(self)
        self.ui.tableWidget.setColumnCount(3)
        self.ui.tableWidget.setHorizontalHeaderLabels(('Название', 'Сумма', 'Сумма по файлу'))

# Получение данных из базы
def getdata(table, column, row):
    global cursor
    cursor.execute(f"""SELECT {column} FROM {table} WHERE id = '{row}'""")
    return str(cursor.fetchall()).replace('[', '').replace(']', '').replace('(', '').replace(')', '').replace(',', '').replace('\'', '').replace('datetime.date','')

# Окно добавления товара
class adderwindow(QtWidgets.QMainWindow):
    def __init__(self, master):
        super(adderwindow, self).__init__()
        self.master = master
        self.ui = Ui_helper()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(lambda: self.calculate())
    
    def calculate(self):
        length = self.master.ui.tableWidget.rowCount()
        self.master.ui.tableWidget.setRowCount(length+1)
        self.master.ui.tableWidget.setItem(length, 1, QTableWidgetItem(self.ui.lineEdit_3.text()))
        self.master.ui.tableWidget.setItem(length, 0, QTableWidgetItem(self.ui.lineEdit.text()))
        self.master.ui.tableWidget.setItem(length, 2, QTableWidgetItem(self.ui.lineEdit_2.text()))
        insertQuery = f"""INSERT INTO table_goods (id, data, name, val) VALUES ('{length+1}', '{self.ui.lineEdit.text()}', '{self.ui.lineEdit_3.text()}', '{self.ui.lineEdit_2.text()}')"""
        cursor.execute(insertQuery)
        connection.commit()
        self.close()

# Окно выбора даты
class chooserwindow(QtWidgets.QMainWindow):
    def __init__(self, master):
        super(chooserwindow, self).__init__()
        self.master = master
        self.ui = Ui_ChoiceWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(lambda: self.select())
    
    def select(self):
        needed = []
        length = self.master.ui.tableWidget.rowCount()
        ss = self.ui.lineEdit.text().split()
        start = datetime.date(int(ss[0]), int(ss[1]), int(ss[2]))
        ee = self.ui.lineEdit_2.text().split()
        end = datetime.date(int(ee[0]), int(ee[1]), int(ee[2]))
        for i in range(length):
            td = self.master.ui.tableWidget.item(i, 0).text().split()
            thisdate = datetime.date(int(td[0]), int(td[1]), int(td[2]))
            if start <= thisdate <= end:
                needed.append([str(thisdate), self.master.ui.tableWidget.item(i, 1).text(), self.master.ui.tableWidget.item(i, 2).text()])
        prepdict = {}
        for item in needed:
            if item[1] in prepdict.keys():
                prepdict[item[1]] += int(item[2])
            else: prepdict[item[1]] = int(item[2])
        fillerfunc(prepdict)
        self.close()

# Главное окно
class bosswindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(bosswindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.tableWidget.setRowCount(0)
        self.ui.tableWidget.setColumnCount(3)
        self.ui.tableWidget.setHorizontalHeaderLabels(('Дата', 'Название', 'Сумма'))
        self.ui.tableWidget.setColumnWidth(0, 200)
        self.ui.tableWidget.setColumnWidth(1, 200)
        self.populate()
        self.adder = adderwindow(self)
        self.chooser = chooserwindow(self)
        self.ui.actionAdd.triggered.connect(lambda: self.adder.show())
        self.ui.actionChoose.triggered.connect(lambda: self.chooser.show())

    # Заполнение таблицы
    def populate(self):
        cursor.execute('SELECT count(*) AS exact_count FROM table_goods;')
        tablesize = int(re.sub('\D', ' ', str(cursor.fetchall())))
        for i in range(tablesize):
            self.ui.tableWidget.setRowCount(i+1)
            self.ui.tableWidget.setItem(i, 1, QTableWidgetItem(getdata('table_goods', 'name', i+1)))
            self.ui.tableWidget.setItem(i, 0, QTableWidgetItem(getdata('table_goods', 'data', i+1)))
            self.ui.tableWidget.setItem(i, 2, QTableWidgetItem(getdata('table_goods', 'val', i+1)))

# Основной цикл
def main():
    global outputwindow
    app = QtWidgets.QApplication(sys.argv)
    outputwindow = output()
    mainwindow = bosswindow()
    mainwindow.show()
    app.exec()


if __name__ == "__main__":
    main()
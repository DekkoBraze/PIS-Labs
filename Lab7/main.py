from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QTableWidgetItem
from mainwindow import Ui_MainWindow
from untitled import Ui_helper
import sys
import psycopg2
import re

columnset = ['id', 'kodpodr', 'vnutkod']

# Подключение к базе данных
connection = psycopg2.connect(user="postgres",
                              password="12345",    
                              host="127.0.0.1",
                              port="5432",
                              database="lab7")
cursor = connection.cursor()

# Взятие данных из таблицы
def getdata(table, column, row):
    global cursor
    cursor.execute(f"""SELECT {column} FROM {table} WHERE id = '{row}'""")
    return str(cursor.fetchall()).replace('[', '').replace(']', '').replace('(', '').replace(')', '').replace(',', '').replace('\'', '')

# Окно добавления нового элемента таблицы
class helperwindow(QtWidgets.QMainWindow):
    # Инициализация окна
    def __init__(self, master):
        super(helperwindow, self).__init__()
        self.master = master
        self.ui = Ui_helper()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(lambda: self.calculate())
    
    # Обработка данных и изменение таблицы
    def calculate(self):
        length = self.master.ui.tableWidget.rowCount()
        self.master.ui.tableWidget.setRowCount(length+1)
        val = length + int(self.ui.lineEdit.text()) + 1
        self.ui.label_3.setText(str(val))
        self.master.ui.tableWidget.setItem(length, 1, QTableWidgetItem(str(val)))
        self.master.ui.tableWidget.setItem(length, 0, QTableWidgetItem(self.ui.lineEdit.text()))
        self.close()
        insertQuery = f"""INSERT INTO table7 (id, kodpodr, vnutkod) VALUES ('{length+1}', '{self.ui.lineEdit.text()}', '{val}')"""
        cursor.execute(insertQuery)
        connection.commit()

# Главное окно
class bosswindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(bosswindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.tableWidget.setRowCount(0)
        self.ui.tableWidget.setColumnCount(2)
        self.ui.tableWidget.setHorizontalHeaderLabels(('Код подразделения', 'Код внутреннего учёта'))
        self.ui.tableWidget.setColumnWidth(0, 200)
        self.ui.tableWidget.setColumnWidth(1, 200)
        self.populate()
        self.helper = helperwindow(self)
        self.ui.actionAdd.triggered.connect(lambda: self.helper.show())

    # Отображение таблицы в главном окне
    def populate(self):
        cursor.execute('SELECT count(*) AS exact_count FROM table7;')
        tablesize = int(re.sub('\D', ' ', str(cursor.fetchall())))
        for i in range(tablesize):
            self.ui.tableWidget.setRowCount(i+1)
            self.ui.tableWidget.setItem(i, 0, QTableWidgetItem(getdata('table7', 'kodpodr', i+1)))
            self.ui.tableWidget.setItem(i, 1, QTableWidgetItem(getdata('table7', 'vnutkod', i+1)))

# Основной цикл
def main():
    app = QtWidgets.QApplication(sys.argv)
    mainwindow = bosswindow()
    mainwindow.show()
    app.exec()

if __name__ == "__main__":
    main()

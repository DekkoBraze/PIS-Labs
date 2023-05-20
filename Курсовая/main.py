from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTableWidgetItem

from bossWindow import Ui_MainWindow
from addToCheck import Ui_addToCheck
from addToFilial import Ui_addToFilial
from chooseDay import Ui_chooseDay
from movingToFilial import Ui_movingToFilial
from newCheck import Ui_newCheck
from outputRashodNaklad import Ui_outputRashodNaklad

import sys
import psycopg2
import re
import datetime

# Подключение к базе данных
connection = psycopg2.connect(user="postgres",
                              password="12345",    
                              host="127.0.0.1",
                              port="5432",
                              database="pis_kursov")
cursor = connection.cursor()

# Метод взятия данных из базы
def getdata(table, column, row):
    global cursor
    cursor.execute(f"""SELECT {column} FROM {table} WHERE id = '{row}'""")
    return str(cursor.fetchall()).replace('[', '').replace(']', '').replace('(', '').replace(')', '').replace(',', '').replace('\'', '').replace('datetime.date','')

# Метод создания лога
def makeLog(event, bool):
    data = datetime.datetime.now()
    cursor.execute('SELECT count(*) AS exact_count FROM event_log;')
    length = int(re.sub('\D', ' ', str(cursor.fetchall())))
    insertQuery = f"""INSERT INTO event_log (id, data, event, successfully) VALUES ('{length+1}', '{data}', '{event}', '{bool}')"""
    cursor.execute(insertQuery)
    connection.commit()

# Метод создания записи обмена
def makeExchange(table_name):
    data = datetime.datetime.now()
    cursor.execute(f'SELECT count(*) AS exact_count FROM {table_name};')
    length = int(re.sub('\D', ' ', str(cursor.fetchall())))
    cursor.execute(f'SELECT count(*) AS exact_count FROM exchange_history;')
    id = int(re.sub('\D', ' ', str(cursor.fetchall())))
    result = 0
    for i in range(length):
        selectQuery = f"""SELECT price FROM {table_name} WHERE id={i+1}"""
        cursor.execute(selectQuery)
        price = cursor.fetchall()[0][0]
        selectQuery = f"""SELECT amount FROM {table_name} WHERE id={i+1}"""
        cursor.execute(selectQuery)
        amount = cursor.fetchall()[0][0]
        result += price * amount
    insertQuery = f"""INSERT INTO exchange_history (id, data, length, result) VALUES ('{id+1}', '{data}', '{length}', '{result}')"""
    cursor.execute(insertQuery)
    makeLog("exchange created", 'TRUE')
    connection.commit()

# Окно перемещения товаров в филиал
class movingToFilial(QtWidgets.QMainWindow):
    def __init__(self, master):
        super(movingToFilial,self).__init__()
        self.master = master
        self.ui = Ui_movingToFilial()
        self.ui.setupUi(self)
        makeLog("movingToFilial Opened", 'TRUE')
        self.ui.addedGoods.setRowCount(0)
        self.ui.addedGoods.setColumnCount(3)
        self.ui.addedGoods.setHorizontalHeaderLabels(('Имя', 'Цена', 'Количество'))
        for i in range(3):
            self.ui.addedGoods.setColumnWidth(i, 175)
        self.ui.newItem.triggered.connect(lambda: addToFilial(self).show())
        self.ui.prihodNaklad.triggered.connect(lambda: prihodNaklad(self))

        # Формирование приходной накладной
        def prihodNaklad(self):
            selectQuery = "SELECT * FROM moving_to_filial"
            cursor.execute(selectQuery)
            filial_records = cursor.fetchall()
            for record in filial_records:
                name = record[1]
                selectQuery = f"""SELECT id FROM goods_codes WHERE name = '{name}'"""
                cursor.execute(selectQuery)
                id = cursor.fetchall() 
                if id == []:
                    cursor.execute('SELECT count(*) AS exact_count FROM goods_codes;')
                    length = int(re.sub('\D', ' ', str(cursor.fetchall())))
                    insertQuery = f"""INSERT INTO goods_codes (id, name) VALUES ('{length+1}', '{name}')"""
                    cursor.execute(insertQuery)
                    connection.commit() 
                selectQuery = f"""SELECT id FROM goods_codes WHERE name = '{name}'"""
                cursor.execute(selectQuery)
                code = cursor.fetchall()[0][0]
                makeLog("Code created", 'TRUE')
                selectQuery = f"""SELECT id FROM naklad WHERE name = '{name}'"""
                cursor.execute(selectQuery)
                id = cursor.fetchall() 
                if id == []:
                    cursor.execute('SELECT count(*) AS exact_count FROM naklad;')
                    length = int(re.sub('\D', ' ', str(cursor.fetchall())))
                    insertQuery = f"""INSERT INTO naklad (id, code, name, price, amount) VALUES ('{length+1}', '{code}', '{name}', '{record[2]}', '{record[3]}')"""
                    cursor.execute(insertQuery)
                    connection.commit()
                else:
                    updateQuery = f"""UPDATE naklad SET amount = amount + {record[3]} WHERE id = {id[0][0]}"""
                    cursor.execute(updateQuery)
                    connection.commit()
            makeExchange('moving_to_filial')
            query = f"SELECT * from moving_to_filial"
            outputquery = "COPY ({0}) TO STDOUT WITH CSV HEADER".format(query)
            with open(r'C:\Users\GreenDe\Desktop\VUZ\PIS (LABA)\Kurs\prihodNaklad.csv', 'w') as f:
                cursor.copy_expert(outputquery, f)
            self.master.populate()
            insertQuery = "DELETE FROM moving_to_filial"
            cursor.execute(insertQuery)
            connection.commit()
            makeLog("prihodNaklad created", 'TRUE')
            self.close()

# Окно добавления товаров в документ перемещение в филиал 
class addToFilial(QtWidgets.QMainWindow):
    def __init__(self, master):
        super(addToFilial,self).__init__()
        self.master = master
        self.ui = Ui_addToFilial()
        self.ui.setupUi(self)
        makeLog("addToFilial opened", 'TRUE')
        self.ui.pushButton.clicked.connect(lambda: self.addition())

    def addition(self):
        makeLog("addToFilial pushed", 'TRUE')
        length = self.master.ui.addedGoods.rowCount()
        self.master.ui.addedGoods.setRowCount(length+1)
        self.master.ui.addedGoods.setItem(length, 0, QTableWidgetItem(self.ui.name.text()))
        self.master.ui.addedGoods.setItem(length, 1, QTableWidgetItem(self.ui.price.text()))
        self.master.ui.addedGoods.setItem(length, 2, QTableWidgetItem(self.ui.amount.text()))
        insertQuery = f"""INSERT INTO moving_to_filial (id, name, price, amount) VALUES ('{length+1}', '{self.ui.name.text()}', '{self.ui.price.text()}', '{self.ui.amount.text()}')"""
        cursor.execute(insertQuery)
        connection.commit()
        self.close()

# Создание нового чека (покупки)
class newCheck(QtWidgets.QMainWindow):
    def __init__(self, master):
        super(newCheck,self).__init__()
        self.master = master
        self.ui = Ui_newCheck()
        self.ui.setupUi(self)
        makeLog("newCheck opened", 'TRUE')
        self.ui.addedGoods.setRowCount(0)
        self.ui.addedGoods.setColumnCount(5)
        self.ui.addedGoods.setHorizontalHeaderLabels(('Код отдела', 'Имя', 'Цена', 'Количество', 'Дата'))
        for i in range(5):
            self.ui.addedGoods.setColumnWidth(i, 175)
        self.ui.newItem.triggered.connect(lambda: addToCheck(self).show())
        self.ui.newCheck.triggered.connect(lambda: self.new_check())

    # Подтверждение нового чека
    def new_check(self):
        updateQuery = f"""DELETE FROM naklad WHERE amount = 0"""
        cursor.execute(updateQuery)
        connection.commit()
        self.master.populate()
        makeLog("newCheck created", 'TRUE')
        self.close()

# Окно добавления товаров в чек
class addToCheck(QtWidgets.QMainWindow):
    def __init__(self, master):
        super(addToCheck,self).__init__()
        self.master = master
        self.ui = Ui_addToCheck()
        self.ui.setupUi(self)
        makeLog("addToCheck opened", 'TRUE')
        self.ui.pushButton.clicked.connect(lambda: self.addition())

    def addition(self):
        selectQuery = f"""SELECT id FROM goods_codes WHERE name = '{self.ui.name.text()}'"""
        cursor.execute(selectQuery)
        id = cursor.fetchall()
        if id != []:
            amount = getdata('naklad', 'amount', id[0][0])
            price = getdata('naklad', 'price', id[0][0])
            if int(amount) >= int(self.ui.amount.text()) and int(price) <= int(self.ui.price.text()): 
                cursor.execute('SELECT count(*) AS exact_count FROM tovar_check;')
                length = int(re.sub('\D', ' ', str(cursor.fetchall())))
                self.master.ui.addedGoods.setRowCount(length+1)
                self.master.ui.addedGoods.setItem(length, 0, QTableWidgetItem(self.ui.otdelNum.text()))
                self.master.ui.addedGoods.setItem(length, 1, QTableWidgetItem(self.ui.name.text()))
                self.master.ui.addedGoods.setItem(length, 2, QTableWidgetItem(self.ui.price.text()))
                self.master.ui.addedGoods.setItem(length, 3, QTableWidgetItem(self.ui.amount.text()))
                self.master.ui.addedGoods.setItem(length, 4, QTableWidgetItem(self.ui.data.text()))
                insertQuery = f"""INSERT INTO tovar_check (id, otdel_code, name, price, amount, data) VALUES ('{length+1}', '{self.ui.otdelNum.text()}', '{self.ui.name.text()}', '{self.ui.price.text()}', '{self.ui.amount.text()}', '{self.ui.data.text()}')"""
                cursor.execute(insertQuery)
                connection.commit()
                updateQuery = f"""UPDATE naklad SET amount = amount - {self.ui.amount.text()} WHERE id = {id[0][0]}"""
                cursor.execute(updateQuery)
                connection.commit()
                makeLog("addToCheck pushed", 'TRUE')
                self.close()
            else:
                makeLog("ChooseDay pushed", 'FALSE')

# Окно выбора дня
class chooseDay(QtWidgets.QMainWindow):
    def __init__(self, master):
        super(chooseDay,self).__init__()
        self.master = master
        self.ui = Ui_chooseDay()
        self.ui.setupUi(self)
        makeLog("ChooseDay opened", 'TRUE')
        self.ui.pushButton.clicked.connect(lambda: self.select())

    def fillerfunc(self, prepdict):
        global outputwindow
        outputwindow.ui.tableWidget.clearContents()
        for item in prepdict:
            lenny = outputwindow.ui.tableWidget.rowCount()
            outputwindow.ui.tableWidget.setRowCount(lenny+1)
            outputwindow.ui.tableWidget.setItem(lenny, 0, QTableWidgetItem(item[0]))
            outputwindow.ui.tableWidget.setItem(lenny, 1, QTableWidgetItem(item[1]))
            outputwindow.ui.tableWidget.setItem(lenny, 2, QTableWidgetItem(item[2]))
            outputwindow.ui.tableWidget.setItem(lenny, 3, QTableWidgetItem(item[3]))
            outputwindow.ui.tableWidget.setItem(lenny, 4, QTableWidgetItem(item[4]))
        outputwindow.show()

    def select(self):
        needed = []
        length = self.master.ui.soldTable.rowCount()
        ss = self.ui.lineEdit.text().split()
        start = datetime.date(int(ss[0]), int(ss[1]), int(ss[2]))
        for i in range(length):
            td = self.master.ui.soldTable.item(i, 4).text().split()
            thisdate = datetime.date(int(td[0]), int(td[1]), int(td[2]))
            if start == thisdate:
                sum = str(int(self.master.ui.soldTable.item(i, 3).text()) * int(self.master.ui.soldTable.item(i, 2).text()))
                needed.append(['Филиал', self.master.ui.soldTable.item(i, 1).text(), self.master.ui.soldTable.item(i, 2).text(), self.master.ui.soldTable.item(i, 3).text(), sum])
        self.fillerfunc(needed)
        makeLog("ChooseDay pushed", 'TRUE')
        self.close()
    
# Формирование расходной накладной (отчета по продажам)
class outputRashodNaklad(QtWidgets.QMainWindow):
    def __init__(self):
        super(outputRashodNaklad,self).__init__()
        self.ui = Ui_outputRashodNaklad()
        self.ui.setupUi(self)
        self.ui.tableWidget.setColumnCount(5)
        self.ui.tableWidget.setHorizontalHeaderLabels(('Клиент', 'Имя', 'Цена', 'Количество', 'Итог'))

# Окно логов
class eventLog(QtWidgets.QMainWindow):
    def __init__(self, ):
        super(eventLog,self).__init__()
        self.ui = Ui_outputRashodNaklad()
        self.ui.setupUi(self)
        self.ui.tableWidget.setColumnCount(5)
        self.ui.tableWidget.setHorizontalHeaderLabels(('id', 'Дата', 'Событие', 'Успех'))

# Окно истории обмена
class history(QtWidgets.QMainWindow):
    def __init__(self):
        super(history,self).__init__()
        self.ui = Ui_outputRashodNaklad()
        self.ui.setupUi(self)
        self.ui.tableWidget.setColumnCount(4)
        self.ui.tableWidget.setHorizontalHeaderLabels(('id', 'Дата', 'Количество строк', 'Общая стоимость'))

# Основное окно
class bosswindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(bosswindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        makeLog("bosswindow opened", 'TRUE')
        self.ui.codesTable.setRowCount(0)
        self.ui.codesTable.setColumnCount(2)
        self.ui.codesTable.setHorizontalHeaderLabels(('Код', 'Имя'))
        for i in range(2):
            self.ui.codesTable.setColumnWidth(i, 175)
        self.ui.filialTable.setRowCount(0)
        self.ui.filialTable.setColumnCount(4)
        self.ui.filialTable.setHorizontalHeaderLabels(('Код', 'Имя', 'Цена', 'Количество'))
        for i in range(4):
            self.ui.filialTable.setColumnWidth(i, 175)
        self.ui.soldTable.setRowCount(0)
        self.ui.soldTable.setColumnCount(5)
        self.ui.soldTable.setHorizontalHeaderLabels(('Код отдела', 'Имя', 'Цена', 'Количество', 'Дата'))
        for i in range(5):
            self.ui.soldTable.setColumnWidth(i, 175)
        self.populate()
        self.ui.movingToFilial.triggered.connect(lambda: movingToFilial(self).show())
        self.ui.check.triggered.connect(lambda: newCheck(self).show())
        self.ui.svodNaklad.triggered.connect(lambda: chooseDay(self).show())
        self.ui.log.triggered.connect(lambda: self.fillLog())
        self.ui.history.triggered.connect(lambda: self.fillHistory())

    # Заполнение таблиц
    def populate(self):
        cursor.execute('SELECT count(*) AS exact_count FROM goods_codes;')
        tablesize = int(re.sub('\D', ' ', str(cursor.fetchall())))
        for i in range(tablesize):
            self.ui.codesTable.setRowCount(i+1)
            self.ui.codesTable.setItem(i, 0, QTableWidgetItem(getdata('goods_codes', 'id', i+1)))
            self.ui.codesTable.setItem(i, 1, QTableWidgetItem(getdata('goods_codes', 'name', i+1)))
        cursor.execute('SELECT count(*) AS exact_count FROM naklad;')
        tablesize = int(re.sub('\D', ' ', str(cursor.fetchall())))
        for i in range(tablesize):
            self.ui.filialTable.setRowCount(i+1)
            self.ui.filialTable.setItem(i, 0, QTableWidgetItem(getdata('naklad', 'code', i+1)))
            self.ui.filialTable.setItem(i, 1, QTableWidgetItem(getdata('naklad', 'name', i+1)))
            self.ui.filialTable.setItem(i, 2, QTableWidgetItem(getdata('naklad', 'price', i+1)))
            self.ui.filialTable.setItem(i, 3, QTableWidgetItem(getdata('naklad', 'amount', i+1)))
        cursor.execute('SELECT count(*) AS exact_count FROM tovar_check;')
        tablesize = int(re.sub('\D', ' ', str(cursor.fetchall())))
        for i in range(tablesize):
            self.ui.soldTable.setRowCount(i+1)
            self.ui.soldTable.setItem(i, 0, QTableWidgetItem(getdata('tovar_check', 'otdel_code', i+1)))
            self.ui.soldTable.setItem(i, 1, QTableWidgetItem(getdata('tovar_check', 'name', i+1)))
            self.ui.soldTable.setItem(i, 2, QTableWidgetItem(getdata('tovar_check', 'price', i+1)))
            self.ui.soldTable.setItem(i, 3, QTableWidgetItem(getdata('tovar_check', 'amount', i+1)))
            self.ui.soldTable.setItem(i, 4, QTableWidgetItem(getdata('tovar_check', 'data', i+1)))
        makeLog("bosswindow populated", 'TRUE')

    # Заполнение логов
    def fillLog(self):
        global logwindow
        logwindow.ui.tableWidget.clearContents()
        cursor.execute('SELECT count(*) AS exact_count FROM event_log;')
        tablesize = int(re.sub('\D', ' ', str(cursor.fetchall())))
        for i in range(tablesize):
            logwindow.ui.tableWidget.setRowCount(i+1)
            logwindow.ui.tableWidget.setItem(i, 0, QTableWidgetItem(getdata('event_log', 'id', i+1)))
            logwindow.ui.tableWidget.setItem(i, 1, QTableWidgetItem(getdata('event_log', 'data', i+1)))
            logwindow.ui.tableWidget.setItem(i, 2, QTableWidgetItem(getdata('event_log', 'event', i+1)))
            logwindow.ui.tableWidget.setItem(i, 3, QTableWidgetItem(getdata('event_log', 'successfully', i+1)))
        makeLog("eventLog opened", 'TRUE')
        logwindow.show()

    # Заполнение истории обмена
    def fillHistory(self):
        global historywindow
        historywindow.ui.tableWidget.clearContents()
        cursor.execute('SELECT count(*) AS exact_count FROM exchange_history;')
        tablesize = int(re.sub('\D', ' ', str(cursor.fetchall())))
        for i in range(tablesize):
            historywindow.ui.tableWidget.setRowCount(i+1)
            historywindow.ui.tableWidget.setItem(i, 0, QTableWidgetItem(getdata('exchange_history', 'id', i+1)))
            historywindow.ui.tableWidget.setItem(i, 1, QTableWidgetItem(getdata('exchange_history', 'data', i+1)))
            historywindow.ui.tableWidget.setItem(i, 2, QTableWidgetItem(getdata('exchange_history', 'length', i+1)))
            historywindow.ui.tableWidget.setItem(i, 3, QTableWidgetItem(getdata('exchange_history', 'result', i+1)))
        makeLog("history opened", 'TRUE')
        historywindow.show()
    
# Основной цикл
def main():
    global outputwindow
    global logwindow
    global historywindow
    app = QtWidgets.QApplication(sys.argv)
    outputwindow = outputRashodNaklad()
    logwindow = eventLog()
    historywindow = history()
    mainwindow = bosswindow()
    mainwindow.show()
    app.exec()

if __name__ == "__main__":
    main()

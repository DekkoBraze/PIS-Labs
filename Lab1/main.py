import psycopg2
import datetime
import tkinter as tk
import re
from tkinter import *
from tkinter.ttk import Combobox

# Заданные переменные
tablesizecust = 0
tablesizegoods = 0
tablesizeorders = 0
columnsetcust = ['name', 'totalbuys', 'currentaccount', 'maxcredint', 'currentdebt', 'creditremains', 'comments']
columnsetgoods = ['name', 'price', 'remaining']
columnsetorders = ['id', 'date', 'sum', 'customer', 'item']

# Берем данные из таблицы
def getdata(table, column, row):
    global cursor
    cursor.execute(f"""SELECT {column} FROM {table} WHERE name = '{row}'""")
    return str(cursor.fetchall()).replace('[', '').replace(']', '').replace('(', '').replace(')', '').replace(',', '').replace('\'', ' ')

# Вывод окна с клиентами
def displaycustomers():
    global tablesizecust
    global columnsetcust
    global customerswindow
    global widgetrefcust
    customerswindow = Tk()
    customerswindow.geometry('1080x880')
    customerswindow.title('Таблица клиентов')
    cursor.execute('SELECT count(*) AS exact_count FROM customers;')
    tablesizecust = int(re.sub('\D', ' ', str(cursor.fetchall())))
    widgetrefcust = []
    namelabel = Label(customerswindow, text='     Name    ')
    namelabel.grid(column=0, row=0)
    totalbuyslabel = Label(customerswindow, text='     Total Buys     ')
    totalbuyslabel.grid(column=1, row=0)
    currentaccountlabel = Label(customerswindow, text='    Current Account    ')
    currentaccountlabel.grid(column=2, row=0)
    maxcredintlabel = Label(customerswindow, text='   Max Credit  ')
    maxcredintlabel.grid(column=3, row=0)
    currentdebtlabel = Label(customerswindow, text='   Current Debt   ')
    currentdebtlabel.grid(column=4, row=0)
    creditremains = Label(customerswindow, text='  Remaining Credit   ')
    creditremains.grid(column=5, row=0)
    commentslabel = Label(customerswindow, text='  Comments  ')
    commentslabel.grid(column=6, row=0)
    for i in range(tablesizecust):
        collie = 0
        for col in columnsetcust:
            cursor.execute('SELECT ' + col + ' FROM customers ORDER BY name ASC OFFSET ' + str(i) + ' LIMIT 1')
            currentdata = str(cursor.fetchall()).replace('[', '').replace(']', '').replace('(', '').replace(')', '').replace(',', '').replace('\'', ' ')
            curelem = Label(customerswindow, text=str(currentdata))
            curelem.grid(column=collie, row=i+1)
            widgetrefcust.append(curelem)
            collie += 1
    addcustomer = Button(customerswindow, text='Добавить', command=newcustomer)
    addcustomer.grid(column=7, row=0)
    customerswindow.mainloop()

# Создание нового клиента при нажатии на кнопку
def newcustomer():
    global customerswindow
    global cursor
    global connection
    global confirmbuttoncust
    newcustname = Entry(customerswindow, width=14)
    newcustname.grid(column=0, row=tablesizecust+1)
    newcustbuys = Label(customerswindow, text='0')
    newcustbuys.grid(column=1, row=tablesizecust+1)
    newcustacc = Entry(customerswindow, width=14)
    newcustacc.grid(column=2, row=tablesizecust+1)
    newcustmcred = Label(customerswindow, text='140')
    newcustmcred.grid(column=3, row=tablesizecust+1)
    newcustcdebt = Label(customerswindow, text='0')
    newcustcdebt.grid(column=4, row=tablesizecust+1)
    newcustrem = Label(customerswindow, text='0')
    newcustrem.grid(column=5, row=tablesizecust+1)
    newcustcomm = Entry(customerswindow, width=14)
    newcustcomm.grid(column=6, row=tablesizecust+1)
    confirmbuttoncust = Button(customerswindow, text='Подтвердить добавление', command=lambda: [confirmcustaddition(str(newcustname.get()), str(newcustbuys.cget('text')), str(newcustacc.get()), str(newcustmcred.cget('text')), str(newcustcdebt.cget('text')), str(newcustrem.cget('text')), str(newcustcomm.get())),
                                                                                             newcustname.destroy(), newcustbuys.destroy(), newcustcomm.destroy(), newcustrem.destroy(), newcustcdebt.destroy(), newcustacc.destroy(), newcustmcred.destroy(), refreshcustomers()])
    confirmbuttoncust.grid(column=7, row=2)

# Добавление клиента в базу данных
def confirmcustaddition(name, buys, acc, mcred, cdebt, rem, comm):
    global customerswindow
    global cursor
    global connection
    global confirmbuttoncust
    insert_query = f"""INSERT INTO customers (name, totalbuys, currentaccount, maxcredint, currentdebt, creditremains, comments)
       VALUES ('{name}', {buys}, {acc}, {mcred}, {cdebt}, {rem}, '{comm}');"""
    cursor.execute(insert_query)
    connection.commit()
    confirmbuttoncust.destroy()

# Обновление списка клиентов
def refreshcustomers():
    global customerswindow
    global connection
    global cursor
    global widgetrefcust
    cursor.execute('SELECT count(*) AS exact_count FROM customers;')
    tablesizecust = int(re.sub('\D', ' ', str(cursor.fetchall())))
    for label in widgetrefcust:
        label.destroy()
    widgetrefcust.clear()
    for i in range(tablesizecust):
        collie = 0
        for col in columnsetcust:
            cursor.execute('SELECT ' + col + ' FROM customers OFFSET ' + str(i) + ' LIMIT 1')
            currentdata = str(cursor.fetchall()).replace('[', '').replace(']', '').replace('(', '').replace(')',
                                                                                                            '').replace(
                ',',
                '').replace(
                '\'', ' ')
            curelem = Label(customerswindow, text=str(currentdata))
            curelem.grid(column=collie, row=i+1)
            widgetrefcust.append(curelem)
            collie += 1

# Отображение таблицы с товарами
def displaygoods():
    global tablesizegoods
    global columnsetgoods
    global goodswindow
    global widgetrefgoods
    goodswindow = Tk()
    goodswindow.geometry('1080x880')
    goodswindow.title('Таблица товаров')
    cursor.execute('SELECT count(*) AS exact_count FROM goods;')
    tablesizegoods = int(re.sub('\D', ' ', str(cursor.fetchall())))
    widgetrefgoods = []
    namelabel = Label(goodswindow, text='     Name    ')
    namelabel.grid(column=0, row=0)
    pricelabel = Label(goodswindow, text='Цена')
    pricelabel.grid(column=1, row=0)
    remaininglabel = Label(goodswindow, text='Остаток')
    remaininglabel.grid(column=2, row=0)
    for i in range(tablesizegoods):
        collie = 0
        for col in columnsetgoods:
            cursor.execute('SELECT ' + col + ' FROM goods ORDER BY name ASC OFFSET ' + str(i) + ' LIMIT 1')
            currentdata = str(cursor.fetchall()).replace('[', '').replace(']', '').replace('(', '').replace(')',
                                                                                                            '').replace(
                ',', '').replace('\'', ' ')
            curelem = Label(goodswindow, text=str(currentdata))
            curelem.grid(column=collie, row=i + 1)
            widgetrefgoods.append(curelem)
            collie += 1
    additem = Button(goodswindow, text='Добавить', command=newitem)
    additem.grid(column=7, row=0)
    goodswindow.mainloop()

# Добавление товара
def newitem():
    global goodswindow
    global cursor
    global connection
    global confirmbuttongoods
    newgoodsname = Entry(goodswindow, width=14)
    newgoodsname.grid(column=0, row=tablesizegoods + 1)
    newgoodsprice = Entry(goodswindow, width=14)
    newgoodsprice.grid(column=1, row=tablesizegoods + 1)
    newgoodsrem = Entry(goodswindow, width=14)
    newgoodsrem.grid(column=2, row=tablesizegoods + 1)
    confirmbuttongoods = Button(goodswindow, text='Подтвердить добавление', command=lambda: [
    confirmgoodsaddition(str(newgoodsname.get()), str(newgoodsprice.get()), str(newgoodsrem.get())), ItemCheck(str(newgoodsname.get()), str(newgoodsprice.get()), str(newgoodsrem.get())),
        newgoodsname.destroy(), newgoodsprice.destroy(), newgoodsrem.destroy(), refreshgoods()])
    confirmbuttongoods.grid(column=3, row=2)

def ItemCheck(newgoodsname, newgoodsprice, newgoodsrem):
    if (str(newgoodsname) == "" or str(newgoodsprice) == "" or str(newgoodsrem) == ""):
        errorLabel = Label(goodswindow, text="Ошибка! Одно из значений не введено.")
        errorLabel.grid(column=5, row=5)

# Подтверждение добавления товара
def confirmgoodsaddition(name, price, rem):
    if (name != "" and price != "" and rem != ""):
        global goodswindow
        global cursor
        global connection
        global confirmbuttongoods
        insert_query = f"""INSERT INTO goods (name, price, remaining)
            VALUES ('{name}', {price}, {rem});"""
        cursor.execute(insert_query)
        connection.commit()
        confirmbuttongoods.destroy()
    

# Обновление таблицы с товарами
def refreshgoods():
    global goodswindow
    global connection
    global cursor
    global widgetrefgoods
    global tablesizegoods
    cursor.execute('SELECT count(*) AS exact_count FROM goods;')
    tablesizegoods = int(re.sub('\D', ' ', str(cursor.fetchall())))
    for label in widgetrefgoods:
        label.destroy()
    widgetrefgoods.clear()
    for i in range(tablesizegoods):
        collie = 0
        for col in columnsetgoods:
            cursor.execute('SELECT ' + col + ' FROM goods OFFSET ' + str(i) + ' LIMIT 1')
            currentdata = str(cursor.fetchall()).replace('[', '').replace(']', '').replace('(', '').replace(')',
                                                                                                            '').replace(
                ',',
                '').replace(
                '\'', ' ')
            curelem = Label(goodswindow, text=str(currentdata))
            curelem.grid(column=collie, row=i + 1)
            widgetrefgoods.append(curelem)
            collie += 1

# Отображение таблицы с заказами
def displayorders():
    global tablesizeorders
    global columnsetorders
    global orderswindow
    global widgetreforders
    orderswindow = Tk()
    orderswindow.geometry('1080x880')
    orderswindow.title('Таблица заказов')
    cursor.execute('SELECT count(*) AS exact_count FROM orders;')
    tablesizeorders = int(re.sub('\D', ' ', str(cursor.fetchall())))
    widgetreforders = []
    idlabel = Label(orderswindow, text='     ID    ')
    idlabel.grid(column=0, row=0)
    datelabel = Label(orderswindow, text='    Дата    ')
    datelabel.grid(column=1, row=0)
    sumlabel = Label(orderswindow, text='  Сумма заказа  ')
    sumlabel.grid(column=2, row=0)
    customerLabel = Label(orderswindow, text='    Покупатель    ')
    customerLabel.grid(column=3, row=0)
    itemLabel = Label(orderswindow, text='     Товар     ')
    itemLabel.grid(column=4, row=0)
    for i in range(tablesizeorders):
        collie = 0
        for col in columnsetorders:
            cursor.execute('SELECT ' + col + ' FROM orders ORDER BY id ASC OFFSET ' + str(i) + ' LIMIT 1')
            if col=='date':
                currentdata = str(cursor.fetchall()).replace('[', '').replace(']', '').replace('(', '').replace(')',
                                                                                                                '').replace(
                    ',', '').replace('\'', ' ').replace('d', '').replace('a', '').replace('t', '').replace('e', '').replace('i', '').replace('m','').replace('.', '')
            else:
                currentdata = str(cursor.fetchall()).replace('[', '').replace(']', '').replace('(', '').replace(')',
                                                                                                            '').replace(
                ',', '').replace('\'', ' ')
            curelem = Label(orderswindow, text=str(currentdata))
            curelem.grid(column=collie, row=i + 1)
            widgetreforders.append(curelem)
            collie += 1
    additem = Button(orderswindow, text='Добавить', command=neworder)
    additem.grid(column=7, row=0)
    orderswindow.mainloop()

# Новый заказ
def neworder():
    global orderswindow
    global cursor
    global connection
    global confirmbuttonorders
    global tablesizeorders
    neworderid = Label(orderswindow, text=str(tablesizeorders+1))
    neworderid.grid(column=0, row=tablesizeorders+1)
    neworderdate = Label(orderswindow, text=str(datetime.date.today()))
    neworderdate.grid(column=1, row=tablesizeorders+1)
    newordersum = Entry(orderswindow, width=14)
    newordersum.grid(column=2, row=tablesizeorders+1)
    newordercust = Entry(orderswindow, width=14)
    newordercust.grid(column=3, row=tablesizeorders+1)
    neworderitem = Entry(orderswindow, width=14)
    neworderitem.grid(column=4, row=tablesizeorders+1)
    ordertype = Combobox(orderswindow, width=14, values=('Наличный рассчёт', 'Безналичный рассчёт', 'Кредит', 'Бартер', 'Взаимозачёт'))
    ordertype.grid(column=6, row=tablesizeorders+1)
    confirmbuttonorders = Button(orderswindow, text='Подтвердить добавление', command=lambda: [
        confirmordersaddition(str(neworderid.cget('text')), str(neworderdate.cget('text')), str(newordersum.get()),
        str(newordercust.get()), str(neworderitem.get()), str(ordertype.get())), neworderid.destroy(), neworderdate.destroy(),
        newordersum.destroy(), newordercust.destroy(), neworderitem.destroy(), ordertype.destroy()])
    confirmbuttonorders.grid(column=6, row=2)

# Подтверждение нового заказа
def confirmordersaddition(idd, date, summ, cust, item, typee):
    global orderswindow
    global cursor
    global connection
    global confirmbuttonorders
    itemprice = getdata('goods', 'price', item)
    itemrem = getdata('goods', 'remaining', item)
    customertotal = getdata('customers', 'totalbuys', cust)
    customeraccount = getdata('customers', 'currentaccount', cust)
    customercurrentdebt = getdata('customers', 'currentdebt', cust)
    customercredremains = getdata('customers', 'creditremains', cust)
    canRefresh = False
    match typee:
        case 'Наличный рассчёт':
            cursor.execute(f"""UPDATE goods SET remaining={int(itemrem) - int(summ)/int(itemprice)} WHERE name='{item}'""")
            connection.commit()
            cursor.execute(f"""UPDATE customers SET totalbuys={int(customertotal)+int(summ)} WHERE name='{cust}'""")
            connection.commit()
            canRefresh = True
        case 'Безналичный рассчёт':
            if int(customeraccount) >= int(summ) and int(itemrem) >= int(summ) / int(itemprice):
                cursor.execute(f"""UPDATE goods SET remaining={int(itemrem) - int(summ) / int(itemprice)} WHERE name='{item}'""")
                connection.commit()
                cursor.execute(f"""UPDATE customers SET totalbuys={int(customertotal) + int(summ)} WHERE name='{cust}'""")
                connection.commit()
                cursor.execute(f"""UPDATE customers SET currentaccount={int(customeraccount)-int(summ)} WHERE NAME='{cust}'""")
                connection.commit()
                canRefresh = True
            else:
                errorLabel = Label(orderswindow, text="Ошибка! У клиента недостаточно средств, либо товар на складе закончился.")
                errorLabel.grid(column=5, row=5)
        case 'Кредит':
            if int(customercredremains) >= int(summ) and int(itemrem) >= int(summ) / int(itemprice):
                cursor.execute(f"""UPDATE goods SET remaining={int(itemrem) - int(summ) / int(itemprice)} WHERE name='{item}'""")
                connection.commit()
                cursor.execute(f"""UPDATE customers SET totalbuys={int(customertotal) + int(summ)} WHERE name='{cust}'""")
                connection.commit()
                cursor.execute(f"""UPDATE customers SET currentdebt={int(customercurrentdebt) + int(summ)} WHERE name='{cust}'""")
                connection.commit()
                cursor.execute(f"""UPDATE customers SET creditremains={int(customercredremains) - int(summ)} WHERE name='{cust}'""")
                connection.commit()
                if (abs(int(customercurrentdebt) * 0.9) >= int(customercredremains)):
                    errorLabel = Label(orderswindow, text="Внимание! Кредитные средства клиента подходят к концу.")
                    errorLabel.grid(column=5, row=5)
                canRefresh = True
            else:
                errorLabel = Label(orderswindow, text="Ошибка! У клиента недостаточно средств, либо товар на складе закончился.")
                errorLabel.grid(column=5, row=5)
        case "Бартер":
            global barterconfirm
            global barteritem
            global barterwindow
            barterwindow = Tk()
            barterwindow.title('Введите товар, который хотите обменять')
            barterwindow.geometry('400x100')
            barteritem = Entry(barterwindow, width=20)
            barteritem.grid(column=0, row=0)
            barterconfirm = Button(barterwindow, text='Подтвердить', command=lambda: barterconfirmation(item, summ, int(itemprice), int(itemrem)))
            barterconfirm.grid(column=1, row=0)
            barterwindow.mainloop()
            canRefresh = True
        case 'Взаимозачёт':
            cursor.execute(f"""UPDATE goods SET remaining={int(itemrem) + int(summ) / int(itemprice)} WHERE name='{item}'""")
            connection.commit()
            cursor.execute(f"""UPDATE customers SET currentdebt={int(customercurrentdebt) - int(summ)} WHERE name='{cust}'""")
            connection.commit()
            cursor.execute(f"""UPDATE customers SET creditremains={int(customercredremains) + int(summ)} WHERE name='{cust}'""")
            connection.commit()
            if (int(customercurrentdebt) * 0.9 >= int(customercredremains)):
                    errorLabel = Label(orderswindow, text="Внимание! Кредитные средства клиента подходят к концу.")
                    errorLabel.grid(column=5, row=5)
            canRefresh = True
    insert_query = f"""INSERT INTO orders (id, date, sum, customer, item)
       VALUES ('{idd}', '{date}', {summ}, '{cust}', '{item}');"""
    if (canRefresh):
        refreshorders()
    cursor.execute(insert_query)
    connection.commit()
    confirmbuttonorders.destroy()

# Подтверждение операции бартера
def barterconfirmation(itemselling, summa, priceselling, remainingselling):
    global barterwindow
    global barteritem
    global barterconfirm
    global cursor
    global connection
    barterconfirm.destroy()
    item = str(barteritem.get())
    barteritem.destroy()
    barterwindow.destroy()
    itemcost = getdata('goods', 'price', item)
    itemrem = getdata('goods', 'remaining', item)
    if (remainingselling > summa):
        cursor.execute(f"""UPDATE goods SET remaining={remainingselling - int(summa) / priceselling} WHERE name='{itemselling}'""")
    else:
        errorLabel = Label(orderswindow, text="Ошибка! Товара на складе недостаточно.")
        errorLabel.grid(column=5, row=5)
    connection.commit()
    cursor.execute(f"""UPDATE goods SET remaining={int(itemrem) + int(summa)/int(itemcost)} WHERE name='{item}'""")
    connection.commit()

# Обновление таблицы с заказами
def refreshorders():
    global orderswindow
    global connection
    global cursor
    global widgetreforders
    global tablesizeorders
    cursor.execute('SELECT count(*) AS exact_count FROM orders;')
    tablesizeorders = int(re.sub('\D', ' ', str(cursor.fetchall())))
    for label in widgetreforders:
        label.destroy()
    widgetreforders.clear()
    for i in range(tablesizeorders):
        collie = 0
        for col in columnsetorders:
            cursor.execute('SELECT ' + col + ' FROM orders OFFSET ' + str(i) + ' LIMIT 1')
            currentdata = str(cursor.fetchall()).replace('[', '').replace(']', '').replace('(', '').replace(')',
                                                                                                            '').replace(
                ',',
                '').replace(
                '\'', ' ')
            curelem = Label(orderswindow, text=str(currentdata))
            curelem.grid(column=collie, row=i + 1)
            widgetreforders.append(curelem)
            collie += 1

# Создание коннекта
connection = psycopg2.connect(user="postgres", password="12345", host="127.0.0.1", port="5432", database="list1")
cursor = connection.cursor()

# Создание окна с выбором таблиц
mainwindow = Tk()
mainwindow.geometry('1080x720')
mainwindow.title('Menu')
tableslabel = Label(mainwindow, text='Просмотр таблиц')
tableslabel.grid(column=0, row=0)
customersbutton = Button(mainwindow, text='Таблица клиентов', command=displaycustomers, width=20)
customersbutton.grid(column=0, row=1)
itemsbutton = Button(mainwindow, text='Таблица товаров', command=displaygoods, width=20).grid(column=0, row=2)
ordersbutton = Button(mainwindow, text='Таблица заказов', command=displayorders, width=20).grid(column=0,row=3)
mainwindow.mainloop()
import tkinter as tk
from tkinter import *
import random


def create(name, group, number, disc, baseprice, buyprice):
    number = int(number)
    #group = int(group)
    number = int(number)
    disc = int(disc)
    baseprice = int(baseprice)
    buyprice = int(buyprice)
    with open(r'C:\Users\GreenDe\Desktop\VUZ\PIS (LABA)\Lab3\out.txt', mode='a') as out:
        out.write(f"{name} {group} {number} {baseprice} {buyprice} {disc}")
        out.write('\n')
        


window = Tk()
window.geometry('600x200')
window.title("Задание товара")
namelabel = Label(window, text='Имя').grid(column=0, row =0)
nameentry = Entry(window)
nameentry.grid(column=1, row=0, columnspan=2)
grouplabel = Label(window, text='Группа').grid(column=0, row =1)
groupentry = Entry(window)
groupentry.grid(column=1, row=1, columnspan=2)
numberlabel = Label(window, text='Количество').grid(column=0, row =2)
numberentry = Entry(window)
numberentry.grid(column=1, row=2, columnspan=2)
basepricelabel = Label(window, text='Цена продажи').grid(column=3, row =0)
basepriceentry = Entry(window)
basepriceentry.grid(column=4, row=0, columnspan=2)
buyprice = Label(window, text='Цена закупки').grid(column=3, row =1)
buypriceentry = Entry(window)
buypriceentry.grid(column=4, row=1, columnspan=2)
disclabel = Label(window, text='Скидка').grid(column=3, row =2)
discentry = Entry(window)
discentry.grid(column=4, row=2, columnspan=2)
# pricelabel = Label(window, text='Закупочная цена').grid(column=3, row =2)
# priceentry = Entry(window).grid(column=4, row=2, columnspan=2)
acceptbutton = Button(window, text='Создать', command= lambda: create(nameentry.get(), groupentry.get(), numberentry.get(), discentry.get(), basepriceentry.get(), buypriceentry.get()))
acceptbutton.grid(column=0, row=3)
window.mainloop()
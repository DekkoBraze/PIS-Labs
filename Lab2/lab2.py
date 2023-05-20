import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
import math as m
import pyglet
from tkinter import *
from tkinter.ttk import Combobox

lst = []
lstOtbor = []

def InputFloat(num):
    lst.append(num)
    if len(lst) > 1 and (lst[-2] * (1/5) <= abs(lst[-2] - lst[-1])):
        music = pyglet.resource.media('sound.wav')
        music.play()
    mid = np.mean(lst)
    x = [i for i in range(0, len(lst))]
    midAr = []
    for i in range(0, len(lst)):
        midAr.append(mid)
    plt.plot(x, lst)
    plt.plot(x, midAr)
    plt.show()
    RefreshLst()

def OtborPoNiz(num):
    lstOtbor = []
    for i in lst:
        if i >= num:
            lstOtbor.append(i)
    mid = np.mean(lstOtbor)
    x = [i for i in range(0, len(lstOtbor))]
    midAr = []
    for i in range(0, len(lstOtbor)):
        midAr.append(mid)
    plt.plot(x, lstOtbor)
    plt.plot(x, midAr)
    plt.show()
    curelem1 = Label(mainwindow, text=str(lstOtbor))
    curelem1.grid(column=5, row=1)

def OtborPoVerh(num):
    lstOtbor = []
    for i in lst:
        if i <= num:
            lstOtbor.append(i)
    mid = np.mean(lstOtbor)
    x = [i for i in range(0, len(lstOtbor))]
    midAr = []
    for i in range(0, len(lstOtbor)):
        midAr.append(mid)
    plt.plot(x, lstOtbor)
    plt.plot(x, midAr)
    plt.show()
    curelem1 = Label(mainwindow, text=str(lstOtbor))
    curelem1.grid(column=5, row=1)

def OtborMod(num):
    lstOtbor = []
    for i in lst:
        if i % num == 0:
            lstOtbor.append(i)
    mid = np.mean(lstOtbor)
    x = [i for i in range(0, len(lstOtbor))]
    midAr = []
    for i in range(0, len(lstOtbor)):
        midAr.append(mid)
    plt.plot(x, lstOtbor)
    plt.plot(x, midAr)
    #plt.bar(len(lstOtbor), lstOtbor)
    plt.show()
    curelem1 = Label(mainwindow, text=str(lstOtbor))
    curelem1.grid(column=5, row=1)

def RefreshLst():
    global mainwindow
    curelem = Label(mainwindow, text=str(lst))
    curelem.grid(column=5, row=0)

def RefreshLstOtbor():
    global mainwindow
    curelem = Label(mainwindow, text=str(lstOtbor))
    curelem.grid(column=5, row=1)

global mainwindow
mainwindow = Tk()
mainwindow.geometry('1080x720')
mainwindow.title('Menu')

tableslabel = Label(mainwindow, text='Ввод значения')
tableslabel.grid(column=0, row=0)
newfloat = Entry(mainwindow, width=14)
newfloat.grid(column=0, row=1)
addfloat = Button(mainwindow, text='Добавить', command=lambda: [InputFloat(int(newfloat.get()))])
addfloat.grid(column=0, row=2)

otborPoNizGran = Label(mainwindow, text='Отбор по нижней границе')
otborPoNizGran.grid(column=0, row=3)
newfloat1 = Entry(mainwindow, width=14)
newfloat1.grid(column=0, row=4)
addfloat1 = Button(mainwindow, text='Отобрать', command=lambda: [OtborPoNiz(int(newfloat1.get()))])
addfloat1.grid(column=0, row=5)

otborPoVerh= Label(mainwindow, text='Отбор по верхней границе')
otborPoVerh.grid(column=0, row=6)
newfloat2 = Entry(mainwindow, width=14)
newfloat2.grid(column=0, row=7)
addfloat2 = Button(mainwindow, text='Отобрать', command=lambda: [OtborPoVerh(int(newfloat2.get()))])
addfloat2.grid(column=0, row=8)

otborMod= Label(mainwindow, text='Отбор по кратности')
otborMod.grid(column=0, row=9)
newfloat3 = Entry(mainwindow, width=14)
newfloat3.grid(column=0, row=10)
addfloat3 = Button(mainwindow, text='Отобрать', command=lambda: [OtborMod(int(newfloat3.get()))])
addfloat3.grid(column=0, row=11)

arrayText = Label(mainwindow, text=str(lst))
arrayText.grid(column=5, row=0)

arrayText1 = Label(mainwindow, text=str(lstOtbor))
arrayText1.grid(column=5, row=1)
#drawGraf = Button(mainwindow, text='График', command=DrawGraf)
#drawGraf.grid(column=0, row=3)
mainwindow.mainloop()

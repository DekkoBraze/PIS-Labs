from mainwindow import Ui_MainWindow
from PyQt6 import QtWidgets
import sys
import math
from numpy import exp
from matplotlib import pyplot as plt
import numexpr as ne

# Главное окно
class bosswindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(bosswindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(lambda: self.clicker())
    
    # Основная функция вывода
    def clicker(self):
        vars = []
        # Получаем ограничения графика
        leftlimit = int(self.ui.lineEdit.text())
        rightlimit = int(self.ui.lineEdit_2.text())
        diff = rightlimit - leftlimit
        x = [leftlimit + i for i in range(diff+1)]
        y = x.copy()
        vars.append(self.ui.comboBox.currentData())
        vars.append(self.ui.comboBox_2.currentData())
        vars.append(self.ui.comboBox_3.currentData())
        # Цикл проходит по всем нашим функциям, обрабатывая массивы x и y. Следующей функции передается результат старой
        for item in vars:
            if item == 'a':
                temp1=[]
                temp2=[]
                line1 = str(self.ui.lineEdit_5.text())
                line2 = str(self.ui.lineEdit_4.text())
                line3 = str(self.ui.lineEdit_3.text())
                for x_axis, x in zip(x,y):
                    try:
                        temp2.append(ne.evaluate(line1))
                        temp1.append(x_axis)
                    except:
                        print("Вне зоны допустимых значений: ", x)
                x = temp1.copy()
                y = temp2.copy()
            elif item == 'b':
                temp1=[]
                temp2=[]
                for x_axis, x in zip(x,y):
                    try:
                        temp2.append(math.sqrt(x))
                        temp1.append(x_axis)
                    except:
                        print("Вне зоны допустимых значений: ", x)
                x = temp1.copy()
                y = temp2.copy()
            elif item == 'c':
                temp1=[]
                temp2=[]
                for x_axis, x in zip(x,y):
                    try:
                        temp2.append(math.log(x))
                        temp1.append(x_axis)
                    except:
                        print("Вне зоны допустимых значений: ", x)
                x = temp1.copy()
                y = temp2.copy()
        plt.plot(x, y)
        plt.show()
        self.close()

# Основной цикл
def main():
    app = QtWidgets.QApplication(sys.argv)
    mainwindow = bosswindow()
    mainwindow.show()
    app.exec()

if __name__ == "__main__":
    main()
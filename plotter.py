from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

class SecondWindow(QtWidgets.QMainWindow):
    def __init__(self,xlist,ylist):
        super(SecondWindow, self).__init__()
        self.main_widget = QtWidgets.QWidget(self)
        self.setWindowTitle("result")
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        QtWidgets.QVBoxLayout(self.main_widget)
        sc = MplCanvas(self, width=5, height=4, dpi=100)
        sc.axes.plot(xlist, ylist)
        self.setCentralWidget(sc)

class Ui_MainWindow(object):

    def isNotValid(self,character,prev):
        if character == '*':
            if prev == '*':
                prev = character
                return True
            prev = '*'
            return False
        prev = character
        if character == ' ' or character.isnumeric() or character == "-" or character == '/' or character == '+'or character == "^" or character == 'x':
            return False
        return True
    
    def isValidFunction(self):
        function = self.function.text().strip()
        prev = '+'
        if function == "":
            self.showErrorMessage("please input the function you want to plot")
            self.function.setFocus()
            return False
        for character in function:
            if self.isNotValid(character,prev):
                self.showErrorMessage("The equation must be function of (x) with supported operators(+ - / * ^) and valid syntax")
                self.function.setFocus()
                return False
        return True  

    def showErrorMessage(self,errorMessage):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("INVALID INPUT")
        msg.setWindowIcon(QtGui.QIcon("warning.png"))
        msg.setText(errorMessage)
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.exec()
        
    def check_if_number(self,num):
        try:
            int(num)
            return True
        except:
            return False

    def check_x_values(self):
        if self.max_x.text() == "":
            self.showErrorMessage("please input the maximum value of x")
            self.max_x.setFocus()
            return False
        if self.min_x.text() == "":
            self.showErrorMessage("please input the minimum value of x")
            self.min_x.setFocus()
            return False
            
        if not self.check_if_number(self.max_x.text()):
            self.showErrorMessage("The maximum value of x is not a number")
            self.max_x.setText("")
            return False
        if not self.check_if_number(self.min_x.text()):
            self.showErrorMessage("The minimum value of x is not a number")
            self.min_x.setText("")
            return False
        if int(self.max_x.text()) <= int(self.min_x.text()):
            self.showErrorMessage("The maximum value of x has to be smaller than the minimum value of x")
            self.min_x.setFocus()
            return False
        return True

    def clicked(self):
        if not self.isValidFunction():
            return
        function = self.function.text().replace("^","**")
        if not self.check_x_values():
            return
        xlist = np.linspace(int(self.min_x.text()),int(self.max_x.text()),num=1000)
        ylist =[]
        try:
            ylist = eval(function, {'x': xlist})
        except:
            self.showErrorMessage("There is a syntax error in the entered function")
            self.function.setFocus()
            return
        self.SW = SecondWindow(xlist,ylist)
        self.SW.resize(550,480)
        self.SW.show()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(641, 729)
        MainWindow.setStyleSheet("#MainWindow{\n"
"    background-color:#2155CD;\n"
"}\n"
"#mainFrame{\n"
"    width:100%;\n"
"    padding:50px\n"
"}\n"
"#MMvalues\n"
"{\n"
"    padding:0\n"
"}\n"
"#program_title\n"
"{\n"
"    color: #fff;\n"
"    font-size:50px;\n"
"    font-weight:600;\n"
"}\n"
"QLabel{\n"
"    color:#fff;\n"
"    font-size:20px;\n"
"    margin:20px 0px 8px\n"
"}\n"
"#plotButton\n"
"{\n"
"    background-color:#fff;\n"
"    font-size: 25px;\n"
"    border-radius:3px;\n"
"    padding: 13px 0;\n"
"}\n"
"QLineEdit\n"
"{\n"
"    padding: 14px 16px;\n"
"    font-size: 15px;\n"
"    border-radius:3px;\n"
"}\n"
"#min_x{\n"
"    margin-bottom:35px\n"
"}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.mainFrame = QtWidgets.QFrame(self.centralwidget)
        self.mainFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.mainFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.mainFrame.setObjectName("mainFrame")
        self.formLayout = QtWidgets.QFormLayout(self.mainFrame)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.mainFrame)
        self.label.setObjectName("label")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.SpanningRole, self.label)
        self.function = QtWidgets.QLineEdit(self.mainFrame)
        self.function.setText("")
        self.function.setObjectName("Function")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.SpanningRole, self.function)
        self.label_2 = QtWidgets.QLabel(self.mainFrame)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.max_x = QtWidgets.QLineEdit(self.mainFrame)
        self.max_x.setObjectName("max_x")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.SpanningRole, self.max_x)
        self.label_3 = QtWidgets.QLabel(self.mainFrame)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.min_x = QtWidgets.QLineEdit(self.mainFrame)
        self.min_x.setObjectName("min_x")
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.SpanningRole, self.min_x)
        self.plotButton = QtWidgets.QPushButton(self.mainFrame)
        self.plotButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.plotButton.setObjectName("plotButton")
        self.formLayout.setWidget(9, QtWidgets.QFormLayout.SpanningRole, self.plotButton)
        self.program_title = QtWidgets.QLabel(self.mainFrame)
        self.program_title.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.program_title.setAlignment(QtCore.Qt.AlignCenter)
        self.program_title.setObjectName("program_title")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.program_title)
        self.gridLayout.addWidget(self.mainFrame, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.plotButton.clicked.connect(self.clicked)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowIcon(QtGui.QIcon('icon.png'))
        MainWindow.setWindowTitle(_translate("MainWindow", "Plotter"))
        self.label.setText(_translate("MainWindow", "Function"))
        self.function.setPlaceholderText(_translate("MainWindow", "Enter the desired function ..."))
        self.label_2.setText(_translate("MainWindow", "X max value"))
        self.max_x.setPlaceholderText(_translate("MainWindow", "Enter the maximum value of x ..."))
        self.label_3.setText(_translate("MainWindow", "X min value"))
        self.min_x.setPlaceholderText(_translate("MainWindow", "Enter the minimum value of x ..."))
        self.plotButton.setText(_translate("MainWindow", "Plot"))
        self.program_title.setText(_translate("MainWindow", "Function Plotter "))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

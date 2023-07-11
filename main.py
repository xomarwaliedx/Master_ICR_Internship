import sys
from PySide6.QtWidgets import QApplication, QMessageBox, QMainWindow, QWidget, QGridLayout, QLineEdit, QPushButton, QLabel
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Slot
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import numpy as np

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        central_widget = QWidget(self)
        # making grid layout
        layout = QGridLayout(central_widget)
        # Logo
        logo_label = QLabel()
        logo_pixmap = QPixmap("logo.png")
        logo_pixmap = logo_pixmap.scaled(188, 47)
        logo_label.setPixmap(logo_pixmap)
        layout.addWidget(logo_label, 0, 2, 2, 1)
        # text boxes labels
        label1 = QLabel("Equation:")
        layout.addWidget(label1, 0, 0)
        label2 = QLabel("X1:")
        layout.addWidget(label2, 1, 0)
        label3 = QLabel("X2:")
        layout.addWidget(label3, 2, 0)
        # error label
        self.error_label = QLabel(self)
        self.error_label.setStyleSheet("color: red;")
        layout.addWidget(self.error_label, 2, 2)
        #text boxes
        self.text_box_eq = QLineEdit()
        self.text_box_eq.textChanged.connect(self.update_graph_live)
        self.text_box_eq.returnPressed.connect(self.update_graph)
        layout.addWidget(self.text_box_eq, 0, 1)
        self.text_box_x_min = QLineEdit()
        self.text_box_x_min.textChanged.connect(self.update_graph_live)
        self.text_box_x_min.returnPressed.connect(self.update_graph)
        layout.addWidget(self.text_box_x_min, 1, 1)
        self.text_box_x_max = QLineEdit()
        self.text_box_x_max.textChanged.connect(self.update_graph_live)
        self.text_box_x_max.returnPressed.connect(self.update_graph)
        layout.addWidget(self.text_box_x_max, 2, 1)
        # making the figure
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.subplot = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas, 4, 0, 1, 3)
        self.figure.clear()
        self.canvas.draw()
        ax = self.figure.add_subplot(111)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.grid(True)
        self.canvas.draw()
        self.setWindowTitle("Master ICR Internship")
        self.setCentralWidget(central_widget)

    @Slot()
    def update_graph(self):
        # clear previous plot
        self.figure.clear()
        self.canvas.draw()
        ax = self.figure.add_subplot(111)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_title('Graph of ' + self.text_box_eq.text())
        ax.grid(True)
        self.canvas.draw()
        # empty error message
        errorm = ""
        # retrieve inputs from textboxed
        equation = self.text_box_eq.text()
        xmin = self.text_box_x_min.text()
        xmax = self.text_box_x_max.text()
        # replace `^` with `**` to be handeled by the function eval
        equation = equation.replace("^", "**")
        # if no input bounds set to default 0  and 10
        if xmin.strip() == "":
            xmin = 0
        if xmax.strip() == "":
            xmax = 10
        # convert input bounds to float for further calculations and test for errors if the input is non numeric append the error to the error message
        try:
            xmin = float(xmin)
        except:
            errorm = "Invalid X1 must be a number\n"+errorm
        try:
            xmax = float(xmax)
        except:
            errorm = "Invalid X2 must be a number\n"+errorm
        # initiate the horizontal space if error occur it will be already added to the error message before but we will proceed with a right space for further error detection only
        try:
            x = np.linspace(xmin, xmax, 100)
        except:
            x = np.linspace(0, 10, 100)
        # handle any char by checking if only one char exist replace it with `x` so it would be recognised by eval else append error to error message
        unique_chars = set()
        for char in equation:
            unique_chars.add(char)
        unique_chars.discard('+')
        unique_chars.discard('*')
        unique_chars.discard('-')
        unique_chars.discard('/')
        unique_chars.discard('^')
        unique_chars.discard('.')
        unique_chars = {item for item in unique_chars if not item.isdigit()}
        if len(unique_chars) <= 1:
            try:
                first_element = next(iter(unique_chars))
                equation = equation.replace(first_element, 'x')
            except:
                errorm = "No input found\n"+errorm
        else:
            errorm = "Input must have only one variable\n"+errorm
        # change string to function and if any errors happen append to the error message
        try:
            y = eval(equation.strip())
        except:
            errorm = "Invalid equation!\n"+errorm
        # if their is any errors view error message and return else clear the error message
        if not errorm == "":
            self.error_label.setText(errorm)
            return errorm
        else:
            self.error_label.setText(errorm)
        # plot the graph in the GUI
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(x, y)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_title('Graph of ' + equation)
        ax.grid(True)
        self.canvas.draw()

    def update_graph_live(self):
        # clear graph
        if (self.text_box_eq.text().strip() == ""):
            self.figure.clear()
            self.canvas.draw()
            ax = self.figure.add_subplot(111)
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.grid(True)
            self.canvas.draw()
        # the same function but with no error messages
        try:
            equation = self.text_box_eq.text()
            equation = equation.replace("^", "**")
            xmin = self.text_box_x_min.text()
            xmax = self.text_box_x_max.text()
            if xmin.strip() == "":
                xmin = 0
            if xmax.strip() == "":
                xmax = 10
            xmin = float(xmin)
            xmax = float(xmax)
            x = np.linspace(xmin, xmax, 100)
            unique_chars = set()
            for char in equation:
                unique_chars.add(char)
            unique_chars.discard('+')
            unique_chars.discard('*')
            unique_chars.discard('-')
            unique_chars.discard('/')
            unique_chars.discard('^')
            unique_chars.discard('.')
            unique_chars = {
                item for item in unique_chars if not item.isdigit()}
            if len(unique_chars) <= 1:
                first_element = next(iter(unique_chars))
                equation = equation.replace(first_element, 'x')
            y = eval(equation.strip())
            self.error_label.setText("")
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            ax.plot(x, y)
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.set_title('Graph of ' + equation)
            ax.grid(True)
            self.canvas.draw()
        except:
            x = 0


if __name__ == "__main__":
    # Create the Qt application
    app = QApplication(sys.argv)
    # Create the main window
    main_window = MainWindow()
    main_window.show()
    # Start the Qt event loop
    sys.exit(app.exec_())

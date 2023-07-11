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

        # Create a central widget and a layout
        central_widget = QWidget(self)
        layout = QGridLayout(central_widget)
        
        logo_label = QLabel()
        logo_pixmap = QPixmap("logo.png")  # Replace with the actual path to your logo image
        logo_pixmap = logo_pixmap.scaled(188, 47)  # Adjust the width and height values as needed
        logo_label.setPixmap(logo_pixmap)
        layout.addWidget(logo_label,0,2,2,1)

        # Create a label
        label1 = QLabel("Equation:")
        layout.addWidget(label1, 0, 0)  # Add label to row 0, column 0
 # Create a label
        label2 = QLabel("X1:")
        layout.addWidget(label2, 1, 0)  # Add label to row 0, column 0
 # Create a label
        label3 = QLabel("X2:")
        layout.addWidget(label3, 2, 0)  # Add label to row 0, column 0
        
        
        self.error_label = QLabel(self)
        self.error_label.setStyleSheet("color: red;")  # Set text color to red
        layout.addWidget(self.error_label, 2,2)  # Add label to row 3, spanning 1 row and 3 columns


        # Create a text box
        self.text_box_eq = QLineEdit()
        self.text_box_eq.textChanged.connect(self.update_graph_live)
        self.text_box_eq.returnPressed.connect(self.update_graph)  # Connect returnPressed signal
        layout.addWidget(self.text_box_eq, 0, 1)  # Add text box to row 0, column 1
        # Create a text box
        self.text_box_x_min = QLineEdit()
        self.text_box_x_min.textChanged.connect(self.update_graph_live)
        self.text_box_x_min.returnPressed.connect(self.update_graph)  # Connect returnPressed signal
        layout.addWidget(self.text_box_x_min, 1, 1)  # Add text box to row 0, column 1
        # Create a text box
        self.text_box_x_max = QLineEdit()
        self.text_box_x_max.textChanged.connect(self.update_graph_live)
        self.text_box_x_max.returnPressed.connect(self.update_graph)  # Connect returnPressed signal
        layout.addWidget(self.text_box_x_max, 2, 1)  # Add text box to row 0, column 1

        # Create a button
        # self.button = QPushButton("Update Graph")
        # layout.addWidget(self.button, 3, 0, 1, 3)  # Add button to row 1, spanning 1 row and 2 columns

        # Create a graph
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.subplot = self.figure.add_subplot(111)
        # Add initial data to the graph
        # self.subplot.plot(x_data, y_data)

        # Create a canvas to display the graph
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas, 4, 0, 1, 3)  # Add canvas to row 2, spanning 1 row and 2 columns
        
        self.figure.clear()
        self.canvas.draw()
        ax = self.figure.add_subplot(111)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        # ax.set_title('Graph of ' + self.text_box_eq.text())
        ax.grid(True)
        self.canvas.draw()
        self.setWindowTitle("GUI with Graph")

        # Set the central widget
        self.setCentralWidget(central_widget)

        # Connect the button's clicked signal to the update_graph slot
        # self.button.clicked.connect(self.update_graph)

    @Slot()
    def update_graph(self):
        self.figure.clear()
        self.canvas.draw()
        ax = self.figure.add_subplot(111)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_title('Graph of ' + self.text_box_eq.text())
        ax.grid(True)
        self.canvas.draw()
        
        errorm=""
        equation = self.text_box_eq.text()
        equation = equation.replace("^", "**")
        xmin = self.text_box_x_min.text()
        xmax = self.text_box_x_max.text()

        if xmin.strip() == "":
            xmin=0
        if xmax.strip() == "":
            xmax=10
        
        try:
            xmin=float(xmin)
        except:
            errorm="Invalid X1 must be a number\n"+errorm
        try:
            xmax=float(xmax)
        except:
            #  self.error_label.setText("Invalid Xmax must be a number")
             errorm="Invalid X2 must be a number\n"+errorm
        # if xmax<xmin:
        #     errorm="Error! Invalid range entered\n"+errorm
        

                # Evaluate the equation for each x value
        try:
            x = np.linspace(xmin, xmax, 100)
        except:
            x = np.linspace(0, 10, 100)
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
        if len(unique_chars)<=1:
            try:
                first_element = next(iter(unique_chars))
                equation = equation.replace(first_element, 'x')
            except:
                errorm="No input found\n"+errorm
        else:
            errorm="Input must have only one variable\n"+errorm
        try:
            y = eval(equation.strip())
        except:
            errorm="Invalid equation!\n"+errorm          
        if not errorm=="":
            self.error_label.setText(errorm)
            return errorm
        else:
            self.error_label.setText(errorm)
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(x, y)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_title('Graph of ' + equation)
        ax.grid(True)   
        self.canvas.draw()
        
        
    def update_graph_live(self):
        if(self.text_box_eq.text().strip()==""):
            self.figure.clear()
            self.canvas.draw()
            ax = self.figure.add_subplot(111)
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.grid(True)
            self.canvas.draw()
        
        try:
            equation = self.text_box_eq.text()
            equation = equation.replace("^", "**")
            xmin = self.text_box_x_min.text()
            xmax = self.text_box_x_max.text()

            if xmin.strip() == "":
                xmin=0
            if xmax.strip() == "":
                xmax=10
            
            xmin=float(xmin)
            xmax=float(xmax)
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
            unique_chars = {item for item in unique_chars if not item.isdigit()}
            if len(unique_chars)<=1:
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
            x=0
            

if __name__ == "__main__":
    # Create the Qt application
    app = QApplication(sys.argv)

    # Create the main window
    main_window = MainWindow()
    main_window.show()

    # Start the Qt event loop
    sys.exit(app.exec_())

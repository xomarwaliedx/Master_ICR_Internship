import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QLineEdit, QPushButton, QLabel
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
import pytest
from main import MainWindow 

@pytest.fixture(scope="session")
def app(request):
    test_app = QApplication.instance()
    if test_app is None:
        test_app = QApplication(sys.argv)

        def close_app():
            test_app.quit()

        request.addfinalizer(close_app)

    return test_app


@pytest.fixture
def main_window(app, qtbot):
    main_window = MainWindow()
    main_window.show()
    qtbot.addWidget(main_window)
    qtbot.waitExposed(main_window)
    return main_window


def test_update_graph_button(main_window, qtbot):
    text_box_eq = main_window.text_box_eq
    text_box_x_min = main_window.text_box_x_min
    text_box_x_max = main_window.text_box_x_max
    canvas = main_window.canvas
    qtbot.keyClicks(text_box_eq, "x**2")
    qtbot.keyClicks(text_box_x_min, "0")
    qtbot.keyClicks(text_box_x_max, "10")
    text_box_eq.returnPressed.emit()
    with qtbot.waitExposed(main_window):
        assert canvas.figure.axes[0].get_title() == "Graph of x**2"


def test_update_graph_invalid_input(main_window, qtbot):
    text_box_eq = main_window.text_box_eq
    text_box_x_min = main_window.text_box_x_min
    text_box_x_max = main_window.text_box_x_max
    error_label = main_window.error_label
    qtbot.keyClicks(text_box_eq, "x**") 
    qtbot.keyClicks(text_box_x_min, "a") 
    qtbot.keyClicks(text_box_x_max, "b") 
    text_box_eq.returnPressed.emit()
    with qtbot.waitExposed(main_window):
        assert error_label.text() == "Invalid equation!\nInvalid X2 must be a number\nInvalid X1 must be a number\n"


def test_update_graph_no_input(main_window, qtbot):
    error_label = main_window.error_label
    text_box_eq = main_window.text_box_eq
    text_box_eq.returnPressed.emit()
    with qtbot.waitExposed(main_window):
        assert error_label.text() == "Invalid equation!\nNo input found\n"


def test_update_graph_default_range(main_window, qtbot):
    text_box_eq = main_window.text_box_eq
    canvas = main_window.canvas

    qtbot.keyClicks(text_box_eq, "x**2")

    text_box_eq.returnPressed.emit()

    with qtbot.waitExposed(main_window):
        assert np.allclose(canvas.figure.axes[0].get_xlim(), (0, 10),atol=6)
        assert np.allclose(canvas.figure.axes[0].get_ylim(), (0, 100),atol=6)


def test_update_graph_custom_range(main_window, qtbot):
    text_box_eq = main_window.text_box_eq
    text_box_x_min = main_window.text_box_x_min
    text_box_x_max = main_window.text_box_x_max
    canvas = main_window.canvas

    qtbot.keyClicks(text_box_eq, "x**2")
    qtbot.keyClicks(text_box_x_min, "-5")
    qtbot.keyClicks(text_box_x_max, "5")

    text_box_eq.returnPressed.emit()

    with qtbot.waitExposed(main_window):
        assert np.allclose(canvas.figure.axes[0].get_xlim(), (-5.5, 5.5),atol=2)
        assert np.allclose(canvas.figure.axes[0].get_ylim(), (-1.2, 26),atol=2)

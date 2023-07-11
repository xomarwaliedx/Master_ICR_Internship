# Graph plotter
A graph plotting tool using python
## Description
It is a python app that plots polynomial curves on a GUI based on the equation and horizontal bounds
The vertical bounds are set automatically according to user input function

## Dependencies:

### Need to install python
- For [windows](https://www.simplilearn.com/tutorials/python-tutorial/python-installation-on-windows)
- For [mac](https://www.dataquest.io/blog/installing-python-on-mac/)
- For [linux](https://www.scaler.com/topics/python/install-python-on-linux/)
 
### Need to install the following libraries
Open terminal and run the following commands
```
$ pip install matplotlib
$ pip install PySide6
$ pip install pytest
$ pip install numpy
$ pip install pytest-qt
```
## Running:
After downloading the libraries it should run just fine through any python interpretter
#### `main`
The main is the main program with tha GUI can be run normally from the interpretter
#### `test_main`
The test_main has some test examples that when run are executed and show the number of successful executions and is run from terminal using `python3 -m pytest`

### How to use it
In the GUI their is 3 textboxes the `Equation` where you should input your polynomial function in the form of a string, `X1` the first bound of the X-axis that will be shown in the GUI (set to zero by default if the text box was left empty) and the `X2` the second bound of the X-axis that will be shown in the GUI (set to 10 by default if the text box was left empty) the smaller entry is automatically used as the lower bound and the larger one is automatically set as the higher bound.

The program has live plotting however as long as you are typing no errors will appear not to bother you with errors until you finish the input and it will keep updating each time it has a valid input and freeze when an invalid input is entered so if you need to check which state is plotted at the moment you will have to check the graph title or press enter/return which will make any errors will pop in the GUI

## Cases handeled
- Can take any letter of the alphabet not just the letter`x`
- Check if the `equation` textbox is empty and alerts you in the GUI
- Check if the input function has more than one variable and alerts you in the GUI
- Check that both the `X1` and the `X2` are numbers
 


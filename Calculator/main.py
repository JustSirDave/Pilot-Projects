import re  # Importing the regular expression module for pattern matching
import tkinter as tk  # Importing tkinter for creating GUI
from math import sqrt  # Importing square root function from math module


# Defining the Application class that inherits from tkinter Frame
class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.master = master
        self.pack()

        # Initial input set to '0' and calling the method to draw the calculator layout
        self.input = '0'
        self.draw_frame()

    # Method to create a button widget with properties and place it in a grid layout
    def create_button(self, text, color, command, r, c, cspan=1, w=8):
        self.button = tk.Button(self, bg=color, fg='white')  # Create a button with bg color and text color
        self.button['text'] = text  # Set the button's label
        self.button['command'] = command  # Set the command function to be called when button is clicked
        self.button.config(height=2, width=w)  # Set the height and width of the button
        self.button.grid(row=r, column=c, columnspan=cspan, pady=4)  # Place button using grid layout

        return self.button  # Return the created button

    # Method to design and layout the calculator buttons and screen (label)
    def draw_frame(self):
        # Create the label that shows the input/output on the calculator's display
        self.label = tk.Label(self, font=("Helvetica", 16), bg='gray30', fg='white', anchor='se')
        self.label['text'] = '0'  # Set the initial label value to '0'
        self.label.configure(width=23, height=5)  # Configure size of the label
        self.label.grid(row=0, column=0, columnspan=4, pady=10)  # Place label in grid

        # Creating buttons for the calculator and arranging them on the frame
        self.ce = self.create_button('CE', 'red2', self.clear, 1, 0)
        self.back = self.create_button(u'\u232b', 'gray20', self.back, 1, 1)
        self.mod = self.create_button('%', 'gray20', lambda: self.get('%'), 1, 2)
        self.div = self.create_button('/', 'gray20', lambda: self.get('/'), 1, 3)

        self.seven = self.create_button('7', 'gray20', lambda: self.get('7'), 2, 0)
        self.eight = self.create_button('8', 'gray20', lambda: self.get('8'), 2, 1)
        self.nine = self.create_button('9', 'gray20', lambda: self.get('9'), 2, 2)
        self.mul = self.create_button('X', 'gray20', lambda: self.get('*'), 2, 3)

        self.four = self.create_button('4', 'gray20', lambda: self.get('4'), 3, 0)
        self.five = self.create_button('5', 'gray20', lambda: self.get('5'), 3, 1)
        self.six = self.create_button('6', 'gray20', lambda: self.get('6'), 3, 2)
        self.minus = self.create_button('-', 'gray20', lambda: self.get('-'), 3, 3)

        self.one = self.create_button('1', 'gray20', lambda: self.get('1'), 4, 0)  # Correct the order here
        self.two = self.create_button('2', 'gray20', lambda: self.get('2'), 4, 1)
        self.three = self.create_button('3', 'gray20', lambda: self.get('3'), 4, 2)
        self.plus = self.create_button('+', 'gray20', lambda: self.get('+'), 4, 3)

        self.root = self.create_button('√', 'gray20', lambda: self.get('√'), 5, 0)
        self.zero = self.create_button('0', 'gray20', lambda: self.get('0'), 5, 1)
        self.dot = self.create_button('.', 'gray20', lambda: self.get('.'), 5, 2)
        self.equal = self.create_button('=', 'gray20', self.output, 5, 3)

    # Method to handle user input (button presses)
    def get(self, value):
        # Add the value to the current input (convert value to string if necessary)
        self.input += str(value)

        # Define list of operators (for validation purposes)
        self.ops = ['+', '-', '*', '/', '%', '√']

        # Ensure no two consecutive operators are allowed
        if self.input[-1] in self.ops and self.input[-2] in self.ops:
            # Replace the second-to-last operator with the most recent operator
            self.input = str(self.input[:-2] + self.input[-1])

        # Remove leading zero unless it's the only character left
        if self.input[0] == '0':
            self.input = self.input[1:]

        # Ensure the first character is valid (cannot be an operator except for square root)
        if self.input[0] in self.ops:
            if self.input[0] == '√':  # Allow √ to be the first character
                pass
            else:
                self.input = self.input[1:]  # Remove invalid operator and prepend '0'
                self.input = '0' + self.input

        # Update the display label with the current input
        self.label['text'] = self.input

    # Method to clear the calculator's input
    def clear(self):
        self.input = '0'  # Reset input to '0'
        self.label['text'] = self.input  # Update display label

    # Method to remove the last character (backspace functionality)
    def back(self):
        self.text = self.input
        # If only one character left, clear the input
        if len(self.input) == 1:
            self.clear()
        else:
            # Remove the last character from the input and update the label
            self.input = self.text[:-1]
            self.label['text'] = self.input

    # Method to calculate and display the result when '=' is pressed
    def output(self):
        # If the last character is a decimal point, remove it to avoid errors
        if self.input[-1] == '.':
            self.input = self.input[:-1]

        # Regular expression pattern to find square root operations (e.g., √number)
        root_ = re.compile(r'√\d+')
        all_roots = re.findall(root_, self.input)  # Find all matches in the input

        # If there are square root operations, calculate and replace them
        if all_roots:
            for num in all_roots:
                # Calculate the square root of the number (after removing √)
                calc = sqrt(int(num.lstrip('√')))
                # Replace the √number with the calculated value in the input string
                self.input = re.sub(num, '*' + str(round(calc, 3)), self.input)

                # If the first character is '*', remove it (not valid to start with multiplication)
                if self.input[0] == '*':
                    self.input = self.input[1:]

        # Evaluate the final mathematical expression and round the result
        self.out = str(round(eval(self.input), 5))
        # Display the result on the calculator's label
        self.label['text'] = self.out
        # Set the input to the result for further calculations
        self.input = self.out


# *********************************************************************************

# Main part of the code: Create the application window and start the Tkinter loop

root = tk.Tk()  # Initialize Tkinter root window
root.geometry('300x400')  # Set the window size
root.wm_title('Calculator')  # Set the window title

# Create an instance of the Application class and pass the root window
app = Application(master=root)
# Start the Tkinter event loop (runs the app)
app.mainloop()

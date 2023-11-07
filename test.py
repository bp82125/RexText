# Import tkinter library
from tkinter import *

# Create an instance of tkinter frame
win = Tk()
# Set the geometry
win.geometry("750x200")


def select_text():
    text.tag_add("sel", "1.0", "end")
    text.focus_set()


# Create a Text Widget
text = Text(win)
text.insert(INSERT, """Python is an interpreted, high-level and generalpurpose
programming language. Python's design philosophy emphasizes
code readability with its notable use of significant indentation""")
text.pack()
# Create a button to select all the text in the text widget
button = Button(win, text="Select", background="gray71", command=select_text)
button.pack(pady=20, side=TOP)
win.mainloop()

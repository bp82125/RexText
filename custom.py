import tkinter as tk
import tkinter.filedialog
import re

def open_file():
    file_path = tk.filedialog.askopenfilename()
    if file_path:
        with open(file_path, 'r') as file:
            text.delete(1.0, tk.END)
            text.insert(tk.END, file.read())

def save_file():
    file_path = tk.filedialog.asksaveasfilename(defaultextension=".txt")
    if file_path:
        with open(file_path, 'w') as file:
            file.write(text.get(1.0, tk.END))

def search_text():
    global search_pattern
    search_pattern = search_entry.get()
    text_to_search = text.get(1.0, tk.END)
    global matches
    matches = list(re.finditer(search_pattern, text_to_search))
    text.tag_remove('search', '1.0', tk.END)
    if matches:
        highlight_match(0)
    text.focus_set()
def find_all():
    global search_pattern
    search_pattern = search_entry.get()
    text_to_search = text.get(1.0, tk.END)
    global matches
    matches = list(re.finditer(search_pattern, text_to_search))
    text.tag_remove('search', '1.0', tk.END)
    text.focus_set()
    for i in range(0, len(matches)):
        highlight_match(i)

def highlight_match(match_index):
    if 0 <= match_index < len(matches):
        match = matches[match_index]
        start = text.index(f"1.0 + {match.start()} chars")
        end = text.index(f"1.0 + {match.end()} chars")
        text.tag_add('search', start, end)
        text.tag_configure('search', background='yellow', foreground='black')
        text.see(start)
        text.mark_set("insert", end)  # Set the cursor to the start of the match

def find_next():
    find_all()
    global current_match
    current_match += 1
    if current_match < len(matches):
        highlight_match(current_match)
    else:
        current_match = -1
        # text.tag_remove('search', '1.0', tk.END)
def clear_search():
    text.tag_remove('search', '1.0', tk.END)

# Create the main window
root = tk.Tk()
root.title("Simple Notepad with Regex Search")

# Create a menu
menu = tk.Menu(root)
root.config(menu=menu)

file_menu = tk.Menu(menu)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

# Create a text widget
text = tk.Text(root)
text.pack()

# Create a search bar
search_label = tk.Label(root, text="Search:")
search_label.pack()
search_entry = tk.Entry(root)
search_entry.pack()
search_button = tk.Button(root, text="Search", command=search_text)
search_button.pack()

# Create a "Find Next" button
find_next_button = tk.Button(root, text="Find Next", command=find_next)
find_next_button.pack()

find_all_button = tk.Button(root, text="Find All", command=find_all)
find_all_button.pack()
clear_search_button = tk.Button(root, text="Clear Search", command=clear_search)
clear_search_button.pack()
# Global variables
search_pattern = ""
matches = []
current_match = -1

# Start the GUI main loop
root.mainloop()

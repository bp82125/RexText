import tkinter as tk
from tkinter import filedialog

class Notepad:
    def __init__(self, root):
        self.root = root
        self.root.title("Notepad")
        self.text_area = tk.Text(self.root, wrap="word", undo=True)
        self.text_area.pack(expand="yes", fill="both")
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # File Menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=root.destroy)

        # Edit Menu
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Undo", command=self.undo)
        self.edit_menu.add_command(label="Redo", command=self.redo)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Cut", command=self.cut_text)
        self.edit_menu.add_command(label="Copy", command=self.copy_text)
        self.edit_menu.add_command(label="Paste", command=self.paste_text)

        # Keep track of changes for undo and redo
        self.changes = []

        # Index to track the current change
        self.current_change = -1

        # Boolean to check if changes are being applied (for undo/redo)
        self.applying_changes = False

        # Trace changes to update undo and redo buttons
        self.text_area.bind("<Key>", self.on_key_press)

    def new_file(self):
        self.text_area.delete(1.0, tk.END)
        self.reset_changes()

    def open_file(self):
        file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, content)
                self.reset_changes()

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                content = self.text_area.get(1.0, tk.END)
                file.write(content)
                self.reset_changes()

    def cut_text(self):
        self.copy_text()
        self.text_area.delete("sel.first", "sel.last")

    def copy_text(self):
        self.root.clipboard_clear()
        text = self.text_area.get("sel.first", "sel.last")
        self.root.clipboard_append(text)

    def paste_text(self):
        text = self.root.clipboard_get()
        self.text_area.insert(tk.INSERT, text)
        self.add_change()

    def undo(self):
        if self.current_change > 0:
            self.applying_changes = True
            self.current_change -= 1
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, self.changes[self.current_change])
            self.applying_changes = False

    def redo(self):
        if self.current_change < len(self.changes) - 1:
            self.applying_changes = True
            self.current_change += 1
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, self.changes[self.current_change])
            self.applying_changes = False

    def on_key_press(self, event):
        if not self.applying_changes:
            self.add_change()

    def add_change(self):
        content = self.text_area.get(1.0, tk.END)
        # Remove the changes after the current change index
        self.changes = self.changes[: self.current_change + 1]
        self.changes.append(content)
        self.current_change = len(self.changes) - 1

    def reset_changes(self):
        self.changes = []
        self.current_change = -1

if __name__ == "__main__":
    root = tk.Tk()
    notepad = Notepad(root)
    root.mainloop()

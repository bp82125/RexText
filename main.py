import tkinter as tk
from tkinter import filedialog as fd

from controller import Controller


class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
    
        self.menubar = tk.Menu()
        self.parent.config(menu=self.menubar)
        
        self.sub_menu_file = tk.Menu(self.menubar, tearoff=False)
        self.sub_menu_file.add_command(label="   Open   ", command=self.open_file)
        self.sub_menu_file.add_command(label="   Save As   ", command=self.save_file)
        self.sub_menu_file.add_command(label="  New file    ", command=self.new_file)
        self.sub_menu_file.add_separator()
        self.sub_menu_file.add_command(label="   Exit   ", command=self.exit_file)
        self.menubar.add_cascade(label="File", menu=self.sub_menu_file)



        self.controller = Controller(self)   
        self.controller.pack(side="bottom", fill="both", expand=True)

        self.edit_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="    Edit    ", menu=self.edit_menu)
        self.edit_menu.add_command(label="    Undo    ", command=self.undo_text)
        self.edit_menu.add_command(label="    Redo    ", command=self.redo_text)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="    Cut     ", command=self.cut_text)
        self.edit_menu.add_command(label="    Copy    ", command=self.copy_text)
        self.edit_menu.add_command(label="    Paste   ", command=self.paste_text)

        self.changes = []
        self.current_change = -1
        self.applying_changes = False
        self.typing = False

        # Trace changes to update undo and redo buttons
        self.controller.text_widget.text_area.bind("<KeyRelease>", self.on_key_press)

        self.parent.bind("<Control-n>", lambda event: self.new_file())
        self.parent.bind("<Control-s>", lambda event: self.save_file())
        self.parent.bind("<Control-o>", lambda event: self.open_file())

    def new_file(self):
        self.controller.text_widget.text_area.delete(1.0, tk.END)
        self.reset_changes()
    def open_file(self):
        file_path = fd.askopenfilename()
        if file_path:
            with open(file_path, 'r') as file:
                self.controller.text_widget.text_area.delete(1.0, tk.END)
                self.controller.text_widget.text_area.insert(tk.END, file.read())
                self.reset_changes()

    def save_file(self):
        file_path = tk.filedialog.asksaveasfilename(filetypes=(("Text files", "*.txt"),("All files", "*.")), defaultextension=".txt")
        if file_path:
            with open(file_path, 'w') as file:
                file.write(self.controller.text_widget.text_area.get(1.0, tk.END))
                self.reset_changes()
                
    def exit_file(self):
        self.parent.destroy()

    def copy_text(self):
        self.parent.clipboard_clear()
        text = self.controller.text_widget.text_area.get("sel.first", "sel.last")
        self.parent.clipboard_append(text)
    def cut_text(self):
        self.copy_text()
        self.controller.text_widget.text_area.delete("sel.first", "sel.last")
        self.add_change()

    def paste_text(self):
        text = self.parent.clipboard_get()
        self.controller.text_widget.text_area.insert(tk.INSERT, text)
        self.add_change()

    def undo_text(self):
        if self.current_change > 0:
            self.applying_changes = True
            self.current_change -= 1
            self.controller.text_widget.text_area.delete(1.0, tk.END)
            self.controller.text_widget.text_area.insert(tk.END, self.changes[self.current_change])
            self.applying_changes = False

    def redo_text(self):
        if self.current_change < len(self.changes) - 1:
            self.applying_changes = True
            self.current_change += 1
            self.controller.text_widget.text_area.delete(1.0, tk.END)
            self.controller.text_widget.text_area.insert(tk.END, self.changes[self.current_change])
            self.applying_changes = False

    def on_key_press(self, event):
        if not self.typing:
            self.typing = True
            self.add_change()
        self.typing = False

    def add_change(self):
        content = self.controller.text_widget.text_area.get(1.0, tk.END)
        # Remove the changes after the current change index
        if not self.changes or content != self.changes[self.current_change]:
            self.changes = self.changes[: self.current_change + 1]
            self.changes.append(content)
            self.current_change = len(self.changes) - 1
    def reset_changes(self):
        self.changes = []
        self.current_change = -1

if __name__ == '__main__':
    root = tk.Tk()
    
    root.title(" RegText - A minimal text editor with Regex support searching")
    root.minsize(400, 300)
    
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()

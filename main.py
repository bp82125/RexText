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
        self.sub_menu_file.add_separator()
        self.sub_menu_file.add_command(label="   Exit   ", command=self.exit_file)      

        self.menubar.add_cascade(label="File", menu=self.sub_menu_file)
        
        self.controller = Controller(self)   
        self.controller.pack(side="bottom", fill="both", expand=True)

    def open_file(self):
        file_path = fd.askopenfilename()
        if file_path:
            with open(file_path, 'r') as file:
                self.controller.text_widget.text_area.delete(1.0, tk.END)
                self.controller.text_widget.text_area.insert(tk.END, file.read())

    def save_file(self):
        file_path = tk.filedialog.asksaveasfilename(filetypes=(("Text files", "*.txt"),("All files", "*.")), defaultextension=".txt")
        if file_path:
            with open(file_path, 'w') as file:
                file.write(self.controller.text_widget.text_area.get(1.0, tk.END))
                
    def exit_file(self):
        self.parent.destroy()
        
        


if __name__ == '__main__':
    root = tk.Tk()
    
    root.title(" RegText - A minimal text editor with Regex support searching")
    root.minsize(400, 300)
    
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()

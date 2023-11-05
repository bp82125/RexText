import tkinter as tk

from search import Search
from text_editor import CustomText


class Main(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.text_widget = CustomText(self)
        self.search = Search(self)

        self.search.pack(side="top")
        self.text_widget.pack(side="top", fill="both", expand=True)


class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.main = Main(self)
        self.main.pack(expand=True, fill="both")


if __name__ == "__main__":
    root = tk.Tk()
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()

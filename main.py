import tkinter as tk

from controller import Controller


class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.controller = Controller(self)

        self.controller.pack(side="bottom", fill="both", expand=True)


if __name__ == '__main__':
    root = tk.Tk()
    Controller(root).pack(side="top", fill="both", expand=True)
    root.mainloop()

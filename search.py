import tkinter as tk


class Search(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        self.entry = tk.Entry(self)
        self.entry.insert(0, "Regex")
        self.entry.configure(state='disabled')

        self.button = tk.Button(self, text="Search")

        self.entry.grid(row=0, column=1, padx=20, pady=10, ipady=3)
        self.button.grid(row=0, column=2, padx=20, pady=10)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(3, weight=1)

        self.entry.bind('<FocusOut>', lambda x: on_focus_out(self.entry, 'Regex'))
        self.entry.bind('<Button-1>', lambda x: on_focus_in(self.entry))

        def on_focus_in(entry):
            if entry.cget('state') == 'disabled':
                entry.configure(state='normal')
                entry.delete(0, 'end')

        def on_focus_out(entry, placeholder):
            if entry.get() == "":
                entry.insert(0, placeholder)
                entry.configure(state='disabled')


if __name__ == '__main__':
    root = tk.Tk()
    Search(root).pack(side="top", fill="both", expand=True)
    root.mainloop()

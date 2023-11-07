import tkinter as tk
from tkinter import messagebox

from search import Search
from custom_text import CustomText


class Controller(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.text_widget = CustomText(self)
        self.search = Search(self)

        self.search.pack(side="top")
        self.text_widget.pack(side="top", fill="both", expand=True)

        self.search.search_button.configure(command=self.highlight_text)
        self.search.find_next.configure(command=self.find_next)

    def highlight_text(self):
        pattern = self.search.get_entry()
        all_matches = self.text_widget.highlight_match(pattern)

        if len(all_matches) == 0:
            messagebox.showinfo("showinfo", f"There are no matches in the entire file.")
        elif len(all_matches) == 1:
            messagebox.showinfo("showinfo", f"There is 1 match in the entire file.")
        else:
            messagebox.showinfo("showinfo", f"There are {len(all_matches)} matches in the entire file.")

        self.text_widget.text_area.clean_all_tag("match")

    def find_next(self):
        pattern = self.search.get_entry()

        cursor_pos = self.text_widget.text_area.index(tk.INSERT)

        next_match = self.text_widget.text_area.next_match(cursor_pos, pattern)

        if next_match is None:
            self.text_widget.text_area.clean_all_tag("match")
            return

        match_start = next_match[0]
        match_end = next_match[1]

        self.text_widget.text_area.focus_set()
        self.text_widget.text_area.tag_remove("match", match_start, match_end)

        self.text_widget.text_area.clean_all_tag("sel")
        self.text_widget.text_area.tag_add('sel', match_start, match_end)
        self.text_widget.text_area.mark_set(tk.INSERT, match_end)

        self.text_widget.highlight_match(pattern)


if __name__ == "__main__":
    root = tk.Tk()
    Controller(root).pack(side="top", fill="both", expand=True)
    root.mainloop()

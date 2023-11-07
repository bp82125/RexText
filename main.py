import tkinter as tk
from tkinter import messagebox

from search import Search
from text_editor import CustomText


class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.text_widget = CustomText(self)
        self.search = Search(self)

        self.search.pack(side="top")
        self.text_widget.pack(side="top", fill="both", expand=True)

        self.search._search_button.configure(command=self.highlight_text)
        self.search._find_next.configure(command=self.next_match)

    def highlight_text(self):
        pattern = self.search.get_entry()
        all_matches = self.text_widget.highlight_match(pattern)

        if len(all_matches) == 0:
            messagebox.showinfo("showinfo", f"There are no matches in the entire file.")
        elif len(all_matches) == 1:
            messagebox.showinfo("showinfo", f"There is 1 match in the entire file.")
        else:
            messagebox.showinfo("showinfo", f"There are {len(all_matches)} matches in the entire file.")

        self.text_widget._text.clean_highlights("match")

    def next_match(self):
        pattern = self.search.get_entry()
        all_matches = self.text_widget.highlight_match(pattern)

        matches_start = [match[0] for match in all_matches]
        matches_end = [match[1] for match in all_matches]

        if len(all_matches) > 0:
            match_start = matches_start[0]
            match_end = matches_end[0]

            old_cursor_pos = self.text_widget._text.index(tk.INSERT)

            self.text_widget._text.focus_set()
            self.text_widget._text.tag_remove("match", match_start, match_end)
            self.text_widget._text.tag_add('sel', match_start, match_end)

            self.text_widget._text.mark_set(tk.INSERT, match_end)
        return "break"

if __name__ == "__main__":
    root = tk.Tk()
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()

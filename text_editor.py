import re
import tkinter as tk
from tkinter import ttk


# Kế thừa từ Canvas
class TextLineNumbers(tk.Canvas):
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        self.text_widget = None

    def attach(self, text_widget):
        self.text_widget = text_widget

    def redraw(self):
        # Xoá hết các đánh số dòng hiện tại
        self.delete("all")

        # lấy thứ tự của dòng đầu tiên hiện tại trên Text
        # Ví dụ: hàng trên cùng hiện tại là hàng thứ 17 thì i = "17.0"
        i = self.text_widget.index("@0,0")
        while True:
            # dline = (x, y, width, height, baseline)
            # x, y là toạ độ của dòng hiện tại bên Text
            dline = self.text_widget.dlineinfo(i)

            # Hiện tại đang quá cuối màn hình
            if dline is None:
                break

            # Để vẽ số đánh số dòng chính xác song song với dòng bên Text
            # Cần phải biết dòng hiện tại đang cách góc trên là bao nhiêu px

            y = dline[1]

            # i có dạng "line.column"
            # Lấy số trước dấu . sẽ ra thứ tự hàng của i hiện tại
            line_num = str(i).split(".")[0]

            # Thêm só đánh số dòng vào, thụt vào bên trái 2px, và cách góc trên y px
            self.create_text(self.winfo_width() - 10, y, anchor="ne", text=line_num)

            # i trỏ đến dòng kế tiếp
            i = self.text_widget.index(f'{i}+1line')


class TextWithProxy(tk.Text):
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)

        # Tạo một proxy(design pattern) để handle quá trình tcl accpet và response với thao tác người dùng
        # self._w là tên của widget
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

    def _proxy(self, command, *args):

        # if command == 'get' and (args[0] == 'sel.first' and args[1] == 'sel.last') and not self.tag_ranges(
        #         'sel'):
        #     return
        #
        # # avoid error when deleting
        # if command == 'delete' and (args[0] == 'sel.first' and args[1] == 'sel.last') and not self.tag_ranges(
        #         'sel'):
        #     return

        # Thực hiện thao tác của người dùng như bình thường
        cmd = (self._orig, command) + args
        result = self.tk.call(cmd)

        # Tạo 1 event nếu có hành động thêm, hoặc xoá, hoặc vị trí cursor thay đổi
        if (args[0] in ("insert", "replace", "delete") or
                args[0:3] == ("mark", "set", "insert") or
                args[0:2] == ("xview", "moveto") or
                args[0:2] == ("xview", "scroll") or
                args[0:2] == ("yview", "moveto") or
                args[0:2] == ("yview", "scroll")
        ):
            self.event_generate("<<Change>>")
            self.event_generate("<<Highlight>>")

        # Trả về kết quả hành động người dùng như bình thường
        return result

    def highlight(self, tag, start, end):
        self.tag_add(tag, start, end)

    def highlight_all(self, pattern, tag):
        all_matches = self.search_re(pattern)
        for match in all_matches:
            self.highlight(tag, match[0], match[1])

        return all_matches

    def clean_highlights(self, tag):
        self.tag_remove(tag, "1.0", tk.END)

    def search_re(self, pattern):
        matches = []
        text = self.get("1.0", tk.END).splitlines()
        for i, line in enumerate(text):
            for match in re.finditer(pattern, line):
                matches.append((f"{i + 1}.{match.start()}", f"{i + 1}.{match.end()}"))

        return matches

    def highlight_pattern(self, pattern, tag="match"):
        self.clean_highlights(tag)
        return self.highlight_all(pattern, tag)


class CustomText(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        self._text = TextWithProxy(self, wrap="none", borderwidth=0)
        self._text_vsb = ttk.Scrollbar(self, orient="vertical", command=self._text.yview)
        self._text_hsb = ttk.Scrollbar(self, orient="horizontal", command=self._text.xview)
        self._text.configure(yscrollcommand=self._text_vsb.set, xscrollcommand=self._text_hsb.set)

        self._text.tag_config("match", background="yellow")

        self._line_numbers = TextLineNumbers(self, width=50)
        self._line_numbers.attach(self._text)

        self._text.grid(row=0, column=1, sticky="nsew")
        self._text_vsb.grid(row=0, column=2, sticky="ns")
        self._text_hsb.grid(row=1, column=1, sticky="ew")

        self._line_numbers.grid(row=0, column=0, sticky="ns")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)

        self._text.bind("<<Change>>", self._on_change)
        self._text.bind("<Configure>", self._on_change)

    def _on_change(self, event):
        self._line_numbers.redraw()

    def highlight_match(self, pattern):
        return self._text.highlight_pattern(pattern)

    def relocate_cursor(self, location):
        line = location[0]
        column = location[1]
        self._text.mark_set("insert", "%d.%d" % (line + 1, column + 1))


if __name__ == '__main__':
    root = tk.Tk()
    CustomText(root).pack(side="top", fill="both", expand=True)
    root.mainloop()

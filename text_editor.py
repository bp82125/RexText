import tkinter as tk


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
            self.create_text(2, y, anchor="nw", text=line_num)

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

    def _proxy(self, *args):
        # Thực hiện thao tác của người dùng như bình thường
        cmd = (self._orig,) + args
        result = self.tk.call(cmd)

        # Tạo 1 event nếu có hành động thêm, hoặc xoá, hoặc vị trí cursor thay đổi
        if (args[0] in ("insert", "replace", "delete") or
                args[0:3] == ("mark", "set", "insert") or
                args[0:2] == ("xview", "moveto") or
                args[0:2] == ("xview", "scroll") or
                args[0:2] == ("yview", "moveto") or
                args[0:2] == ("yview", "scroll")
        ):
            self.event_generate("<<Change>>", when="tail")

        # Trả về kết quả hành động người dùng như bình thường
        return result


class CustomText(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        self._text = TextWithProxy(self, wrap="none", borderwidth=0)
        self._text_vsb = tk.Scrollbar(self, orient="vertical", command=self._text.yview)
        self._text_hsb = tk.Scrollbar(self, orient="horizontal", command=self._text.xview)
        self._text.configure(yscrollcommand=self._text_vsb.set, xscrollcommand=self._text_hsb.set)

        self._line_numbers = TextLineNumbers(self, width=40)
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


if __name__ == '__main__':
    root = tk.Tk()
    CustomText(root).pack(side="top", fill="both", expand=True)
    root.mainloop()


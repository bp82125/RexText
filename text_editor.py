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


class CustomText(tk.Text):
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)

        # create a proxy for the underlying widget
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

    def _proxy(self, *args):
        # let the actual widget perform the requested action
        cmd = (self._orig,) + args
        result = self.tk.call(cmd)

        # generate an event if something was added or deleted,
        # or the cursor position changed
        if (args[0] in ("insert", "replace", "delete") or
                args[0:3] == ("mark", "set", "insert") or
                args[0:2] == ("xview", "moveto") or
                args[0:2] == ("xview", "scroll") or
                args[0:2] == ("yview", "moveto") or
                args[0:2] == ("yview", "scroll")
        ):
            self.event_generate("<<Change>>", when="tail")

        # return what the actual widget returned
        return result


class TextWithLineNumbers(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.text = CustomText(self)
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.text.yview)
        self.text.configure(yscrollcommand=self.vsb.set)

        self.line_numbers = TextLineNumbers(self, width=30)
        self.line_numbers.attach(self.text)

        self.vsb.pack(side="right", fill="y")
        self.line_numbers.pack(side="left", fill="y")
        self.text.pack(side="right", fill="both", expand=True)

        self.text.bind("<<Change>>", self._on_change)
        self.text.bind("<Configure>", self._on_change)

    def _on_change(self, event):
        self.line_numbers.redraw()

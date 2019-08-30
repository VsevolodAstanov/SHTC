import tkinter as tk
from shtc.shtc import TagCounter


class TagCounterGUI(tk.Frame):

    def __init__(self, root):
        self.title = "Simple HTML Tag Counter"
        self.geometry = ("650x450+300+200")
        super().__init__(root)


def run_gui_app():

    tc = TagCounter()
    print(tc.get_db_data())

    root = tk.Tk()
    app = TagCounterGUI(root)
    app.pack()
    root.title(app.title)
    root.geometry(app.geometry)
    root.resizable(False, False)
    root.mainloop()
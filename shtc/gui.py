import tkinter as tk
from tkinter import ttk
import json
from shtc.shtc import TagCounter


class TagCounterGUI(tk.Frame):

    def __init__(self, root):
        super().__init__(root)
        self.tc = TagCounter()

        # Input Block
        input_url_label = tk.Label(root, text='URL or Synonym: ')
        self.input_url = tk.Entry(root)
        start_btn_ = tk.Button(root, text='Start', command=self.get_data, bg='green', fg='white')

        input_url_label.place(x=10, y=10)
        self.input_url.place(x=110, y=10)
        start_btn_.place(x=240, y=10, height=20)

        # Output block
        name_label = tk.Label(root, text='Name: ')
        url_label = tk.Label(root, text='URL: ')
        date_label = tk.Label(root, text='Last Update: ')
        name_label.place(x=10, y=50)
        url_label.place(x=10, y=70)
        date_label.place(x=10, y=90)

        # self.date = tk.Text(root, state=tk.DISABLED)
        # self.url = tk.Text(root, state=tk.DISABLED)
        # self.name = tk.Text(root, state=tk.DISABLED)

        #
        # oy=50
        # for i in range(0,2):
        #     self.output_container[i].place(x=80, y=oy, width=195, height=20)
        #     oy += 20

        self.name = tk.Text(root, state='disabled')
        self.url = tk.Text(root, state='disabled')
        self.date = tk.Text(root, state='disabled')
        self.output_container = [self.name, self.url, self.date]
        self.name.place(x=80, y=50, width=195, height=20)
        self.url.place(x=80, y=70, width=195, height=20)
        self.date.place(x=80, y=90, width=195, height=20)

        # Grid
        self.output_grid = ttk.Treeview(root, columns=('Tag', 'Amount'), show='headings')
        self.output_grid.column('Tag', anchor='center')
        self.output_grid.column('Amount', anchor='center')
        self.output_grid.heading('Tag', text='Tag')
        self.output_grid.heading('Amount', text='Amount')

        self.output_grid.place(x=10, y=110)

    def get_data(self):
        self.tc.parse_input_url(self.input_url.get())
        self.tc.get_db_data()
        print('Logging [GUI]: Get DB Data')

        if not self.tc.data:
            self.tc.get_http_data()
            print('Logging [GUI]: Get HTTP Data')

        if self.tc.data:
            self.display()
            print('Logging [GUI]: Display')
        else:
            print('No Data to Display')

    def display(self):
        for e in range(len(self.output_container)):
            self.output_container[e].config(state='normal')
            self.output_container[e].delete(1.0, 'end')
            self.output_container[e].insert('end', self.tc.data[e])
            self.output_container[e].config(state='disabled')

        tags = json.loads(self.tc.data[3])
        [self.output_grid.delete(i) for i in self.output_grid.get_children()]
        [self.output_grid.insert('', 'end', values=(str(row), str(tags[row]))) for row in tags]

        self.input_url.delete(0, 'end')


def run_gui_app():
    root = tk.Tk()
    app = TagCounterGUI(root)
    app.pack()
    root.title('Simple HTML Tag Counter')
    root.geometry('423x400+700+300')
    root.resizable(False, False)
    root.mainloop()

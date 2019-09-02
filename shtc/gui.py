import tkinter as tk
from tkinter import ttk
import json
from shtc.shtc import TagCounter


class TagCounterGUI(tk.Frame):

    def __init__(self, root):
        super().__init__(root)

        self.tc = TagCounter()

        # Define Input Block
        label_url = tk.Label(root, text='URL or Synonym: ')
        self.entry_url = tk.Entry(root)
        btn_start = tk.Button(root, text='Start', command=self.get_data, bg='green', fg='white')
        label_url.place(x=10, y=10)
        self.entry_url.place(x=110, y=10)
        btn_start.place(x=240, y=10, height=20)

        # Define Output block
        self.output_grid = ttk.Treeview(root, columns=('Tag', 'Amount'), show='headings')
        self.output_grid.column('Tag', anchor=tk.CENTER)
        self.output_grid.column('Amount', anchor=tk.CENTER)
        self.output_grid.heading('Tag', text='Tag')
        self.output_grid.heading('Amount', text='Amount')

        self.output_grid.place(x=10, y=50)

    def get_data(self):
        self.tc.parse_input_url(self.entry_url.get())
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
        name = self.tc.data[0]
        url = self.tc.data[1]
        date = self.tc.data[2]
        tags = json.loads(self.tc.data[3])

        [self.output_grid.delete(i) for i in self.output_grid.get_children()]
        [self.output_grid.insert('', 'end', values=(row, tags[row])) for row in tags]

        self.entry_url.delete(0, tk.END)



def run_gui_app():
    root = tk.Tk()
    app = TagCounterGUI(root)
    app.pack()
    root.title('Simple HTML Tag Counter')
    root.geometry('423x400+0+0')
    root.resizable(False, False)
    root.mainloop()

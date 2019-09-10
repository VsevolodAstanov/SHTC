import sys
import json
import tkinter as tk
from tkinter import ttk
from tagcounter.logger import Logger
from tagcounter.tagcounter import TagCounter


class TagCounterGUI(tk.Frame):

    def __init__(self, root):
        try:
            super().__init__(root)
            self.log = Logger()()
            self.tc = TagCounter()

            self.log.info('INITIALIZE GUI APPLICATION')

            # Input Block
            inp_url_lab = tk.Label(root, text='URL or Synonym: ')
            self.inp_url = tk.Entry(root)
            start_btn_ = tk.Button(root, text='Start', command=self.get_data, bg='green', fg='white')

            inp_url_lab.place(x=8, y=10)
            self.inp_url.place(x=107, y=10, width=165)
            start_btn_.place(x=275, y=10, height=20)

            # Output block
            out_lab_conf = [
                {'text': 'Name: ', 'x': 7, 'y': 50},
                {'text': 'URL: ', 'x': 7, 'y': 70},
                {'text': 'Last Update: ', 'x': 7, 'y': 90}
            ]
            out_labels = [tk.Label(root, text=out_lab_conf[ol]['text']) for ol in range(len(out_lab_conf))]
            [out_labels[ol].place(x=out_lab_conf[ol]['x'], y=out_lab_conf[ol]['y']) for ol in range(len(out_labels))]

            out_val_conf = [
                {'x': 80, 'y': 50},
                {'x': 80, 'y': 70},
                {'x': 80, 'y': 90}
            ]
            self.out_values = [tk.Text(root, state='disabled') for t in range(len(out_val_conf))]
            [self.out_values[ov].place(x=out_val_conf[ov]['x'], y=out_val_conf[ov]['y'], width=230, height=20) for ov in
             range(len(out_labels))]

            # Grid
            self.output_grid = ttk.Treeview(root, columns=('Tag', 'Amount'), show='headings', selectmode='browse')
            self.output_grid.column('Tag', anchor='center', width=140)
            self.output_grid.column('Amount', anchor='center', width=140)
            self.output_grid.heading('Tag', text='Tag')
            self.output_grid.heading('Amount', text='Amount')
            self.output_grid.place(x=10, y=115, width=300, height=230)

            # Scrollbar
            vsb = ttk.Scrollbar(root, orient="vertical", command=self.output_grid.yview)
            vsb.place(x=292, y=116, height=228)
            self.output_grid.configure(yscrollcommand=vsb.set)

            # process Message
            self.info_message = tk.Label(root, font=('', 11))
            self.info_message.place(x=7, y=345, width=306)
        except:
            self.log.critical('Cannot initialize GUI Application: ' + str(sys.exc_info()[1]))
            sys.exit()

    def get_data(self):
        try:
            self.log.info('GET GUI DATA')
            self.clear_info_message()

            self.tc.parse_input_url(self.inp_url.get())
            self.tc.get_db_data()

            if not self.tc.get_data():
                self.tc.get_http_data()

            if self.tc.get_data():
                self.display()
            else:
                raise Exception('Cannot display data using this URL')
        except Exception as err:
            self.clear_output()
            self.log.warning(str(err))
            self.add_info_message('error', str(err))

    def display(self):
        try:
            self.log.info('DISPLAY GUI DATA')

            for v, value in enumerate(self.out_values):
                value.config(state='normal')
                value.delete(1.0, 'end')
                value.insert('end', self.tc.get_data()[v])
                value.config(state='disabled')

            [self.output_grid.delete(i) for i in self.output_grid.get_children()]
            tags = json.loads(self.tc.get_data()[3])
            [self.output_grid.insert('', 'end', values=(str(row), str(tags[row]))) for row in tags]
            self.add_info_message('info', 'Done')
        except Exception as err:
            self.clear_output()
            self.log.warning(str(err))
            self.add_info_message('error', 'Cannot display data using this URL')

    def clear_output(self):
        for v, value in enumerate(self.out_values):
            value.config(state='normal')
            value.delete(1.0, 'end')
            value.config(state='disabled')

        [self.output_grid.delete(i) for i in self.output_grid.get_children()]

    def add_info_message(self, ty,  msg):
        if ty is 'error':
            self.info_message.config(fg='red', text=msg)
        else:
            self.info_message.config(fg='green', text=msg)

    def clear_info_message(self):
        self.info_message['text'] = ''


def run_gui_app():
    root = tk.Tk()
    app = TagCounterGUI(root)
    app.pack()
    root.title('Simple HTML Tag Counter')
    windowWidth = root.winfo_reqwidth()
    windowHeight = root.winfo_reqheight()
    positionRight = int(root.winfo_screenwidth() / 2 - windowWidth / 2) - 80
    positionDown = int(root.winfo_screenheight() / 2 - windowHeight / 2) - 100
    root.geometry('320x370+{}+{}'.format(positionRight, positionDown))
    root.resizable(False, False)
    root.mainloop()

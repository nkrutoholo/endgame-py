import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from reqResp import *


def funcForTable(table, container, type):
    # types list of dicts = 1 || dict of dicts = 2 || list = 3 || dict = 4
    if type == 1:
        # print("list of dicts")
        columns = []
        for k in container:
            for j in k.keys():
                if j not in columns:
                    columns.append(j)
        table['columns'] = columns
        table.column('#0', width=0, stretch=NO)
        for j in columns:
            table.column(j, stretch=YES)
            table.heading(j, text=j, anchor=CENTER)
        i = 0
        for data in container:
            input_v = []
            for key in columns:
                input_v.append(data.get(key))
            table.insert(parent='', index=i, iid=i, text='', values=input_v)
            i = i + 1
    elif type == 2:
        # print("dict of dicts")
        columns = [""]
        for j in container.values():
            for k in j:
                if k not in columns:
                    columns.append(k)
        table['columns'] = columns
        table.column('#0', width=0, stretch=NO)
        for j in columns:
            table.column(j, stretch=YES)
            table.heading(j, text=j, anchor=CENTER)
        i = 0
        for data in container:
            input_v = [data]
            for dic in container[data]:
                input_v.append(container.get(data).get(dic))
            table.insert(parent='', index=i, iid=i, text='', values=input_v)
            i = i + 1
    elif type == 3:
        # print("list")
        table['columns'] = ("id", "value")
        table.column('#0', width=0, stretch=NO)
        table.column("id", stretch=YES)
        table.column("value", stretch=YES)
        table.heading("value", text="value", anchor=CENTER)
        table.heading("id", text="", anchor=CENTER)
        i = 0
        for data in container:
            table.insert(parent='', index=i, iid=i, text='', values=(i, data))
            i = i + 1
    elif type == 4:
        # print("dict")
        table.column('#0', width=0, stretch=NO)
        table['columns'] = ("id", "value")
        table.column("id", stretch=YES)
        table.column("value", stretch=YES)
        table.heading("value", text="value", anchor=CENTER)
        table.heading("id", text="", anchor=CENTER)
        i = 0
        for data in container:
            table.insert(parent='', index=i, iid=i, text='', values=(data, container.get(data)))
            i = i + 1


def recForTree(tree, bId, big_data, type):
    # types list = 1 || dict = 2
    tree['columns'] = ()
    tree.column('#0', width=1000, stretch=YES)
    i = 0
    for data in big_data:
        key = data
        if type == 2:
            key = big_data.get(data)
        if isinstance(key, list):
            string = f'{data}' + ": [" + f'{len(key)}' + "]"
            # print(f'list = {key}, {string}')
            newId = tree.insert(bId, i, text=string)
            recForTree(tree, newId, key, 1)
        elif isinstance(key, dict):
            if type == 1:
                string = f'{i}' + ": {" + f'{len(key)}' + "}"
            elif type == 2:
                string = f'{data}' + ": {" + f'{len(key)}' + "}"
            # print(f'dict = {key}, {string}')
            newId = tree.insert(bId, i, text=string)
            recForTree(tree, newId, key, 2)
        else:
            if type == 1:
                if isinstance(key, str):
                    string = f'{i}: "{key}"'
                else:
                    string = f'{i}: {key}'
            elif type == 2:
                if isinstance(key, str):
                    string = f'{data}: "{key}"'
                else:
                    string = f'{data}: {key}'
            # print(f'else = {key}, {string}')
            tree.insert(bId, i, text=string)
        i = i + 1


def treeFilling(tree, data):
    tree.delete(*tree.get_children())

    if isinstance(data, list):
        dicts = filter(lambda l: isinstance(l, dict), data.copy())
        other_values = filter(lambda l: isinstance(l, (dict, list)) == False, data.copy())
        if len(list(dicts)) == len(data):
            funcForTable(tree, data, 1)
        elif len(list(other_values)) == len(data):
            funcForTable(tree, data, 3)
        else:
            string = "[" + f'{len(data)}' + "]"
            bId = tree.insert('', 0, text=string)
            recForTree(tree, bId, data, 1)
    elif isinstance(data, dict):
        dicts = filter(lambda l: isinstance(l, dict), data.values())
        other_values = filter(lambda l: isinstance(l, (dict, list)) == False, data.values())
        if len(list(dicts)) == len(data):
            funcForTable(tree, data, 2)
        elif len(list(other_values)) == len(data):
            funcForTable(tree, data, 4)
        else:
            string = "{" + f'{len(data)}' + "}"
            bId = tree.insert('', 0, text=string)
            recForTree(tree, bId, data, 2)
    else:
        messagebox.showerror(title="SOMETHING WRONG WITH FILE!", message="Cannot parse this file.")


def methods_changed(event):
    print(f'You selected {methods.get()}!')


def render_packed(root, data=None):
    notebook = ttk.Notebook(root)
    notebook.pack(expand=True)

    # create frames
    frame1 = ttk.Frame(notebook)
    frame2 = ttk.Frame(notebook)

    frame1.pack(expand=True)
    frame2.pack(expand=True)

    # add frames to notebook

    notebook.add(frame1, text='Main')
    notebook.add(frame2, text='History')

    meth = tk.StringVar()
    methods = ttk.Combobox(frame1, textvariable=meth, values=('GET', 'POST', 'PATCH', 'PUT', 'DELETE'))
    methods.current(0)
    methods.bind('<<ComboboxSelected>>', methods_changed)
    methods.pack()

    tree = ttk.Treeview(frame1)
    tree.column('#0', width=30, stretch=YES)
    tree.pack()


def visual_start(db):
    root = tk.Tk()
    root.title('Endgame')
    # root.geometry('1000x800')
    # root.maxsize(1000, 1000)  # or root.minsize(100, 100)
    root.eval('tk::PlaceWindow . center')
    root.configure(background='gray')

    render_packed(root, data=None)

    root.mainloop()

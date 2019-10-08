import tkinter as tk
import os

T = None
data = []

def display_text(): 
    T.delete(1.0,tk.END)
    value = ""
    for index, item in enumerate(data):
        value += str(index + 1) + ". " + str(item) + "\n"
    T.insert(tk.END, value)

def callback(e):
    data.append(str(e.get()))
    display_text()
    e.delete(0, tk.END)

def update_past_notes(user_name): 
    global data
    file_name = user_name + ".txt"
    with open(file_name, 'w+') as output_file: 
        for line in data: 
            output_file.write(str(line) + "\n")

def remove_text(second, user_name): 
    try:
        name = str(second.get())
        value = int(name) - 1
        if value < 0: 
            update_past_notes(user_name)
            exit()
        if value >= 0 and value < len(data): 
            data.pop(value)
        display_text()
        second.delete(0, tk.END)
    except Exception as error_message:
        print(error_message)

def get_past_user_data(user_name, data): 
    file_name = user_name + ".txt"
    if os.path.exists(file_name): 
        with open(file_name) as past_data: 
            lines = past_data.readlines()
            for line in lines: 
                line = line.strip()
                base = line
                if '\n' in line:
                    base = line[:line.index('\n')]
                data.append(base)
            if len(data) > 0: 
                display_text()

def runner(user_name):
    global T, data

    master = tk.Tk()
    master.title(user_name)
    size = 50

    separator = tk.Frame(height=10, bd=1, relief=tk.SUNKEN)
    separator.pack(fill=tk.X, padx=5, pady=5)

    e = tk.Entry(master, width = size)
    e.pack()
    e.focus_set()

    b = tk.Button(master, text="Add Note", width=10, command= lambda: callback(e))
    b.pack()

    separator = tk.Frame(height=10, bd=1, relief=tk.SUNKEN)
    separator.pack(fill=tk.X, padx=5, pady=5)

    buffer = tk.Text(master, height = 1, width = size)
    buffer.insert(tk.INSERT, "Enter index to remove (-1 to quit):")
    buffer.pack()

    separatorthree = tk.Frame(height=10, bd=1, relief=tk.SUNKEN)
    separatorthree.pack(fill=tk.X, padx=5, pady=5)

    second = tk.Entry(master, width = size)
    second.pack()
    second.focus_set()
    
    remove_button = tk.Button(master, text="Remove", width=10, command= lambda: remove_text(second, user_name))
    remove_button.pack()

    separatordoes = tk.Frame(height=10, bd=1, relief=tk.SUNKEN)
    separatordoes.pack(fill=tk.X, padx=5, pady=5)

    S = tk.Scrollbar(master)
    T = tk.Text(master, height = 4, width = 50)
    S.pack(side=tk.RIGHT, fill=tk.Y)
    T.pack(side=tk.LEFT, fill=tk.Y)
    S.config(command=T.yview)
    T.config(yscrollcommand=S.set)

    get_past_user_data(user_name, data)

    tk.mainloop() 

if __name__ == '__main__': 
    runner("None")
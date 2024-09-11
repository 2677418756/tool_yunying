import tkinter as tk
from tkinter import Label, Button, Tk, filedialog, messagebox
from tkinter.ttk import Entry

import calculate


def select_path(x):
    if x == 1:
        path = filedialog.askdirectory()
        input_allStatus.delete(0, tk.END)
        input_allStatus.insert(0, path)
    elif x == 2 :
        path = filedialog.askdirectory()
        input_out_position.delete(0, tk.END)
        input_out_position.insert(0, path)


def submit():
    path = input_allStatus.get()
    output_path = input_out_position.get()
    info=""
    if path == "":
        messagebox.showinfo("提示", "请选择需要计算的文件夹")
        return
    try:
        info = calculate.generate_table(path,output_path)
        print(info)
    except Exception as e:
        messagebox.showinfo("提示",e)
        return
    messagebox.showinfo("提示", info)


root = Tk()
root.title("小工具")

path_list = []

# 获取屏幕的宽度和高度
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# 计算窗口的宽度和高度
window_width = 600
window_height = 200

# 计算窗口在屏幕中的坐标
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

# 设置窗口大小为 500x300 像素
root.geometry("600x200+"+str(x)+"+"+str(y))

# 输入 抖音1
label_allStatus = Label(root, text="请选择需要处理的文件夹位置：")
label_allStatus.grid(row=0, column=0, padx=15, pady=10)

input_allStatus = Entry(root, width=40)
input_allStatus.grid(row=0, column=1, pady=10)

button_allStatus = Button(root, text="选择", width=10, command=lambda: select_path(1))
button_allStatus.grid(row=0, column=2, padx=15, pady=10)

# 输出 文件位置
label_out_position = Label(root, text="请选择文件输出位置（可选）：")
label_out_position.grid(row=1, column=0, padx=15, pady=10)

input_out_position = Entry(root, width=40)
input_out_position.grid(row=1, column=1, pady=10)

button_out_position = Button(root, text="选择", width=10, command=lambda: select_path(2))
button_out_position.grid(row=1, column=2, padx=15, pady=10)

# 提交
button_submit = Button(root, text="提交", command=submit)
button_submit.grid(row=2, column=1, padx=15, pady=6)

root.mainloop()

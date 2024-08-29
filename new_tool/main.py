import tkinter as tk
from tkinter import Label, Button, Tk, filedialog, messagebox
from tkinter.ttk import Entry, Combobox

import calculate


def select_path(x):
    if x == 1:
        path = filedialog.askdirectory()
        input_dy_1.delete(0, tk.END)
        input_dy_1.insert(0, path)
    elif x == 2:
        path = filedialog.askdirectory()
        input_dy_2.delete(0, tk.END)
        input_dy_2.insert(0, path)
    elif x == 3:
        path = filedialog.askdirectory()
        input_ks_1.delete(0, tk.END)
        input_ks_1.insert(0, path)
    elif x == 4:
        path = filedialog.askdirectory()
        input_ks_2.delete(0, tk.END)
        input_ks_2.insert(0, path)
    elif x == 5:
        path = filedialog.askdirectory()
        input_out_position.delete(0, tk.END)
        input_out_position.insert(0, path)


def submit():
    path1 = input_dy_1.get()
    path2 = input_dy_2.get()
    path3 = input_ks_1.get()
    path4 = input_ks_2.get()
    if path1 == "" and path2 == "" and path3 == "" and path4 == "":
        messagebox.showinfo("提示", "至少选择一个需要处理的文件夹")
        return
    elif input_out_position.get() == "":
        messagebox.showinfo("提示", "请选择输出文件位置")
        return
    file_name = "发货数据 - 终表 - " + input_remarks.get()
    try:
        calculate.generate_table([path1,path2,path3,path4],input_out_position.get(),file_name)
    except Exception as e:
        messagebox.showinfo("提示",e)


root = Tk()
root.title("小工具")

path_list = []

# 获取屏幕的宽度和高度
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# 计算窗口的宽度和高度
window_width = 600
window_height = 300

# 计算窗口在屏幕中的坐标
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

# 设置窗口大小为 500x300 像素
root.geometry("600x300+"+str(x)+"+"+str(y))

# 输入 抖音1
label_dy_1 = Label(root, text="处理文件1文件夹位置：")
label_dy_1.grid(row=0, column=0, padx=15, pady=6)

input_dy_1 = Entry(root, width=40)
input_dy_1.grid(row=0, column=1, pady=6)

button_dy_1 = Button(root, text="选择", width=10, command=lambda: select_path(1))
button_dy_1.grid(row=0, column=2, padx=15, pady=6)

# 输入 抖音2
label_dy_2 = Label(root, text="处理文件2文件夹位置：")
label_dy_2.grid(row=1, column=0, padx=15, pady=6)

input_dy_2 = Entry(root, width=40)
input_dy_2.grid(row=1, column=1, pady=6)

button_dy_2 = Button(root, text="选择", width=10, command=lambda: select_path(2))
button_dy_2.grid(row=1, column=2, padx=15, pady=6)

# 输入3 快手1
label_ks_1 = Label(root, text="处理文件3文件夹位置：")
label_ks_1.grid(row=2, column=0, padx=15, pady=6)

input_ks_1 = Entry(root, width=40)
input_ks_1.grid(row=2, column=1, pady=6)

button_ks_1 = Button(root, text="选择", width=10, command=lambda: select_path(3))
button_ks_1.grid(row=2, column=2, padx=15, pady=6)

# 输入4 快手2
label_ks_2 = Label(root, text="处理文件4文件夹位置：")
label_ks_2.grid(row=3, column=0, padx=15, pady=6)

input_ks_2 = Entry(root, width=40)
input_ks_2.grid(row=3, column=1, pady=6)

button_ks_2 = Button(root, text="选择", width=10, command=lambda: select_path(4))
button_ks_2.grid(row=3, column=2, padx=15, pady=6)

# 输出路径
label_out_position = Label(root, text="请选择文件输出位置：")
label_out_position.grid(row=4, column=0, padx=15, pady=6)

input_out_position = Entry(root, width=40)
input_out_position.grid(row=4, column=1, pady=6)

button_out_position = Button(root, text="选择", width=10, command=lambda: select_path(5))
button_out_position.grid(row=4, column=2, padx=15, pady=6)

# 输出文件名
label_remarks = Label(root, text="备注：")
label_remarks.grid(row=5, column=0, padx=15, pady=6)

input_remarks = Entry(root, width=40)
input_remarks.grid(row=5, column=1, pady=6)

# 提交
button_submit = Button(root, text="提交", command=submit)
button_submit.grid(row=6, column=1, padx=15, pady=6)

root.mainloop()

from genericpath import isfile
import filecmp
import os
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import codes
import time

path = r"G:\\vsc\\testmaker\\"#null
var_index = 0
data_input = ""


def error(type):
    if type == 0:
        messagebox.showinfo(title = '错误', message = '找不到main函数入口.')

def show_example_1():
    text_iner.delete('0.0', END)
    text_iner.insert('0.0', codes.example1_iner)
    text_sol.delete('0.0', END)
    text_sol.insert('0.0', codes.example1_sol)
    text_input.delete('0.0', END)
    text_output.delete('0.0', END)

def show_example_2():
    text_iner.delete('0.0', END)
    text_iner.insert('0.0', codes.example2_iner)
    text_sol.delete('0.0', END)
    text_sol.insert('0.0', codes.example2_sol)
    text_input.delete('0.0', END)
    text_output.delete('0.0', END)

def make_input():
    global data_input
    iner_code = text_iner.get('0.0', END)
    iner_code = codes.iner_head + iner_code + codes.iner_tail
    f = open(path + "iner.py", "w")
    f.write(iner_code)
    f.close()
    os.system("python {}iner.py".format(path))
    os.remove("{}iner.py".format(path))
    f = open("{}tin.txt".format(path), "r")
    data_input = f.read()
    text_input.delete("0.0", END)
    text_input.insert("0.0", data_input[:10000])
    f.close()
    return 0

def compile():
    sol_code = text_sol.get('0.0', END)
    pos = sol_code.find("main")
    if pos == -1:
        error(0)
        return -1
    pos = sol_code.find("{", pos)
    if pos == -1:
        error(0)
        return -1
    sol_code = sol_code[ : pos + 1] + codes.sol_insert.format(path = path) + sol_code[pos + 1: -1]
    f = open("{}sol.cpp".format(path), "w")
    f.write(sol_code)
    f.close()
    os.system("g++.exe -g -Wall -std=c++11 {path}sol.cpp -o {path}sol.exe".format(path = path))
    os.remove("{}sol.cpp".format(path))
    #text_log.insert(END, "编译成功.\n")
    #text_log.update()
    return 0    

def compile2():
    dp_code = text_dp.get('0.0', END)
    pos = dp_code.find("main")
    if pos == -1:
        error(0)
        return -1
    pos = dp_code.find("{", pos)
    if pos == -1:
        error(0)
        return -1
    dp_code = dp_code[ : pos + 1] + codes.dp_insert.format(path = path) + dp_code[pos + 1: -1]
    f = open("{}dp.cpp".format(path), "w")
    f.write(dp_code)
    f.close()
    os.system("g++.exe -g -Wall -std=c++11 {path}dp.cpp -o {path}dp.exe".format(path = path))
    os.remove("{}dp.cpp".format(path))
    #text_log.insert(END, "对拍程序编译成功.\n")
    #text_log.update()
    return 0 

def run():
    input_data = text_input.get('0.0', END)
    if len(input_data) > 8888:
        input_data = data_input
    f = open("{}tin.txt".format(path), "w")
    f.write(input_data)
    f.close()
    t1 = time.perf_counter()
    os.system("{}sol.exe".format(path))
    t2 = time.perf_counter()
    f = open("{}tout.txt".format(path), "r")
    text_output.delete("0.0", END)
    text_output.insert("0.0", f.read()[:10000])
    f.close()
    dt = int((t2 - t1) * 1000)
    if dt < 0:
        dt = 0
    return dt

def run2():
    input_data = text_input.get('0.0', END)
    if len(input_data) > 8888:
        input_data = data_input
    f = open("{}tin.txt".format(path), "w")
    f.write(input_data)
    f.close()
    os.system("{}dp.exe".format(path))
    f = open("{}pout.txt".format(path), "r")
    f.close()

def make_output():
    dp_result = '/'
    status = '✓'
    if compile() == -1:
        status = '×'
    t = run() - 230
    if check_var_dp.get() == 1:
        if compile2() == -1:
            return -1
        else:
            run2()
            res = filecmp.cmp("{}tout.txt".format(path), "{}pout.txt".format(path))
            if res == True:
                dp_result = '✓'
            else:
                dp_result = '×'
    for row in tree_log.get_children():
        tree_log.delete(row)
    tree_log.insert("", 0, values = ("test", str(t) + 'ms', dp_result, status))
    return 0

def make():
    if compile() == -1:
        return -1
    if check_var_dp.get() == 1:
        if compile2() == -1:
            return -1
    pid = entry_pid.get()
    test_num = int(entry_test_num.get())
    tid = int(entry_tid.get())
    if os.path.exists("{}export".format(path)) == False:
        os.mkdir("{}export".format(path))
    if os.path.exists("{}export\\{}".format(path, pid)) == False:
        os.mkdir("{}export\\{}".format(path, pid))
    #for filename in os.listdir("{}export\\{}\\".format(path, pid)):
    #    file_path = "{}export\\{}\\{}".format(path, pid,filename)
    #    if(os.path.isfile(file_path)):
    #        os.remove(file_path)
    for row in tree_log.get_children():
        tree_log.delete(row)
    for i in range(tid, tid + test_num):
        res = make_input()
        if res != 0:
            status = '×'
        else:
            test_id = "{}{}".format(pid, i)
            dp_result = '/'
            status = '✓'
            time_run = run()
            if i == tid:
                time_run = time_run - 230
            os.system("copy {}tin.txt {}export\\{}\\{}{}.in".format(path, path, pid, pid, i))
            os.system("copy {}tout.txt {}export\\{}\\{}{}.out".format(path, path, pid, pid, i))
            if check_var_dp.get() == 1:
                run2()
                res = filecmp.cmp("{}tout.txt".format(path), "{}pout.txt".format(path))
                if res == True:
                    dp_result = '✓'
                else:
                    dp_result = '×'
        tree_log.insert("", END, values = (test_id, str(time_run) + 'ms', dp_result, status))
        tree_log.update()
    

def add_int():
    num = entry_int1.get()
    sep = entry_int2.get()
    mi = entry_int3.get()
    ma = entry_int4.get()
    name = entry_int5.get()
    is_var = check_var_varonly.get()
    random_mode = combo_var_random_model.get()
    name = ''.join(name.split())
    num = ''.join(num.split())
    mi = ''.join(mi.split())
    ma = ''.join(ma.split())
    random_mode = ''.join(random_mode.split())
    num = num.split(',')
    if random_mode == '各行递增':
        random_mode = 1
    elif random_mode == '各行递减':
        random_mode = -1
    else:
        random_mode = 0
    if len(num) == 0:
        return
    elif len(num) == 1:
        if not num[0].isdigit():
            num[0] = "var_{}".format(num[0])
    else:
        if not num[0].isdigit():
            num[0] = "var_{}".format(num[0])
        if not num[1].isdigit():
            num[1] = "var_{}".format(num[1])
    if name == '':
        global var_index
        var_index = var_index + 1
        name = 'var_{}'.format(var_index)
    elif not name.isalpha():
        error(1)
    else:
        name = 'var_{}'.format(name)
    if not mi.isdigit() and mi[0] != '-':
        mi = "var_{}".format(mi)
    if not ma.isdigit() and ma[0] != '-':
        ma = "var_{}".format(ma)
    if is_var == 0:
        if len(num) == 1:
            code = codes.add_int_1.format(num = num[0], var_name = name, mi = mi, ma = ma, sep = sep, random_mode = random_mode)
        else:
            code = codes.add_int_2.format(x = num[0], y = num[1], var_name = name, mi = mi, ma = ma, sep = sep, random_mode = random_mode)
    else:
        if len(num) == 1:
            code = codes.add_var_1.format(num = num[0], var_name = name, mi = mi, ma = ma, random_mode = random_mode)
        else:
            code = codes.add_var_2.format(x = num[0], y = num[1], var_name = name, mi = mi, ma = ma, random_mode = random_mode)
    text_iner.insert(END, code)

def add_str():
    num = entry_str1.get()
    sep = entry_str2.get()
    mi = entry_str4.get()
    ma = entry_str5.get()
    have_123 = check_var_123.get()
    have_abc = check_var_abc.get()
    have_ABC = check_var_ABC.get()
    extra = entry_str3.get()
    repeat = check_var_repeat.get()
    num = ''.join(num.split())
    mi = ''.join(mi.split())
    ma = ''.join(ma.split())
    if not num.isdigit():
        num = "var_{}".format(num)
    if not mi.isdigit():
        mi = "var_{}".format(mi)
    if not ma.isdigit():
        ma = "var_{}".format(ma)
    if repeat == 1:
        code = codes.add_str_1.format(extra = extra, have_123 = have_123, have_abc = have_abc, have_ABC = have_ABC, num = num, sep = sep, mi = mi, ma = ma)
    else:
        code = codes.add_str_2.format(extra = extra, have_123 = have_123, have_abc = have_abc, have_ABC = have_ABC, num = num, sep = sep, mi = mi, ma = ma)
    text_iner.insert(END, code)

def add_enter():
    text_iner.insert(END, codes.add_enter)

def add_space():
    text_iner.insert(END, codes.add_space)


main_window = Tk()
main_window.title("TestMaker")
main_window.geometry('1150x600+600+200')
main_window.minsize(1150, 600)
main_window.maxsize(1150, 600)
#area1
label_tips1 = Label(main_window, text = "Python for making the input data:")
label_tips1.place(x = 10, y = 12)
label_tips4 = Label(main_window, text = "Input data:")
label_tips4.place(x = 10, y = 341)
label_tips5 = Label(main_window, text = "Output data:")
label_tips5.place(x = 220, y = 341)
button_input = Button(main_window, text = "预览输入", width = 7, height = 1, command = make_input)
button_input.place(x = 10, y = 560)
button_output = Button(main_window, text = "预览输出", width = 7, height = 1, command = make_output)
button_output.place(x = 220, y = 560)
button_example1 = Button(main_window, text = "预设一", width = 8, height = 1, command = show_example_1)
button_example1.place(x = 300, y = 4)
button_example2 = Button(main_window, text = "预设二", width = 8, height = 1, command = show_example_2)
button_example2.place(x = 370, y = 4)
text_iner = Text(main_window, width = 60, height = 23)
text_iner.place(x = 12, y = 35)
text_input = Text(main_window, width = 27, height = 14)
text_input.place(x = 10, y = 364)
text_output = Text(main_window, width = 30, height = 14)
text_output.place(x = 220, y = 364)
#area2
label_int1 = Label(main_window, text = "[整数]")
label_int2 = Label(main_window, text = "生成数量:")
label_int3 = Label(main_window, text = "分隔符:")
label_int4 = Label(main_window, text = "最小值:")
label_int5 = Label(main_window, text = "最大值:")
label_int6 = Label(main_window, text = "CatchAs:")
label_int7 = Label(main_window, text = "随机模式:")
label_str1 = Label(main_window, text = "[字符串]")
label_str2 = Label(main_window, text = "生成数量:")
label_str3 = Label(main_window, text = "分隔符:")
label_str4 = Label(main_window, text = "额外字符:")
label_str5 = Label(main_window, text = "最小长度:")
label_str6 = Label(main_window, text = "最大长度:")
label_enter = Label(main_window, text = "[换行]")
label_space = Label(main_window, text = "[空格]")
button_int = Button(main_window, text = "添加", width = 7, height = 1, command = add_int)
button_int.place(x = 550, y = 80-10)
button_str = Button(main_window, text = "添加", width = 7, height = 1, command = add_str)
button_str.place(x = 730, y = 80-10)
button_enter = Button(main_window, text = "添加", width = 7, height = 1, command = add_enter)
button_enter.place(x = 550, y = 35)
button_space = Button(main_window, text = "添加", width = 7, height = 1, command = add_space)
button_space.place(x = 730, y = 35)
entry_int1 = Entry(main_window, width = 12)
entry_int1.insert("0", "5")
entry_int2 = Entry(main_window, width = 12)
entry_int2.insert("0", " ")
entry_int3 = Entry(main_window, width = 12)
entry_int3.insert("0", "1")
entry_int4 = Entry(main_window, width = 12)
entry_int4.insert("0", "100")
entry_int5 = Entry(main_window, width = 12)
entry_str1 = Entry(main_window, width = 12)
entry_str1.insert("0", "5")
entry_str2 = Entry(main_window, width = 12)
entry_str2.insert("0", r"\n")
entry_str3 = Entry(main_window, width = 12)
entry_str4 = Entry(main_window, width = 12)
entry_str4.insert("0", "1")
entry_str5 = Entry(main_window, width = 12)
entry_str5.insert("0", "10")
check_var_123 = IntVar(value = 0)
check_123 = Checkbutton(main_window, text = "123", variable = check_var_123)
check_var_abc = IntVar(value = 1)
check_abc = Checkbutton(main_window, text = "abc", variable = check_var_abc)
check_var_ABC = IntVar(value = 0)
check_ABC = Checkbutton(main_window, text = "ABC", variable = check_var_ABC)
check_var_repeat = IntVar(value = 0)
check_repeat = Checkbutton(main_window, text = "不允许出现重复字符", variable = check_var_repeat)
check_var_varonly = IntVar(value = 0)
check_varonly = Checkbutton(main_window, text = "不输出", variable = check_var_varonly)
check_var_controlled = IntVar(value = 0)
check_controlled = Checkbutton(main_window, text = "受生成模式控制", variable = check_var_controlled)
combo_var_random_model = StringVar(value = '完全随机')
combo_random_model = ttk.Combobox(main_window, width = 8, textvariable = combo_var_random_model, values = ('完全随机', '各行递增', '各行递减'))
tree_log = ttk.Treeview(main_window, height = 10, show = "headings")
tree_log["columns"] = ("tid", "run_time", "dp_result", "status")
tree_log.column("tid", width = 80, anchor = "center")
tree_log.column("run_time", width = 80, anchor = "center")
tree_log.column("dp_result", width = 80, anchor = "center")
tree_log.column("status", width = 80, anchor = "center")
tree_log.heading("tid", text = "数据组")
tree_log.heading("run_time", text = "运行耗时")
tree_log.heading("dp_result", text = "对拍结果")
tree_log.heading("status", text = "状态")
tree_log.place(x = 456, y = 325)

label_int1.place(x = 450, y = 83-10)
label_int2.place(x = 450, y = 113-10)
label_int3.place(x = 450, y = 143-10)
label_int4.place(x = 450, y = 173-10)
label_int5.place(x = 450, y = 203-10)
label_int6.place(x = 450, y = 233-10)
label_int7.place(x = 450, y = 263-10)
entry_int1.place(x = 520, y = 113-10)
entry_int2.place(x = 520, y = 143-10)
entry_int3.place(x = 520, y = 173-10)
entry_int4.place(x = 520, y = 203-10)
entry_int5.place(x = 520, y = 233-10)
label_str1.place(x = 625, y = 83-10)
label_str2.place(x = 625, y = 113-10)
label_str3.place(x = 625, y = 143-10)
label_str5.place(x = 625, y = 173-10)
label_str6.place(x = 625, y = 203-10)
label_enter.place(x = 450, y = 83-45)
label_space.place(x = 625, y = 83-45)
check_123.place(x = 625, y = 233-10)
check_abc.place(x = 675, y = 233-10)
check_ABC.place(x = 725, y = 233-10)
check_repeat.place(x = 635, y = 293-10)
check_varonly.place(x = 560, y = 293-10)
check_controlled.place(x = 450, y = 293-10)
combo_random_model.place(x = 520, y = 263-10)
label_str4.place(x = 625, y = 263-10)
entry_str1.place(x = 700, y = 113-10)
entry_str2.place(x = 700, y = 143-10)
entry_str3.place(x = 700, y = 263-10)
entry_str4.place(x = 700, y = 173-10)
entry_str5.place(x = 700, y = 203-10)
#area3
label_tips2 = Label(main_window, text = "Solution(CPP):")
label_tips2.place(x = 800, y = 12)
label_tips6 = Label(main_window, text = "对拍(CPP):")
label_tips6.place(x = 800, y = 252)
#label_tips7 = Label(main_window, text = "log:")
#label_tips7.place(x = 800, y = 392)
label_tips8 = Label(main_window, text = "生成模式:")
label_tips8.place(x = 950, y = 500)
button_make = Button(main_window, text = "MAKE", width = 7, height = 1, command = make)
button_make.place(x = 925, y = 560)
text_sol = Text(main_window, width = 47, height = 16)
text_sol.place(x = 800, y = 35)
#text_log = Text(main_window, width = 47, height = 12)
#text_log.insert("0.0", "准备就绪.\n")
#text_log.place(x = 800, y = 418)
text_dp = Text(main_window, width = 47, height = 16)
text_dp.place(x = 800, y = 277)
check_var_dp = IntVar(value = 0)
check_dp = Checkbutton(main_window, text = "启用对拍", variable = check_var_dp)
check_dp.place(x = 950, y = 250)
label_pid = Label(main_window, text = "问题编号:")
label_pid.place(x = 800, y = 500)
entry_pid = Entry(main_window, width = 3)
entry_pid.insert("0", 'A')
entry_pid.place(x = 860, y = 500)
label_test_num = Label(main_window, text = "生成数据组数:")
label_test_num.place(x = 800, y = 530)
entry_test_num = Entry(main_window, width = 3)
entry_test_num.insert("0", '10')
entry_test_num.place(x = 890, y = 530)
label_tid = Label(main_window, text = "数据组起始编号:")
label_tid.place(x = 950, y = 530)
entry_tid = Entry(main_window, width = 3)
entry_tid.insert("0", '0')
entry_tid.place(x = 1050, y = 530)
combo_var_make_model = StringVar(value = '完全随机')
combo_make_model = ttk.Combobox(main_window, width = 8, textvariable = combo_var_make_model, values = ('完全随机', '正态分布', '线性递增'))
combo_make_model.place(x = 1010, y = 500)
#
main_window.mainloop()

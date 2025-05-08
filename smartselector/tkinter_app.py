from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showerror, showwarning, showinfo

# root = Tk()
# root.title("METANIT.COM")
# root.geometry("250x200")

# def open_info(): 
#     showinfo(title="Информация", message="Информационное сообщение")
 
# def open_warning(): 
#     showwarning(title="Предупреждение", message="Сообщение о предупреждении")
 
# def open_error(): 
#     showerror(title="Ошибка", message="Сообщение об ошибке")
 
# info_button = ttk.Button(text="Информация", command=open_info)
# info_button.pack(anchor="center", expand=1)
 
# warning_button = ttk.Button(text="Предупреждение", command=open_warning)
# warning_button.pack(anchor="center", expand=1)
 
# error_button = ttk.Button(text="Ошибка", command=open_error)
# error_button.pack(anchor="center", expand=1)
 
# root.mainloop()
if __name__ == '__main__':
    while True:
        answer = input()
        if answer.lower() == 'y':
            showinfo(title="Информация", message="Информационное сообщение")
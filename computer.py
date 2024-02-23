import os
from re import T
import sys
import tkinter as tk
from tkinter import ttk
from PySide6 import QtWidgets
from PySide6.QtCore import QUrl
from PySide6.QtWidgets import QApplication
from camera import Camera
from main import create_main_window
import time
from player import Player
check=0
w=0
wrong_time=20

def countUP(): #로긴시 시작 메뉴 생성
    root.quit()
    root.destroy()
    root_2=tk.Tk()
    root_2.geometry("740x500+100+100")
    root_2.resizable(False, False)
    root_2.title("lamon os")
    # root_2.iconphoto(False, tk.PhotoImage(file='lemon.png'))

    def webing():
        if __name__ == '__main__':
            if not QtWidgets.QApplication.instance():
                web_app = QtWidgets.QApplication(sys.argv)
            else:
                web_app = QtWidgets.QApplication.instance()
            main_win = create_main_window()
            initial_urls = sys.argv[1:]
            if not initial_urls:
                initial_urls.append('http://google.com')
            for url in initial_urls:
                main_win.load_url_in_new_tab(QUrl.fromUserInput(url))
            main_win.write_bookmarks()
            web_app.exec()
        
    def file_serch():#파일 탐색기
        root_4=tk.Tk()
        root_4.geometry("740x500+100+100")
        root_4.resizable(False, False)
        root_4.title("file serch")
        def plus():#노트패드 생성
            root_5=tk.Tk()
            root_5.geometry("740x500+100+100")
            root_5.title("notepad")
            root_5.resizable(False, False)
            l1=tk.Label(root_5, text="")
            l1.grid(row=0, column=0)
            l2=tk.Label(root_5, text="")
            l2.grid(row=1, column=0)
            l3=tk.Label(root_5, text="")
            l3.grid(row=2, column=0)
            l4=tk.Label(root_5, text="")
            l4.grid(row=3, column=0)
            l5=tk.Label(root_5, text="")
            l5.grid(row=4, column=0)
            l6=tk.Label(root_5, text="")
            l6.grid(row=5, column=0)
            global text1
            text1=""
            def a(event):
                global text1
                text1=text1+"a"
                l1.config(text=text1)
            def b(event):
                global text1
                text1=text1+"b"
                l1.config(text=text1)
            def c(event):
                global text1
                text1=text1+"c"
                l1.config(text=text1)
            def d(event):
                global text1
                text1=text1+"d"
                l1.config(text=text1)
            def e(event):
                global text1
                text1=text1+"e"
                l1.config(text=text1)
            def backspace(event):
                global text1
                text1=text1-text1[-1]
                l1.config(text=text1)
            E=tk.Entry(root_5)
            E.place(x=5,y=340)
            E.bind("<a>", a)
            E.bind("<b>", b)
            E.bind("<c>", c)
            E.bind("<d>", d)
            E.bind("<e>", e)
            E.bind("<BackSpace>", backspace)
            root_5.mainloop()
        b_plus=tk.Button(root_4,overrelief="sunken", width=2, command=plus, repeatdelay=1000, repeatinterval=100, text="+")
        b_plus.pack()
        root_4.mainloop()
    def camera():
        if __name__ == '__main__':
            if not QtWidgets.QApplication.instance():
                camera_app = QtWidgets.QApplication(sys.argv)
            else:
                camera_app = QtWidgets.QApplication.instance()
            main_win = Camera()
            available_geometry = main_win.screen().availableGeometry()
            main_win.resize(available_geometry.width() / 3, available_geometry.height() / 2)
            main_win.show()
            camera_app.exec()
    def player():
        if __name__ == '__main__':
            if not QtWidgets.QApplication.instance():
                player_app = QtWidgets.QApplication(sys.argv)
            else:
                player_app = QtWidgets.QApplication.instance()
            main_win = Player()
            available_geometry = main_win.screen().availableGeometry()
            main_win.resize(available_geometry.width() / 3,
                        available_geometry.height() / 2)
            main_win.show()
            player_app.exec()

    button_internet = ttk.Button(root_2, width=9, command=webing, text="internet ")
    button_file=ttk.Button(root_2, width=9, command=file_serch, text="file serch")
    button_camera=ttk.Button(root_2, width=9, command=camera, text="camera")
    button_player=ttk.Button(root_2, width=9, command=player, text="player")


    def menu():
        global check
        if check==1 :
            check=0
            button_internet.pack_forget()
            button_file.pack_forget()
            button_camera.pack_forget()
            button_player.pack_forget()
        else:
            check=check+1
            button_internet.pack(side="bottom",anchor="w")
            button_file.pack(side="bottom",anchor="w")
            button_camera.pack(side="bottom",anchor="w")
            button_player.pack(side="bottom",anchor="w")

    def logoff():
        root_2.quit()
        root_2.destroy()

    def clock_main(): # 현재 시간 표시 / 반복
        t_main=time.time()
        kor_main = time.localtime(t_main)
        live_T_mian = time.strftime("%H:%M:%S") # Real Time
        clock_width_main.config(text=live_T_mian+"_")
        year_label_main.config(text=str(kor_main.tm_year)+"-"+str(kor_main.tm_mon)+"-"+str(kor_main.tm_mday))
        clock_width_main.after(200, clock_main)

    button_menu = ttk.Button(root_2, width=9, command=menu, text="menu")
    button_logoff = ttk.Button(root_2, width=9, command=logoff, text="logoff")
    

    clock_width_main = tk.Label(root_2, font=("Times",16), bd=1)

    year_label_main=tk.Label(root_2, font=("Times",16), bd=1)
    year_label_main.pack(side="right",anchor="s")
    clock_width_main.pack(side="right",anchor="s")
    button_logoff.pack(side="bottom",anchor="w")
    button_menu.pack(side="bottom",anchor="w")
    clock_main()
    root_2.attributes('-fullscreen', True)
    root_2.mainloop()

root=tk.Tk()

root.geometry("740x500+100+100")
root.resizable(False, False)
root.title("login")

password = tk.StringVar()


def check_data():
    global w
    global wrong_time
    if password.get() == "a":
        countUP()
        clock=False
    else:
        wrong.config(text="wrong pasword")
        w+=1
        if w==5:
            wrong.config(text="please input password after "+str(20)+" second")
            old_kor=time.strftime("%S")
            if int(time.strftime("%S"))-int(old_kor)==20:
                wrong.config(text="input your password")
            
def clock(): # 현재 시간 표시 / 반복
    t=time.time()
    kor = time.localtime(t)
    live_T = time.strftime("%H:%M:%S") # Real Time
    clock_width.config(text=live_T)
    year_label.config(text=str(kor.tm_year)+"-"+str(kor.tm_mon)+"-"+str(kor.tm_mday))
    clock_width.after(200, clock) # .after(지연시간{ms}, 실행함수)
ttk.Label(root,text="").pack()
ttk.Label(root,text="").pack()
ttk.Label(root,text="").pack()
ttk.Label(root,text="").pack()
ttk.Label(root,text="").pack()
ttk.Label(root,text="").pack()
ttk.Label(root,text="").pack()
ttk.Label(root,text="").pack()   
txt_frame = tk.Frame(root)
txt_frame.pack()    

clock_frame = tk.Frame(root)
clock_frame.pack()
year_label=tk.Label(clock_frame, font=("Times",18), bg="white", bd=8)
year_label.pack()

clock_width = tk.Label(clock_frame, font=("Times",18), bg="white", bd=8)
clock_width.pack()
clock()

# id와 password, 그리고 확인 버튼의 UI를 만드는 부분
ttk.Label(root,text="").pack()
ttk.Label(root,text="").pack()
ttk.Label(root,text="").pack()
ttk.Label(root,text="").pack()
ttk.Label(root,text="").pack()
ttk.Label(root,text="").pack()
ttk.Label(root,text="").pack()
ttk.Label(root,text="").pack()
ttk.Label(root,text="").pack()
ttk.Label(root,text="").pack()
ttk.Label(root,text="").pack()
ttk.Label(root,text="").pack()
ttk.Label(root,text="").pack()
ttk.Label(root,text="").pack()
ttk.Label(root, text = "admin").pack()
ttk.Entry(root, textvariable = password).pack()
ttk.Button(root, text = "Login", command = check_data).pack()
wrong=tk.Label(root,text="")
wrong.pack()
root.attributes('-fullscreen', True)
root.mainloop()
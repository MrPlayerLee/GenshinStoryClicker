import tkinter, pyautogui, threading, time, yaml, os, win32gui
from tkinter import ttk
from tkinter import *
import pygetwindow as gw

# Functions
def GUI():  # GUI
    global winGUI, resetPOS, reset_button, notifi_1,x, y, R_Speed, Entry_R_Speed, Status, int_R_Speed
    winGUI = tkinter.Tk()
    winGUI.title("원신 스토리 클리커")
    winGUI.geometry("220x280")
    winGUI.resizable(False, False)


    LabelText('마우스 포인터 위치 :', 'black', '5', '5')
    LabelText('클릭 속도   ─────', 'black', '5', '103')
    LabelText('(초) 단위로 계산됩니다.(권장값:0.1)', '#ff5733', '7', '125')
    Status = LabelText('비활성화', 'red', '3', '260')

    DefaultButton('프로그램 시작/종료', StartHandler, '26', '6', '14', '150')

    Entry_R_Speed = StringVar()
    SetSpeed = ttk.Entry(winGUI, textvariable=Entry_R_Speed)
    SetSpeed.place(x=150,y=103,width=60,height=20)
    SetSpeed.insert(0, round(float(R_Speed),2))

    MousePOSVisual('140', '5')
    reset_button = DefaultButton('마우스 위치 재설정', ResetMousPosition, '26', '2', '14', '32')
    LabelText('원신 스토리 클리커', 'gray', '110', '260')
    notifi_1 = tkinter.Label(winGUI, text="ESC를 눌러 설정 저장 및 잠금해제", relief="flat", fg="#ff5733")
    notifi_1.place(x=15,y=75)
    notifi_1.place_forget()

    sep_1 = ttk.Separator(winGUI, orient='horizontal')
    sep_1.pack(fill="x", pady=97)


    # 특정 키를 눌렀을 때 on_key_press 함수 호출
    winGUI.bind("<Escape>", on_key_press)

    winGUI.protocol("WM_DELETE_WINDOW", on_closing)
    winGUI.mainloop()
    return x, y, R_Speed

def MousePOSVisual(lab_x, lab_y):  # Mouse position to label
    global MousePOS

    MousePOS = tkinter.Label(winGUI, text="0, 0", relief="flat")
    MousePOS.pack()
    MousePOS.place(x=lab_x, y=lab_y)

    update_MousePos()

def LabelText(string, color, lab_x, lab_y):  # Normal Label
    TextLabel = tkinter.Label(winGUI, text=string, relief="flat", fg=color)
    TextLabel.pack()
    TextLabel.place(x=lab_x, y=lab_y)
    return TextLabel

def DefaultButton(string, DefTarget, wid, hei, lab_x, lab_y):  # Default setting Button
    button = tkinter.Button(winGUI, overrelief="flat", width=wid, height=hei, command=DefTarget, text=string)
    button.pack()
    button.place(x=lab_x, y=lab_y)
    return button

def ResetMousPosition():
    global resetPOS, IsChanged
    resetPOS = True
    reset_button.config(state="disabled")  # 버튼 비활성화
    IsChanged = True
    notifi_1.place(x=15, y=75)

    # 마우스 위치 스레드 시작
    mouse_thread = threading.Thread(target=CheckMousPOS)
    mouse_thread.daemon = True
    mouse_thread.start()

def on_key_press(event):
    global resetPOS
    resetPOS = False  # resetPOS False로 전환
    reset_button.config(state="normal")  # 버튼 활성화
    notifi_1.place_forget()

def CheckMousPOS():  # Mouse position checker
    global x, y, LocX, LocY
    while resetPOS:
        x, y = pyautogui.position()
        time.sleep(0.1)
    return x, y

def update_MousePos():  # Mouse updater
    MousePOS.config(text=f"{x}, {y}")
    winGUI.after(100, update_MousePos)

def Load_Config():
    global config
    config_path = os.path.join(os.path.dirname(__file__), "Config.yml")
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
    except FileNotFoundError:
        print("404: File not Found")
    return {'Default': {'LOC_X': 0, 'LOC_Y': 0, 'Repeat_Speed': 100}}

def Save_config():
    config_path = os.path.join(os.path.dirname(__file__), "Config.yml")  # 현재 스크립트 위치에서 Config.yml 경로 얻기
    config['Default']['LOC_X'] = Saved_X
    config['Default']['LOC_Y'] = Saved_Y
    config['Default']['Repeat_Speed'] = Saved_R_Speed
    with open(config_path, 'w') as file:
        yaml.dump(config, file)
    print("Config.yml has been updated!")

def TraceWindow():
    active_window = gw.getActiveWindow()
    if active_window is not None:
        return active_window.title == Target
    return False

def StartRepeat():
    while ToggleStart == True:
        time.sleep(waittime)
        if TraceWindow():
            #print("'원신' is Detect.")
            pyautogui.leftClick(x, y)
        #else:
        #    print("'원신' is not Detect.")
    return

def StartHandler():
    global ToggleStart, PosibleStart, waittime
    if ToggleStart == False:
        waittime = round(float(Entry_R_Speed.get()),2)
        Status.config(text="활성화", fg="green")
        ToggleStart = True
        PosibleStart = True
        print("Rapid Click Started.")
        # 마우스 클릭 스레드 시작
        click_thread = threading.Thread(target=StartRepeat)
        click_thread.daemon = True
        click_thread.start()
        #StartRepeat()
    elif ToggleStart == True:
        Status.config(text="비활성화", fg="red")
        ToggleStart = False
        PosibleStart = False
        print("Rapid Click Stoped.")
    return

def on_closing():
    global IsChanged, Saved_X, Saved_Y, Saved_R_Speed, PosibleStart
    PosibleStart = False
    Saved_X = x
    Saved_Y = y
    Saved_R_Speed = float(Entry_R_Speed.get())
    Save_config()
    winGUI.destroy()

# Main Code
Target = '원신'
IsChanged = False
resetPOS = False
PosibleStart = True
ToggleStart = False
Handler = win32gui.FindWindow(None, 'GenshinImpact.exe')
Load_Config()
x, y = config['Default'] ['LOC_X'], config['Default'] ['LOC_Y']
R_Speed = config['Default'] ['Repeat_Speed']
GUI()

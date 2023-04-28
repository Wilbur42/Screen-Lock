import os
import sys
import tkinter
import threading
import shutil
from time import sleep

import keyboard
from pynput.mouse import Controller
from PIL import Image, ImageTk # pip install pillow
import PyInstaller.__main__ # pip install pyinstaller


NAME = "ScreenLock"

def Install():
    PyInstaller.__main__.run([
        os.path.abspath(__file__),
        f'--name={NAME}',
        '--onefile',
        '--windowed',
        '--add-data',
        'background.jpg;.'
    ])

    shutil.move(os.getcwd() + f'\\dist\\{NAME}.exe', os.getcwd())

    os.remove(f'{NAME}.spec')

    sleep(5)
    shutil.rmtree('./build/')
    shutil.rmtree('./dist/')

def blockinput():
    global block_input_flag
    block_input_flag = True
    t1 = threading.Thread(target=blockinput_start)
    t1.start()
    print('[SUCCESS] Input blocked!')

def unblockinput():
    blockinput_stop()
    print('[SUCCESS] Input unblocked!')

def blockinput_start():
    global block_input_flag
    mouse = Controller()
    for i in range(150):
        keyboard.block_key(i)
    while block_input_flag:
        mouse.position = (0, 0)

def blockinput_stop():
    global block_input_flag
    for i in range(150):
        keyboard.unblock_key(i)
    block_input_flag = False

def MainLoop(tk):
    sleep(5) # Will Lock for 5 seconds
    unblockinput()
    tk.quit()

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath('.')

    return os.path.join(base_path, relative_path)

if __name__ == '__main__':


    if len(sys.argv) > 1:
        if sys.argv[1] in ["-i", "--install"]:
            Install()
    else:
        block_input_flag = False

        blockinput()

        tk = tkinter.Tk()

        tk.attributes('-fullscreen', True)
        tk.attributes('-topmost', True)

        width = tk.winfo_screenwidth()
        height = tk.winfo_screenheight()

        img = Image.open(resource_path('background.jpg')).resize((width, height))
        img = ImageTk.PhotoImage(img)

        tkinter.Label(image=img).pack()

        t = threading.Thread(target=MainLoop, args=(tk,))
        t.start()

        tk.protocol('WM_DELETE_WINDOW', lambda: sys.exit())
        tk.mainloop()

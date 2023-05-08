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


block_input_flag = False

def Install(name, background):
    PyInstaller.__main__.run([
        os.path.abspath(__file__),
        f'--name={name}',
        '--onefile',
        '--windowed',
        '--add-data',
        f'{background};.'
    ])

    shutil.move(os.getcwd() + f'\\dist\\{name}.exe', os.getcwd())

    os.remove(f'{name}.spec')

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

def MainLoop(tk, duration):
    sleep(duration)
    unblockinput()
    tk.quit()

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath('.')

    return os.path.join(base_path, relative_path)

if __name__ == '__main__':

    name = "ScreenLock"
    background = "background.jpg"
    duration = 5 # Seconds
    block_input_flag = False

    if len(sys.argv) > 1:
        for arg in ["-d", "--duration"]:
            if arg in sys.argv:
                index = sys.argv.index(arg)+1
                duration = int(sys.argv[index]) if len(sys.argv) > index+1 else duration

        for arg in ["-n", "--name"]:
            if arg in sys.argv:
                index = sys.argv.index(arg)+1
                name = sys.argv[index] if len(sys.argv) > index+1 else name

        for arg in ["-b", "--background"]:
            if arg in sys.argv:
                index = sys.argv.index(arg)+1
                background = sys.argv[index] if len(sys.argv) > index+1 else background

        if sys.argv[1] in ["--uninstall"]:
            name = sys.argv[2] if len(sys.argv) > 2 else name
            if os.path.exists(name + '.exe'):
                os.remove(name + '.exe')
            sys.exit()

        if sys.argv[1] in ["-i", "--install"]:
            name = sys.argv[2] if len(sys.argv) > 2 else name
            Install(name, background)
            sys.exit()

        if sys.argv[1] in ["-u", "--update"]:
            name = sys.argv[2] if len(sys.argv) > 2 else name
            if os.path.exists(name + '.exe'):
                os.remove(name + '.exe')
            Install(name, background)
            sys.exit()

    blockinput()

    tk = tkinter.Tk()

    tk.attributes('-fullscreen', True)
    tk.attributes('-topmost', True)

    width = tk.winfo_screenwidth()
    height = tk.winfo_screenheight()

    img = Image.open(resource_path(background)).resize((width, height))
    img = ImageTk.PhotoImage(img)

    tkinter.Label(image=img).pack()

    t = threading.Thread(target=MainLoop, args=(tk, duration))
    t.start()

    tk.protocol('WM_DELETE_WINDOW', lambda: sys.exit())
    tk.mainloop()

import os
import sys
import tkinter
import threading
import shutil
import argparse
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

    block_input_flag = False

    parser = argparse.ArgumentParser(description='Screen lock application')
    parser.add_argument('-d', '--duration', type=int, default=5, help='The duration in seconds')
    parser.add_argument('-n', '--name', default='ScreenLock', help='The name of the application')
    parser.add_argument('-b', '--background', default='background.jpg', help='The path to the background image')
    parser.add_argument('--install', action='store_true', help='Install the application')
    parser.add_argument('--update', action='store_true', help='Update the application to the latest version (reinstall)')
    parser.add_argument('--uninstall', action='store_true', help='Uninstall the application')
    args = parser.parse_args()

    duration = args.duration
    name = args.name
    background = args.background

    if args.uninstall:
        if os.path.exists(name + '.exe'):
            os.remove(name + '.exe')
        sys.exit()

    if args.install:
        Install(name, background)
        sys.exit()

    if args.update:
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

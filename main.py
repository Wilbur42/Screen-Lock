import os
import sys
import tkinter
import threading
import shutil
import argparse
from time import sleep

import keyboard
from pynput.mouse import Controller
from PIL import Image, ImageTk
import PyInstaller.__main__


class ScreenLock:
    def __init__(self, duration, name, background, password=None):
        self.duration = duration
        self.name = name
        self.background = background
        self.password = password
        self.block_input_flag = False
        self.tk = None

    def install(self):
        PyInstaller.__main__.run([
            os.path.abspath(__file__),
            f'--name={self.name}',
            '--onefile',
            '--windowed',
            '--add-data',
            f'{self.background};.'
        ])

        shutil.move(os.path.join(os.getcwd(), f'dist/{self.name}.exe'), os.getcwd())

        os.remove(f'{self.name}.spec')

        sleep(5)
        shutil.rmtree('./build/')
        shutil.rmtree('./dist/')

    def block_input(self):
        self.block_input_flag = True
        t1 = threading.Thread(target=self.block_input_start)
        t1.start()
        print('[SUCCESS] Input blocked!')

    def unblock_input(self):
        self.block_input_stop()
        print('[SUCCESS] Input unblocked!')

    def block_input_start(self):
        mouse = Controller()
        for i in list(range(56, 71)) + list(range(87, 150)):  # range(150)
            keyboard.block_key(i)
        while self.block_input_flag:
            mouse.position = (0, 0)

    def block_input_stop(self):
        if self.block_input_flag:
            for i in list(range(56, 71)) + list(range(87, 150)):  # range(150)
                keyboard.unblock_key(i)
            self.block_input_flag = False

    def main_loop(self):
        sleep(self.duration)
        self.unblock_input()
        self.tk.quit()

    def check_password(self, password_entry):
        entered_password = password_entry.get()
        if self.password and entered_password == self.password:
            self.unblock_input()
            self.tk.destroy()
        elif not self.password:
            self.unblock_input()
            self.tk.destroy()

    def resource_path(self, relative_path):
        base_path = os.path.abspath(os.path.dirname(__file__))
        return os.path.join(base_path, relative_path)

    def run(self):
        self.block_input()

        self.tk = tkinter.Tk()
        self.tk.attributes('-fullscreen', True)
        self.tk.attributes('-topmost', True)

        width = self.tk.winfo_screenwidth()
        height = self.tk.winfo_screenheight()

        img = Image.open(self.resource_path(self.background)).resize((width, height))
        img = ImageTk.PhotoImage(img)

        bg = tkinter.Label(self.tk, image=img)
        bg.pack()

        if self.password:
            print('[INFO] Password selected!')
            password_entry = tkinter.Entry(bg, show="*")
            password_entry.place(x=width // 2 - 100, y=height // 2 - 20, width=200, height=40)
            password_entry.focus()

            check_password_command = lambda event: self.check_password(password_entry)
            password_entry.bind('<Return>', check_password_command)

        t = threading.Thread(target=self.main_loop)
        t.start()

        self.tk.protocol('WM_DELETE_WINDOW', lambda: sys.exit())
        self.tk.mainloop()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Screen lock application')
    parser.add_argument('-d', '--duration', type=int, default=5, help='The duration in seconds')
    parser.add_argument('-n', '--name', default='ScreenLock', help='The name of the application')
    parser.add_argument('-b', '--background', default='background.jpg', help='The path to the background image')
    parser.add_argument('-p', '--password', help='The password required to unlock the screen')
    parser.add_argument('--install', action='store_true', help='Install the application')
    parser.add_argument('--update', action='store_true', help='Update the application to the latest version (reinstall)')
    parser.add_argument('--uninstall', action='store_true', help='Uninstall the application')
    args = parser.parse_args()

    screen_lock = ScreenLock(args.duration, args.name, args.background, args.password)

    if args.uninstall:
        if os.path.exists(screen_lock.name):
            os.remove(screen_lock.name)
        sys.exit()

    if args.install and (screen_lock.name and not os.path.exists(screen_lock.name)):
        print('File not found, installing...')
        screen_lock.install()
        sys.exit()
    elif args.install and (screen_lock.name and os.path.exists(screen_lock.name)):
        print('File already exists, please use --update or --uninstall')
        sys.exit()

    if args.update:
        if os.path.exists(screen_lock.name):
            os.remove(screen_lock.name)
        screen_lock.install()
        sys.exit()

    screen_lock.run()

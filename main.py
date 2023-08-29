from tkinter import Tk, ttk
import keyboard
import queue
from pynput.mouse import Button, Controller as MouseController
from time import sleep
from point_obj import Point

list_point_obj = []
mouse = MouseController()
click_loop = False


def destroy():
    for pt in list_point_obj:
        pt.root.destroy()

    for i in range(len(list_point_obj)):
        list_point_obj.pop()

    root.destroy()


def hide_all_markers():
    for pt in list_point_obj:
        pt.window.withdraw()


def show_all_markers():
    for pt in list_point_obj:
        pt.window.deiconify()


def add_pt():
    pt = Point()
    list_point_obj.append(pt)
    pt.create_point()


def remove_pt():
    if len(list_point_obj) > 0:
        list_point_obj[-1].root.destroy()
        list_point_obj.pop()


def get_all_click_points():
    list_click_point = []
    for pt in list_point_obj:
        list_click_point.append(pt.get_click_point())

    return list_click_point


def start_clicker():
    global click_loop

    get_all_click_points()
    q.put(hide_all_markers)

    click_loop = True
    print(click_loop)


def stop_clicker():
    global click_loop

    click_loop = False
    q.put(show_all_markers)
    print(click_loop)


def check_condition():
    while click_loop:
        for pt in get_all_click_points():
            mouse.position = pt
            mouse.click(Button.left, 1)
            sleep(2)

    root.after(1000, check_condition)


def check_queue():
    try:
        func = q.get(block=False)
    except queue.Empty:
        pass
    else:
        func()
    root.after(100, check_queue)


if __name__ == '__main__':
    q = queue.Queue()

    keyboard.add_hotkey("ctrl+alt+d", start_clicker)
    keyboard.add_hotkey("ctrl+alt+n", stop_clicker)

    root = Tk()
    root.title("Clicker by dn")
    root.attributes("-topmost", True)

    frm = ttk.Frame(root, padding=10)
    frm.grid()

    ttk.Label(frm, text="CTRL+ALT+D to start clicker").grid(column=0, row=0, columnspan=3)
    ttk.Label(frm, text="CTRL+ALT+N to stop clicker").grid(column=0, row=1, columnspan=3)
    ttk.Button(frm, text="Add Point", command=add_pt).grid(column=0, row=2, pady=5)
    ttk.Button(frm, text="Remove Point", command=remove_pt).grid(column=1, row=2, pady=5)
    ttk.Button(frm, text="Quit", command=destroy).grid(column=2, row=2)
    root.after(1000, check_condition)
    root.after(500, check_queue)
    root.mainloop()

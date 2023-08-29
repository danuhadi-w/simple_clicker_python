from tkinter import Tk, Toplevel, Canvas
from functools import partial


class Point:
    num_clicks = 1
    click_point = (0, 0)

    root = None
    window = None

    def on_window_drag(self, event, window):
        # Move the window to the new position
        x = window.winfo_pointerx() - window._offsetx
        y = window.winfo_pointery() - window._offsety
        self.window.geometry(f'+{x}+{y}')
        self.click_point = (x + window._offsetx, y + window._offsety)

    def on_window_press(self, event, window):
        # Record the current mouse position
        window._offsetx = event.x
        window._offsety = event.y

    def get_click_point(self):
        return self.click_point

    def minimize(self):
        self.root.iconify()

    def create_point(self):
        # Create the main window
        self.root = Tk()
        self.root.withdraw()

        # Create a new window
        self.window = Toplevel(self.root)
        # Initialize the list of click points

        self.window.attributes("-topmost", True)
        self.window.geometry("30x30")
        self.window.overrideredirect(True)
        self.window.attributes("-transparentcolor", "white")

        # Create a canvas to draw on
        canvas = Canvas(self.window, width=30, height=30, bg="white", highlightthickness=0)
        canvas.pack()

        # Draw a circle on the canvas
        canvas.create_oval(5, 5, 25, 25, fill="light green")

        # Bind the window events using functools.partial
        self.window.bind("<ButtonPress-1>", partial(self.on_window_press, window=self.window))
        self.window.bind("<B1-Motion>", partial(self.on_window_drag, window=self.window))

        # Run the main loop
        self.root.mainloop()

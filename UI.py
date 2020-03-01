import tkinter as tk
from tkinter import font

from PIL import ImageTk, Image

from Ui_Board import UiBoard


class TicTacToeUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title('Dummy Window')
        self.geometry("500x500")
        self.resizable(0, 0)

        self.title_font = font.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        container = tk.Frame(self)
        container.pack(side="bottom", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, MenuPage, OnePlayer, TwoPlayer):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        """Show a frame for the given page name"""
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):

    # TODO 1: put an image and other things to be seen in the homepage, Basically the menu

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='black')
        self.controller = controller

        path = "resources/img/ttt.jpeg"
        image = Image.open(path)
        image = image.resize((500, 75), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(image)
        self.panel = tk.Label(self, image=img, bg='black')
        self.panel.image = img
        self.panel.pack(side="top", fill="x", expand="yes")

        label = tk.Label(self, text="Welcome", bg='black', fg='white', height='5', font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        path = 'resources/img/GreenPlayButton.png'
        image = Image.open(path)
        image = image.resize((75, 75), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(image)
        button1 = tk.Button(self, image=img, bg='black',
                            command=lambda: controller.show_frame("MenuPage"))
        button1["border"] = "0"
        button1.image = img
        # button2 = tk.Button(self, text="Go to Page Two",
        #                     command=lambda: controller.show_frame("TwoPlayer"))
        button1.pack(side='top')
        # button2.pack()


class MenuPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='black')
        self.controller = controller

        path = "resources/img/ttt.jpeg"
        image = Image.open(path)
        image = image.resize((500, 75), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(image)
        self.panel = tk.Label(self, image=img, bg='black')
        self.panel.image = img
        self.panel.pack(side="top", fill="x", expand="yes")

        label = tk.Label(self, text="Welcome", bg='black', fg='white', font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="Go to Page One",
                            command=lambda: controller.show_frame("OnePlayer"))
        button2 = tk.Button(self, text="Go to Page Two",
                            command=lambda: controller.show_frame("TwoPlayer"))
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button1.pack()
        button2.pack()
        button.pack()


class OnePlayer(tk.Frame):

    # TODO 3: Call the AI script to make it work and render the UI for game here.

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        print(parent, "From here")
        frame = UiBoard(self, parent)
        frame.pack_propagate(0)
        frame.pack(fill=tk.BOTH, expand=1)
        frame.controller = controller
        frame.pack()
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("MenuPage"))
        button.pack()


class TwoPlayer(tk.Frame):

    # TODO 5: Call the multiplayer Logic here.

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        print(parent, "From here")
        frame = UiBoard(self, parent)
        frame.pack_propagate(0)
        frame.pack(fill=tk.BOTH, expand=1)
        frame.controller = controller
        frame.pack()
        label = tk.Label(self, text="This is page 2", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("MenuPage"))
        button.pack()


if __name__ == "__main__":
    app = TicTacToeUI()
    app.mainloop()

''' Inserting a container(frame) HERE'''
#
# frame = tk.Frame(root, bg='black')
# frame.pack_propagate(0)
# frame.pack(fill=tk.BOTH, expand=1)
#
# ''' Inserting other widgets inside the container '''
#
# label = tk.Label(frame, text="Hello World", fg='white', bg='black')
# label.pack()
#
# root.mainloop()

from tkinter import *
from tkinter import ttk
from tkinter import messagebox


def unimplemented():
    messagebox.showerror("Unimplemented", "This feature has not yet been implemented, sorry!")


if __name__ == '__main__':
    mainMenu = Tk()
    mainMenu.title("Firulais Software Center")
    mainMenu.geometry("800x600")

    menuBar = Menu(mainMenu)
    fileMenu = Menu(menuBar, tearoff=0)
    fileMenu.add_command(label="New", command=unimplemented)
    fileMenu.add_command(label="Open", command=unimplemented)
    fileMenu.add_command(label="Save", command=unimplemented)
    fileMenu.add_separator()
    fileMenu.add_command(label="Exit", command=mainMenu.quit)
    menuBar.add_cascade(label="File", menu=fileMenu)
    helpMenu = Menu(menuBar, tearoff=0)
    helpMenu.add_command(label="Help Index", command=unimplemented)
    helpMenu.add_command(label="About...", command=unimplemented)
    menuBar.add_cascade(label="Help", menu=helpMenu)

    mainMenu.config(menu=menuBar)

    frame = ttk.Frame(mainMenu, padding=10)
    frame.grid()
    ttk.Label(frame, text="Hello World!").grid(column=0, row=8)
    ttk.Button(frame, text="Quit", command=mainMenu.destroy).grid(column=1, row=8)
    mainMenu.mainloop()

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk
import csv
import sqlite3
from sqlite3 import Error
import os

LARGE_FONT = ("Verdana", 35)


# Controller for app navigation
class AppController(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title("Firulais Software Center")
        self.geometry("800x600")

        # Create/Open a Database
        databasePath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Database", "")
        os.makedirs(databasePath, exist_ok=True)
        databasePath = os.path.join(databasePath, "db_file.db")

        try:
            self.databaseConnection = sqlite3.connect(databasePath)
        except Error as e:
            messagebox.showerror("Failure connecting to database", e)

        self.executeDbQuery(""" CREATE TABLE IF NOT EXISTS transactions (
                                    transactionId integer PRIMARY KEY,
                                    date integer NOT NULL,
                                    accountId integer NOT NULL,
                                    descriptionId integer NOT NULL,
                                    amount integer NOT NULL,
                                    categoryId integer NOT NULL
                            ); """)

        self.executeDbQuery(""" CREATE TABLE IF NOT EXISTS accounts (
                                    accountId integer PRIMARY KEY,
                                    name text NOT NULL,
                                    ownerId integer NOT NULL
                            ); """)

        self.executeDbQuery(""" CREATE TABLE IF NOT EXISTS owners (
                                    ownerId integer PRIMARY KEY,
                                    name text NOT NULL
                            ); """)

        self.executeDbQuery(""" CREATE TABLE IF NOT EXISTS categories (
                                    categoryId integer PRIMARY KEY,
                                    name text NOT NULL
                            ); """)

        self.executeDbQuery(""" CREATE TABLE IF NOT EXISTS descriptions (
                                    descriptionId integer PRIMARY KEY,
                                    description text NOT NULL
                            ); """)


        # Create a menu bar
        menuBar = Menu(self)
        fileMenu = Menu(menuBar, tearoff=0)
        fileMenu.add_command(label="New file", command=unimplemented)
        fileMenu.add_command(label="Open", command=unimplemented)
        fileMenu.add_command(label="Save", command=unimplemented)
        fileMenu.add_command(label="Save as...", command=unimplemented)
        fileMenu.add_command(label="Set up", command=unimplemented)
        fileMenu.add_command(label="Print", command=unimplemented)
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", command=self.quit)
        menuBar.add_cascade(label="File", menu=fileMenu)
        editMenu = Menu(menuBar, tearoff=0)
        editMenu.add_command(label="Undo", command=unimplemented)
        editMenu.add_command(label="Redo", command=unimplemented)
        editMenu.add_command(label="Cut", command=unimplemented)
        editMenu.add_command(label="Copy", command=unimplemented)
        editMenu.add_command(label="Paste", command=unimplemented)
        editMenu.add_command(label="Delete", command=unimplemented)
        editMenu.add_command(label="Find", command=unimplemented)
        editMenu.add_command(label="Preference", command=unimplemented)
        menuBar.add_cascade(label="Edit", menu=editMenu)
        viewMenu = Menu(menuBar, tearoff=0)
        viewMenu.add_command(label="Zoom", command=unimplemented)
        viewMenu.add_command(label="Status Bar", command=unimplemented)
        menuBar.add_cascade(label="View", menu=viewMenu)
        helpMenu = Menu(menuBar, tearoff=0)
        helpMenu.add_command(label="Help Index", command=unimplemented)
        helpMenu.add_command(label="About...", command=unimplemented)
        menuBar.add_cascade(label="Help", menu=helpMenu)

        self.config(menu=menuBar)

        # Create a container frame
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Dictionary to keep references to the frames we've initialized
        self.frames = {}

        # Iterate through a tuple consisting of the different page layouts, and construct each frame
        for Page in (Home, Reports, NewData):
            frame = Page(container, self)
            self.frames[Page] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Default to the Home page
        self.showFrame(Home)

    # Display the given page
    def showFrame(self, page):
        frame = self.frames[page]
        frame.tkraise()

    # Execute query on table
    def executeDbQuery(self, query):
        try:
            cursor = self.databaseConnection.cursor()
            cursor.execute(query)
        except Error as e:
            messagebox.showerror("Failure executing database query", e)


# Home page
class Home(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        homeLabel = ttk.Label(self, text="Home", font=LARGE_FONT)
        homeLabel.grid(row=0, column=4, padx=10, pady=10)

        reportsImage = ImageTk.PhotoImage(Image.open("icons/reports.png"))
        ttk.Button(self, image=reportsImage, command=lambda: controller.showFrame(Reports)).grid(row=1, column=0)
        ttk.Label(self, text="Reports").grid(row=2, column=0)

        newDataImage = ImageTk.PhotoImage(Image.open("icons/new.png"))
        ttk.Button(self, image=newDataImage, command=lambda: controller.showFrame(NewData)).grid(row=1, column=1)
        ttk.Label(self, text="New Data").grid(row=2, column=1)


# Reports page
class Reports(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        label = ttk.Label(self, text="Reports", font=LARGE_FONT)
        label.grid(row=0, column=4, padx=10, pady=10)

        homeImage = ImageTk.PhotoImage(Image.open("icons/home.png"))
        ttk.Button(self, image=homeImage, command=lambda: controller.showFrame(Home)).grid(row=1, column=0)
        ttk.Label(self, text="Home").grid(row=2, column=0)


# New Data page
class NewData(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        label = ttk.Label(self, text="New Data", font=LARGE_FONT)
        label.grid(row=0, column=4, padx=10, pady=10)

        homeImage = ImageTk.PhotoImage(Image.open("icons/home.png"))
        ttk.Button(self, image=homeImage, command=lambda: controller.showFrame(Home)).grid(row=1, column=0)
        ttk.Label(self, text="Home").grid(row=2, column=0)

        importImage = ImageTk.PhotoImage(Image.open("icons/upload.png"))
        ttk.Button(self, image=importImage, command=self.selectFile).grid(row=1, column=1)
        ttk.Label(self, text="Import").grid(row=2, column=1)

    def selectFile(self):
        filename = filedialog.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=(('csv files', '*.csv'),)
        )

        messagebox.showinfo(title='Selected File', message=filename)

        with open(filename, newline='') as csvfile:
            csvReader = csv.reader(csvfile)
            for row in csvReader:
                print(', '.join(row))


def unimplemented():
    messagebox.showerror("Unimplemented", "This feature has not yet been implemented, sorry!")


if __name__ == '__main__':
    # Start the GUI
    app = AppController()
    app.mainloop()

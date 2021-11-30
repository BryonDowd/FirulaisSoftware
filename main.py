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

        self.executeDbQuery(""" CREATE TABLE IF NOT EXISTS configurations (
                                    configurationId integer PRIMARY KEY,
                                    name text NOT NULL,
                                    value text NOT NULL
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

    # Execute query on database
    def executeDbQuery(self, query):
        try:
            cursor = self.databaseConnection.cursor()
            return cursor.execute(query)
        except Error as e:
            messagebox.showerror("Failure executing database query", e)

    # Return the last used import path from the config table, or '/' if empty
    def getImportPath(self):
        path = self.executeDbQuery(f'select value from configurations where name = "Import Path"').fetchone()
        if path is None:
            return '/'
        else:
            return path[0]

        # Write the last used import path to the config table
    def setImportPath(self, path):
        self.executeDbQuery(f"""insert or replace into configurations (configurationId, name, value) values (
                                   (select configurationId from configurations where name = "Import Path"),
                                   "Import Path",
                                   "{path}");
                             """)

    # Return the categoryId of category
    def getCategoryId(self, category):
        categoryId = self.executeDbQuery(f'select categoryId from categories where name = "{category}"').fetchone()
        if categoryId is None:
            return self.executeDbQuery(f'insert into categories (name) values ("{category}");').lastrowid
        else:
            return categoryId[0]

    # Return the descriptionId of category
    def getDescriptionId(self, description):
        descriptionId = self.executeDbQuery(f'select descriptionId from descriptions where description = "{description}"').fetchone()
        if descriptionId is None:
            return self.executeDbQuery(f'insert into descriptions (description) values ("{description}");').lastrowid
        else:
            return descriptionId[0]

    # Insert a transaction into the database
    def insertTransaction(self, date, account, description, amount, category):
        self.executeDbQuery(f"""insert into transactions (date, accountId, descriptionId, amount, categoryId)
                                values ("{date}", "{account}", {self.getDescriptionId(description)}, "{amount}", {self.getCategoryId(category)}); """)


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

        self.controller = controller

        label = ttk.Label(self, text="New Data", font=LARGE_FONT)
        label.grid(row=0, column=4, padx=10, pady=10)

        homeImage = ImageTk.PhotoImage(Image.open("icons/home.png"))
        ttk.Button(self, image=homeImage, command=lambda: controller.showFrame(Home)).grid(row=1, column=0)
        ttk.Label(self, text="Home").grid(row=2, column=0)

        importImage = ImageTk.PhotoImage(Image.open("icons/upload.png"))
        ttk.Button(self, image=importImage, command=self.importNewData).grid(row=1, column=1)
        ttk.Label(self, text="Import").grid(row=2, column=1)

    def importNewData(self):
        results = self.controller.executeDbQuery("select name from accounts").fetchall()
        if results is None:
            accountList = []
        else:
            accountList = [r for r, in results]
        accountList.insert(0, "Create New Account")

        accountName = SelectionPopup(self, "Select an account for import.", accountList).show()

        if accountName == "Create New Account":
            while True:
                accountName = TextEntryPopup(self, "Enter an Account Name").show()
                if accountName and accountName not in accountList and accountName != "Create New Account":
                    results = self.controller.executeDbQuery("select name from owners").fetchall()
                    if results is None:
                        ownerList = []
                    else:
                        ownerList = [r for r, in results]
                    ownerList.insert(0, "Create New Owner")
                    ownerName = SelectionPopup(self, "Select an owner for this account.", ownerList).show()
                    if ownerName == "Create New Owner":
                        while True:
                            ownerName = TextEntryPopup(self, "Enter an Owner Name").show()
                            if ownerName and ownerName not in ownerList and ownerName != "Create New Owner":
                                ownerId = self.controller.executeDbQuery(f'insert into owners (name) values ("{ownerName}")').lastrowid
                                break
                    else:
                        ownerId = self.controller.executeDbQuery(f'select ownerId from owners where name = "{ownerName}"').fetchone()[0]
                    accountId = self.controller.executeDbQuery(f'insert into accounts (name, ownerId) values ("{accountName}", {ownerId})').lastrowid
                    break
        else:
            accountId = self.controller.executeDbQuery(f'select accountId from accounts where name = "{accountName}"').fetchone()[0]

        self.selectFile(accountId)

    def selectFile(self, account):
        filename = filedialog.askopenfilename(
                        title='Import a CSV file',
                        initialdir=self.controller.getImportPath(),
                        filetypes=(('csv files', '*.csv'),)
                   )

        # If the user clicks cancel, don't try to open any file.
        if not filename:
            return

        # Store the last opened file directory for next time
        self.controller.setImportPath(os.path.dirname(filename))

        with open(filename, newline='') as csvFile:
            next(csvFile)
            csvReader = csv.reader(csvFile)
            for row in csvReader:
                self.controller.insertTransaction(row[0], account, row[2], row[3], row[4])
        self.controller.databaseConnection.commit()


class TextEntryPopup(Toplevel):
    def __init__(self, parent, prompt):
        Toplevel.__init__(self, parent)
        self.prompt = Label(self, text=prompt)
        self.prompt.pack(side="top", fill="x")

        self.entryText = StringVar()
        self.entry = Entry(self, textvariable=self.entryText)
        self.entry.pack(side="top", fill="x")

        self.okButton = Button(self, text="OK", command=self.onClickOk)
        self.okButton.pack(side="right")

    def onClickOk(self):
        self.destroy()

    def show(self):
        self.wm_deiconify()
        self.entry.focus_force()
        self.wait_window()
        return self.entryText.get()


class SelectionPopup(Toplevel):
    def __init__(self, parent, prompt, options):
        Toplevel.__init__(self, parent)
        self.prompt = Label(self, text=prompt)
        self.prompt.pack(side="top", fill="x")

        self.selection = StringVar()
        self.selection.set(options[0])
        self.menu = OptionMenu(self, self.selection, *options)
        self.menu.pack(side="top", fill="x")

        self.okButton = Button(self, text="OK", command=self.onClickOk)
        self.okButton.pack(side="right")

    def onClickOk(self):
        self.destroy()

    def show(self):
        self.wm_deiconify()
        self.menu.focus_force()
        self.wait_window()
        return self.selection.get()


def unimplemented():
    messagebox.showerror("Unimplemented", "This feature has not yet been implemented, sorry!")


if __name__ == '__main__':
    # Start the GUI
    app = AppController()
    app.mainloop()

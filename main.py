from decimal import Decimal
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk
import csv
import sqlite3
from sqlite3 import Error
import os
import time
import datetime

LARGE_FONT = ("Verdana", 35)


# Controller for app navigation
class AppController(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title("Firulais Software Center")
        self.geometry("1600x800")

        # Create/Open a Database
        databasePath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Database", "")
        os.makedirs(databasePath, exist_ok=True)
        databasePath = os.path.join(databasePath, "db_file.db")

        try:
            self.databaseConnection = sqlite3.connect(databasePath)
        except Error as e:
            messagebox.showerror("Failure connecting to database", e)

        self.executeDbQuery(""" CREATE TABLE IF NOT EXISTS transactions (
                                    transactionId integer CHECK(TYPEOF(transactionId) = 'integer') PRIMARY KEY,
                                    date integer CHECK(TYPEOF(date) = 'integer') NOT NULL,
                                    accountId integer CHECK(TYPEOF(accountId) = 'integer') NOT NULL,
                                    descriptionId integer CHECK(TYPEOF(descriptionId) = 'integer') NOT NULL,
                                    amount integer CHECK(TYPEOF(amount) = 'integer') NOT NULL,
                                    categoryId integer CHECK(TYPEOF(categoryId) = 'integer') NOT NULL
                            ); """)

        self.executeDbQuery(""" CREATE TABLE IF NOT EXISTS accounts (
                                    accountId integer CHECK(TYPEOF(accountId) = 'integer') PRIMARY KEY,
                                    name text CHECK(TYPEOF(name) = 'text') UNIQUE NOT NULL,
                                    ownerId integer CHECK(TYPEOF(ownerId) = 'integer') NOT NULL
                            ); """)

        self.executeDbQuery(""" CREATE TABLE IF NOT EXISTS owners (
                                    ownerId integer CHECK(TYPEOF(ownerId) = 'integer') PRIMARY KEY,
                                    name text CHECK(TYPEOF(name) = 'text') UNIQUE NOT NULL
                            ); """)

        self.executeDbQuery(""" CREATE TABLE IF NOT EXISTS categories (
                                    categoryId integer CHECK(TYPEOF(categoryId) = 'integer') PRIMARY KEY,
                                    name text CHECK(TYPEOF(name) = 'text') UNIQUE NOT NULL
                            ); """)

        self.executeDbQuery(""" CREATE TABLE IF NOT EXISTS descriptions (
                                    descriptionId integer CHECK(TYPEOF(descriptionId) = 'integer') PRIMARY KEY,
                                    description text CHECK(TYPEOF(description) = 'text') NOT NULL
                            ); """)

        self.executeDbQuery(""" CREATE TABLE IF NOT EXISTS configurations (
                                    configurationId integer CHECK(TYPEOF(configurationId) = 'integer') PRIMARY KEY,
                                    name text CHECK(TYPEOF(name) = 'text') UNIQUE NOT NULL,
                                    value text CHECK(TYPEOF(value) = 'text') NOT NULL
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
                                   "{path}");""")

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
    def insertTransaction(self, date, accountId, description, amount, category):
        timestampDate = time.mktime(datetime.datetime.strptime(date, "%m/%d/%Y").timetuple())
        integerAmount = int((Decimal(amount).quantize(Decimal('0.01')) * 100).to_integral_value())
        self.executeDbQuery(f"""insert into transactions (date, accountId, descriptionId, amount, categoryId)
                                values ({timestampDate}, {accountId}, {self.getDescriptionId(description)}, {integerAmount}, {self.getCategoryId(category)}); """)


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
def displayAmount(amount):
    if amount is None:
        return "$0.00"
    amountValue = (Decimal(amount) / 100).quantize(Decimal('0.01'))
    if amountValue < 0.0:
        return f"(${format(-amountValue, '1.2f')})"
    else:
        return f"${format(amountValue, '1.2f')}"


class Reports(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        self.controller = controller

        label = ttk.Label(self, text="Reports", font=LARGE_FONT)
        label.grid(row=0, column=2, padx=10, pady=10)

        homeImage = ImageTk.PhotoImage(Image.open("icons/home.png"))
        ttk.Button(self, image=homeImage, command=lambda: controller.showFrame(Home)).grid(row=1, column=0)
        ttk.Label(self, text="Home").grid(row=2, column=0)

        reportTypes = ["Monthly", "Summary"]
        selectedReportType = StringVar()
        selectedReportType.set(reportTypes[0])
        reportTypeMenu = ttk.OptionMenu(self, selectedReportType, "Select a Report", *reportTypes, command=self.selectReportType)
        reportTypeMenu.grid(row=3, column=0, padx=10, pady=10)

        self.selectedYear = IntVar()
        self.yearMenu = ttk.OptionMenu(self, self.selectedYear, "Select a Year", [], command=self.selectYear)
        self.yearMenu.grid(row=4, column=0, padx=10, pady=10)

        self.monthValid = False
        self.monthsList = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        self.selectedMonth = StringVar()
        self.monthMenu = ttk.OptionMenu(self, self.selectedMonth, "Select a Month", *self.monthsList, command=self.selectMonth)
        self.monthMenu.grid(row=4, column=1, padx=10, pady=10)

        self.monthlyReport = ttk.Treeview(self, column=("Date", "Account", "Owner", "Description", "Amount", "Category"), show='headings')
        self.monthlyReport.grid(row=5, column=0, columnspan=5, padx=10, pady=10)
        self.monthlyReport.column("#1", anchor=E, width=70)
        self.monthlyReport.heading("#1", text="Date")
        self.monthlyReport.column("#2", anchor=W, width=100)
        self.monthlyReport.heading("#2", text="Account")
        self.monthlyReport.column("#3", anchor=W, width=60)
        self.monthlyReport.heading("#3", text="Owner")
        self.monthlyReport.column("#4", anchor=W, width=800)
        self.monthlyReport.heading("#4", text="Description")
        self.monthlyReport.column("#5", anchor=E, width=70)
        self.monthlyReport.heading("#5", text="Amount")
        self.monthlyReport.column("#6", anchor=W, width=150)
        self.monthlyReport.heading("#6", text="Category")

        self.summaryReport = None

        self.selectReportType(selectedReportType.get())

    def selectReportType(self, selectedReportType):
        if selectedReportType == "Monthly":
            if self.summaryReport is not None:
                self.summaryReport.grid_remove()
            latestTransaction = self.controller.executeDbQuery(f'select max(date) from transactions').fetchone()[0]
            if latestTransaction is not None:
                oldestTransaction = self.controller.executeDbQuery(f'select min(date) from transactions').fetchone()[0]

                validYears = [*range(datetime.datetime.fromtimestamp(latestTransaction).year,
                                     datetime.datetime.fromtimestamp(oldestTransaction).year - 1, -1)]
                self.yearMenu.grid()
                self.yearMenu.set_menu("Select a Year", *validYears)
            else:
                messagebox.showwarning("No data", "Cannot generate report, no transactions have been imported.")
        elif selectedReportType == "Summary":
            self.yearMenu.grid_remove()
            self.monthMenu.grid_remove()
            self.monthlyReport.grid_remove()
            self.generateSummaryReport()
        else:
            self.yearMenu.grid_remove()
            self.monthMenu.grid_remove()
            self.monthlyReport.grid_remove()
            if self.summaryReport is not None:
                self.summaryReport.grid_remove()

    def selectYear(self, selectedYear):
        self.monthMenu.grid()
        if self.monthValid:
            self.generateMonthlyReport()

    def selectMonth(self, selectedMonth):
        self.monthValid = True
        self.generateMonthlyReport()

    def generateMonthlyReport(self):
        monthNumeric = self.monthsList.index(self.selectedMonth.get()) + 1
        earliestTimestamp = time.mktime(datetime.date(self.selectedYear.get(), monthNumeric, 1).timetuple())
        latestTimestamp = time.mktime(datetime.date(self.selectedYear.get(), monthNumeric + 1, 1).timetuple()) - 1
        transactions = self.controller.executeDbQuery(f"""select transactionId, date(date, 'unixepoch'), accounts.name, owners.name, descriptions.description, amount, categories.name
                                                               from transactions JOIN accounts on transactions.accountId = accounts.accountId
                                                               join owners on accounts.ownerId = owners.ownerId
                                                               join descriptions on transactions.descriptionId = descriptions.descriptionId
                                                               join categories on transactions.categoryId = categories.categoryId
                                                               where (date between {earliestTimestamp} and {latestTimestamp});""").fetchall()
        self.monthlyReport.delete(*self.monthlyReport.get_children())
        for transaction in transactions:
            displayTransaction = list(transaction)[1:]
            displayTransaction[4] = displayAmount(displayTransaction[4])
            self.monthlyReport.insert("", END, transaction[0], values=displayTransaction)

        self.monthlyReport.grid()

    def generateSummaryReport(self):
        categories = self.controller.executeDbQuery("select name from categories").fetchall()
        if categories is None:
            return
        categories = [category for category, in categories]

        columnList = categories.copy()
        columnList.insert(0, "Month")
        self.summaryReport = ttk.Treeview(self, column=columnList, show='headings')
        self.summaryReport.column("#1", anchor=W, width=50)
        self.summaryReport.heading("#1", text="Month")
        summaryQuery = "select cast(strftime('%m', date, 'unixepoch') as integer) as month"
        for category in categories:
            summaryQuery += f", SUM(CASE WHEN categories.name = '{category}' THEN transactions.amount END)"
            self.summaryReport.column(category, anchor=E)
            self.summaryReport.heading(category, text=category)
        summaryQuery += ' from transactions join categories on transactions.categoryId = categories.categoryId where categories.name != "Payments and Credits" group by month'
        summaries = self.controller.executeDbQuery(summaryQuery).fetchall()
        if summaries is None:
            return

        self.summaryReport.delete(*self.summaryReport.get_children())
        for summary in summaries:
            displaySummary = list(summary)
            for column in range(1, len(displaySummary)):
                displaySummary[column] = displayAmount(displaySummary[column])
            self.summaryReport.insert("", END, values=displaySummary)
        self.summaryReport.grid(row=5, column=0, columnspan=5, padx=10, pady=10)


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
                if not accountName:
                    messagebox.showwarning("Prompt closed", "Aborting import.")
                    return
                elif accountName not in accountList and accountName != "Create New Account":
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
                            if not ownerName:
                                messagebox.showwarning("Prompt closed", "Aborting import.")
                                return
                            elif ownerName not in ownerList and ownerName != "Create New Owner":
                                ownerId = self.controller.executeDbQuery(f'insert into owners (name) values ("{ownerName}")').lastrowid
                                break
                            messagebox.showwarning("Invalid entry", "The entered account name either already exists or is invalid, please enter another.")
                    elif ownerName == "Select an owner for this account.":
                        messagebox.showwarning("Prompt closed", "Aborting import.")
                        return
                    else:
                        ownerId = self.controller.executeDbQuery(f'select ownerId from owners where name = "{ownerName}"').fetchone()[0]
                    accountId = self.controller.executeDbQuery(f'insert into accounts (name, ownerId) values ("{accountName}", {ownerId})').lastrowid
                    break
                messagebox.showwarning("Invalid entry", "The entered account name either already exists or is invalid, please enter another.")
        elif accountName == "Select an account for import.":
            messagebox.showwarning("Prompt closed", "Aborting import.")
            return
        else:
            accountId = self.controller.executeDbQuery(f'select accountId from accounts where name = "{accountName}"').fetchone()[0]

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

        progressPopup = Toplevel(self)
        progress = DoubleVar()
        progressBar = ttk.Progressbar(progressPopup, variable=progress, maximum=1, orient=HORIZONTAL, length=200, mode='determinate')
        progressBar.pack(pady=10)
        progressPopup.wm_deiconify()

        with open(filename, newline='') as csvFile:
            total = sum(1 for line in csvFile) - 1
            csvFile.seek(0)
            next(csvFile)
            csvReader = csv.reader(csvFile)
            for rowNumber, row in enumerate(csvReader):
                self.controller.insertTransaction(row[0], accountId, row[2], row[3], row[4])
                progress.set(rowNumber / total)
                progressPopup.update()
        self.controller.databaseConnection.commit()
        progressPopup.destroy()


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
        self.bind('<Return>', self.onClickOk)

    def onClickOk(self, arg=''):
        if self.entryText.get():
            self.destroy()

    def show(self):
        self.wm_deiconify()
        self.entry.focus_force()
        self.wait_window()
        return self.entryText.get()


class SelectionPopup(Toplevel):
    def __init__(self, parent, prompt, options):
        Toplevel.__init__(self, parent)

        self.prompt = prompt
        self.selection = StringVar()
        self.selection.set(options[0])
        self.menu = ttk.OptionMenu(self, self.selection, prompt, command=self.onSelection, *options)
        self.menu.pack(side="top", fill="x")
        self.bind('<Return>', self.onSelection)

    def onSelection(self, arg=''):
        if self.selection.get() != self.prompt:
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

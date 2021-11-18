from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk
import csv


LARGE_FONT = ("Verdana", 35)

# Controller for app navigation
class AppController(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        # Create a container frame
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Dictionary to keep references to the frames we've initialized
        self.frames = {}

        # Iterate through a tuple consisting of the different page layouts, and construct each frame
        for page in (Home, Reports, NewData):
            frame = page(container, self)
            self.frames[page] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Default to the Home page
        self.show_frame(Home)

    # Display the given page
    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()


# Home page
class Home(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        homeLabel = ttk.Label(self, text="Home", font=LARGE_FONT)
        homeLabel.grid(row=0, column=4, padx=10, pady=10)

        reportsImage = ImageTk.PhotoImage(Image.open("icons/reports.png"))
        ttk.Button(self, image=reportsImage, command=lambda: controller.show_frame(Reports)).grid(row=1, column=0)
        ttk.Label(self, text="Reports").grid(row=2, column=0)

        newDataImage = ImageTk.PhotoImage(Image.open("icons/new.png"))
        ttk.Button(self, image=newDataImage, command=lambda: controller.show_frame(NewData)).grid(row=1, column=1)
        ttk.Label(self, text="New Data").grid(row=2, column=1)


# Reports page
class Reports(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        label = ttk.Label(self, text="Reports", font=LARGE_FONT)
        label.grid(row=0, column=4, padx=10, pady=10)

        homeImage = ImageTk.PhotoImage(Image.open("icons/home.png"))
        ttk.Button(self, image=homeImage, command=lambda: controller.show_frame(Home)).grid(row=1, column=0)
        ttk.Label(self, text="Home").grid(row=2, column=0)

# New Data page
class NewData(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        label = ttk.Label(self, text="New Data", font=LARGE_FONT)
        label.grid(row=0, column=4, padx=10, pady=10)

        homeImage = ImageTk.PhotoImage(Image.open("icons/home.png"))
        ttk.Button(self, image=homeImage, command=lambda: controller.show_frame(Home)).grid(row=1, column=0)
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
                print(', '.join(row))u



def unimplemented():
    messagebox.showerror("Unimplemented", "This feature has not yet been implemented, sorry!")


if __name__ == '__main__':
    # mainMenu = Tk()
    # mainMenu.title("Firulais Software Center")
    # mainMenu.geometry("800x600")
    #
    # menuBar = Menu(mainMenu)
    # fileMenu = Menu(menuBar, tearoff=0)
    # fileMenu.add_command(label="New file", command=unimplemented)
    # fileMenu.add_command(label="Open", command=unimplemented)
    # fileMenu.add_command(label="Save", command=unimplemented)
    # fileMenu.add_command(label="Save as...", command=unimplemented)
    # fileMenu.add_command(label="Set up", command=unimplemented)
    # fileMenu.add_command(label="Print", command=unimplemented)
    # fileMenu.add_separator()
    # fileMenu.add_command(label="Exit", command=mainMenu.quit)
    # menuBar.add_cascade(label="File", menu=fileMenu)
    # editMenu = Menu(menuBar, tearoff=0)
    # editMenu.add_command(label="Undo", command=unimplemented)
    # editMenu.add_command(label="Redo", command=unimplemented)
    # editMenu.add_command(label="Cut", command=unimplemented)
    # editMenu.add_command(label="Copy", command=unimplemented)
    # editMenu.add_command(label="Paste", command=unimplemented)
    # editMenu.add_command(label="Delete", command=unimplemented)
    # editMenu.add_command(label="Find", command=unimplemented)
    # editMenu.add_command(label="Preference", command=unimplemented)
    # menuBar.add_cascade(label="Edit", menu=editMenu)
    # viewMenu = Menu(menuBar, tearoff=0)
    # viewMenu.add_command(label="Zoom", command=unimplemented)
    # viewMenu.add_command(label="Status Bar", command=unimplemented)
    # menuBar.add_cascade(label="View", menu=viewMenu)
    # helpMenu = Menu(menuBar, tearoff=0)
    # helpMenu.add_command(label="Help Index", command=unimplemented)
    # helpMenu.add_command(label="About...", command=unimplemented)
    # menuBar.add_cascade(label="Help", menu=helpMenu)
    #
    # mainMenu.config(menu=menuBar)
    #
    # frame = ttk.Frame(mainMenu, padding=10)
    # frame.grid()

    # Start the GUI
    app = AppController()
    app.mainloop()

    #
    # categoryImage = ImageTk.PhotoImage(Image.open("icons/category.png"))
    # ttk.Button(frame, image=categoryImage, command=categoryClicked).grid(column=1, row=1)
    # ttk.Label(frame, text="Categories").grid(column=1, row=2)
    #
    # documentsImage = ImageTk.PhotoImage(Image.open("icons/documents.png"))
    # ttk.Button(frame, image=documentsImage, command=documentsClicked).grid(column=2, row=1)
    # ttk.Label(frame, text="Documents").grid(column=2, row=2)
    #
    # new_projectImage = ImageTk.PhotoImage(Image.open("icons/new_project.png"))
    # ttk.Button(frame, image=new_projectImage, command=new_projectClicked).grid(column=3, row=1)
    # ttk.Label(frame, text="New Project").grid(column=3, row=2)
    #
    # printImage = ImageTk.PhotoImage(Image.open("icons/print.png"))
    # ttk.Button(frame, image=printImage, command=printClicked).grid(column=4, row=1)
    # ttk.Label(frame, text="Print").grid(column=4, row=2)
    #
    #
    #
    # settingsImage = ImageTk.PhotoImage(Image.open("icons/settings.png"))
    # ttk.Button(frame, image=settingsImage, command=settingsClicked).grid(column=6, row=1)
    # ttk.Label(frame, text="Settings").grid(column=6, row=2)
    #
    # uploadImage = ImageTk.PhotoImage(Image.open("icons/upload.png"))
    # ttk.Button(frame, image=uploadImage, command=uploadClicked).grid(column=7, row=1)
    # ttk.Label(frame, text="Upload").grid(column=7, row=2)
    #
    # downloadImage = ImageTk.PhotoImage(Image.open("icons/download.png"))
    # ttk.Button(frame, image=downloadImage, command=downloadClicked).grid(column=8, row=1)
    # ttk.Label(frame, text="Download").grid(column=8, row=2)

"""
File: sorting_gui.py

A simple GUI using tkinter to help you move and sort files in a folder.
Sorts files into Music, Documents, Videos, Compressed, Photos, Programs and
Miscellaneous.
You are also able to delete the folder which you just sorted.

Exceptions handled(PermissionError and FileNotFoundError) are printed
to the stderr stream
"""

import os
from tkinter import *
import tkinter.messagebox
import tkinter.filedialog
import tkinter.font
import move_files


class SortingGUI:
    def __init__(self, window):
        self.window = window
        self.create_gui()

    def create_gui(self):
        """
        GUI contains a menu bar and three frames:
            -> Left: Contains description.
            -> Middle: Folder selection, Sort button.
            -> Right: Additional options - Check no of files and Delete button.
        """
        self.create_menu()
        self.create_left_frame()
        self.create_middle_frame()
        self.create_right_frame()

    def create_menu(self):
        """Menu creation"""
        main_menu = Menu(self.window)
        self.window.config(menu=main_menu, bg="gray35")

        # file menu
        file_menu = Menu(main_menu, tearoff=0)
        main_menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Exit", command=quit)

    def create_left_frame(self):
        """Includes a label that describes what the program does."""
        left_frame = Frame(self.window, bg="gray25", width=150, height=300).grid(row=0, column=0, rowspan=2)
        left_label1 = Label(left_frame, text="\nWelcome to File-Sorter app\n", justify=LEFT, bg="gray25", fg="white")
        left_label1.grid(row=0)
        f = tkinter.font.Font(left_label1, left_label1.cget("font"))
        f.configure(underline=TRUE)
        left_label1.configure(font=f)

        left_label2 = Label(left_frame, text="This program lets you sort\n"
                                            "files into:\n"
                                            "\u2022 Music\n"
                                            "\u2022 Videos\n"
                                            "\u2022 Documents\n"
                                            "\u2022 Compressed\n"
                                            "\u2022 Photos\n"
                                            "\u2022 Miscellaneous\n\n\n\n"
                                            "Before starting make sure:\n"
                                            "\u2022 All files are closed\n"
                                            "  in the folder you want\n"
                                            "  to sort.\n", justify=LEFT, bg="gray25", fg="white")
        left_label2.grid(row=1)

    def create_middle_frame(self):
        """
        Includes:
            ->Labels, Entry Box and Buttons for Source and Destination folder.
            ->Sort and Quit button.
        """
        mid_frame = Frame(self.window, width=300, height=300, bd=2, bg="gray35")
        mid_frame.grid(row=0, column=1, rowspan=8, columnspan=3)

        # Source folder Label
        source_label = Label(mid_frame, text="Source folder", pady=10, bg="gray35", fg="white")
        source_label.grid(row=0, column=1, sticky=E)

        # Source Entry Box
        self.source_entry = Entry(mid_frame, font="Verdana 8 italic", bg="gray50", fg="white")
        self.source_entry.grid(row=0, column=2)
        self.source_entry.insert(0, "Select folder")

        # Source folder 'Select' button
        source_button = Button(mid_frame, text="Select", command=self.source_directory, width=5,
                               bg="gray35", fg="white")
        source_button.grid(row=0, column=3)

        # empty Label
        Label(mid_frame, text="", bg="gray35").grid(row=1)

        # Destination folder Label
        dest_label = Label(mid_frame, text="Destination folder", pady=10, bg="gray35", fg="white")
        dest_label.grid(row=2, column=1)

        # Destination Entry Box
        self.dest_entry = Entry(mid_frame, font="Verdana 8 italic", bg="gray50", fg="white")
        self.dest_entry.grid(row=2, column=2)
        self.dest_entry.insert(0, "Select folder")

        # Destination folder 'Select' button
        dest_button = Button(mid_frame, text="Select", command=self.dest_directory, width=5,
                             bg="gray35", fg="white")
        dest_button.grid(row=2, column=3)

        # empty Label
        Label(mid_frame, text="", bg="gray35").grid(row=3)

        # Sort Button
        sort_button = Button(mid_frame, text="Sort", command=self.sort_folder, width=10,
                             bg="gray35", fg="white")
        sort_button.grid(row=4, column=2)

        # empty Label
        Label(mid_frame, text="", bg="gray35").grid(row=5)

        # Quit Button
        quit_button = Button(mid_frame, text="Quit", width=10, bg="gray35", fg="white")
        quit_button.grid(row=6, column=2)
        quit_button.bind("<Button-1>", self.quit_prompt)

        # Information label
        inform_label = Label(mid_frame, text="\n\nIf sort or delete button have turned "
                                             "light\ngray ,it means the app is "
                                             "processing.", justify=CENTER, bg="gray35", fg="yellow")
        inform_label.grid(row=7, column=1, columnspan=3)

    def create_right_frame(self):
        """
        Includes:
            ->File Count button: Gives you number of files currently in the source folder.
            ->Delete Folder button: Deletes the source folder entirely.
        """
        right_frame = Frame(self.window, bg="gray25", width=200, height=300)
        right_frame.grid(row=0, column=5, rowspan=6, columnspan=2)

        # Count files label
        count_label = Label(right_frame, text="Click 'File Count' button\n"
                                              "to see if all files have been\n"
                                              "moved.\n", justify=LEFT, bg="gray25", fg="white")
        count_label.grid(row=0, column=5)

        # Count files button
        count_button = Button(right_frame, text="File Count", command=self.check_count,
                              bg="gray25", fg="white")
        count_button.grid(row=1, column=5)

        # Delete source folder label
        delete_label = Label(right_frame, text="\n\nWant to delete the folder   \n"
                                               "which you have already\n"
                                               "sorted?", justify=LEFT, bg="gray25", fg="white")
        delete_label.grid(row=2, column=5)

        # Note label
        note_label = Label(right_frame, text="Note: Delete Folder deletes\n"
                                             "the source folder entirely.\n"
                                             "Only proceed if file count\n"
                                             "comes up 0.\n", justify=LEFT, bg="gray25", fg="red")
        note_label.grid(row=3, column=5)

        # Delete source folder button
        delete_button = Button(right_frame, text="Delete Folder", command=self.delete_source_folder,
                               bg="gray25", fg="white")
        delete_button.grid(row=4, column=5)

        # empty Label
        Label(right_frame, text="", bg="gray25").grid(row=5)

    def source_directory(self):
        """ Prompts and returns the selected folder into the Source Entry box."""
        src = tkinter.filedialog.askdirectory(initialdir=os.getcwd(),
                                              title="Select the folder you would like to sort")
        if src:
            self.source_entry.delete(0, END)
            self.source_entry.insert(0, src)

    def dest_directory(self):
        """Prompts and returns the selected folder into the Destination Entry box."""
        dest = tkinter.filedialog.askdirectory(initialdir=os.getcwd(),
                                               title="Select destination folder")
        if dest:
            self.dest_entry.delete(0, END)
            self.dest_entry.insert(0, dest)

    def sort_folder(self):
        """
        Moves and sorts files from source folder into destination folder.
        Raises an error if source and destination folder have not been selected or invalid.
        """
        if os.path.isdir(self.source_entry.get()) and os.path.isdir(self.dest_entry.get()):
            move_files.sort_files(self.source_entry.get() + os.sep, self.dest_entry.get() + os.sep)
        else:
            tkinter.messagebox.showerror("Directory Error", "Please select 'Source' and 'Destination' folder")

    def check_count(self):
        """
        Counts number of files present in source folder.
        Raises an error if source folder has not been selected or path is invalid.
        """
        if os.path.isdir(self.source_entry.get()):
            total = 0
            for root, subdir, files in os.walk(self.source_entry.get()):
                total += len(files)
            tkinter.messagebox.showinfo("File Count", f"File count in source folder = {total}")
        else:
            tkinter.messagebox.showerror("Source Directory Error", f"Please select 'Source folder'")

    def delete_source_folder(self):
        """
        Deletes source folder.
        Raises an error if source folder has not been selected or path is invalid.
        """
        if os.path.isdir(self.source_entry.get()):
            # Delete source folder
            move_files.delete_folder(self.source_entry.get() + os.sep)
        else:
            tkinter.messagebox.showerror("Source Directory Error", "Please select 'Source folder'")

    def quit_prompt(self, event):
        """Quit button handler"""
        answer = tkinter.messagebox.askquestion("Quit?", "Do you want to quit?")
        if answer == "yes":
            quit()


if __name__ == "__main__":
    gui = Tk()
    gui.title("File Sorter")
    gui.geometry("600x300")
    # Commented as on MAC, the gui doesnt come up as expected. MAC users will be able to resize gui.
    # gui.resizable(FALSE, FALSE)
    app = SortingGUI(gui)
    gui.mainloop()

"""
File: move_files.py

Main functions:
    -> sort_files(src, dest) helps sort files into:
    Music, Documents, Videos, Compressed, Photos, Programs and
    Miscellaneous.
    Makes use of functions ext_folder_map() and dest_folder()

    -> delete_folder(src) function deletes a folder completely,
    in case you would like to delete it after sorting.

Exceptions handled: PermissionError and FileNotFoundError
All exceptions are printed to stderr stream.
"""

import os
import sys
import shutil


def ext_folder_map():
    """Returns a dict that maps file extensions to respective folders."""

    # dict that maps folders to different extensions
    folder_ext_dict = {"Music": {".aif", ".cda", ".mid", ".midi", ".mp3", ".mpa",
                                 ".ogg", ".wav", ".wma", ".wpl"},
                       "Documents": {".doc", ".docx", ".pdf", ".rtf", ".txt", ".wpd",
                                     ".xls", ".xlsx", ".xlr", ".pps", ".ppt", ".pptx"},
                       "Videos": {".avi", ".flv", ".m4v", ".mkv", ".mov", ".mp4",
                                  ".mpg", ".mpeg", ".rm", ".vob", ".wmv"},
                       "Compressed": {".7z", ".arj", ".deb", ".pkg", ".rar", ".rpm",
                                      ".tar", ".gz", ".z", ".zip"},
                       "Photos": {".ai", ".bmp", ".gif", ".ico", ".jpeg", ".jpg",
                                  ".png", ".ps", ".psd", ".svg", ".tif", ".tiff"},
                       "Programs": {".apk", ".bat", ".bin", ".cgi", ".pl", ".com",
                                    ".exe", ".gadget", ".jar", ".py", ".wsf"}
                       }

    # maps extensions to folder(reversed folder_ext_dict)
    ext_folder_dict = {}
    for folder, extensions in folder_ext_dict.items():
        for ext in extensions:
            ext_folder_dict[ext] = folder

    return ext_folder_dict


def dest_folder(file_ext, map_dict, dest):
    """
    Returns folder where the file is to be sorted.
    If the folder doesnt already exist, it creates one in the
    destination directory.
    """
    if file_ext.lower() in map_dict:
        folder = map_dict[file_ext.lower()] + os.sep
    else:
        folder = "Miscellaneous" + os.sep

    if not os.path.isdir(dest + folder):
        try:
            os.mkdir(dest + folder)
        except PermissionError as e:
            print("Error occurred:", e, file=sys.stderr)

    return folder


def sort_files(src, dest):
    """
    Sorts files according to their extensions (which are mapped to
    different folders in the ext_folder_dict).

    If it cant recognise a file extension or if a file doesn't have an
    extension, it moves the file into Miscellaneous folder.

    If a file already exists, it appends a number to the file name.
    For example-
        If 'a.txt' already exists, it would append (1) making it 'a(1).txt'.
        If 'a.txt' and 'a(1).txt' exist, it would append (2) making it 'a(2).txt'.
    """
    ext_folder_dict = ext_folder_map()

    for (root, subs, files) in os.walk(src):
        for file in files:
            src = os.path.join(root, file)
            file_ext = os.path.splitext(file)[-1]
            folder = dest_folder(file_ext, ext_folder_dict, dest)

            if os.path.exists(dest + folder + file):
                # Checks if file already exists.
                # If it does, while loop determines the number(copy_num) to
                # be appended to file name to avoid overwriting existing file.
                copy_num = 1
                new_dest = dest + folder + os.path.splitext(file)[0] + f"({copy_num})" + file_ext
                while os.path.exists(new_dest):
                    copy_num += 1
                    new_dest = dest + folder + os.path.splitext(file)[0] + f"({copy_num})" + file_ext
                try:
                    shutil.move(src, new_dest)
                except (PermissionError, FileNotFoundError) as e:
                    print("Error occurred:", e, file=sys.stderr)
            else:
                try:
                    shutil.move(src, dest + folder + file)
                except (PermissionError, FileNotFoundError) as e:
                    print("Error occurred:", e, file=sys.stderr)


def delete_folder(src):
    """Deletes the folder."""
    try:
        shutil.rmtree(src)
    except (PermissionError, FileNotFoundError) as e:
        print("Error occurred:", e, file=sys.stderr)

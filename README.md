# File-Sorter
![Alt Text](https://github.com/starter-coder/File-Sorter/blob/master/images/file-sorter.png)
## Description
A simple tkinter GUI that lets you sort files into Music, Videos, Documents, Photos, Programs, Compressed and Miscellaneous.
## Usage
Its pretty easy to use.
* Select the source and destination folder by using the select button or you can type the path in. Then select the sort button to sort your files.
* You can use the File Count button to see how many files are in the source folder at any time.
* There is a Delete Folder button which you can use to delete your source folder.
* If the app is showing the Sort button or Delete Folder button in light gray colour, then it means it is currently sorting or deleting folder. Once the process is complete, they will change back to dark gray.
* The exceptions handled are - Permission Error and FileNotFoundError. They will displayed on run window(or cmd or console) and are output to stderr stream.
## Limitations
* You cannot have destination folder as a sub-directory of source folder. 
## Installation
## Future Improvements

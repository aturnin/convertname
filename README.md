# convertname
Renaming e-book files.
Supported extensions: "epub", "fb2".
The new title is extracted from the metadata of e-books and
recorded in the format "Author - Book Title".
File run_convert.py runs from the command line.
Using the command line parameter, you can specify the directory in which files will
be searched (os.walk(..)) and renamed.
If the parameter is not specified, the startup directory is scanned.


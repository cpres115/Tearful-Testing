# Tearful-Testing

## list_files.py

Writes a text file listing every file in a folder and all of its sub-folders, one path per line.
Needs Python 3.8 or newer; no extra packages.

```
python list_files.py                                  # asks for the folder
python list_files.py "D:\Drawings"                    # saves file_list_Drawings.txt in the current folder
python list_files.py "D:\Drawings" -o drawings.txt    # choose the output file
python list_files.py "D:\Drawings" --relative         # paths relative to D:\Drawings instead of full paths
```

Folders that cannot be read (for example, no permission) are skipped and named at the end of the run.

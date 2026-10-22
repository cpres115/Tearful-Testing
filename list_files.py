"""Write a text file listing every file in a folder and all of its sub-folders.

Usage:
    python list_files.py                          (asks for the folder)
    python list_files.py "D:\\Drawings"
    python list_files.py "D:\\Drawings" -o drawings.txt --relative

The text file has one path per line, sorted folder by folder. Without -o it is
saved in the current folder as file_list_<folder name>.txt.
"""
import argparse
import os
import sys


def find_files(folder, skip=None):
    """Return (paths, problems): every file path under folder, and the
    sub-folders that could not be read. A path equal to skip is left out."""
    paths = []
    problems = []
    for root, dirs, files in os.walk(folder, onerror=problems.append):
        dirs.sort(key=str.lower)
        for name in sorted(files, key=str.lower):
            path = os.path.join(root, name)
            if skip and os.path.normcase(os.path.abspath(path)) == skip:
                continue
            paths.append(path)
    return paths, problems


def default_output_name(folder):
    name = os.path.basename(os.path.normpath(folder))
    # A drive root such as D:\ has no folder name.
    name = "".join(c for c in name if c.isalnum() or c in " -_.").strip()
    return f"file_list_{name or 'root'}.txt"


def main():
    parser = argparse.ArgumentParser(
        description="List every file in a folder and its sub-folders in a text file.")
    parser.add_argument("folder", nargs="?", help="folder to list (asked for if left out)")
    parser.add_argument("-o", "--output", help="text file to write")
    parser.add_argument("--relative", action="store_true",
                        help="write paths relative to the folder instead of full paths")
    args = parser.parse_args()

    asked = args.folder is None
    folder = args.folder
    if asked:
        # Windows "Copy as path" wraps the path in quotes.
        folder = input("Folder to list: ").strip().strip('"')
    if not os.path.isdir(folder):
        print(f"Not a folder: {folder}", file=sys.stderr)
        if asked:
            input("Press Enter to close...")
        return 2
    folder = os.path.abspath(folder)

    output = os.path.abspath(args.output or default_output_name(folder))
    # If the text file is saved inside the folder, don't list it.
    paths, problems = find_files(folder, skip=os.path.normcase(output))
    if args.relative:
        paths = [os.path.relpath(p, folder) for p in paths]

    # backslashreplace keeps going on the rare file name that is not valid Unicode.
    with open(output, "w", encoding="utf-8", errors="backslashreplace") as f:
        for path in paths:
            f.write(path + "\n")

    print(f"Listed {len(paths)} files from {folder}")
    print(f"Saved to {output}")
    if problems:
        print(f"Could not read {len(problems)} folder(s):", file=sys.stderr)
        for err in problems:
            print(f"  {err.filename}: {err.strerror}", file=sys.stderr)
    if asked:
        input("Press Enter to close...")
    return 0


if __name__ == "__main__":
    sys.exit(main())

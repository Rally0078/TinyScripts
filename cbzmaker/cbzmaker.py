import shutil
import argparse
import os
import sys

def makeCBZ(folderName, wd=None):
    dir_name = wd
    if(wd is None):
        dir_name = os.getcwd()
    fileName = os.path.join(dir_name, folderName)
    shutil.make_archive(fileName, "zip", os.path.join(dir_name, folderName))
    newName = os.path.join(dir_name, folderName + ".cbz")
    print(f"Making file {fileName + ".cbz"}")
    if(os.path.isfile(fileName + ".cbz")):
        os.remove(fileName + ".cbz")
        print(f"File \"{fileName + ".cbz"}\" already exists! Deleting and remaking it...")
    
    os.rename(fileName + ".zip", newName)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog="Make CBZ file from jpegs",
        description="Make a CBZ file from a list of folders given in a textfile, or make CBZ one by one"
    )
    parser.add_argument("-d", "--directory",
                        type=str, action="store",
                        help="Working directory (by default, it is the current working directory)", default=None)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-f", "--file", 
                        type=str, action="store", 
                        help="The name of the text file containing names of the folders", default=None)
    group.add_argument("-i", "--folder", 
                        type=str, action="store", 
                        help="The name of one folder", default=None)
    group.add_argument("-a", "--all", 
                        action="store_true", 
                        help="All folders in the current working directory", default=False)
    
    args = parser.parse_args()
    print(f"Working directory: {args.directory}")
    if(args.all is False):
        if(args.file is None):
            makeCBZ(args.folder, args.directory)
        if(args.folder is None):
            with open(args.file, 'r') as file:
                folderNameList = [line.rstrip('\n') for line in file]
            for folderName in folderNameList:
                makeCBZ(folderName, args.directory)
    if(args.all is True):
        cwd = args.directory
        if(args.directory is None):
            cwd = "./"
        with os.scandir(path=cwd) as it:
            for file in it:
                if file.is_dir():
                    makeCBZ(file.name, args.directory)
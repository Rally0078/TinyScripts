import os
import sys

def main():
    bytes_list = [b'\xff\xd8\xff']
    files_list = []
    wd='./'
    if len(sys.argv) == 2:
        wd=sys.argv[1]
    count = 0
    with os.scandir(path=wd) as it:
        for file in it:
            if file.is_file() and os.path.splitext(file.name)[1] =='':
                with open(file.name, 'rb') as f:
                    byte = f.read(3)
                    if byte in bytes_list:
                        files_list.append(file)
                        
    for file in files_list:
        oldName = os.path.join(wd, file.name)
        newName= os.path.join(wd, file.name + '.jpg')
        print(f"Renaming {oldName} to {newName}")
        count = count + 1
        os.rename(oldName, newName)
    print(f"Renamed {count} file(s) successfully")

if __name__ == '__main__':
    main()

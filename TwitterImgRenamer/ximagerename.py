import os
import sys

def main():
    png_byte = b'\x89\x50\x4e'
    jpeg_byte = b'\xff\xd8\xff'
    bytes_dict = {
        png_byte: '.png',
        jpeg_byte: '.jpg'
    }
    files_list = []
    extensions_list = []
    wd='./'
    if len(sys.argv) == 2:
        wd=sys.argv[1]
    count = 0
    with os.scandir(path=wd) as it:
        for file in it:
            if file.is_file() and os.path.splitext(file.name)[1] =='':
                with open(file.name, 'rb') as f:
                    byte = f.read(3)
                    for byte_key, extension in bytes_dict.items():
                        if byte == byte_key:
                            files_list.append(file)
                            extensions_list.append(extension)
                        
    for file, extension in zip(files_list, extensions_list):
        oldName = os.path.join(wd, file.name)
        newName = os.path.join(wd, file.name + extension)
        if(os.path.isfile(newName)):
            print(f"{newName} already exists! Skipping...")
        else:
            print(f"Renaming {oldName} to {newName}")
            count = count + 1
            os.rename(oldName, newName)
    print(f"Renamed {count} file(s) successfully")

if __name__ == '__main__':
    main()

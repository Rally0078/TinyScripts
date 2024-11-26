import os
from pathlib import Path
import csv
import argparse
import textwrap

version_byte_dict = {
        1: b'\x01',
        7: b'\x07',
        8: b'\x08'
    }

def check_version(version: str):
    if version not in ['1', '7', '8']:
        raise argparse.ArgumentTypeError('Invalid archive version! Use versions 1, 7, or 8')
    else:
        return int(version)
def check_backup_options(option: str):
    if option not in ['fallout', 'full']:
        raise argparse.ArgumentTypeError('Invalid backup option! Use fallout or full')
    else:
        return option

def write_csv(filename: str, *args):
    if(len(args) != 2):
        print("Wrong number of arguments")
        return
    names = args[0]
    versions = args[1]
    with open(filename, 'w', newline='') as f:
        my_writer = csv.writer(f, delimiter=',')
        my_writer.writerow(("ArchiveName","VersionHeaderByte"))
        for name, version in zip(names, versions):
            my_writer.writerow((name, version))

def read_csv(filename: str):
    names = []
    versions = []
    with open(filename, 'r') as f:
        my_reader = csv.reader(f, delimiter=',')
        for row in my_reader:
            if row[0] != 'ArchiveName':
                names.append(row[0])
            if row[1] != 'VersionHeaderByte':
                versions.append(row[1])
    return names, versions

def view_versions(directory: str, **kwargs):
    testing = kwargs.get('testing', False)
    archive_name = list()
    archive_version = list()
    count = 0
    for (root, dirs, files) in os.walk(directory):
        print("Archive version header byte")
        for f in files:
            if(f.endswith('.ba2')):
                with open(os.path.join(path, f), 'rb') as filehandle:
                    filehandle.seek(4)
                    archive_version_byte = filehandle.read(1)
                    print(f"{str(count+1): <5} {f : <50} {archive_version_byte}")
                    archive_name.append(f)
                    archive_version.append(int.from_bytes(archive_version_byte))
                    count += 1
        break
    print(f"{count} file(s) detected")
    if not testing:
        is_finished = False
        while not is_finished:
            choice = input("Do you want to save the list?(Y/N): ")
            if choice == 'Y' or choice == 'y':
                filename = input("Enter filename (a csv extension is automatically added): ")
                write_csv(filename + '.csv', archive_name, archive_version)
                is_finished = True
            elif choice == 'N' or choice == 'n':
                is_finished = True
            else:
                pass

def change_version(directory: str, version: int, **kwargs):
    testing = kwargs.get('testing', False)
    archive_names, versions = read_csv('input.csv')
    count = 0
    count_edited = 0
    if testing:
        mode_string = 'rb'
    else:
        mode_string = 'r+b'
    for (root, dirs, files) in os.walk(directory):
        print("Archive version header byte")
        for f in files:
            if(f in archive_names and f.endswith('.ba2')):
                with open(os.path.join(path, f), mode_string) as filehandle:
                    filehandle.seek(4)
                    archive_version_byte = filehandle.read(1)
                    if archive_version_byte == version_byte_dict[version]:
                        print(f"{str(count+1): <5} {f: <50} - No change needed")
                    else:
                        if testing:
                            print(f"{str(count+1): <5} {f: <50} - Header needs to be changed")
                        else:
                            filehandle.seek(4)
                            filehandle.write(version_byte_dict[version])
                            print(f"{str(count+1): <5} {f: <50} - Header changed")
                        count_edited += 1
                    count += 1
        break
    print(f"{count} file(s) detected")
    if testing:
        print(f"{count_edited} file(s) need editing")
    else:
        print(f"{count_edited} file(s) edited")

def restore_backup(directory: str, **kwargs):
    testing = kwargs.get('testing', False)
    backup_type = kwargs.get('backup', 'fallout')
    backup_name = 'restorefalloutbsa.csv'
    if backup_type == 'full':
        backup_name = 'cleanstateGOTYNG.csv'
    archive_names, versions = read_csv(backup_name)
    count = 0
    count_edited = 0
    if testing:
        mode_string = 'rb'
    else:
        mode_string = 'r+b'
    for (root, dirs, files) in os.walk(directory):
        print("Archive version header byte")
        for f in files:
            if(f in archive_names and f.endswith('.ba2')):
                idx = archive_names.index(f)  #File names are unique, so theres only one item with the name

                with open(os.path.join(path, f), mode_string) as filehandle:
                    filehandle.seek(4)
                    byte_backup = int(versions[idx])
                    archive_version_byte = filehandle.read(1)
                    if archive_names[idx] == f and archive_version_byte == version_byte_dict[byte_backup]:
                        print(f"{str(count+1): <5} {f: <50} - No change needed")
                    else:
                        if testing:
                            print(f"{str(count+1): <5} {f: <50} - Header needs to be restored")
                        else:
                            filehandle.seek(4)
                            filehandle.write(version_byte_dict[byte_backup])
                            print(f"{str(count+1): <5} {f: <50} - Header restored")
                        count_edited += 1
                    count += 1
        break
    print(f"{count} file(s) detected")
    if testing:
        print(f"{count_edited} file(s) need restoring")
    else:
        print(f"{count_edited} file(s) restored")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog="Bethesda Archive(BA2) version switcher",
        description="Switches Bethesda archive version between versions 1(Fallout 4, 76), 7(Fallout 4 NG), and 8(Fallout 4 NG)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''\
         Examples:
             View (and save) archives and versions:
                python -d "Fallout 4\\Data" --view
                               
             Set version of archives listed in input.csv(version column in input.csv is ignored) to version 1
                python -d "Fallout 4\\Data" --change 1
                               
             Restore only Fallout 4 ba2 archive headers to original NG versions
                python -d "Fallout 4\\Data" --restore
                python -d "Fallout 4\\Data" --restore fallout
                               
             Dry run (Don't modify any files, just show changes) for any of the above commands: Add -t or --test
                python -d "Fallout 4\\Data" --restore fallout --test
                python -d "Fallout 4\\Data" --restore full --test
                python -d "Fallout 4\\Data" --change 7 --test
         ''')
    )
    cwd = os.getcwd()
    parser.add_argument("-d", "--directory",
                        type=str, action="store",
                        metavar='path',
                        help="Working directory where the archives are (by default, it is the current working directory)", default=cwd)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-v", "--view", action="store_true", 
                        help="View all archive versions", default=None)
    group.add_argument("-c", "--change", action="store", 
                       metavar='(1|7|8)',
                        help="Change archive versions. Possible versions are 1, 7, 8",type=check_version, default=None)
    group.add_argument("-r", "--restore", 
                        action="store", 
                        metavar='fallout|full',
                        help="Restore archive versions. Restore options: fallout(default) or full", nargs='?', type=check_backup_options, const='fallout')
    parser.add_argument("-t", "--test",
                        action="store_true",
                        help="Test run without changing any files", default=False)
    args = parser.parse_args()
    path = args.directory.strip(r'\/')
    path = path.strip(r'"')
    path = Path(os.path.normpath(path))
    testing = args.test
    print(f"Path to look for BA2 files: {path}")
    if testing:
        print(f"Testing mode: No file changes are done")
    if args.view:
        print(f"View mode:")
        view_versions(path, testing=args.test)
    elif args.change is not None:
        print(f"Change mode:")
        change_version(path, args.change, testing=args.test)
    else:
        print(f"Backup option: {args.restore}")  
        restore_backup(path, backup=args.restore, testing=args.test)
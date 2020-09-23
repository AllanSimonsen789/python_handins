import os
import platform
import argparse


if platform.system() == 'Windows':
    newline = ''
else:
    newline = None

def get_file_names(folderpath,out="output.txt"):
     files = os.listdir(folderpath)
     with open(out, "w") as file_object:
        for file in files:
            file_object.write(file + '\n')

def get_all_file_names(folderpath,out="output.txt"):
    dic = os.walk(folderpath)
    with open(out, "w") as file_object:
        for root, dirs, files in dic:
            for name in files:
                file_object.write(str(name) + '\n')

def print_line_one(file_names):
    for file in file_names:
        with open(file) as file_object:
            print(file_object.readline())

def print_emails(file_names):
    for file in file_names:
        with open(file) as file_object:
            for line in file_object.readlines():
                if "@" in line:
                    print(line)

def write_headlines(md_files, out="output.txt"):
    printlist = []
    for file in md_files:
        with open(file) as file_object:
            for line in file_object.readlines():
                if "#" in line:
                    printlist.append(line)
    print(printlist)
    with open(out, "w") as file_object:
        for string in printlist:
            file_object.write(str(string) + '\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='a program that can detect and list files')
    parser.add_argument("-fp",'--folderpath', help='writes all filenames to a file in output.txt')
    parser.add_argument("-fpw",'--folderpathwalk', help='writes all filenames in dictory and subdirectories to a file in output.txt')
    parser.add_argument("-pfl", "--printfirstline", nargs='+', help="prints first line in files provided")
    parser.add_argument("-pe", "--printemails", nargs='+', help="prints emails found in the files provided")
    parser.add_argument("-w", "--writeheadlines", nargs='+', help="prints a file (output.txt) that contains all the headlines in the files provided")

    args = parser.parse_args()
    if args.folderpath is not None:
        get_file_names(args.folderpath)
    if args.folderpathwalk is not None:
        get_all_file_names(args.folderpathwalk)
    if args.printfirstline is not None:
        print_line_one(args.printfirstline)
    if args.printemails is not None:
        print_emails(args.printemails)
    if args.writeheadlines is not None:
        write_headlines(args.writeheadlines)
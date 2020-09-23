
import argparse
import csv
import platform

if platform.system() == 'Windows':
    newline = ''
else:
    newline = None

def print_file_content(file):
    with open (file) as file_object:
        reader = csv.reader(file_object)
        for row in reader:
            print("Row " + str(reader.line_num) + " " + str(row))

def write_list_to_file(output_file, *lst):
    with open(output_file, "w") as file_object:
        for string in lst:
            file_object.write(str(string) + '\n')

def read_csv(input_file):
    return_list = []
    with open(input_file) as file_object:
        reader = csv.reader(file_object)
        return_list += reader.__next__()
    return return_list

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A program that can read and write csv files')
    parser.add_argument('inputFile', help='inputFile in csv format to read')
    parser.add_argument('-f', "--file", help='name of file to write to')
    
    args = parser.parse_args()
    if args.file is None:
        print_file_content(args.inputFile)
    else:
        lines = read_csv(args.inputFile)
        write_list_to_file(args.file, lines)


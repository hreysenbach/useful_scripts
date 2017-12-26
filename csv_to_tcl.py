#!/usr/bin/python3

import os, sys, csv, getopt


def print_help():
    print("csv_to_tcl.py -i <inputfile> -o <outputfile>\n\r")


inputfile = None
outputfile = None
pin_header = "Pin"
signal_header = "Signal Name"
voltage_header = "Voltage Level"

try :
    opts, args = getopt.getopt(sys.argv[1:], "hi:o:", ["infile=","outfile="])
except getopt.GetoptError :
    print_help()
    sys.exit(1)

for opt, arg in opts :
    if opt == "-h" :
        print_help()
        sys.exit()
    elif opt in ("-i", "--infile") :
        inputfile = arg
    elif opt in ("-o", "--outfile") :
        outputfile = arg

with open(inputfile, 'r') as csvfile :
    with open(outputfile, 'w') as tclfile:
        headers_found = 0
        pin_header_found = 0
        sig_header_found = 0
        volt_header_found = 0
        reader = csv.reader(csvfile)
        for row_index, row in enumerate(reader):
            for col_index, item in enumerate(row) :
                if item == pin_header : 
                    pin_col = col_index
                    pin_row = row_index
                    pin_header_found = 1
                if item == signal_header :
                    sig_col = col_index
                    sig_row = row_index
                    sig_header_found = 1
                if item == signal_header :
                    volt_col = col_index
                    volt_row = row_index
                    volt_header_found = 1

                if (pin_header_found == 1) and (sig_header_found == 1) and (volt_header_found == 1):
                    if (volt_row == sig_row) and (sig_row == pin_row) :
                        headers_found = 1
                        header_row = row_index
                    else :
                        print("Headers found on different rows!\n")
                        sys.exit(3)
            if (headers_found == 1):
                break

        else:
            print("No headers found in CSV file!\n")
            sys.exit(2)

        row_index = row_index + 1

        for row in reader:
            tclfile.write("set_location_assignment PIN_{0} -to {1}\n".format(row[pin_col],row[sig_col]))
            tclfile.write("set_instance_assignment -name IO_STANDARD {0} -to {1}\n".format(row[volt_col],row[sig_col]))
        



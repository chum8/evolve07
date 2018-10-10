# [---IMPORT LIBRARIES---]
import random, sys #, scapy
# from scapy import *

# [---FUNCTIONS---]
# choose random items from a list
def randomize_items(my_list, n):
    temp = []
    for i in range(0, n):
        temp.append(random.choice(my_list))
    return temp

# return items from a file
def load_list(my_file):
    return open(my_file, "r").read().split()

# read system arguments
def load_sys_args(args, max_num = 30):
    default_num = 6
    # we only want to process if there are exactly two arguments
    # the first argument being the name of the py file
    # and the second argument being how many random items to load
    try:
        if len(args) == 2:
            num = int(args[1])
            # print(num) # debug line

            if num > max_num:
                num = max_num
        else:
            num = default_num
    except:
        num = default_num
    return num

# [---PROGRAM BODY---]
# get list from file and count items
my_file = 're_results.txt'
full_list = load_list(my_file)
list_count = len(full_list)
# print(list_count) # debug line

# find out how many random items to choose and choose them
n_items = load_sys_args(sys.argv, list_count)
my_list = randomize_items(full_list, n_items)
# print(my_list) # debug line

# interactive terminal
print("Note: select a custom number of domains to process by passing an integer at command line, as follows:\n\tpython3 scapy_passion_project.py n\nwhere n = the number of domains to process.  The default number is 6.\n\n")
print("/==================================================\\")
print("|Welcome to Douglas Singer's Scapy Passion Project!|")
print("\\==================================================/\n")
print("The following",n_items,"domains have been randomly chosen from a list of", str(list_count),"domains.")
for item in my_list:
    print(item)
if input("\nRun a TCP Stealth Scan against each domain? (Yn) ").lower() == 'y':
    print("Running scan...")



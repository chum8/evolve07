# [---IMPORT LIBRARIES---]
import random, sys
from scapy.all import *


# [---FUNCTIONS---]
# nicer display
def get_whitespace(word_len, target_len):
    if word_len > target_len:
        return ""
    else:
        whitespace = ""
        for i in range(0, target_len - word_len):
            whitespace += " "
        return whitespace

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

# do the scapy scan
# code for this function inspired or copied from 
# https://resources.infosecinstitute.com/port-scanning-using-scapy/#gref
# accessed 10-10-2018
def do_scan(my_list, dst_port=80):
    src_port=RandShort()
    default_timeout=8
    response_list = []
    for item in my_list:
        print("\n[ ...",item,"... ]")
        try:
            response = sr1(IP(dst=item)/TCP(sport=src_port,dport=dst_port,flags="S"),timeout=default_timeout)
            try:
                if(type(response)=="<type 'NoneType'>"):
                    temp = {'Destination':item,'Port':dst_port,'Response':'Filtered'}
                elif(response.haslayer(TCP)):
                    if(response.getlayer(TCP).flags == 0x12):
                        send_rst = sr(IP(dst=item)/TCP(sport=src_port,dport=dst_port,flags="R"),timeout=default_timeout)
                        temp = {'Destination':item,'Port':dst_port,'Response':'Open'}
                    elif(reponse.getlayer(TCP).flags == 0x14):
                        temp = {'Destination':item,'Port':dst_port,'Response':'Closed'}
                    else:
                        temp = {'Destination':item,'Port':dst_port,'Response':'Unknown at TCP check'}
                elif(response.haslayer(ICMP)):
                    if(int(response.getlayer(ICMP).type)==3 and int(response.getlayer(ICMP).code) in [1,2,3,9,10,13]):
                        temp = {'Destination':item,'Port':dst_port,'Response':'Filtered'}
                    else:
                        temp = {'Destination':item,'Port':dst_port,'Response':'Unknown at ICMP check'}
                else:
                    temp = {'Destination':item,'Port':dst_port,'Response':'Unknown at Response check'}
            except:
                temp = {'Destination':item,'Port':dst_port,'Response':'Unable to reach destination'}
        except:
            temp = {'Destination':item,'Port':dst_port,'Response':'Error! Check port number or domain.'}
        response_list.append(temp)
    return response_list

# [---PROGRAM BODY---]
# some default variables
max_ports = 65535
default_port = 80
tab_size = 24

# get list from file and count items
my_file = 're_results.txt'
write_file = 'scapy_results.txt'
full_list = load_list(my_file)
list_count = len(full_list)
# print(list_count) # debug line

# find out how many random items to choose and choose them
n_items = load_sys_args(sys.argv, list_count)
my_list = randomize_items(full_list, n_items)
# print(my_list) # debug line

# interactive terminal
print("Note: select a custom number of domains to process by passing an integer at command line, as follows:\n\tpython3 scapy_passion_project.py n\nwhere n = the number of domains to process.  The default number is 6.\n\n")
print("/=========================================\\")
print("|Welcome to chum8's Scapy Passion Project!|")
print("\\=========================================/\n")
print("The following",n_items,"domains have been randomly chosen from a list of", str(list_count),"domains.")
for item in my_list:
    print(item)
if input("\nRun a TCP Stealth Scan against each domain? (Yn) ").lower() == 'y':
    p = input("Enter the port to scan or ENTER for default (port " + str(default_port) + " is current default): ")
    try:
        if (int(p) >= 0) and (int(p) <= max_ports):
            my_port = int(p)
        else:
            my_port = default_port
    except:
        my_port = default_port
    print("Running scan...")
    scan_result = do_scan(my_list, my_port)

    # to view scan result
    print("\nRESULTS using PORT",my_port)
    print("==================================")
    w1, w2 = "DESTINATION", "RESPONSE"
    print(w1, get_whitespace(len(w1), tab_size), w2)
    for item in scan_result:
        print(item['Destination'],get_whitespace(len(item['Destination']), tab_size),item['Response'])

    # to write to file
    with open(write_file, 'w') as f:
        for item in scan_result:
            temp = item['Destination']+','+str(item['Port'])+','+item['Response']+'\n'
            f.write(temp)
    print("\nResults saved to",write_file)
else:
    print("Exiting system.")
    exit()
print("Exiting system.")
exit()

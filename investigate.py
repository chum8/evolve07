import re
def grab_data(my_file, my_error):
    try:
        the_file = open(my_file, 'r').read()
    except:
        print("There was a problem loading the file",my_error)
        exit()
    return the_file

my_file = 'data.txt'
my_error ='\nExiting application'

print('Welcome to The Forgotten Regex Lab.')

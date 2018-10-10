# [---IMPORT LIBRARIES---]
import re

# [---CLASS DEFINITION---]
class re_builder():

    # initialize class
    def __init__(self):
        # public variables
        # self.data_file = 'data.txt'
        self.data_file = 'universities.txt'
        self.word_list_file = 'words_01.txt'
        self.results = ""
        self.write_file = 're_results.txt'

        # private variables
        self.__re = ""
        self.__data = ""
        self.__default_error = '\nExiting application.'
        self.__words = []


    # load data from file
    def load_data(self):
        try:
            self.__data = open(self.data_file, 'r').read()
            # print(self.__data) # debug line
        except:
            print("There was a problem loading the file",self.__default_error)

    # load word list from file
    def load_word_list(self):
        try:
            self.__words = open(self.word_list_file, 'r').read().split()
            # print(self.words) # debug line
        except:
            print("There was a problem loading the word list file",self.default_error)

    # load a prebuilt regular expression
    def load_re(self, my_re):
        self.__re = my_re

    # build regular expression
    def build_word_search_re(self, case_sensitive = 'y'):
        left_, right_  = '(', ')'
        temp = left_
        try:
            first = True
            for w in self.__words:
                if not first:
                    temp += '|' + str(w)
                else:
                    temp += str(w)
                    first = False
            temp += right_
            self.__re = temp

        except:
            print("There was a problem building the regular expression",self.default_error)

    # get results of regular expression
    def process_re(self, case_sens = 'n'):
        if case_sens.lower() == 'y':
            r = re.compile(self.__re)
        else:
            r = re.compile(self.__re, re.I)

        # print(type(r)) # debug line
        self.results = r.findall(self.__data)
        # print(self.results) # debug line


    # print active regular expression
    def retrieve_re(self):
        return self.__re

# [----PROGRAM BODY----]
# some regex presets
domain_re1 = '\(\w+.\w+.\w+\)'

# instantiate class and load file with data to run re against
my_re = re_builder()
my_re.load_data()

# for regular expressions based on a preloaded regular expression
my_re.load_re(domain_re1)

# for regular expressions based on a word list
# my_re.load_word_list()
# my_re.build_word_search_re()

# interactive terminal
print('Welcome to The Forgotten Five Regex Lab.')
print('Regular expression now in memory is \'' + my_re.retrieve_re() + '\'')
if input('Run this regular expression against \'' + my_re.data_file + '\'? (Yn) ').lower() == 'y':
    my_re.process_re()

    # to print results in terminal
    for item in my_re.results:
        print(item)

    # to write to file
    with open(my_re.write_file, 'w') as f:
        for item in my_re.results:
            # to write stripping paranthese
            f.write(item.translate({ord(c): None for c in '()'}))

            # to write as is
            # f.write(item)

            # add new line
            f.write('\n')

# -- coding: utf-8 --
import os
import re
import sys
import math

SHANONN_UPPER_LIMIT = 4.5

regex_dict = {
    'rsa_key': r'-{3,}\bBEGIN RSA PRIVATE KEY-{3,}',
    'rsa_key_end': r'-{3,}\bEND RSA PRIVATE KEY-{3,}',
    'aws_access_key': r'(?<![A-Za-z0-9/+=])[A-Za-z0-9/+=]{40}(?![A-Za-z0-9/+=])',
    'artifactory_password': r'(?:\s|=|:|"|^)AP[\dABCDEF][a-zA-Z0-9]{8,}',
    'artifactory_token': r'(?:\s|=|:|"|^)AKC[a-zA-Z0-9]{10,}',

    'aws_secret_key': r'aws(.{0,20})?[\'\"][0-9a-zA-Z\/+]{40}[\'\"]',
}


# the function returns a list of all files in directory path
def files_in_directory_path(path):
    files_path = []
    for (dirpath, dirnames, filenames) in os.walk(path):
        for filename in filenames:
            if is_file_potential(filename):
                files_path.append(os.sep.join([dirpath, filename]))

    return files_path


# the function return True if if the file is potential of containing a key else return False.
def is_file_potential(filename):
    # list of types of files which we wont want to go over and check - cause they not created by the programmer
    files_types_list = ['binary', 'exe', 'out', 'jar', 'class' 'nupkg', 'png', 'jpeg', 'rpm', 'bz2', 'gz',
                        'whl', 'zip', 'arr', 'war', 'sql']  # type of files which we wont want to check

    # return filename in files_types_list
    for t in files_types_list:
        if filename.endswith("." + t):
            return False
    else:
        return True


# the function returns how much word is randomize (0 - not random & easy to guss, >=4.5 random word)
def shannon_formula(word):
    stList = list(word)
    alphabet = list(set(stList))  # list of symbols in the string

    # calculate the frequency of each symbol in the string
    freqList = []
    for symbol in alphabet:
        ctr = 0
        for sym in stList:
            if sym == symbol:
                ctr += 1
        freqList.append(float(ctr) / len(stList))

    # Shannon entropy
    ent = 0.0
    for freq in freqList:
        ent = ent + freq * math.log(freq, 2)
    ent = -ent
    return ent


def find_match_key(path, regex):
    dict_match = {}  # dict format {path : [keys]}

    with open(path, encoding="ascii", errors="surrogateescape") as fil:
        lst_keys = []
        found_rsa_begin = False

        try:
            for line in fil.readlines():
                match = re.search(regex, line, re.IGNORECASE)

                if found_rsa_begin:
                    if re.search(regex_dict["rsa_key_end"], line):
                        break
                    if shannon_formula(line) >= SHANONN_UPPER_LIMIT:
                        lst_keys.append(line)

                elif match:
                    if regex == regex_dict['rsa_key']:
                        found_rsa_begin = True
                        continue

                    token = match.group()
                    if shannon_formula(token) >= SHANONN_UPPER_LIMIT:
                        if "\"" in token:
                            lst_keys.append(token.split('\"')[1])
                        else:
                            lst_keys.append(token)

            if lst_keys:
                dict_match[path] = lst_keys
            return dict_match
        except():
            print("there was a problem with the file")


def general_test(directory, key):
    print("you are searching for : ", key, " in this path : ", directory)
    files_dic = files_in_directory_path(directory)
    for path in files_dic:
        dict_found_keys = find_match_key(path, regex_dict[key])  # find_key(path)
        if dict_found_keys:
            for cur_file, cur_key in dict_found_keys.items():
                print("the file is: ", cur_file, " keys: ", cur_key)


def main():
    general_test(sys.argv[1], sys.argv[2])


if __name__ == '__main__':
    main()

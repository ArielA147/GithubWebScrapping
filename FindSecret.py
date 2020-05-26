# -- coding: utf-8 --
import os
import re
import sys

regex_dict = {
    'rsa_key': {'rsa_pk_begin': r'-{3,}\bBEGIN RSA PRIVATE KEY-{3,}',
                'rsa_pk_end': r'-{3,}\bEND RSA PRIVATE KEY-{3,}'},
    'aws_secret_key': r'(?i)aws(.{0,20})?(?-i)[\'\"][0-9a-zA-Z\/+]{40}[\'\"]',
    'aws_access_key': r'(?<![A-Za-z0-9/+=])[A-Za-z0-9/+=]{40}(?![A-Za-z0-9/+=])',
    'artifactory_password': r'(?:\s|=|:|"|^)AP[\dABCDEF][a-zA-Z0-9]{8,}',
    'artifactory_token': r'(?:\s|=|:|"|^)AKC[a-zA-Z0-9]{10,}'
}
keys_dict = {}  # dict {key_type : {file: key}}


#
# # the function check if there is aws access key on path and return them
# def check_aws_access_key(path):
#     aws_keys = set()
#
#     # 40-character, base-64 strings that don’t have any base 64 characters immediately before or after.
#
#     aws_access_key_patten = r'(?<![A-Za-z0-9/+=])[A-Za-z0-9/+=]{40}(?![A-Za-z0-9/+=])'
#
#     with open(path, encoding="ascii", errors="surrogateescape") as fil:
#         try:
#             for line in fil:
#                 match = re.findall(aws_access_key_patten, line)
#                 for m in match:
#                     if m:
#                         aws_keys.add(str(m))
#                         print("the key is ", str(m), " in path of ", path)
#             return aws_keys
#         except():
#             print("problem open the file")
#
#
# # the function finds if there is rsa key in the path and return them
# def check_rsa_key(path):
#     keys = []
#     cur_key = []
#     found_key = False
#
#     # RSA key in PEM format
#     rsa_pk_begin = r'-{3,}\bBEGIN RSA PRIVATE KEY-{3,}'
#     rsa_pk_end = r'-{3,}\bEND RSA PRIVATE KEY-{3,}'
#
#     with open(path, encoding="ascii", errors="surrogateescape") as fil:
#         try:
#             for line in fil:
#                 # 1 if the line match for rsa_begin, 2 if line match for rsa_end otherwise 0
#                 regex_fit = 1 if re.search(rsa_pk_begin, line) else 2 if re.search(rsa_pk_end, line) else 0
#
#                 if regex_fit == 2:  # end of key
#                     found_key = False
#                     if cur_key:
#                         full_key = ''.join(cur_key)
#                         keys.append(full_key)
#
#                 elif found_key and not regex_fit:
#                     cur_key.append(line)
#                 elif regex_fit == 1:  # start of key
#                     found_key = True
#
#             return keys
#         except():
#             print("problem open the file")
#
#
# # the function finds if there is any key in path and return them
# def find_key(path):
#     keys = {}
#
#     rsa_keys = check_rsa_key(path)
#     if rsa_keys:
#         keys["rsa_key"] = rsa_keys
#
#     aws_access_key_set = check_aws_access_key(path)
#     if aws_access_key_set:
#         keys["aws_access_key"] = aws_access_key_set
#
#     return keys
#

# @param path: the path of the file
# @param regex: the regex of the key

# the function search the regex in the file
def find_match_key(path, regex):
    dict_match = {}  # {path : [keys]}

    with open(path, encoding="ascii", errors="surrogateescape") as fil:
        lst_keys = []
        try:
            file_data = fil.readlines()

            for line in file_data:
                match = re.search(regex, line)
                if match:
                    if "\"" in match.group():
                        lst_keys.append(match.group().split('\"')[1])
                    else:
                        lst_keys.append(match.group())

            if lst_keys:
                dict_match[path] = lst_keys
            fil.close()
            return dict_match
        except():
            print("there was a problem with the file")


# the function return True if if the file is potential of containing a key else return False.
def is_file_potential(filename):
    # list of types of files which we wont want to go over and check - cause they not created by the programmer
    files_types_list = ['binary', 'exe', 'out', 'jar', 'class' 'nupkg', 'png', 'jpeg', 'rpm', 'bz2', 'gz', 'whl', 'zip',
                        'arr', 'war']  # type of files which we wont want to check

    for t in files_types_list:
        if filename.endswith("." + t):
            return False
    else:
        return True


# the function returns a list of all files in directory path
def files_in_directory_path(path):
    files_path = []
    for (dirpath, dirnames, filenames) in os.walk(path):
        for filename in filenames:
            if is_file_potential(filename):
                files_path.append(os.sep.join([dirpath, filename]))

    return files_path


### TESTS

def general_test(directory, key):
    files_dic = files_in_directory_path(directory)
    for path in files_dic:
        dict_found_keys = find_match_key(path, regex_dict[key])  # find_key(path)
        if dict_found_keys:
            for cur_file, cur_key in dict_found_keys.items():
                print("the file is : ", cur_file, " the key is : ", cur_key)


# def test1(directory):
#     # 'C:\\Users\\User\\Desktop\\cycode\\TEMP'
#     files_dic = files_in_directory_path(directory)
#     keys = []
#
#     for path in files_dic:
#         path_keys = find_key(path)
#         for cur_key in path_keys:
#             if cur_key:
#                 keys.extend(path_keys[cur_key])
#
#     print(True) if len(keys) == 2 else print(False)
#
#
# def test2(directory):
#     # 'C:\\Users\\User\\Desktop\\cycode\\wolfssh'
#     files_dic = files_in_directory_path(directory)
#
#     keys = []
#
#     for path in files_dic:
#         path_keys = find_key(path)
#         for cur_key in path_keys:
#             if cur_key == "rsa_key":
#                 keys.extend(path_keys[cur_key])
#
#     print(True) if len(keys) == 3 else print(False)
#
#
# def test3(directory):
#     # 'C:\\Users\\User\\Desktop\\cycode\\pem-reader'
#     files_dic = files_in_directory_path(directory)
#     keys = []
#     for path in files_dic:
#         path_keys = find_key(path)
#         for cur_key in path_keys:
#             if cur_key == "rsa_key":
#                 keys.extend(path_keys[cur_key])
#     print(True) if len(keys) == 1 else print(False)
#
#
# def test4(directory):
#     files_dic = files_in_directory_path(directory)
#     keys = []
#
#     for path in files_dic:
#         path_keys = find_key(path)
#         for cur_key in path_keys:
#             if cur_key == "rsa_key":
#                 keys.extend(path_keys[cur_key])
#     print(True) if len(keys) == 6 else print(False)
#
#
# def test5(directory):
#     files_dic = files_in_directory_path(directory)
#     keys = []
#     for path in files_dic:
#         path_keys = find_key(path)
#         for cur_key in path_keys:
#             if cur_key == "aws_access_key":
#                 keys.extend(path_keys[cur_key])
#     print(True) if len(keys) == 2 else print(False)
#
#
# def rsa_test(directory):
#     test2(directory)  # test for 'C:\\Users\\User\\Desktop\\cycode\\wolfssh'
#     test3(directory)  # test for 'C:\\Users\\User\\Desktop\\cycode\\pem-reader'
#     test4(directory)  # test for 'C:\\Users\\User\\Desktop\\cycode
#
#
# def aws_test(directory):
#     test5(directory)  # 'C:\\Users\\User\\Desktop\\cycode\\master-thesis-experiment\\topology'

#
# def run_tests():
#     test1(sys.argv[1])  # test for 'C:\\Users\\User\\Desktop\\cycode\\TEMP'
#     rsa_test(sys.argv[1])
#     aws_test(sys.argv[1])


def main():
    print("you are searching for : ", sys.argv[2], " in this path : ", sys.argv[1])
    print()
    general_test(sys.argv[1], sys.argv[2])
    print()
    print("~DONE~")


if __name__ == '__main__':
    main()

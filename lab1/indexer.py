import sys
import os
import re
import pickle 

def get_files(dir, suffix):
    """
    Returns all the files in a folder ending with suffix
    :param dir:
    :param suffix:
    :return: the list of file names
    """
    files = []
    for file in os.listdir(dir):
        if file.endswith(suffix):
            files.append(file)
    return files

def dictionaries(filepath):
    dic = {}
    with open(filepath, 'r') as file:
        match = re.finditer('\w+', file.read().lower())
        for m in match:
            word = m.group()
            dic[word] = [*dic[word], m.start()] if word in dic else [m.start()]
    pickle.dump(dic, open('{}.idx'.format(filepath.split('.')[0]), 'wb'))
    return dic

def main(folder):
    master_dict = {}
    txt_files = get_files(folder, '.txt')
    for t in txt_files:
        dic = dictionaries('{}/{}'.format(folder, t))
        for d in dic:
            master_dict[d] = {t: dic[d]}
    print(master_dict['samlar']['nils.txt'])

if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print('Wrong amount of inputs')
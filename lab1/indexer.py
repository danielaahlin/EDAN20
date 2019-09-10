import sys
import os
import regex as re
import pickle
import numpy as np
import math

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

def tf(t, d, sum):
    """
    t - the word
    d - the dictionary for the document,
    sum - sum of all the words in the given dictionary
    term frequency
    """
    try:
        raw_count = float(len(d[t]))
    except: 
        raw_count = 0.0
    return raw_count/sum

def idf(N, t, D):
    """
    N - number of text files
    t - the word
    D - master dictionary 
    """
    nt = float(len(D[t]))
    if nt == 0.0:
        nt = 1.0
    return math.log10(float(N)/nt)

def tf_idf(t, d, N, D, sum):
    return tf(t, d, sum) * idf(N, t, D)

def cosine_similarity(A, B):
    """
    A, B - arrays containing tfidf values
    """
    return np.dot(A, B) / np.linalg.norm(A) * np.linalg.norm(B)

def main(folder):
    master_dict = {}
    txt_files = get_files(folder, '.txt')
    for t in txt_files:
        dic = dictionaries('{}/{}'.format(folder, t))
        for d in dic:
            if d in master_dict:
                master_dict[d].update({t: dic[d]})
            else:
                master_dict[d] = {t: dic[d]}

    array_txt = []
    for t in txt_files:
        dic = dictionaries('{}/{}'.format(folder, t))
        array_txt.append(np.array([tf_idf(word, dic, len(txt_files), master_dict, len(re.findall('\w+', '{}/{}'.format(folder, t)))) for word in master_dict]))        

    matrix = []
    for x in range(len(array_txt)):
        row = []
        for y in range(len(array_txt)):
            row.append(cosine_similarity(array_txt[x], array_txt[y]))
        matrix.append(row)
    for m in matrix:
        print(m)

        
if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print('Wrong amount of inputs')
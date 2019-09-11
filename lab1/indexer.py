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
        match = re.finditer('\p{L}+', file.read().lower())
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
    return np.log10(float(N)/nt)

def tf_idf(t, d, N, D, sum):
    return tf(t, d, sum) * idf(N, t, D)

def cosine_similarity(A, B):
    """
    A, B - arrays containing tfidf values
    """
    return np.dot(A, B) / (np.linalg.norm(A) * np.linalg.norm(B))

def main(folder):
    master_dict = {}
    txt_files = get_files(folder, '.txt')
    for t in txt_files:
        dic = dictionaries('{}/{}'.format(folder, t))
        for d in dic:
            if t == 'bannlyst.txt':
                if d == 'gjord' or d == 'uppklarnande' or d == 'stjärnor':
                    print('{}: {}'.format(d, dic[d]))
            if d in master_dict:
                master_dict[d].update({t: dic[d]})
            else:
                master_dict[d] = {t: dic[d]}

    print(10 * '-')
    print('{}: {}'.format('samlar',master_dict['samlar']))
    print('{}: {}'.format('ände',master_dict['ände']))
    print(10 * '-')

    array_txt = []
    for t in txt_files:
        dic = dictionaries('{}/{}'.format(folder, t))   
        #sum_of_words = len(re.findall('\p{L}+', '{}/{}'.format(folder, t)))
        sum_of_words = 0
        for d in dic:
            sum_of_words += len(dic[d])
        array_txt.append(np.array([tf_idf(word, dic, len(txt_files), master_dict, sum_of_words) for word in master_dict]))
        if t == 'bannlyst.txt' or t == 'gosta.txt' or t == 'herrgard.txt' or t == 'jerusalem.txt' or t == 'nils.txt':
            print(t)
            print('    {} {}'.format('känna',   tf_idf('känna', dic, len(txt_files), master_dict, sum_of_words)))
            print('    {} {}'.format('gås',     tf_idf('gås',   dic, len(txt_files), master_dict, sum_of_words)))
            print('    {} {}'.format('nils',    tf_idf('nils',  dic, len(txt_files), master_dict, sum_of_words)))
            print('    {} {}'.format('et',      tf_idf('et',    dic, len(txt_files), master_dict, sum_of_words)))
    print(10 * '-')

    matrix = []
    for x in range(len(array_txt)):
        row = []
        for y in range(len(array_txt)):
            row.append(cosine_similarity(array_txt[x], array_txt[y]))
        matrix.append(row)
    print(txt_files)
    for m in matrix:
        #m.sort()
        #print(m[-2])
        print(m)

    #'troll.txt', 'kejsaren.txt' är mest lika
        
if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print('Wrong amount of inputs')
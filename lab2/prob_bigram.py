"""
Mutual information of bigrams in a corpus
Usage: python mutual_info.py < corpus.txt
"""
__author__ = "Pierre Nugues"

import sys
import math

import regex
import tokenizer


def tokenize(text):
    words = regex.findall("\p{L}+", text)
    return words


def count_bigrams(words):
    bigrams = [tuple(words[inx:inx + 2])
               for inx in range(len(words) - 1)]

    frequency_bigrams = {}
    for bigram in bigrams:
        if bigram in frequency_bigrams:
            frequency_bigrams[bigram] += 1
        else:
            frequency_bigrams[bigram] = 1
    return frequency_bigrams

def bigrams(words):
    bigrams = [tuple(words[inx:inx + 2])
               for inx in range(len(words) - 1)]
    return bigrams


def sentence_prob(words, sentence):
    freq = count_bigrams(words)
    
    sentence_bigrams = bigrams(sentence)
    #print(freq2)
    
    prob = 1
    print("Bigram model")
    print('=' * 50)
    print("wi wi+1 Ci,i+1 C(i) P(wi+1|wi)")
    print('=' * 50)
    for word in sentence_bigrams:
        prob *= (freq[word]/len(words))
        print("{}: {}: {}: {}".format(
            word, freq[word], len(words), freq[word]/len(words)))
    #prob *= (freq["</s>"]/len(words))
    #print("{}: {}: {}: {}".format(
    #    "</s>", freq["</s>"], len(words), freq["</s>"]/len(words)))
    print('=' * 50)
    print("Prob. bigrams: {}  ".format(prob))
    print("Geometric mean prob.: {} ".format(1))
    print("Entropy rate: {} ".format("1"))
    print("Perplexity: {} ".format("1"))


if __name__ == '__main__':
    text = sys.stdin.read()
    words = tokenizer.delimiter(text)
    #frequency = count_bigrams(words)
    sentence = "Det var en gång en katt som hette Nils".lower()
    words2 = sentence.split()
    print(words2)
    sentence_prob(words, words2)

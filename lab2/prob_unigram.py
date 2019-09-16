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


def count_unigrams(words):
    frequency = {}
    for word in words:
        if word in frequency:
            frequency[word] += 1
        else:
            frequency[word] = 1
    return frequency


# def mutual_info(words, freq_unigrams, freq_bigrams):
#     mi = {}
#     factor = len(words) * len(words) / (len(words) - 1)
#     for bigram in freq_bigrams:
#         mi[bigram] = (
#             math.log(factor * freq_bigrams[bigram] /
#                      (freq_unigrams[bigram[0]] *
#                       freq_unigrams[bigram[1]]), 2))
#     return mi

def sentence_prob(words, sentence):
    freq = count_unigrams(words)
    prob = 1
    print("Unigram model")
    print('=' * 50)
    print("wi C(wi) #words P(wi)")
    print('=' * 50)
    for word in sentence.split():
        prob *= (freq[word]/len(words))
        print("{}: {}: {}: {}".format(word, freq[word], len(words), freq[word]/len(words)))
    prob *= (freq["</s>"]/len(words))
    print("{}: {}: {}: {}".format("</s>", freq["</s>"], len(words), freq["</s>"]/len(words)))
    print('=' * 50)
    print("Prob. unigrams: {}  ".format(prob))
    print("Geometric mean prob.: {} ".format(1))
    print("Entropy rate: {} ".format("1"))
    print("Perplexity: {} ".format("1"))



if __name__ == '__main__':
    text = sys.stdin.read()
    words = tokenizer.delimiter(text)
    frequency = count_unigrams(words)
    sentence = "Det var en gång en katt som hette Nils".lower()
    sentence_prob(words, sentence)


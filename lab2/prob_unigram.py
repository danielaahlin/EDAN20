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
    prob = 1.0
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
    root = len(sentence.split()) + 1
    print("Geometric mean prob.: {} ".format(prob**(1./root)))
    entropy = math.log2(prob) * (-1 / root)
    print("Entropy rate: {} ".format(entropy))
    perplexity = math.pow(2, entropy)
    print("Perplexity: {} ".format(perplexity))

if __name__ == '__main__':
    text = sys.stdin.read()
    words = tokenizer.delimiter(text)
    frequency = count_unigrams(words)
    sentence = "Det var en gång en katt som hette Nils".lower()
    sentence_prob(words, sentence)


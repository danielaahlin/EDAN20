"""
Mutual information of bigrams in a corpus
Usage: python mutual_info.py < corpus.txt
"""
__author__ = "Pierre Nugues"

import sys
import math

import regex
import tokenizer
from prob_unigram import count_unigrams

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
    unigram_freq = count_unigrams(words)

    sentence_bigrams = bigrams(sentence)
    #print(freq2)
    non_bigram = 1
    prob = 1
    print("Bigram model")
    print('=' * 50)
    print("wi wi+1 Ci,i+1 C(i) P(wi+1|wi)")
    print('=' * 50)
    for word in sentence_bigrams:
        try:
            prob *= (freq[word]/unigram_freq[word[0]])
        except KeyError:
            non_bigram = unigram_freq[word[1]]/len(words)
            prob *= non_bigram

        try:
            print('{} {} {} {} {}'.format(word[0], word[1], freq[word], unigram_freq[word[0]], freq[word]/unigram_freq[word[0]]))
        except KeyError:
            print('{} {} {} {} {} *backoff: {}'.format(word[0], word[1], 0, unigram_freq[word[0]], 0.0, non_bigram))

    print('=' * 50)
    print("Prob. bigrams: {}  ".format(prob))
    root = len(sentence)
    print("Geometric mean prob.: {} ".format(math.pow(prob, 1./root)))
    entropy = math.log2(prob) * (-1 / root)
    print("Entropy rate: {} ".format(entropy))
    perplexetiy = math.pow(2, entropy)
    print("Perplexity: {} ".format(perplexetiy))


if __name__ == '__main__':
    text = sys.stdin.read()
    words = tokenizer.delimiter(text)
    #frequency = count_bigrams(words)
    sentence = "Det var en gång en katt som hette Nils".lower()
    words2 = tokenizer.delimiter(sentence)
    sentence_prob(words, words2)

def extract_pairs(file):
    pairs = {}
    sentence = []
    for f in file:
        line = f.split()
        if line == []:
            for s in sentence:
                if s[7] == 'SS':
                    tup = (s[1].lower(), sentence[int(s[6]) - 1][1].lower())
                    if tup in pairs:
                        pairs[tup] += 1
                    else:
                        pairs.update({tup : 1})
            sentence = []
        else:
            sentence.append(line)
    return pairs

if __name__ == "__main__":
    with open('swedish_talbanken05_train.conll', 'r') as file:
        #pairs
        pairs = extract_pairs(file)
        sorted_pairs = sorted(pairs.items(), key=lambda kv: kv[1])
        five_most_frqnt_pairs = [i[1] for i in sorted_pairs[-5:]]
        five_most_frqnt_pairs.reverse()
        print(five_most_frqnt_pairs)
        #triples
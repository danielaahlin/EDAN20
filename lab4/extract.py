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

def extract_triples(file):
    triples = {}
    sentence = []
    ss_found = []
    oo_found = []
    for f in file:
        line = f.split()
        if line == []:
            for s in sentence:
                if s[7] == 'SS':
                    ss_found.append((int(s[0]) - 1, int(s[6]) - 1))
                elif s[7] == 'OO':
                    oo_found.append((int(s[0]) - 1, int(s[6]) - 1))
            for ss in ss_found:
                for oo in oo_found:
                    if ss[1] == oo[1]:
                        trip = (sentence[ss[1]][1].lower(), sentence[ss[0]][1].lower(), sentence[oo[0]][1].lower())
                        add_trip(trip, triples)
            ss_found = []
            oo_found = []
            sentence = []
        else:
            sentence.append(line)
    return triples

def add_trip(trip, triples):
    if trip in triples:
        triples[trip] += 1
    else:
        triples.update({trip : 1})

if __name__ == "__main__":
    #pairs
    with open('swedish_talbanken05_train.conll', 'r') as file:
        count = 0
        pairs = extract_pairs(file)
        for p in pairs:
            count += pairs[p]
        print(count)
        sorted_pairs = sorted(pairs.items(), key=lambda kv: kv[1])
        five_most_frqnt_pairs = [i[1] for i in sorted_pairs[-5:]]
        five_most_frqnt_pairs.reverse()
        print(five_most_frqnt_pairs)
    #triples
    with open('swedish_talbanken05_train.conll', 'r') as file:
        count = 0
        triples = extract_triples(file)
        for t in triples:
            count += triples[t]
        print(count)
        sorted_triples = sorted(triples.items(), key=lambda kv: kv[1])
        five_most_frqnt_triples = [i[1] for i in sorted_triples[-5:]]
        five_most_frqnt_triples.reverse()
        print(five_most_frqnt_triples)
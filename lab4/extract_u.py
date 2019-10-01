from glob import glob

def extract_pairs(file):
    pairs = {}
    sentence = []
    for f in file:
        line = f.split()
        if line == []:
            for s in sentence:
                # print(s)
                if s[7] == 'nsubj':
                    tup = (s[1].lower(), sentence[int(s[6]) - 1][1].lower())
                    if tup in pairs:
                        pairs[tup] += 1
                    else:
                        pairs.update({tup : 1})
            sentence = []
        elif not is_int(line[0]):
            pass
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
                if s[7] == 'nsubj':
                    ss_found.append((int(s[0]) - 1, int(s[6]) - 1))
                elif s[7] == 'obj':
                    oo_found.append((int(s[0]) - 1, int(s[6]) - 1))
            for ss in ss_found:
                for oo in oo_found:
                    if ss[1] == oo[1]:
                        trip = (sentence[ss[1]][1].lower(), sentence[ss[0]][1].lower(), sentence[oo[0]][1].lower())
                        if trip in triples:
                            triples[trip] += 1
                        else:
                            triples.update({trip : 1})
            ss_found = []
            oo_found = []
            sentence = []
        elif not is_int(line[0]):
            pass
        else:
            sentence.append(line)
    return triples


def is_int(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False


if __name__ == "__main__":
    for path in glob('ud-treebanks-v2.4/*/*train*.conllu'):
        if 'German' in path or 'English' in path or 'Spanish' in path: 
            with open(path, 'r') as file:
                print(path) 
                triples = extract_triples(file)
                sorted_triples = sorted(triples.items(), key=lambda kv: kv[1])
                five_most_frqnt_triples = [i[1] for i in sorted_triples[-5:]]
                five_most_frqnt_triples.reverse()
                sorted_triples.reverse()
                print(sorted_triples[:5])
                print(five_most_frqnt_triples)

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
    #count = 0
    for f in file:
        line = f.split()
        if line == []:
            for s in sentence:
                if s[7] == 'OO':
                    if sentence[int(s[6]) - 1][7] == 'SS':
                        index = int(sentence[int(s[6]) - 1][6])
                        if index == 0:
                            pass
                        else:
                            trip = (s[1].lower(), sentence[int(s[6]) - 1][1].lower() ,sentence[index - 1][1].lower())
                        add_trip(trip, triples)
                    else: 
                        index = int(sentence[int(s[6]) - 1][6])
                        if index == 0:
                            #hita ss som pekar på root
                            for ss in sentence:
                                if ss[7] == 'SS':
                                    idx =int(ss[6]) - 1
                                    if int(sentence[idx][6]) == 0:
                                        trip = (s[1].lower(), sentence[idx][1].lower(), ss[1].lower() ) 
                                        add_trip(trip, triples)

                        elif int(sentence[int(index) - 1][6]) == 0:
                            pass
                        elif sentence[int(index) - 1][7] == 'SS':
                            trip = (s[1].lower(), sentence[int(s[6]) - 1][1].lower() ,sentence[index - 1][1].lower())
                            add_trip(trip, triples)

                elif s[7] == 'SS':




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
    with open('swedish_talbanken05_train.conll', 'r') as file:
        #pairs
        #pairs = extract_pairs(file)
        #sorted_pairs = sorted(pairs.items(), key=lambda kv: kv[1])
        #five_most_frqnt_pairs = [i[1] for i in sorted_pairs[-5:]]
        #five_most_frqnt_pairs.reverse()
        #print(five_most_frqnt_pairs)
        #triples
        count = 0
        triples = extract_triples(file)
        for t in triples:
            count += triples[t]

        print(count)
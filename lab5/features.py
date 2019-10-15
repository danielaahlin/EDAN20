"""
First set  - POS_stack, POS_queue, word_stack, word_queue, can-la, can-re
Second set - POS_stack0, POS_stack1, word_stack0, word_stack1, POS_queue0, POS_queue1, word_queue0, word_queue1, can-la, can-re
Third set  - POS_stack0, POS_stack1, word_stack0, word_stack1, POS_queue0, POS_queue1, word_queue0, word_queue1, can-la, can-re,
             POS_sentece_order, wordform_sentence_order
"""

def extract(stack, queue, graph, feature_names, sentence, model_set):
    features = {}
    if model_set == 1:
        pass
    elif model_set == 2:
        X = ['nil', 'nil', 'nil', 'nil', queue[0][3], queue[1][3], queue[0][1], queue[1][1], False, False]
        y = 'sh'
        print('x = {}, y = {}'.format(X,y))
        while len(queue) > 0:
            # if not stack:
            #     print(len(stack))
            #     X = ['nil', 'nil', 'nil', 'nil', queue[0][3], queue[1][3], queue[0][1], queue[1][1], False, False]
            #     y = 'sh'
            #     stack, queue, graph = shift(stack, queue, graph)
            #     print(stack)
            #     print('x = {}, y = {}'.format(X, y))
            #     #lägg till saker i features
            # else:
            top = stack[0]
            first = queue[0]
            
            top_id = int(top[0])
            first_id = int(first[0])
            #arc
            arced = False
            if (top_id, first_id) in graph:
                arced = True
                X = []
                y = 'ra.{}'.format(first[7])
                stack, queue, graph = shift(stack, queue, graph)
            elif (first_id, top_id) in graph:
                arced = True
                #'can-la' = True
                X = []
                y = 'la.{}'.format(top[7])
                stack, queue, graph = reduce(stack, queue, graph)
            #reduce
            if not arced:
                reduced = False
                for k in stack:
                    k_id = int(k[0])
                    if (k_id, first_id) in graph or (first_id, k_id) in graph:
                        reduced = True
                        stack, queue, graph = reduce(stack, queue, graph)
                        X = []
                        y = 're'
                        #can-re = True
                        #lägga till i features
                    else:    
                        pass
            #shift
            if not arced and not reduced:
                # X = [top[4], ]
                y = 'sh'
                stack, queue, graph = shift(stack, queue, graph)
            print('x = {}, y = {}'.format(X,y))

    else:
        pass    

    return features


def shift(stack, queue, graph):
    stack = [queue[0]] + stack
    queue = queue[1:]
    return stack, queue, graph

def reduce(stack, queue, graph):
    return stack[1:], queue, graph

if __name__ == "__main__":
    first_set = ['POS_stack', 'POS_queue', 'word_stack', 'word_queue', 'can-la', 'can-re']
    second_set = ['POS_stack0', 'POS_stack1', 'word_stack0', 'word_stack1', 'POS_queue0', 'POS_queue1', 'word_queue0', 'word_queue1', 'can-la', 'can-re']
    third_set = ['POS_stack0', 'POS_stack1', 'word_stack0', 'word_stack1', 'POS_queue0', 'POS_queue1', 'word_queue0', 'word_queue1', 'can-la', 'can-re',
                'POS_sentece_order', 'wordform_sentence_order']
    # stack = []
    graph = []
    
    train_file = '../lab4/swedish_talbanken05_train.conll'

    with open(train_file, 'r') as file:
        sentence = []
        for f in file:
            line = f.split()
            if line == []:
                root = ['0', 'ROOT', 'ROOT', 'ROOT', 'ROOT', 'ROOT', '0', 'ROOT', '0', 'ROOT']
                stack = [root]
                features = extract(stack, sentence, graph, second_set, sentence, 2)
                break
            else:
                graph.append((int(line[6]), int(line[0])))
                # can-la = tuple plats 0 > tuple plats 1
                sentence.append(line)
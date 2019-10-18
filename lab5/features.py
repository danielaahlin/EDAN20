"""
First set  - POS_stack, word_stack, POS_queue, word_queue, can-la, can-re
Second set - POS_stack0, POS_stack1, word_stack0, word_stack1, POS_queue0, POS_queue1, word_queue0, word_queue1, can-la, can-re
Third set  - POS_stack0, POS_stack1, word_stack0, word_stack1, POS_queue0, POS_queue1, word_queue0, word_queue1, can-la, can-re,
             POS_sentece_order, wordform_sentence_order
"""

def extract(stack, queue, graph, feature_names, sentence, model_set):
    X_features = {}
    y_features = {}
    if model_set == 1:
        X = ['nil', 'nil', stack[0][3], stack[0][1], False, False]
        y = 'sh'
        
        X_features.update(zip(feature_names, X))
        y_features.update(zip('action', y))
        # print('x = {}, y = {}'.format(X,y))
        while len(queue) > 0:
            top = stack[0]
            first = queue[0]
            
            top_id = int(top[0])
            first_id = int(first[0])
            #arc
            arced = False
            if (top_id, first_id) in graph:
                arced = True
                X = firstSetX(stack, queue, graph)
                y = 'ra.{}'.format(first[7])
                
                X_features.update(zip(feature_names, X))
                y_features.update(zip('action', y))
                
                stack, queue, graph = shift(stack, queue, graph)
            elif (first_id, top_id) in graph:
                arced = True
                #'can-la' = True
                X = firstSetX(stack, queue, graph)
                y = 'la.{}'.format(top[7])

                X_features.update(zip(feature_names, X))
                y_features.update(zip('action', y))

                stack, queue, graph = reduce(stack, queue, graph)
            #reduce
            if not arced:
                reduced = False
                for k in stack:
                    k_id = int(k[0])
                    if (k_id, first_id) in graph or (first_id, k_id) in graph:
                        reduced = True
                        stack, queue, graph = reduce(stack, queue, graph)
                        X = firstSetX(stack, queue, graph)
                        y = 're'

                        X_features.update(zip(feature_names, X))
                        y_features.update(zip('action', y))
                    else:    
                        pass
            #shift
            if not arced and not reduced:
                X = firstSetX(stack, queue, graph)
                y = 'sh'
                
                X_features.update(zip(feature_names, X))
                y_features.update(zip('action', y))
                
                stack, queue, graph = shift(stack, queue, graph)
            
            # print('x = {}, y = {}'.format(X,y))
    elif model_set == 2:
        X = ['nil', 'nil', 'nil', 'nil', stack[0][3], queue[0][3], stack[0][1], queue[0][1], False, False]
        y = 'sh'

        X_features.update(zip(feature_names, X))
        y_features.update(zip('action', y))
        print('x = {}, y = {}'.format(X,y))
        #print(queue)
        while len(queue) > 0:
            #     #lägg till saker i features
            top = stack[0]
            first = queue[0]
            
            top_id = int(top[0])
            first_id = int(first[0])
            #arc
            arced = False
            if (top_id, first_id) in graph:
                arced = True
                X = secondSetX(stack, queue, graph)
                y = 'ra.{}'.format(first[7])
                
                X_features.update(zip(feature_names, X))
                y_features.update(zip('action', y))
                
                stack, queue, graph = shift(stack, queue, graph)
            elif (first_id, top_id) in graph:
                arced = True
                #'can-la' = True
                X = secondSetX(stack, queue, graph)
                y = 'la.{}'.format(top[7])

                X_features.update(zip(feature_names, X))
                y_features.update(zip('action', y))

                stack, queue, graph = reduce(stack, queue, graph)
            #reduce
            if not arced:
                reduced = False
                for k in stack:
                    k_id = int(k[0])
                    if (k_id, first_id) in graph or (first_id, k_id) in graph:
                        reduced = True
                        stack, queue, graph = reduce(stack, queue, graph)
                        X = secondSetX(stack, queue, graph)
                        y = 're'

                        X_features.update(zip(feature_names, X))
                        y_features.update(zip('action', y))
                        #can-re = True
                        #lägga till i features
                    else:    
                        pass
            #shift
            if not arced and not reduced:
                X = secondSetX(stack, queue, graph)
                y = 'sh'

                X_features.update(zip(feature_names, X))
                y_features.update(zip('action', y))
                
                stack, queue, graph = shift(stack, queue, graph)
            
            print('x = {}, y = {}'.format(X,y))
    else:
                
        X = ['nil', 'nil', 'nil', 'nil', stack[0][3], queue[0][3], stack[0][1], queue[0][1], False, False]
        y = 'sh'

        X_features.update(zip(feature_names, X))
        y_features.update(zip('action', y))
        # print('x = {}, y = {}'.format(X,y))
        #print(queue)
        while len(queue) > 0:
            #     #lägg till saker i features
            top = stack[0]
            first = queue[0]
            
            top_id = int(top[0])
            first_id = int(first[0])
            #arc
            arced = False
            if (top_id, first_id) in graph:
                arced = True
                X = thirdSetX(stack, queue, graph)
                y = 'ra.{}'.format(first[7])

                X_features.update(zip(feature_names, X))
                y_features.update(zip('action', y))

                stack, queue, graph = shift(stack, queue, graph)
            elif (first_id, top_id) in graph:
                arced = True
                #'can-la' = True
                X = thirdSetX(stack, queue, graph)
                y = 'la.{}'.format(top[7])

                X_features.update(zip(feature_names, X))
                y_features.update(zip('action', y))

                stack, queue, graph = reduce(stack, queue, graph)
            #reduce
            if not arced:
                reduced = False
                for k in stack:
                    k_id = int(k[0])
                    if (k_id, first_id) in graph or (first_id, k_id) in graph:
                        reduced = True
                        stack, queue, graph = reduce(stack, queue, graph)
                        X = thirdSetX(stack, queue, graph)
                        y = 're'

                        X_features.update(zip(feature_names, X))
                        y_features.update(zip('action', y))

                        #can-re = True
                        #lägga till i features
                    else:    
                        pass
            #shift
            if not arced and not reduced:
                X = thirdSetX(stack, queue, graph)
                y = 'sh'

                X_features.update(zip(feature_names, X))
                y_features.update(zip('action', y))

                stack, queue, graph = shift(stack, queue, graph)
            
            # print('x = {}, y = {}'.format(X,y))

    return X_features, y_features
    

def firstSetX(stack, queue, graph):
    return [stack[0][3], stack[0][1], queue[0][3], queue[0][1], canLA(int(stack[0][0]), int(queue[0][0]), stack, graph), canRe(stack, int(queue[0][0]), graph)]

def secondSetX(stack, queue, graph):
    POS_stack1, word_stack1, POS_queue1, word_queue1 = '', '', '', ''
    if len(stack) < 2:
        POS_stack1 = 'nil'
        word_stack1 = 'nil'
    else:
        POS_stack1 = stack[1][3]
        word_stack1 = stack[1][1]
    if len(queue) < 2:
        POS_queue1 = 'nil'
        word_queue1 = 'nil'
    else:
        POS_queue1 = queue[1][3]
        word_queue1 = queue[1][1]
    return [stack[0][3], POS_stack1, stack[0][1], word_stack1, queue[0][3], POS_queue1, queue[0][1], 
    word_queue1, canRe(stack, int(queue[0][0]), graph), canLA(int(stack[0][0]), int(queue[0][0]), stack, graph)]

def thirdSetX(stack, queue, graph):
    POS_stack1, word_stack1, POS_queue1, word_queue1, POS_sentece_order, wordform_sentence_order = '', '', '', '', '', ''
    if len(stack) < 2:
        POS_stack1 = 'nil'
        word_stack1 = 'nil'
        POS_sentece_order = 'nil'
        wordform_sentence_order = 'nil'
    else:
        POS_stack1 = stack[1][3]
        word_stack1 = stack[1][1]
        stack1_id = stack[1][0]
        if int(stack1_id)+1 >= len(queue):
            POS_sentece_order = 'nil'
            wordform_sentence_order = 'nil'
        else:
            POS_sentece_order = queue[int(stack1_id)+1][3]
            wordform_sentence_order = queue[int(stack1_id)+1][1]
    if len(queue) < 2:
        POS_queue1 = 'nil'
        word_queue1 = 'nil'
    else:
        POS_queue1 = queue[1][3]
        word_queue1 = queue[1][1]
    return [stack[0][3], POS_stack1, stack[0][1], word_stack1, queue[0][3], POS_queue1, queue[0][1], 
    word_queue1, canLA(int(stack[0][0]), int(queue[0][0]), stack, graph), canRe(stack, int(queue[0][0]), graph), POS_sentece_order, wordform_sentence_order]



def canLA(top, first, stack, graph):
    if top == 0:
        return False
    if top > first or not canRe(stack, first, graph):
        return True
    return False

def canRe(stack, first_id, graph):
    for k in stack:
        if (int(k[0][0]), first_id) in graph or (first_id, int(k[0][0])) in graph:
            return True
    
    return False

def shift(stack, queue, graph):
    stack = [queue[0]] + stack
    queue = queue[1:]
    return stack, queue, graph

def reduce(stack, queue, graph):
    return stack[1:], queue, graph


# def parse_ml(stack, queue, graph, trans):
    # if stack and trans[:2] == 'ra':
        # stack, queue, graph = transition.right_arc(stack, queue, graph, trans[3:])
        # return stack, queue, graph, 'ra'

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
                print(len(sentence))
                # for s in sentence:
                #     print(s)
                #     tup = (int(s[6]), int(s[0]))
                #     print(tup)
                #     graph.append(tup)
                #     print(graph)
                # print(len(graph))
                X_features, y_features = extract(stack, sentence, graph, second_set, sentence, 2)
                graph = []
                sentence = []
                stack = []
                break
            else:
                graph.append((int(line[6]), int(line[0])))
                # can-la = tuple plats 0 > tuple plats 1
                sentence.append(line)
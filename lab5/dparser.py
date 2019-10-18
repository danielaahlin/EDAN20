"""
Gold standard parser
"""
__author__ = "Pierre Nugues"

import transition
import conll
import features_new as feats
from sklearn import linear_model
from sklearn.feature_extraction import DictVectorizer
import pickle
from sklearn import metrics

def reference(stack, queue, graph):
    """
    Gold standard parsing
    Produces a sequence of transitions from a manually-annotated corpus:
    sh, re, ra.deprel, la.deprel
    :param stack: The stack
    :param queue: The input list
    :param graph: The set of relations already parsed
    :return: the transition and the grammatical function (deprel) in the
    form of transition.deprel
    """
    # Right arc
    if stack and stack[0]['id'] == queue[0]['head']:
        # print('ra', queue[0]['deprel'], stack[0]['cpostag'], queue[0]['cpostag'])
        deprel = '.' + queue[0]['deprel']
        stack, queue, graph = transition.right_arc(stack, queue, graph)
        return stack, queue, graph, 'ra' + deprel
    # Left arc
    if stack and queue[0]['id'] == stack[0]['head']:
        # print('la', stack[0]['deprel'], stack[0]['cpostag'], queue[0]['cpostag'])
        deprel = '.' + stack[0]['deprel']
        stack, queue, graph = transition.left_arc(stack, queue, graph)
        return stack, queue, graph, 'la' + deprel
    # Reduce
    if stack and transition.can_reduce(stack, graph):
        for word in stack:
            if (word['id'] == queue[0]['head'] or
                        word['head'] == queue[0]['id']):
                # print('re', stack[0]['cpostag'], queue[0]['cpostag'])
                stack, queue, graph = transition.reduce(stack, queue, graph)
                return stack, queue, graph, 're'
    # Shift
    # print('sh', [], queue[0]['cpostag'])
    stack, queue, graph = transition.shift(stack, queue, graph)
    return stack, queue, graph, 'sh'

def parse_ml(stack, queue, graph, trans):
    if stack and trans[:2] == 'ra':
        stack, queue, graph = transition.right_arc(stack, queue, graph, trans[3:])
        return stack, queue, graph, 'ra'
    if stack and trans[:2] == 'la' and transition.can_leftarc(stack, graph):
        stack, queue, graph = transition.left_arc(stack, queue, graph, trans[3:])
        return stack, queue, graph, 'la'
    if stack and trans[:2] == 're' and transition.can_reduce(stack, graph):
        stack, queue, graph = transition.reduce(stack, queue, graph)
        return stack, queue, graph, 're'
    stack, queue, graph = transition.shift(stack, queue, graph)
    return stack, queue, graph, 'sh'

if __name__ == "__main__":
    train_file = '../lab4/swedish_talbanken05_train.conll'
    test_file = '../lab4/swedish_talbanken05_test_blind.conll'
    column_names_2006 = ['id', 'form', 'lemma', 'cpostag', 'postag', 'feats', 'head', 'deprel', 'phead', 'pdeprel']
    column_names_2006_test = ['id', 'form', 'lemma', 'cpostag', 'postag', 'feats']

    sentences = conll.read_sentences(train_file)
    formatted_corpus = conll.split_rows(sentences, column_names_2006)

    sentences_test = conll.read_sentences(test_file)
    formatted_corpus_test = conll.split_rows(sentences_test, column_names_2006_test)

    sent_cnt = 0

    graph_list = []
    y = []
    queue_list = []
    first_set = ['POS_stack', 'POS_queue', 'word_stack', 'word_queue', 'can-la', 'can-re']
    second_set = ['POS_stack0', 'POS_stack1', 'word_stack0', 'word_stack1', 'POS_queue0', 'POS_queue1', 'word_queue0', 'word_queue1', 'can-la', 'can-re']
    third_set = ['POS_stack0', 'POS_stack1', 'word_stack0', 'word_stack1', 'POS_queue0', 'POS_queue1', 'word_queue0', 'word_queue1', 'can-la', 'can-re',
                'POS_before', 'word_before', 'POS_after', 'word_after']

    features1 = []
    features2 = []
    features3 = []
    all_transitions = []
    X = []

    # vec = DictVectorizer(sparse=True)

    # for sentence in formatted_corpus:
    #     sent_cnt += 1
    #     if sent_cnt % 1000 == 0:
    #         print(sent_cnt, 'sentences on', len(formatted_corpus), flush=True)
    #     stack = []
    #     queue = list(sentence)
    #     graph = {}
    #     graph['heads'] = {}
    #     graph['heads']['0'] = '0'
    #     graph['deprels'] = {}
    #     graph['deprels']['0'] = 'ROOT'
    #     transitions = []


    #     while queue:
    #         # features1.append(feats.extract1(stack, queue, graph, first_set, sentence))
    #         # features2.append(feats.extract2(stack, queue, graph, second_set, sentence))
    #         # features3.append(feats.extract3(stack, queue, graph, third_set, sentence))
    #         X.append(feats.extract3(stack, queue, graph, third_set, sentence))
    #         stack, queue, graph, trans = reference(stack, queue, graph)
    #         transitions.append(trans)
    #     all_transitions.extend(transitions)
    #     stack, graph = transition.empty_stack(stack, graph)
    #     # print('Equal graphs:', transition.equal_graphs(sentence, graph))

    #     # Poorman's projectivization to have well-formed graphs.
    #     for word in sentence:
    #         word['head'] = graph['heads'][word['id']]
    #     # print(transitions)
    #     # print(graph)
    # # model1 = classifier.fit(features1, all_transitions)
    # # model2 = classifier.fit(features2, all_transitions)
    # # model3 = classifier.fit(features3, all_transitions)

    # X_vec = vec.fit_transform(X)
    classifier = linear_model.LogisticRegression(penalty='l2', solver='liblinear', dual=True, verbose=2)
    # 
    # model = classifier.fit(X_vec, all_transitions)
    # with open('training.pkl', 'wb') as f:
        # pickle.dump((vec, model), f, protocol=pickle.HIGHEST_PROTOCOL)
    # print(model)


    X = []
    y_test_pred = []
    (vec, model) = pickle.load(open('training.pkl', 'rb'))
    for sentence in formatted_corpus_test:
        sent_cnt += 1
        if sent_cnt % 1000 == 0:
            print(sent_cnt, 'sentences on', len(formatted_corpus), flush=True)
        stack = []
        queue = list(sentence)
        graph = {}
        graph['heads'] = {}
        graph['heads']['0'] = '0'
        graph['deprels'] = {}
        graph['deprels']['0'] = 'ROOT'
        transitions = []


        while queue:
            X_vec = feats.extract3(stack, queue, graph, third_set, sentence)
            # X.append(X_vec)
            X_test = vec.transform(X_vec)
            trans = model.predict(X_test)[0]
            y_test_pred.append(trans)
            stack, queue, graph, trans = parse_ml(stack, queue, graph, trans)
            transitions.append(trans)
        all_transitions.extend(transitions)
        stack, graph = transition.empty_stack(stack, graph)
        # print('Equal graphs:', transition.equal_graphs(sentence, graph))
        # Poorman's projectivization to have well-formed graphs.
        for word in sentence:
            word['head'] = graph['heads'][word['id']]
            word['deprel'] = graph['deprels'][word['id']]
    conll.save('out_file', formatted_corpus_test, column_names_2006)
            
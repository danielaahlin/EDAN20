import dparser
import transition


def extract1(stack, queue, graph, feature_names, sentence):
    feat_vec = ['','','','','','']
    if not stack:
        feat_vec[0] = feat_vec[1] = 'nil'
        feat_vec[2] = queue[0]['postag'] 
        feat_vec[3] = queue[0]['form']
    elif not queue:
        feat_vec[2] = feat_vec[3] = 'nil'
        feat_vec[0] = stack[0]['postag']
        feat_vec[1] = stack[0]['form']
    else:
        feat_vec[0] = stack[0]['postag']
        feat_vec[1] = stack[0]['form']
        feat_vec[2] = queue[0]['postag'] 
        feat_vec[3] = queue[0]['form']
    feat_vec[4] = transition.can_reduce(stack, graph)
    feat_vec[5] = transition.can_leftarc(stack, graph)
    return dict(zip(feature_names, feat_vec))

def extract2(stack, queue, graph, feature_names, sentence):
    features = {}
    feat_vec = ['','','','','','','','','','']
    if not stack:
        feat_vec[0] = feat_vec[1] = feat_vec[2] = feat_vec[3] = 'nil'
    elif len(stack) < 2:
        feat_vec[1] = feat_vec[3] = 'nil'
        feat_vec[0] = stack[0]['postag']
        feat_vec[2] = stack[0]['form']
    else:
        feat_vec[0] = stack[0]['postag']
        feat_vec[1] = stack[1]['postag']
        feat_vec[2] = stack[0]['form']
        feat_vec[3] = stack[1]['form']

    if not queue:
        feat_vec[5] = feat_vec[6] = feat_vec[7] = feat_vec[8] = 'nil'
    if len(queue) < 2:
        feat_vec[4] = queue[0]['postag']
        feat_vec[6] = queue[0]['form']
        feat_vec[5] = feat_vec[7] = 'nil'
    else:
        feat_vec[4] = queue[0]['postag']
        feat_vec[5] = queue[1]['postag']
        feat_vec[6] = queue[0]['form']
        feat_vec[7] = queue[1]['form']

    feat_vec[8] = transition.can_reduce(stack, graph)
    feat_vec[9] = transition.can_leftarc(stack, graph)

    return dict(zip(feature_names, feat_vec))


def extract3(stack, queue, graph, feature_names, sentence):
    features = {}
    feat_vec = ['','','','','','','','','','','','','','']
    if not stack:
        feat_vec[0] = feat_vec[1] = feat_vec[2] = feat_vec[3] = 'nil'
    elif len(stack) < 2:
        feat_vec[1] = feat_vec[3] = 'nil'
        feat_vec[0] = stack[0]['postag']
        feat_vec[2] = stack[0]['form']
    else:
        feat_vec[0] = stack[0]['postag']
        feat_vec[1] = stack[1]['postag']
        feat_vec[2] = stack[0]['form']
        feat_vec[3] = stack[1]['form']

    if not queue:
        feat_vec[5] = feat_vec[6] = feat_vec[7] = feat_vec[8] = 'nil'
    if len(queue) < 2:
        feat_vec[4] = queue[0]['postag']
        feat_vec[6] = queue[0]['form']
        feat_vec[5] = feat_vec[7] = 'nil'
    else:
        feat_vec[4] = queue[0]['postag']
        feat_vec[5] = queue[1]['postag']
        feat_vec[6] = queue[0]['form']
        feat_vec[7] = queue[1]['form']

    feat_vec[8] = transition.can_reduce(stack, graph)
    feat_vec[9] = transition.can_leftarc(stack, graph)

    #before 10, 11
    #after 12,13

    if not stack:
        feat_vec[10] = feat_vec[11] = feat_vec[12] = feat_vec[13] = 'nil'
    else:
        st_id = stack[0]['id']
        if int(st_id) == 0:
            feat_vec[10] = feat_vec[11] = 'nil'
        else:
            feat_vec[10] = sentence[int(st_id) - 1]['postag']
            feat_vec[11] = sentence[int(st_id) - 1]['form']
        
        if int(st_id) > len(sentence):
            feat_vec[12] = feat_vec[13] = 'nil'
        else:
            feat_vec[12] = sentence[int(st_id) + 1]['postag']
            feat_vec[13] = sentence[int(st_id) + 1]['form']

    return dict(zip(feature_names, feat_vec))   
     
# if __name__ == "__main__":
    # graphs, y, queues = dparser.parse()
# 
    # first_set = ['POS_stack', 'POS_queue', 'word_stack', 'word_queue', 'can-la', 'can-re']
    # second_set = ['POS_stack0', 'POS_stack1', 'word_stack0', 'word_stack1', 'POS_queue0', 'POS_queue1', 'word_queue0', 'word_queue1', 'can-la', 'can-re']
    # third_set = ['POS_stack0', 'POS_stack1', 'word_stack0', 'word_stack1', 'POS_queue0', 'POS_queue1', 'word_queue0', 'word_queue1', 'can-la', 'can-re',
                # 'POS_sentece_order', 'wordform_sentence_order']
# 
    # for g, y, q in zip(graphs, y, queues):
        # print(g)
        # print(y)
        # print(q)
        # features = extract2([], q, g, second_set, g)
        # print(features)
        
from collections import defaultdict
from fractions import Fraction

word_train = '../train/word.txt'
tag_train = '../train/tag.txt'

def train(word_train=word_train, tag_train=tag_train):
    '''
        From training set, calculate emission probabilities, transition probabilities
        input:
            - word_train: string, represents path to file that contains training words 
        output:
            - tag_train: string, represents path to file that contains tags (for training words)
        return:
            - transition_map: dictionary, represents transition probabilities
            - emission_map: dictionary, represents emission probabilities
            - tags_words_map: dictionary, for later on calculation 
    '''
    # first count how many sentences first 
    # n: number of sentences 
    word_count = 0
    with open(word_train) as f:
        n = len(f.readlines())
        
    # all non duplicated words  
    V = set()

    word_bag = open(word_train)
    tag_bag = open(tag_train)

    word_line = word_bag.readline().strip()
    tag_line = tag_bag.readline().strip()
    # map words and tags like:
    # IN: ['cua', 'o'], ....
    tags_words_map = defaultdict(list)
    # map store string-like transitions ti-1 to ti and their probability
    # {'NN|IN': 0.5, ...} 'NN|IN' is transition from IN to NN (NN follows IN)
    # or more specific, transition probability map
    transition_map = dict()
    while word_line and tag_line:
        # build tags-words map 
        words = word_line.split()
        tags = tag_line.split()
        word_count += len(words)
        assert len(words) == len(tags)
        for i in range(len(tags)):
            tags_words_map[tags[i]].append(words[i])
            V.add(words[i])
        
        # build transition map 
        # but we only store the number of times they appear first
        # we gonna caculate their prob at @2
        for i in range(len(tags)):
            if i == 0:
                transition_map[(tags[i], 'qo')] = transition_map.setdefault((tags[i], 'qo'), 0) + 1
            else:
                transition_map[(tags[i], tags[i-1])] = transition_map.setdefault((tags[i], tags[i-1]), 0) + 1
        

        # proceed to new line 
        tag_line = tag_bag.readline().strip()
        word_line = word_bag.readline().strip()
    
    # @2: calculate transition probabilities
    # QA : number of states 
    QA = len(tags_words_map) 
    for ti, ti_1 in transition_map:
        count = transition_map[(ti, ti_1)]
        if ti_1 != 'qo':
            transition_map[(ti, ti_1)] = transition_smoothing(count, len(tags_words_map[ti_1]), QA)
        else:
            transition_map[(ti, ti_1)] = transition_smoothing(count, n, QA)
    
    states = list(tags_words_map)
    for state in states:
        if (state, 'qo') not in transition_map:
            transition_map[(state, 'qo')] = transition_smoothing(0, n, QA)

    
    # calculate emission probabilities
    emission_map = dict()
    for state, words in tags_words_map.items():
        nonduplicated_words = set(words)
        for word in nonduplicated_words:
            emission_map[(word, state)] = emission_smoothing(words.count(word), len(words), len(V))
    
    # print out for testing
    # can remove later
    print(len(V))
    print(word_count)
    # for tag, val in emission_map.items():
    #     print(tag,":",val)
    # for tag, val in transition_map.items():
    #     print(tag,":",val)
    # for tag, words in tags_words_map.items():
    #     print(tag,":",words)
    
    return transition_map, emission_map, tags_words_map, V
        

def transition_smoothing(transition_count, prev_state_count, QA):
    return Fraction(transition_count+1, prev_state_count+QA)

def emission_smoothing(emission_count, tag_count, all_words):
    '''
        emission_count: number of times a word appear in a specific state 
            NN : ['gia_đình', 'quê', 'sách', 'thư_viện', 'lớp']
            emission_count of gia_đình = 1
        tag_count: number of words of a specific state 
            IN : ['của', 'ở', 'ở']
            tag_count = 2
        all_words: number of all non duplicated words 
    '''
    return Fraction(emission_count+1, tag_count+all_words)

if __name__ == '__main__':
    test_1 = 'Nam ở quê'
    test_2 = 'gia_đình của Lan sống ở thư_viện'
    test_3 = 'Lan thích học ở lớp'
    train()

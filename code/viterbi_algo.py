from train import train, emission_smoothing, transition_smoothing
import time

def viterbi(s, trans_prob, emit_p, states, V):
    v_matrix = [{}]
    for state in states:
        if (s[0], state) not in emit_p:
            prob = emission_smoothing(0, len(states[state]), len(V))*trans_prob[(state, 'qo')]
        else:
            prob = emit_p[(s[0],state)]*trans_prob[(state, 'qo')]
        v_matrix[0][state] = {'prob': prob, 'prev':None}
    
    # only work with sentences that have more than 1 words
    assert len(s) > 1
       
    # forward
    prepair_emission_calculation(states, s, emit_p, V)
    for i in range(1, len(s)):
        next_v = forward(v_matrix[i-1], states, s[i], trans_prob, emit_p)
        v_matrix.append(next_v)

    # for i in range(len(v_matrix)):
    #     max_prob = max(v_matrix[i][x]['prob'] for x in states)
    #     for key, val in v_matrix[i].items():
    #         print(key, ":", val)
    #     print(max_prob,'\n')
    # backtrack
    return trace_back(v_matrix)
    

def prepair_transition_calculation(states, trans_prob):
    '''
        for some transition states ti_1 to ti that not in the training set
        we have to use lablace smoothing to make sure that prob will not be 0 
        this will be called 1 after training
    '''
    for state in states:
        for prev_state in states:
            if (state, prev_state) not in trans_prob:
                trans_prob[(state, prev_state)] = transition_smoothing(0, len(states[prev_state]), len(states))


def prepair_emission_calculation(states, s, emit_p, V):
    '''
        same as prepair_transition_calculation, but for observed words 
        that don't have corresponding states, 
        except that this will be called whenever we run viterbi algo
    '''
    for word in s:
        for state in states:
            if (word, state) not in emit_p:
                emit_p[(word, state)] = emission_smoothing(0, len(states[state]), len(V))


def forward(vi_1, states, s_i, trans_prob, emit_p):
    next_v = {}
    for state in states:
        # get the maximum transition probability
        max_t_prob = max(
            vi_1[prev_state]['prob']*trans_prob[(state, prev_state)] 
            for prev_state in states
        )
        # and multiply it with emission probability of word s_i given state 'state'  
        for prev_state in states:
            if vi_1[prev_state]['prob']*trans_prob[(state,prev_state)] == max_t_prob:
                max_prob = max_t_prob * emit_p[(s_i,state)]
                next_v[state] = {'prob':max_prob, 'prev': prev_state}
                break
    return next_v

def trace_back(v_matrix):
    # first we get the highst probability at the final column
    max_prob = max(state['prob'] for state in v_matrix[-1].values())
    pos_tag_sq = []
    prev = None
    # and get the state with probability = highest probability 
    # to be the last pos-tag for the observation sequence 
    for state in v_matrix[-1]:
        if v_matrix[-1][state]['prob'] == max_prob:
            pos_tag_sq.insert(0, state)
            prev = v_matrix[-1][state]['prev']
            pos_tag_sq.insert(0, prev)
            break 

    # trace back until prev is None 
    # it means we're at the first column 
    # v_matrix = list(reversed(v_matrix))
    v_matrix.pop()
    while prev is not None:
        if v_matrix[-1][prev]['prev'] is not None:
            pos_tag_sq.insert(0, v_matrix[-1][prev]['prev'])
        prev = v_matrix[-1][prev]['prev']
        v_matrix.pop()
    print(pos_tag_sq)
    return pos_tag_sq

def print_viterbi_matrix(v_matrix):
    yield " ".join('{:12d}'.format(i) for i in range(len(v_matrix)))
    for state in states:
        yield '{:7s}'.format(state) + ' '.join('{:7s}'.format('{:10.5f}'.format(v[state]['prob'])) for v in v_matrix) 

def test(trans_prob, emission_prob, tags_words_map, V, test_folder='../test'):
    total_word, correct_word = 0, 0
    words_test = open(test_folder+'/word.txt')
    tags_test = open(test_folder+'/tag.txt')
    output = open('../hmm_output/hmm_output.txt', 'w')
    start = time.time()
    observation = words_test.readline().strip()
    pos_tag_sq = tags_test.readline().strip()
    while observation and pos_tag_sq:
        s = observation.split()
        pos_tag_sq = pos_tag_sq.split()
        result = viterbi(s, trans_prob, emission_prob, tags_words_map, V)
        assert len(result) == len(pos_tag_sq), s
        output.write(' '.join(result) + '\n')
        total_word += len(pos_tag_sq)
        for i in range(len(result)):
            if result[i] == pos_tag_sq[i]:
                correct_word += 1
        observation = words_test.readline().strip()
        pos_tag_sq = tags_test.readline().strip()
    if total_word != 0:
        print('Accuracy: {:.2f}%'.format((correct_word/total_word)*100))
        print('Test size: {:d} words'.format(total_word))
        print('Running Time: {} second(s)'.format(time.time()-start))
        output.close()

if __name__ == '__main__':
    trans_prob, emission_prob, tags_words_map, V = train()
    prepair_transition_calculation(tags_words_map, trans_prob)
    test(trans_prob, emission_prob, tags_words_map, V)
    # s = 'Nam ở quê'.split()
    # print(s, "->", end=' ')
    # viterbi(s, trans_prob, emission_prob, tags_words_map, V)
    # s = 'Lan thích học ở lớp'.split()
    # print(s, "->", end=' ')
    # viterbi(s, trans_prob, emission_prob, tags_words_map, V)
    # s = 'gia_đình của Lan sống ở thư_viện'.split()
    # print(s, "->", end=' ')
    # viterbi(s, trans_prob, emission_prob, tags_words_map, V)
    # s = 'Nam thích Lan'.split()
    # print(s, "->", end=' ')
    # viterbi(s, trans_prob, emission_prob, tags_words_map, V)
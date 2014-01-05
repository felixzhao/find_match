import sys
import string, gzip
import time
import math

from heapq import *

from reference.find_cands import find_cands
from reference.nsmallestcandidates import nsmallestcandidates
from reference.update_docs import update_docs



def beam_search(match_word_test, test_vectors, train_vectors, beam_width, unk_dict, stroke_dict, stroke_feature_weight, do_stroke_feature_flag):

    print >>sys.stderr, 'beam search started. at', time.strftime('%X')  

    #define
    unks = []
    docs = []
    cands = [] # dist, cand, #doc
    result = {} # unki : [ candj]
    
    nsmallest = []

    # init
    topnum = 50
    unks = match_word_test
    docs.append(test_vectors)
    
    for u in unks:

# log
        print u
# end log

        for d in xrange(len(docs)):
            cands = list( \
                merge( \
                   find_cands(u, docs[d], trainvectors, topnum, d, unk_dict, stroke_dict, stroke_feature_weight, do_stroke_feature_flag) \
                        ,cands) \
                    )                    
            # debug
            print cands[0][0]
            print cands[0][1]
            print cands[0][2]
            # end debug
        t_docs = []
        for item in nsmallestcandidates(beam_width, cands):
            print len(item)
            print item[-1]

            # unk, cand, doc
            t_docs.append( \
                update_docs( \
                        u, \
                        item[1], \
                        docs[ item[2] ],\
                        train_vectors \
                        ) \
                    )

# log
            print ' => ' + item[1] + ' : ' + str(item[0])
# end log
            # add result
            if(u not in result):
                result[u] = []
            result[u].append(item[1])

        # perpare for next turn
        docs = t_docs
        cands = []
        print >>sys.stderr, 'unk: ', u, ' done. at time: ', time.strftime('%X')
# debug
        print ' ++++++ result ++++++ '
        print u
        print result[u]
        print result[u][0]
        print result[u][1]
        print result[u][2]
        print '{0}:{1}|{2}|{3}'.format(u,result[u][0],result[u][1],result[u][2])
        out_str = '{0}:'.format(u)
        for item in result[u]:
            out_str += '{0}|'.format(item)
        print >>sys.stderr, out_str
        print ' ++++++ end of result ++++++ '
# end bebug
    # end of beam search
    return result

if __name__ == '__main__':

    if len(sys.argv) < 6:
        print ' para: 1. train word embed file path\n 2. test word embed file path\n 3. beam width (int)\n 4. noise size for stroke feature (int) (if 0 < ns <= 4 then disable stroke feature)\n 5. stroke feature weight\n 6. input type (the type of word embed source: 33 or 50 or 67)\n'
        

## get input
    train_path = sys.argv[1]
    test_path = sys.argv[2]
    beam_width = int(sys.argv[3])
    noise_size = int(sys.argv[4])
    stroke_feature_weight = int(sys.argv[5])
    input_type = sys.argv[6] # 33, 50, 67

    print 'trian path: ' + train_path
    print 'test path: ' + test_path
    print 'beam width: ' + str(beam_width)
    print 'noise_size: ' + str(noise_size)

## declare
    out_path = 'out.bw' + str(beam_width) + '.ns' + str(noise_size) + '.sfw'  + str(stroke_feature_weight) + '.type' + str(input_type) + '.txt'
    stroke_dict = {}
    unk_dict = {}
    trainwords = set()
    testwords = set()
    knownwords = set()
    matchwords_train = []
    unk_list = []
    trainvectors = {}
    testvectors = {}
    do_stroke_feature_flag = noise_size > 0 and noise_size <= 4

## get stroke data
    if do_stroke_feature_flag == True:
        stroke_code_file = 'wubi_code_dict_6563.txt'
        terms = open(stroke_code_file,'r').readline().split(';')
        unk_code = open('stroke_feature/unk_code_ns' + str(noise_size) + '_type' + str(input_type) + '.txt','r').readlines()

    ## get stroke feature code
        words = [w.split() for w in terms]
        for w in words:
            if len(w) > 1:
                stroke_dict[w[0]] = w[1]
    ## get unk stroke feature code
        for line in unk_code:
            w = line.split(' ')
            if len(w) > 1:
                unk_dict[w[0]] = w[1]
    
## get source data
    trainfile = gzip.open(train_path, "rb")
    testfile = gzip.open(test_path, "rb")    
    outfile = open(out_path,'w')
    
    #Read files
    for l in trainfile:
        toks = string.split(l)
        if toks[0] == '*UNKNOWN*':
            continue
        trainwords.add(toks[0])
        trainvectors[toks[0]] = [float(f) for f in toks[1:]]
    for l in testfile:
        toks = string.split(l)
        if toks[0] == '*UNKNOWN*':
            continue
        testwords.add(toks[0])
        testvectors[toks[0]] = [float(f) for f in toks[1:]]
    
    knownwords = trainwords & testwords
    matchwords_train = list(trainwords - knownwords)
    #Deal with the OOV words in test corpus
    for w in testwords:
        if w.startswith('<unk>'):
            unk_list.append(w)
        
    print len(unk_list)
## get result
    actual =  beam_search(unk_list, testvectors, trainvectors, beam_width, unk_dict, stroke_dict, stroke_feature_weight, do_stroke_feature_flag)
    ## pirnt out result
    for k in actual.keys():
        print >> outfile, ' ===== start of ' + k + ' ====== '

        out_str = '{0}:'.format(k)
        for item in actual[k]:
            out_str += '{0}|'.format(item)
        print out_str

        print >> outfile, out_str

        print >> outfile, ' ===== end of ' + k + ' ====== '
        print >> outfile, ' '

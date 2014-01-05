from calcMatchScore import *
from calcStrokeFeatureScore import *
from calcdist import *

from heapq import *

def find_cands(match_word_test, testvectors, trainvectors, topnum, doc_num, unk_dict, stroke_dict, stroke_feature_weight, do_strock_feature_flag):

    trainwords = set(trainvectors.keys())
    testwords = set(testvectors.keys())
    knownwords = trainwords & testwords
    matchwords_train = list(trainwords - knownwords)

# Get knn
# calculate clostest known_words in test_vectors which count is topnum
# The test_vectors could be change in bean search

    heap = []
    knn = []
    for known_word in knownwords:
        dist = calcdist(testvectors[match_word_test],testvectors[known_word])
        heappush(heap, (dist,known_word))
    for item in nsmallest(topnum, heap):
        knn.append(item[1])

# End of Get knn

# Get match words
# get match word & match_score in train_words to test_word
# which size based on topnum
# "knn", "test_vectors" could be change in bean_search

    heap = []
    for match_word_train in matchwords_train:
#        print >>sys.stderr, 'Generating match scores for: ', match_word_train, ' and ', match_word_test
        match_score = calcMatchScore(match_word_test, match_word_train, knn, trainvectors, testvectors)

## get stroke feature score
        if do_strock_feature_flag == True:
           strokeFeatureScore = calcStrokeFeatureScore(match_word_test, match_word_train, unk_dict, stroke_dict, stroke_feature_weight)
           print 'strokeFeatureScore: ' + str(strokeFeatureScore)

           match_score -= strokeFeatureScore

        heappush(heap, (match_score,match_word_train,doc_num))

    return heap

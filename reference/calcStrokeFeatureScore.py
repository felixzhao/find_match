def GetStrokeFeatureInfo(match_word_test, match_word_train, unk_dict, stroke_dict):

## debug
    print 'unk:' + match_word_test
    if match_word_test in unk_dict:
        print 'unk strock feature code: ' + unk_dict[match_word_test]
    else:
       print 'unk ' + match_word_test + ' not in dict'
## end debug

    if (match_word_train not in stroke_dict) or (match_word_test not in unk_dict):
        return 0

    test_code = unk_dict[match_word_test]
    train_code = stroke_dict[match_word_train]
    SFscore = len(set(test_code) & set(train_code))

## Debug
    if SFscore is None or SFscore == '':
        print 'No Stroke Feature info Return.'
    else:
        print 'Stroke Feature Info:' + str(SFscore)
## end Debug

    return SFscore

def calcStrokeFeatureScore(match_word_test, match_word_train, unk_dict, stroke_dict, stroke_feature_weight):
    if (match_word_train not in stroke_dict) or (match_word_test not in unk_dict):
        return 0.0

    match_score = 0.0
    test_code = unk_dict[match_word_test]
    train_code = stroke_dict[match_word_train]
    stroke_info = len(set(test_code) & set(train_code))

    if stroke_info == 0:
        return 0.0
    weight = (int)stroke_feature_weight
# debug
    print 'stroke common length:' + str(stroke_info)
    print 'type of Stroke Info: ' + str(type(stroke_info))
    print 'type of stroke_feature_weight: ' + str(type(stroke_feature_weight))
    print 'type of weight: ' + str(type(weight))
    print 'weight :' + str(weight)
# end debug

    match_score = stroke_info * 0.25 * weight

## Debug
    print 'stroke feature weight: ' + str(stroke_feature_weight)
    print 'match_score:' + str(match_score)
## end Debug

    return match_score

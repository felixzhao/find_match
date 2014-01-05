def GetStrokeFeatureInfo(match_word_test, match_word_train, unk_dict, stroke_dict):
    test_code = unk_dict[match_word_test]
    train_code = stroke_dict[match_word_train]
    return len(set(test_code) & set(train_code))

def calcStrokeFeatureScore(match_word_test, match_word_train, unk_dict, stroke_dict, stroke_feature_weight):
    match_score = ( GetStrokeFeatureInfo(match_word_test, match_word_train)/4) * stroke_feature_weight
    return match_score

def nsmallestcandidates(width, candi_tuple_list):
    result = [] # dist, cand, #doc

    dict = {} # key: cand ; value: [ sum, count, # mini tuple ]

    sorted_list = []

    for item in candi_tuple_list:
        if item[1] not in dict:
            dict[item[1]] = [ item[0], 1, item ]
        else:
            if item[0] < dict[item[1]][2][0]: # current score < min score
                cur_dist = dict[item[1]][0]
                dict[item[1]] = [ cur_dist + item[0], dict[item[1]][1] + 1, item ] # sum dist, count+1, min node

    sorted_list = sorted([ ( x[0]/x[1], x[2] ) for x in dict.values()], key = lambda x:x[0])[:width]

    result = [ x[1] for x in sorted_list ]

    return result

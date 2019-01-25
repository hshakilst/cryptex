#!/usr/bin/python
from fastText import FastText

model = FastText.load_model('./model/final_ns.bin')

def validate_keyword(key):
    tup = ()
    words = key.split(' ')
    
    for word in words:
        tup = tup + model.get_subwords(word)
    
    tup_list = list(tup)
    
    for l in tup_list:
        if(type(l) is not list):
            tup_list.remove(l)
    keyword = ''
    for l in tup_list:
        if(len(l) == 0):
            tup_list.remove(l)
        else:
            keyword = keyword + ' ' + str(l[0])
    if(len(keyword) != 0):
        return True
    else:
        return False
        


def predict_label(key):
    if(validate_keyword(key)):
        tup = model.predict(key)
        s = ''
        for t in tup[0]:
            s = t[9:]
        return s
    else:
        return ''
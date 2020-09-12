import re 

def add_to_dict(entity, ner_dict):
    entity = re.sub(r'\_', ' ', entity)
    if entity not in ner_dict:
        ner_dict[entity] = 1
    else:
        ner_dict[entity] += 1

def get_dict_ner(result, ner_dict, NEXT_CATE):
    ner = []
    n_sentences = len(result)

    for i in range(n_sentences):
        for i, dict_word in enumerate(result[i]):
            if dict_word['nerLabel'] != 'O':
                try:
                    if dict_word['nerLabel'].split('-')[1] == 'MISC':
                        continue
                    if len(ner) > 0 and (ner[-1][1] == i-1) and NEXT_CATE[ner[-1][2]] == dict_word['nerLabel']:
                        ner[-1][0] += ' ' + dict_word['form']
                        ner[-1][1] += 1
                    else:
                        ner.append([dict_word['form'], i, dict_word['nerLabel']])
                except Exception as e:
                    print(e)

    for name_entity in ner:
        add_to_dict(name_entity[0], ner_dict)

def is_vietnamese(text, vowels):
    if "This review has been hidden" in text:
        text = text.split("This review has been hidden because it contains spoilers. To view it, click here.")[1]
    try:
        five_word = text.split(' ')[:20]
    except:
        five_word = text.split(' ')
    for word in five_word:
        for ch in word:
            if ch.lower() in vowels:
                return True 
    return False

def normalize(txt):
    txt = re.sub(r'[\.\n]', '. ', txt)
    txt = re.sub(r'[\-]', ' ', txt)
    txt = re.sub(r'[\(\)]', ' ', txt)   
    txt = re.sub(r'\s+', ' ', txt)
    return txt 
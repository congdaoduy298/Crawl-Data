from vncorenlp import VnCoreNLP
import json
from tqdm import tqdm 
import time 
import nltk 
import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
import json
import sys 
import re 

def add_to_dict(entity, ner_dict):
    entity = re.sub(r'\_', ' ', entity)
    if entity not in ner_dict:
        ner_dict[entity] = 1
    else:
        ner_dict[entity] += 1

def get_dict_ner(result, ner_dict):
    ner = []
    n_sentences = len(result)

    for i in range(n_sentences):
        for i, dict_word in enumerate(result[i]):
            if dict_word['nerLabel'] != 'O':
                try:
                    if dict_word['nerLabel'].split('-')[1] == 'MISC':
                        continue
                    if len(ner) > 0 and (ner[-1][1] == i-1) and next_cate[ner[-1][2]] == dict_word['nerLabel']:
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

if __name__ == "__main__":

    # 1. Connect to VnCoreNLP server
    annotator = VnCoreNLP(address="http://127.0.0.1", port=9000) 
    
    # 2. Load spacy 
    nlp = en_core_web_sm.load()

    # 3. Download all packages needed of nltk
    try:
        nltk.download('punkt')
        nltk.download('averaged_perceptron_tagger')
        nltk.download('maxent_ne_chunker')
        nltk.download('words')
    except Exception as e:
        print(e)
        pass

    with open('data.json', 'r') as f:
        data = json.load(f)

    count = 0
    vowels = ['á', 'ạ', 'à', 'ả', 'ã', 
              'ă', 'ắ', 'ặ', 'ằ', 'ẳ', 'ẵ',
              'â', 'ấ', 'ậ', 'ầ', 'ẩ', 'ẫ',
              'đ', 'é', 'ẹ', 'è', 'ẻ', 'ẽ',
              'ê', 'ế', 'ệ', 'ề', 'ể', 'ễ',
              'í', 'ị', 'ì', 'ỉ', 'ĩ',
              'ó', 'ọ', 'ò', 'ỏ', 'õ',
              'ô', 'ố', 'ộ', 'ồ', 'ổ', 'ỗ',
              'ơ', 'ớ', 'ợ', 'ờ', 'ở', 'ỡ',
              'ú', 'ụ', 'ù', 'ủ', 'ũ',
              'ý', 'ỵ', 'ỳ', 'ỷ', 'ỹ']
    CHOOSE_LIST = ['NORP', 'ORG', 'PERSON', 'LOC', 'GPE']
    next_cate = {'B-PER': 'I-PER', 'B-ORG': 'I-ORG', 'B-LOC': 'I-LOC', 'I-PER': 0, 'I-ORG': 0, 'I-LOC': 0, 'B-MISC': 'I-MISC'}
    ner_dict = {}
    ner = []
    try_save = ''
    start = time.time()
    i_book = 0
    for book in tqdm(data.values()):
        texts = []
        i_book += 1
        texts.append(book['Description']) 
        for review in book['Review'].values():
            texts.append(review['Content'])
            for comment in review['Comment']:
                texts.append(comment[2])

        # To perform word segmentation, POS tagging, NER and then dependency parsing
        for text in texts:
            if len(text)>0:
                is_vn = is_vietnamese(text, vowels)
                if is_vn:
                    text = normalize(text)
                #     # Vietnamese NER by using VnCoreNLP
                    annotated_text = annotator.annotate(text)   
                    result = annotated_text['sentences']
                    get_dict_ner(result, ner_dict)
                               
                if not is_vn:
                
                    # Compare two answers of nltk and spacy , count value if it's pretty same.
                    doc = nlp(text)
                    entities = []
                    for sent in nltk.sent_tokenize(text):
                        for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
                            if hasattr(chunk, 'label'):
                                entity = ' '.join(c[0] for c in chunk)
                                entities.append(entity)
                                # add_to_dict(entity, ner_dict)

                    for X in doc.ents:
                        if X.label_ in CHOOSE_LIST:
                            # add_to_dict(X.text, ner_dict)   
                            for entity in entities:
                                if X.text in entity:
                                    add_to_dict(entity, ner_dict)
                                    break 
                                elif entity in X.text:
                                    add_to_dict(entity, ner_dict)
                                    break     
                
                count += 1

    with open('name_entity.json', 'w', encoding='utf-8') as outfile:
        json.dump(ner_dict, outfile, indent=2, separators=(", ", ": "), ensure_ascii=False)
    

    print(time.time() - start)
    print(ner_dict)
    print(count)
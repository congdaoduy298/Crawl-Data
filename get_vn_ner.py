from vncorenlp import VnCoreNLP
from utils_ner import add_to_dict, get_dict_ner, is_vietnamese, normalize
from tqdm import tqdm 
import time 
import json

if __name__ == "__main__":

    # 1. Connect to VnCoreNLP server
    annotator = VnCoreNLP(address="http://127.0.0.1", port=9000) 

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
    NEXT_CATE = {'B-PER': 'I-PER', 'B-ORG': 'I-ORG', 'B-LOC': 'I-LOC', 'I-PER': 0, 'I-ORG': 0, 'I-LOC': 0, 'B-MISC': 'I-MISC'}
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
                    get_dict_ner(result, ner_dict, NEXT_CATE)
                               
                count += 1

    with open('VN_name_entity.json', 'w', encoding='utf-8') as outfile:
        json.dump(ner_dict, outfile, indent=2, separators=(", ", ": "), ensure_ascii=False)
    

    print(time.time() - start)
    print(ner_dict)
    print(count)
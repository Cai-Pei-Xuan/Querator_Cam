# -*- coding: utf-8 -*-
from ckiptagger import data_utils, construct_dictionary, WS, POS, NER
import os

# ckip應用來源:https://github.com/p208p2002/interface-for-ckiptagger
class ckip_tagger():
    def __init__(self,ckip_data_path = './data', custom_dict_path='./dict'):
        # Load model
        self.ws = WS(ckip_data_path)
        self.pos = POS(ckip_data_path)
        self.ner = NER(ckip_data_path)
        self.dictionary = construct_dictionary(self.__load_custom_dict(custom_dict_path))
        
    def __load_custom_dict(self,custom_dict_path):
        # load all file under path
        dicts = os.listdir(custom_dict_path)
        word_to_weight = {}
        for dic in dicts:
            with open(custom_dict_path + '/' + dic, 'r', encoding='utf-8') as f:
                while(True):
                    line = f.readline()
                    if(len(line)==0):
                        break
                    line_split = line.split()
                    word = line_split[0]
                    try:
                        word_weight = line_split[1]
                    except:
                        word_weight = 1
                    word_to_weight.update({word:word_weight})
        return word_to_weight

    def __get_word_pos_sentence(self,word_sentence, pos_sentence):
        # Show results
        assert len(word_sentence) == len(pos_sentence)
        res = []
        for word, pos in zip(word_sentence, pos_sentence):
            res.append((word,pos)) #(斷詞,詞性)
        return res
    
    def parse(self,sentence_list):
        word_sentence_list = self.ws(sentence_list,recommend_dictionary = self.dictionary)
        pos_sentence_list = self.pos(word_sentence_list)
        entity_sentence_list = self.ner(word_sentence_list, pos_sentence_list)
        res = []
        for i, sentence in enumerate(sentence_list):
            res.append(self.__get_word_pos_sentence(word_sentence_list[i],  pos_sentence_list[i]))
        return res

    def _get_entity(self,sentence_list):
        word_sentence_list = self.ws(sentence_list,recommend_dictionary = self.dictionary)
        pos_sentence_list = self.pos(word_sentence_list)
        entity_sentence_list = self.ner(word_sentence_list, pos_sentence_list)
        return entity_sentence_list[0]

            
if __name__ == "__main__":
    ckip = ckip_tagger()
    sentence = input("輸入句子:\n")
    result = ckip._get_entity([sentence])
    print(ckip._get_entity([sentence]))
    need_list = ["'PERSON'"]
    entity_list = []
    for i in result:
        name_list = str(i).split(', ')
        if name_list[2] in need_list:
            entity = name_list[3].replace('\'',"").replace(')',"")
            if entity not in entity_list:
                entity_list.append(entity)

    for i in entity_list:
        print(i)

    index = 0
    while True:
        index = sentence.find('韓國瑜', index)
        print(index)
        if index == -1: break
        index +=1
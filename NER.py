import random
import requests
import json
import spacy
import ckip
import time

class testNER():
    def __init__(self):
        self.ckip_test = ckip.ckip_tagger()          # 載入中文NER模組
        self.nlp = spacy.load("en_core_web_sm")      # 載入英文NER模組
        self.remove_word_list = self.load_remove_word()

    # 載入要排除的字
    def load_remove_word(self):
        with open('./remove_word.txt','r') as fp:
            all_lines = fp.readlines()
        for i in range(len(all_lines)):
            all_lines[i] = all_lines[i].replace('\n',"")
        return all_lines

    # 獲得使用NER當作答案的問題
    def get_NER_question(self, context, language):   
        # t1 = time.time()
        # Entity Types:https://github.com/ckiplab/ckiptagger/wiki/Entity-Types
        # Entity Types:https://spacy.io/api/annotation#named-entities
        need_1_list = ["PERSON", "GPE", "DATE", "ORG"]  # 第一優先(人物，行政區，日期，組織)
        need_2_list = ["CARDINAL", "NORP", "LOC", "TIME"]  # 第二優先(數字，民族、宗教、政治團體，地理區，時間)
        need_3_list = ["FAC", "MONEY", "EVENT", "WORK_OF_ART"]  # 第三優先(設施，金錢，事件，作品)
        need_4_list = ["QUANTITY", "PERCENT", "LANGUAGE", "PRODUCT", "LAW"]  # 第四優先(數量，百分比率，語言，產品，法律)

        all_entity_list = []
        entity_1_list = []
        entity_2_list = []
        entity_3_list = []
        entity_4_list = []
        all_entity_loc_list = []
        entity_loc_1_list = []
        entity_loc_2_list = []
        entity_loc_3_list = []
        entity_loc_4_list = []

        if language == "cht":
            # ckip標記NER
            result = self.ckip_test._get_entity([context])
            for i in result:
                name_list = str(i).split(', ')
                ent_label = name_list[2].replace('\'',"")
                entity = name_list[3].replace('\'',"").replace(')',"")
                ent_loc = name_list[0].replace('(',"")
                if ent_label in need_1_list:
                    if entity not in entity_1_list:
                        entity_1_list.append(entity)
                        entity_loc_1_list.append(ent_loc)
                elif ent_label in need_2_list:
                    if entity not in entity_2_list:
                        entity_2_list.append(entity)
                        entity_loc_2_list.append(ent_loc)
                elif ent_label in need_3_list:
                    if entity not in entity_3_list:
                        entity_3_list.append(entity)
                        entity_loc_3_list.append(ent_loc)
                elif ent_label in need_4_list:
                    if entity not in entity_4_list:
                        entity_4_list.append(entity)
                        entity_loc_4_list.append(ent_loc)
        elif language == "eng":
            # 使用範例來源:https://spacy.io/usage/linguistic-features#named-entities
            # spacy標記NER
            result = self.nlp(context)
            for ent in result.ents:
                ent_label = ent.label_
                entity = ent.text
                ent_loc = ent.start_char
                if ent_label in need_1_list:
                    if entity not in entity_1_list:
                        entity_1_list.append(entity)
                        entity_loc_1_list.append(ent_loc)
                elif ent_label in need_2_list:
                    if entity not in entity_2_list:
                        entity_2_list.append(entity)
                        entity_loc_2_list.append(ent_loc)
                elif ent_label in need_3_list:
                    if entity not in entity_3_list:
                        entity_3_list.append(entity)
                        entity_loc_3_list.append(ent_loc)
                elif ent_label in need_4_list:
                    if entity not in entity_4_list:
                        entity_4_list.append(entity)
                        entity_loc_4_list.append(ent_loc)
        
        # 同时将两个list按照相同的顺序打乱:https://blog.csdn.net/yideqianfenzhiyi/article/details/79197570
        if len(entity_1_list) != 0:
            cc1 = list(zip(entity_1_list, entity_loc_1_list))
            entity_1_list.clear()
            entity_loc_1_list.clear()
            random.shuffle(cc1)
            entity_1_list[:], entity_loc_1_list[:] = zip(*cc1)
            cc1.clear()
        if len(entity_2_list) != 0:
            cc2 = list(zip(entity_2_list, entity_loc_2_list))
            entity_2_list.clear()
            entity_loc_2_list.clear()
            random.shuffle(cc2)
            entity_2_list[:], entity_loc_2_list[:] = zip(*cc2)
            cc2.clear()
        if len(entity_3_list) != 0:
            cc3 = list(zip(entity_3_list, entity_loc_3_list))
            entity_3_list.clear()
            entity_loc_3_list.clear()
            random.shuffle(cc3)
            entity_3_list[:], entity_loc_3_list[:] = zip(*cc3)
            cc3.clear()
        if len(entity_4_list) != 0:
            cc4 = list(zip(entity_4_list, entity_loc_4_list))
            entity_4_list.clear()
            entity_loc_4_list.clear()
            random.shuffle(cc4)
            entity_4_list[:], entity_loc_4_list[:] = zip(*cc4)
            cc4.clear()

        all_entity_list.append(entity_1_list)
        all_entity_list.append(entity_2_list)
        all_entity_list.append(entity_3_list)
        all_entity_list.append(entity_4_list)
        all_entity_loc_list.append(entity_loc_1_list)
        all_entity_loc_list.append(entity_loc_2_list)
        all_entity_loc_list.append(entity_loc_3_list)
        all_entity_loc_list.append(entity_loc_4_list)

        # t2 = time.time()
        # print('time elapsed: ' + str(round(t2-t1, 2)) + ' seconds')
        
        headers = {
        'Content-Type': 'application/raw'
        }

        All_result = {}
        result = []
        limit = 7   # 限制7個問題
        question_num = 0

        use_word_list = [] # 避免同一個詞有多個實體，所以紀錄使用過的詞
        for i in range(len(all_entity_list)):
            for j in range(len(all_entity_list[i])):
                if all_entity_list[i][j] in use_word_list:
                    continue
                if all_entity_list[i][j] in self.remove_word_list:
                    continue
                if len(all_entity_list[i][j]) == 1:
                    continue
                if question_num < limit:
                    index = int(all_entity_loc_list[i][j])
                    data = {}
                    answers = {}
                    a = []
                    answer = {}
                    if len(context) <= 467:
                        data["article"] = context
                        answer["start_at"] = index
                    elif (index+1) <= 233:
                        data["article"] = context[:467]
                        answer["start_at"] = index
                    elif (len(context) - (index+1)) >= 233:
                        data["article"] = context[(index-234):(index+233)]
                        answer["start_at"] = 234
                    else:
                        data["article"] = context[index - (467 - (len(context) - index)):]
                        answer["start_at"] = 467 - (len(context) - index)

                    answer["tag"] = all_entity_list[i][j]
                    answer["end_at"] = answer["start_at"]+len(all_entity_list[i][j])-1
                    a.append(answer)
                    answers["ans_detail"] = a
                    data["answers"] = answers

                    data = json.dumps(data)
                    # print(data.encode('utf-8').decode('utf-8'))
                    response = {}
                    if language == "cht":
                        response = requests.post('http://XXXXX', data, headers)
                    elif language == "eng":
                        response = requests.post('http://XXXXX', data, headers)
                    response_dic = response.json()
                    response_dic["question_detail"][0]["tag_padding"] = index - answer["start_at"]
                    result.append(response_dic)

                    question_num += 1
                    use_word_list.append(all_entity_list[i][j])
                else:
                    break

                
        All_result["result"] = result
        return All_result

    # 獲得使用NER當作答案的問題
    def get_CloudNaturalLanguage_NER_question(self, context, language): 
        t1 = time.time()
        # Entity Types:https://cloud.google.com/natural-language/docs/reference/rest/v1/Entity
        need_1_list = ["PERSON", "DATE", "ORGANIZATION"]  # 第一優先(人物，日期，組織)
        need_2_list = ["LOCATION", "ADDRESS"]  # 第二優先(位置，地址)
        need_3_list = ["PRICE", "EVENT", "WORK_OF_ART"]  # 第三優先(價錢，事件，藝術品)
        need_4_list = ["CONSUMER_GOOD", "OTHER", "UNKNOWN", "PHONE_NUMBER", "NUMBER"]  # 第四優先(消費品，其他，未知，電話號碼，數字)

        all_entity_list = []
        entity_1_list = []
        entity_2_list = []
        entity_3_list = []
        entity_4_list = []
        all_entity_loc_list = []
        entity_loc_1_list = []
        entity_loc_2_list = []
        entity_loc_3_list = []
        entity_loc_4_list = []

        headers = {
            'Content-Type': 'application/raw'
        }

        data = {
            'document': {
                'type': 'PLAIN_TEXT',
                'content': context
            },
            'encodingType': 'UTF32'
        }
        data = json.dumps(data)
        response = requests.post('https://language.googleapis.com/v1/documents:analyzeEntities?key=XXXXXX', data, headers)          # key要去申請
        response_dic = response.json()
        
        for entities in response_dic["entities"]:
            ent_label = entities["type"]
            for mentions in entities["mentions"]:
                entity = mentions["text"]["content"]
                ent_loc = mentions["text"]["beginOffset"]
                if ent_label in need_1_list:
                    if entity not in entity_1_list:
                        entity_1_list.append(entity)
                        entity_loc_1_list.append(ent_loc)
                elif ent_label in need_2_list:
                    if entity not in entity_2_list:
                        entity_2_list.append(entity)
                        entity_loc_2_list.append(ent_loc)
                elif ent_label in need_3_list:
                    if entity not in entity_3_list:
                        entity_3_list.append(entity)
                        entity_loc_3_list.append(ent_loc)
                elif ent_label in need_4_list:
                    if entity not in entity_4_list:
                        entity_4_list.append(entity)
                        entity_loc_4_list.append(ent_loc)

        # 同时将两个list按照相同的顺序打乱:https://blog.csdn.net/yideqianfenzhiyi/article/details/79197570
        if len(entity_1_list) != 0:
            cc1 = list(zip(entity_1_list, entity_loc_1_list))
            entity_1_list.clear()
            entity_loc_1_list.clear()
            random.shuffle(cc1)
            entity_1_list[:], entity_loc_1_list[:] = zip(*cc1)
            cc1.clear()
        if len(entity_2_list) != 0:
            cc2 = list(zip(entity_2_list, entity_loc_2_list))
            entity_2_list.clear()
            entity_loc_2_list.clear()
            random.shuffle(cc2)
            entity_2_list[:], entity_loc_2_list[:] = zip(*cc2)
            cc2.clear()
        if len(entity_3_list) != 0:
            cc3 = list(zip(entity_3_list, entity_loc_3_list))
            entity_3_list.clear()
            entity_loc_3_list.clear()
            random.shuffle(cc3)
            entity_3_list[:], entity_loc_3_list[:] = zip(*cc3)
            cc3.clear()
        if len(entity_4_list) != 0:
            cc4 = list(zip(entity_4_list, entity_loc_4_list))
            entity_4_list.clear()
            entity_loc_4_list.clear()
            random.shuffle(cc4)
            entity_4_list[:], entity_loc_4_list[:] = zip(*cc4)
            cc4.clear()

        all_entity_list.append(entity_1_list)
        all_entity_list.append(entity_2_list)
        all_entity_list.append(entity_3_list)
        all_entity_list.append(entity_4_list)
        all_entity_loc_list.append(entity_loc_1_list)
        all_entity_loc_list.append(entity_loc_2_list)
        all_entity_loc_list.append(entity_loc_3_list)
        all_entity_loc_list.append(entity_loc_4_list)

        t2 = time.time()
        print('time elapsed: ' + str(round(t2-t1, 2)) + ' seconds')

        All_result = {}
        result = []
        limit = 7   # 限制7個問題
        question_num = 0

        use_word_list = [] # 避免同一個詞有多個實體，所以紀錄使用過的詞
        for i in range(len(all_entity_list)):
            for j in range(len(all_entity_list[i])):
                if all_entity_list[i][j] in use_word_list:
                    continue
                if all_entity_list[i][j] in self.remove_word_list:
                    continue
                if len(all_entity_list[i][j]) == 1:
                    continue
                if question_num < limit:
                    index = int(all_entity_loc_list[i][j])
                    data = {}
                    answers = {}
                    a = []
                    answer = {}
                    if len(context) <= 467:
                        data["article"] = context
                        answer["start_at"] = index
                    elif (index+1) <= 233:
                        data["article"] = context[:467]
                        answer["start_at"] = index
                    elif (len(context) - (index+1)) >= 233:
                        data["article"] = context[(index-234):(index+233)]
                        answer["start_at"] = 234
                    else:
                        data["article"] = context[index - (467 - (len(context) - index)):]
                        answer["start_at"] = 467 - (len(context) - index)

                    answer["tag"] = all_entity_list[i][j]
                    answer["end_at"] = answer["start_at"]+len(all_entity_list[i][j])-1
                    a.append(answer)
                    answers["ans_detail"] = a
                    data["answers"] = answers

                    data = json.dumps(data)
                    # print(data.encode('utf-8').decode('utf-8'))
                    response = {}
                    if language == "cht":
                        response = requests.post('http://XXXXX', data, headers)
                    elif language == "eng":
                        response = requests.post('http://XXXXX', data, headers)
                    response_dic = response.json()
                    response_dic["question_detail"][0]["tag_padding"] = index - answer["start_at"]
                    result.append(response_dic)

                    question_num += 1
                    use_word_list.append(all_entity_list[i][j])
                else:
                    break

                
        All_result["result"] = result
        return All_result
# -*- coding: utf-8 -*-
import OCR
import NER
from flask import Flask, request
import os
import json

# os.environ["CUDA_VISIBLE_DEVICES"] = "1"
OCR_test = OCR.testOCR()                # 載入OCR模組
NER_test = NER.testNER()                # 載入NER模組

# Flask應用來源:https://www.cnblogs.com/lsdb/p/10488448.html
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# route()方法用于设定路由；类似spring路由配置
#等价于在方法后写：app.add_url_rule('/', 'helloworld', hello_world)
@app.route('/')
def hello_world():
    return 'Hello, World!'

# Python flask.request raw應用來源:http://codingdict.com/sources/py/flask.request/4366.html

@app.route('/cht/up_photo', methods=['post'])
def up_photo_cht():
    a = request.get_data()
    dict1 = json.loads(a)
    base64_data = dict1["photo"]
    OCR_context = {}

    try:
        provider = dict1["provider"]
        if provider == "1":
            OCR_context = OCR_test.chtRecognition(base64_data)
        else:
            OCR_context = OCR_test.CloudVisionRecognition(base64_data)
    except:
        print("沒有指定提供者")
        OCR_context = OCR_test.CloudVisionRecognition(base64_data)

    # print(OCR_context)
    return OCR_context

@app.route('/eng/up_photo', methods=['post'])
def up_photo_eng():
    a = request.get_data()
    dict1 = json.loads(a)
    base64_data = dict1["photo"]
    OCR_context = {}

    try:
        provider = dict1["provider"]
        if provider == "1":
            OCR_context = OCR_test.engRecognition(base64_data)
        else:
            OCR_context = OCR_test.CloudVisionRecognition(base64_data)
    except:
        print("沒有指定提供者")
        OCR_context = OCR_test.CloudVisionRecognition(base64_data)

    # print(OCR_context)
    return OCR_context

# python post raw來源:http://www.voidcn.com/article/p-pkuwnmmg-bor.html
@app.route('/cht/up_context', methods=['post'])
def up_context_cht():
    a = request.get_data()
    dict1 = json.loads(a)
    context = dict1["context"]
    All_result = {}

    try:
        provider = dict1["provider"]
        if provider == "1":
            All_result = NER_test.get_NER_question(context, "cht")
        else:
            All_result = NER_test.get_CloudNaturalLanguage_NER_question(context, "cht")

    except:
        print("沒有指定提供者")
        All_result = NER_test.get_NER_question(context, "cht")

    return json.dumps(All_result,ensure_ascii=False)

# python post raw來源:http://www.voidcn.com/article/p-pkuwnmmg-bor.html
@app.route('/eng/up_context', methods=['post'])
def up_context_eng():
    a = request.get_data()
    dict1 = json.loads(a)
    context = dict1["context"]
    All_result = {}

    try:
        provider = dict1["provider"]
        if provider == "1":
            All_result = NER_test.get_NER_question(context, "eng")
        else:
            All_result = NER_test.get_CloudNaturalLanguage_NER_question(context, "eng")
    except:
        print("沒有指定提供者")
        All_result = NER_test.get_NER_question(context, "eng")
    
    return json.dumps(All_result,ensure_ascii=False)

if __name__ == '__main__':
    # app.run(host, port, debug, options)
    # 默认值：host=127.0.0.1, port=5000, debug=False

    app.run(host='0.0.0.0',port='4003', debug=False)
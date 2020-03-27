# -*- coding: utf-8 -*-
# import pytesseract
# from PIL import Image as ImagePIL
# from PIL import ImageEnhance
import requests
import json
import base64
import re
from io import BytesIO

# 圖片轉成 Base64 編碼字串，降低連線請求來源:https://sofree.cc/base64-images/
# 線上圖片轉base64來源:https://www.base64-image.de/ OR https://www.askapache.com/online-tools/base64-image-converter/
# 关于Base64String与图片互转中图片无法正常显示的问题來源:https://blog.csdn.net/qq_23974323/article/details/85288013

class testOCR():
    def __init__(self):
        pass


    # # python提供的OCR
    # # Python驗證碼識別 安裝Pillow、tesseract-ocr與pytesseract模組的安裝以及錯誤解決:https://codertw.com/%E7%A8%8B%E5%BC%8F%E8%AA%9E%E8%A8%80/477312/#outline__2_2
    # # pytesseract安裝來源:https://pypi.org/project/pytesseract/
    # def textRecognition(self, img):
    #     resize_num = 2
    #     b = 2.0
    #     # PIL.Image与Base64 String的互相转换:https://www.jianshu.com/p/2ff8e6f98257
    #     # 解析圖片前處理
    #     base64_data = re.sub('^data:image/.+;base64,', '', img)
    #     # 解析圖片
    #     byte_data = base64.b64decode(base64_data)
    #     image_data = BytesIO(byte_data)
    #     img = ImagePIL.open(image_data)
    #     # 影象放大
    #     img = img.resize((img.width * int(resize_num), img.height * int(resize_num)))
    #     # 影象二值化
    #     imgry = img.convert('L')
    #     # 對比度增強
    #     sharpness = ImageEnhance.Contrast(imgry)
    #     sharp_img = sharpness.enhance(b)
    #     # 使用tesseract庫,進行文字識別
    #     result = {}

    #     try:
    #         print('1')
    #         Rotate = pytesseract.image_to_osd(sharp_img)
    #         Rotate = Rotate[(Rotate.index("Rotate: ")+len("Rotate: ")):Rotate.index("Orientation confidence: ")]
    #         rotated = int(Rotate)
    #         if rotated != 0:
    #             sharp_img = sharp_img.rotate(rotated)
    #         score = pytesseract.image_to_string(sharp_img, lang="chi_tra+eng", config="--psm 6")
    #         print('2')
    #         score = score.replace(" ","").replace("\n","")
    #         result["result"] = "1"      # 代表識別成功
    #         result["context"] = score   # 辨識出來的文章
    #     except Exception as e:
    #         print(e)
    #         print('識別失敗')
    #         result["result"] = "0"      # 代表識別失敗
    #         result["context"] = "error"

    #     return result
    
    
    # OCR api來源:https://ocr.space/
    # 使用方法來源:https://github.com/Zaargh/ocr.space_code_example/blob/master/ocrspace_example.py
    # 中文OCR
    def chtRecognition(self, base64_data):
        payload = {
            'base64Image': base64_data,
            'apikey': 'XXXXXX',             # apikey要去申請
            'language': 'cht',
            'detectOrientation': True,
            'OCREngine': '1'
            }
        response = requests.post('https://api.ocr.space/parse/image', payload)
        response_dic = response.json()

        result = {}
        ParsedText = ""
        if response_dic["IsErroredOnProcessing"]:
            result["result"] = "0"      # 代表識別失敗
            result["context"] = response_dic["ErrorMessage"][0]   # 錯誤訊息
        else:
            for i in response_dic["ParsedResults"]:
                ParsedText += i["ParsedText"]

            # ParsedText = ParsedText.replace(" ","").replace("\n","")

            result["result"] = "1"      # 代表識別成功
            result["context"] = ParsedText   # 辨識出來的文章

        return result

    
    # OCR api來源:https://ocr.space/
    # 使用方法來源:https://github.com/Zaargh/ocr.space_code_example/blob/master/ocrspace_example.py
    # 英文OCR
    def engRecognition(self, base64_data):
        payload = {
            'base64Image': base64_data,
            'apikey': 'XXXXXX',             # apikey要去申請
            'language': 'eng',
            'detectOrientation': True,
            'OCREngine': '1'
            }
        response = requests.post('https://api.ocr.space/parse/image', payload)
        response_dic = response.json()

        result = {}
        ParsedText = ""
        if response_dic["IsErroredOnProcessing"]:
            result["result"] = "0"      # 代表識別失敗
            result["context"] = response_dic["ErrorMessage"][0]   # 錯誤訊息
        else:
            for i in response_dic["ParsedResults"]:
                ParsedText += i["ParsedText"]

            result["result"] = "1"      # 代表識別成功
            result["context"] = ParsedText   # 辨識出來的文章

        return result

    # google的OCR，使用方法:https://cloud.google.com/vision/docs/ocr?hl=zh-CN
    def CloudVisionRecognition(self, base64_data):
        # 解析圖片前處理，code來源:https://www.jianshu.com/p/2ff8e6f98257
        base64_data = re.sub('^data:image/.+;base64,', '', base64_data)

        headers = {
            'Content-Type': 'application/raw'
        }

        data = {
            'requests': [
                {
                'image': {
                    'content': base64_data
                },
                'features': [
                    {
                    'type': 'DOCUMENT_TEXT_DETECTION'
                    }
                ]
                }
            ]
        }
        data = json.dumps(data)
        response = requests.post('https://vision.googleapis.com/v1/images:annotate?key=XXXXXX', data, headers)          # key要去申請
        response_dic = response.json()

        result = {}
        ParsedText = ""

        try:
            result["result"] = "1"      # 代表識別成功
            result["context"] = response_dic["responses"][0]["fullTextAnnotation"]["text"]
        except Exception as e:
            print(e)
            print('識別失敗')
            result["result"] = "0"      # 代表識別失敗
            result["context"] = "error"

        return result
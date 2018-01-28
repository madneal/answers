from datetime import datetime
from elasticsearch import Elasticsearch
from os import listdir
import config
import ocr
from PIL import Image


def initial():
    return Elasticsearch({'localhost'})


def get_questions():
    questions = []
    with open('questions.txt', encoding='utf8') as f:
        lines = f.readlines()
    for line in lines:
        arr = line.split(' ')
        question = {
            'question': arr[0].strip(),
            'answer': arr[1].strip()
        }
        questions.append(question)
    return questions


def write_questions_to_index():
    questions = get_questions()
    es = initial()
    for id, question in enumerate(questions):
        es.index(index='question-index', doc_type='question', id=id, body=question)


def get_question_from_img():
    files = listdir('img')
    config_ = config.load_config()
    for file in files:
        image_path = 'img/' + file
        img = Image.open(image_path)
        img.show()
        question, choices = ocr.ocr_img_baidu(img, config_)
        print(question)
        print(choices)


def search_question(question):
    es = initial()
    res = es.search(index='question-index', body={
        "query": {
            "match": {
                "question": {
                    "query": question,
                    "minimum_should_match": "75%"
                }
            }
        }
    })
    if res['hits']['total'] > 0:
        for hit in res['hits']['hits']:
            print(hit['_source']['question'] + ':' + hit['_source']['answer'])
    else:
       print('未搜索到类似结果')


if __name__ == '__main__':
    get_question_from_img()
    # write_questions_to_index()
    # result = search_question('不鸣则已的下一句')
    # for e in result:
    #     print(e['_source'])
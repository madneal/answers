from datetime import datetime
from elasticsearch import Elasticsearch
import config
import ocr
from PIL import Image
from os import listdir
from os import remove

def initial():
    return Elasticsearch({'localhost'})


def get_questions(config_):
    questions_from_img = get_questions_from_img(config_)
    question_file = open('questions.txt', 'a', encoding='utf8')
    for question in questions_from_img:
        question_file.write('\r\n' + question['question'] + ' ' + question['choice'])
    question_file.close()
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


def get_questions_from_img(config_):
    img_path = 'img'
    img_list = listdir(img_path)
    questions = []
    for img_file in img_list:
        img_file_path = img_path + '/' + img_file
        img = Image.open(img_file_path)
        questions.append({
            'question': ocr.get_text(config_, 'question_region', img),
            'choice': ocr.ocr_right_choice(img, config_)
        })
        remove(img_file_path)
    return questions


def write_questions_to_index(config_):
    questions = get_questions(config_)
    es = initial()
    for id, question in enumerate(questions):
        es.index(index='question-index', doc_type='question', id=id, body=question)


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
    config_ = config.load_config()
    write_questions_to_index(config_)


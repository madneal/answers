import requests
import webbrowser
import urllib.parse
import re
from bs4 import BeautifulSoup
import time
from create_question_bank import initial
# # 颜色兼容Win 10
from colorama import init,Fore
init()

def open_webbrowser(question):
    webbrowser.open('https://www.google.com/search?q=' + urllib.parse.quote(question))


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


def output(counts, is_opsite):
    max_key = max(counts.keys())
    min_key = min(counts.keys())
    if max_key == min_key:
        print(Fore.RED + "高低计数相等此方法失效！" + Fore.RESET)
        return

    for key in counts:
        choice = counts[key]
        print()
        if is_opsite:
            compare_key = min_key
        else:
            compare_key = max_key
        if key == compare_key:
            print(Fore.RED + '{0} : {1}'.format(choice, key) + Fore.RESET)
        else:
            print("{0} : {1}".format(choice, key))


def run_algorithm(al_num, question):
    if al_num == 0:
        open_webbrowser(question)
    elif al_num == 1:
        search_question(question)


if __name__ == '__main__':
    question = '新装修的房子通常哪种化学物质含量会比较高'
    choices = ['甲醛', '苯', '甲醇']
    run_algorithm(1, question, choices)


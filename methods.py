import requests
import webbrowser
import urllib.parse
import re
from bs4 import BeautifulSoup
import time

# # 颜色兼容Win 10
from colorama import init,Fore
init()

def open_webbrowser(question):
    webbrowser.open('https://www.google.com/search?q=' + urllib.parse.quote(question))


def open_webbrowser_count(question,choices):
    print('\n-- 方法2： 题目+选项搜索结果计数法 --\n')
    print('Question: ' + question)
    is_opsite= False
    if '不是' in question:
        print('**请注意此题为否定题,选计数最少的**')
        is_opsite = True

    counts = {}
    for i in range(len(choices)):
        # 请求
        req = requests.get(url='https://www.google.com/search?q=' + question + choices[i])
        content = BeautifulSoup(req.content, 'html.parser')
        result = content.find(id='resultStats').text
        count = re.sub(r'\D', '', result)
        count = int(count.replace(',', ''))
        counts[count] = choices[i]
    output(counts, is_opsite)


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


def run_algorithm(al_num, question, choices):
    if al_num == 0:
        open_webbrowser(question)
    elif al_num == 1:
        open_webbrowser_count(question, choices)


if __name__ == '__main__':
    question = '新装修的房子通常哪种化学物质含量会比较高'
    choices = ['甲醛', '苯', '甲醇']
    run_algorithm(1, question, choices)


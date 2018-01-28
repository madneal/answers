from PIL import Image
import screenshot, ocr, methods
from threading import Thread
import time
import config
import re


def filter_symbol(str):
    return re.sub('[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）《》]+', '', str)

def run():
    while True:
        # 截图
        t = time.clock()
        screenshot.check_screenshot()
        img = Image.open("./screenshot.png")

        config_ = config.load_config()
        # question, choices = ocr.ocr_img_tess(img, config_)
        question, choices = ocr.get_question_and_choices(img, config_)
        question = filter_symbol(question)

        # 多线程
        m1 = Thread(methods.run_algorithm(0, question))
        m2 = Thread(methods.run_algorithm(1, question))
        m1.start()
        m2.start()

        end_time3 = time.clock()
        print('用时: {0}'.format(end_time3 - t))

        go = input('输入回车继续运行,输入 n 回车结束运行: ')
        if go == 'n':
            break
        print('------------------------')


if __name__ == '__main__':
    run()


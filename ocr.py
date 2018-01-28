from PIL import Image
import pytesseract
from aip import AipOcr
import io
import config


# 二值化算法
def binarizing(img, threshold):
    pixdata = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            if pixdata[x, y] < threshold:
                pixdata[x, y] = 0
            else:
                pixdata[x, y] = 255
    return img


def get_region(region_type, config_):
    return config_['region'][region_type]


def get_text(config_, region_type, image):
    region = config_['region'][region_type]
    img_im = get_processed_img(image, region, 190)
    return ''.join(ocr_img_baidu(img_im, config_))


def get_processed_img(image, region, binary_val):
    image = image.crop((region[0], region[1], region[2], region[3]))
    image_im = image.convert('L')
    image_im = binarizing(image_im, binary_val)
    return image_im


def ocr_img_tess(img, config_):
    tesseract_config = config_['tesseract']
    pytesseract.pytesseract.tesseract_cmd =tesseract_config['tesseract_cmd']

    # 语言包目录和参数
    tessdata_dir_config = tesseract_config['tessdata_dir_config']
    text_arr = pytesseract.image_to_string(img, lang='chi_sim', config=tessdata_dir_config)
    for text in text_arr:
        text = text.replace('_', '一')
        text = text.strip()
    return text_arr


def ocr_right_choice(image, config_):
    region = config_['region']
    choices_region = region['choices_region']
    img_all = get_processed_img(image, choices_region, 100)
    img_part = get_processed_img(image, choices_region, 175)
    all_choices = ocr_img_baidu(img_all, config_)
    part_choices = ocr_img_baidu(img_part, config_)
    if config_['is_debug']:
        img_all.show()
        img_part.show()
        print("所有选项是：")
        print(all_choices)
        print("部分选项是：")
        print(part_choices)
    right_choice = [choice for choice in all_choices if choice not in part_choices]
    return ''.join(right_choice)


def ocr_img(image, config):
    region = config['region']
    question_region = region['question_region']
    choices_region = region['choices_region']
    # 把图片变成二值图像
    question_im = get_processed_img(image, question_region, 190)
    choices_im = binarizing(image, choices_region, 120)
    if config_['is_debug']:
        choices_im.show()

    question = ocr_img_tess(question_im, config_)
    choices = ocr_img_tess(choices_im, config_)
    return question, choices


def ocr_img_baidu(image, config_):
    # 百度OCR API  ，在 https://cloud.baidu.com/product/ocr 上注册新建应用即可
    """ 你的 APPID AK SK """
    baidu_config = config_['baidu_ocr']
    APP_ID = str(baidu_config['app_id'])
    API_KEY = baidu_config['api_key']
    SECRET_KEY = baidu_config['secret_key']
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    image_data = img_byte_arr.getvalue()
    response = client.basicGeneral(image_data)
    words_result = response['words_result']

    texts = [x['words'] for x in words_result]
    return texts


def process_texts(texts):
    if len(texts) > 2:
        question = texts[0]
        choices = texts[1:]
        choices = [x.replace(' ', '') for x in choices]

    for choice_index, choice in choices:
        if choice.endswith('?'):
            question = question + choice
            choices.pop(0)
    return question, choices


if __name__ == '__main__':
    image = Image.open("img/screenshot.png")
    config_ = config.load_config()
    right_choice = ocr_right_choice(image, config_)
    print(right_choice)
    # time1 = time.time()
    # question, choices = ocr_img(image, config_)
    # print('ocr time is:' + str(time.time() - time1))
    # print("baidu 识别结果:")
    # print(question)
    # print(choices)
import speech_recognition as sr
import time

APP_ID = '10082951'
APP_KEY = 'qMuA8fTWTM4AwtdP4uGa0ZHqzGOj18LP'
SECRET_KEY = 'VjdnmhW6OuEdKUIegEwvqev5fHipAtQZ'

def get_file_content(filepath):
    with open(filepath, 'rb') as f:
        return f.read()

def get_question():
    # api_speech = AipSpeech(APP_ID, APP_KEY, SECRET_KEY)
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('say something')
        time2 = time.time()
        audio = r.listen(source)
        print('listen:' + str(time.time() - time2))
    # with open('result.wav', 'wb') as f:
    #     f.write(audio.get_raw_data())
    # print(api_speech.asr(audio.get_raw_data(), 'wav', 16000, {
    #     'lan': 'zh'
    # }))

    try:
        print('you said:' + r.recognize_sphinx(audio, language="zh-CN"))
    except Exception as e:
        print(e)


if __name__ == '__main__':
    time1 = time.time()
    get_question()
    print(time.time() - time1)

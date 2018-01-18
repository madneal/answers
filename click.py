import subprocess
import random
from time import sleep

def run():
    while True:
        height = str(random.randint(100, 800))
        width = str(random.randint(100, 500))
        command = 'adb shell input tap ' + width + ' ' + height
        subprocess.Popen(command, shell=True)

if __name__ == '__main__':
    run()
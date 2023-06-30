import os
import time
import re

def find_signal_from_text(txt):        
    # txt = "The rain in Spain"
    signal_percentage = re.search(r"\d+%", txt)
    return signal_percentage

def read_file(filename):
    with open(filename, 'r') as f:
        txt = f.read()
        return txt


def writeLog_file(string_to_write=''):
    f = open("wlan.csv", "a+")
    f.write(string_to_write)


def main():
    try:
        os.system('netsh wlan show interfaces >wlan.txt')
        filename='wlan.txt'
        signal_percentage= find_signal_from_text(read_file(filename))
        signal_percentage = int(signal_percentage)
        print('signal strength - ' + str(signal_percentage))

        if os.path.exists(filename):
            os.remove(filename)
            print('cleaned')
        else:
            print("The file does not exist")

        # ========== log ==================
        data = str(time.time()) + ',' + str(signal_percentage) + '\n'
        print(data)
        writeLog_file(data)

    except:
        print('wifi not available')


if __name__ == '__main__':
    while True:
        time.sleep(3)
        main()

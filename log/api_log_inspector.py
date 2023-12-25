import json
import os
from datetime import datetime
import sys

"""
api log파일을 텍스트모드로 분석합니다.
"""

# 로그파일에 있는 key들을 여기에 넣어서 내용을 찾도록 합니다.
searchKeys = ['uri', 'response', 'statusCode']


# 로그의 구조체를 선언합니다.
class Log:
    def __init__(self, data):
        info = data.split("- access-log: ")
        self.createTime = datetime.strptime(info[0], '%Y-%m-%d %H:%M:%S.%f')
        info = json.loads(info[1])
        self.request = info["request"]
        self.response = info["response"]
        self.user = info["user"]

    def __str__(self):
        return "createTime :: " + str(self.createTime) + "\n" + "request :: " + str(
            self.request) + "\n" + "response :: " + str(self.response) + "\n" + "user :: " + str(self.user)


def load(filename):
    lines = []
    starPoint = 1
    with open(filename, "r", encoding="utf-8") as f:
        while True:
            loadingText = "Loading{}".format("." * starPoint)
            sys.stdout.write("\r" + loadingText)

            line = f.readline()
            if not line:
                break
            log = Log(line)
            lines.append(log)

            if starPoint > 10:
                starPoint = 0
            starPoint += 1
            sys.stdout.flush()

    print(" " * len(loadingText), end="\r")
    return lines


def process(data):
    while True:
        for idx in range(len(searchKeys)):
            print(str(idx + 1) + '.' + searchKeys[idx], end=', ')
        print(str(len(searchKeys) + 1) + '.exit', end=' ')
        try:
            selection = int(input(":: what do you next? ::"))
        except ValueError:
            continue
        finally:
            os.system('cls' if os.name == 'nt' else 'clear')

        if selection < 1 or len(searchKeys) + 1 < selection:
            continue
        elif selection == len(searchKeys) + 1:
            print("\033[42m ****** bye! ****** \033[0m")
            break
        else:
            selection -= 1
            keyword = input("what is the keyword?")
            findIndex = []
            for i in range(len(data)):
                if searchKeys[selection] in data[i].request and keyword in str(
                        data[i].request[searchKeys[selection]]) or \
                        searchKeys[selection] in data[i].response and keyword in str(data[i].response[
                                                                                         searchKeys[selection]]) or \
                        data[i].user is not None and searchKeys[selection] in data[i].user and keyword in str(
                    data[i].user[
                        searchKeys[selection]]):
                    findIndex.append(i)

        if len(findIndex) > 0:
            print("\033[42m ****** found! ****** \033[0m")
            count = 0
            for idx in findIndex:
                count += 1
                print(str(count))
                print(data[idx].__str__())
                print("\033[42m ******************** \033[0m")


if __name__ == "__main__":
    try:
        lines = load(input("input file name: "))
        print(":: load is finished ::")
        process(lines)
    except FileNotFoundError:
        print("\033[42m no such file \033[0m")


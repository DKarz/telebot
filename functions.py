def paraNow():
    import time
    timeNow = time.ctime().split()[3].split(":")[:2]
    timeNow[0] = int(timeNow[0])
    timeNow[1] = int(timeNow[1])

    tN = timeNow[0] * 60 + timeNow[1]

    def calctime(list):
        x = list[0] * 60 + list[1]
        y = list[2] * 60 + list[3]
        if x <= tN < y:
            return True
        return False

    timeSeg = [[9, 0, 10, 20, True],
               [10, 20, 10, 30, False],
               [10, 30, 11, 50, True],
               [11, 50, 12, 10, False],
               [12, 10, 13, 30, True],
               [13, 30, 13, 40, False],
               [13, 40, 15, 00, True],
               [15, 00, 15, 10, False],
               [15, 10, 16, 30, True],
               [16, 30, 16, 40, False],
               [16, 40, 18, 00, True],
               [18, 00, 18, 10, False],
               [18, 10, 19, 30, True],
               [19, 30, 19, 40, False],
               [19, 40, 21, 00, True],
               ]
    counter = -1
    output = ""
    for seg in timeSeg:
        counter += 1
        if calctime(seg):
            if seg[4]:
                f = ""
                s = ""
                if (counter == 0 or counter == 7 or counter == 11): f = "0"
                if counter == 6 or counter == 10 or counter == 14: s = "0"
                output = "{}:{}-{}:{} {}-я пара".format(str(seg[0]), str(seg[1]) + f, str(seg[2]), str(seg[3]) + s,
                                                        str(int(counter / 2 + 1)))
                break
            else:
                output = "Перемена между {}-й и {}-й парой".format(str(int(counter / 2 + 1)), str(int(counter / 2 + 2)))
                break
    return output


def refreshMemesLinks():
    import requests
    from bs4 import BeautifulSoup
    obj = []
    temp = []
    out = []
    while len(obj) == 0:
        base_url = "https://www.reddit.com/r/dankmemes/"
        r = requests.get(base_url)
        soap = BeautifulSoup(r.content, features="html.parser")
        obj = soap.select("img.ImageBox-image.media-element")
    for el in obj:
        t = str(el).split()
        for x in t:
            temp.append(x)
    obj = temp
    for el in obj:
        if len(el) > 2 and str(el[0]) + str(el[1]) + str(el[2]) == "src":
            el = el[5:-1]
            out.append(el)
    file = open("materials/working/memes.txt", "w")
    for el in out:
        x = str(el)
        x = x.replace("amp;", "")
        file.write(x)
        file.write("\n")
    file.close()
    # print(obj, sep="\n")
    # print("")
    # print(out)

    file.close()


def wolf_token():
    counter = 0
    lines = []
    move_forward = True
    wolf_tok = ""
    fileR = open("materials/working/waW.txt", "r")
    for line in fileR:
        lineList = line.split()
        if int(lineList[1]) < 1950 and move_forward == True:
            lineList[1] = str(int(lineList[1]) + 1)
            move_forward = False
            wolf_tok = str(lineList[0])
        newLine = lineList[0] + " " + str(lineList[1]) + "\n"
        lines.append(newLine)
    fileR.close()
    fileW = open("materials/working/waW.txt", "w")
    for line in lines:
        fileW.write(line)
    fileW.close()
    if move_forward != True:
        return wolf_tok


import wolframalpha


def smart_mode(msg):
    wolfToken = wolf_token().strip()
    client = wolframalpha.Client(wolfToken)
    query = str(msg)
    res = client.query(query)
    output = next(res.results).text
    pics_dic = res["pod"]
    titles_list = []
    output_pics_urls = []
    for list_dic in pics_dic:
        titles_list.append(list_dic['@title'])
        temp = list_dic["subpod"]
        if type(temp) == list:
            temp = temp[0]
        output_pics_urls.append(temp["img"]['@src'])

    return [output, output_pics_urls, titles_list]


def log(msg, ans, fname, sname):
    from datetime import datetime
    with open("materials/working/log.txt", "a") as log_file:
        str_out = "\n -------------- \n" + str(datetime.now())[:19]
        str_out += "\nFrom:\n" + fname + " " + sname
        str_out += "\nMessage:\n" + msg + "\n"
        if ans != "":
            str_out += ans + "\n"
        log_file.seek(0, 0)
        log_file.write(str_out)
        # log_file.write("Answer:\n" + ans)


def listToStr(list):
    strout = ""
    for el in list:
        strout += str(el) + "\n"
    return strout


def sch(day, group):
    listout = []
    if group == "БПАД181":
        file = open("materials/working/schedule181.txt", "r", encoding="utf-8")
    else:
        file = open("materials/working/schedule182.txt", "r", encoding="utf-8")
    list = file.read().split("---")
    for el in list:
        newlist = el.split("#")[1:]
        if len(newlist) != 0:
            listout.append(newlist)
    return listout


def isNearestLesson(str):
    time_list = [9, 55] # current time
    import time
    #time_list = time.ctime().split()[3].split(":")[:2]
    
    tt = int(time_list[0]) * 60 + int(time_list[1])
    l1 = [int(str[0:2]), int(str[3:5])]
    t1 = l1[0] * 60 + l1[1]
    l2 = [int(str[8:10]), int(str[11:14])]
    t2 = l2[0] * 60 + l2[1]
    if tt < t2:
        return True
    return False

def refreshSch(current_date,group):
    from selenium import webdriver

    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common import action_chains, keys
    from time import sleep

    import requests
    from bs4 import BeautifulSoup
    # current_date = "03.09.2019"
    # group = "БПАД182"

    def parseRuz(current_date, group):

        op = webdriver.ChromeOptions()
        op.add_argument('headless')
        driver = webdriver.Chrome(executable_path="materials/working/chromedriver.exe",
                                  options=op)

        driver.get("https://ruz.hse.ru/ruz/main")
        sleep(1)
        calendar = driver.find_element_by_xpath("//*[@id='start']")
        i = 0
        while i < 20:
            i += 1
            calendar.send_keys(Keys.BACKSPACE)
        calendar.send_keys(current_date)
        input_line = driver.find_element_by_xpath("//*[@id='autocomplete-group']")
        input_line.send_keys(group)
        # input_line.send_keys(Keys.ENTER)
        sleep(1.5)
        #input_line.send_keys(Keys.ARROW_DOWN)
        input_line.send_keys(Keys.ENTER)

        #####
        sleep(1.5)
        input_line.send_keys(Keys.PAGE_DOWN)
        sleep(0.5)
        input_line.send_keys(Keys.PAGE_DOWN)
        sleep(0.5)
        input_line.send_keys(Keys.PAGE_DOWN)

        #print(driver.page_source)
        with open("my_file.html", "w") as my_file:
            my_file.write(driver.page_source)
        sleep(3)
        driver.close()

    ######################### parsing
    schlist = []

    def schParse(string):
        days = ["пн", "вт", "ср", "чт", "пт", "сб", "вс"]
        if string[0:2] in days:
            string = string[2:]
        i = string.find(current_date)
        string = string[i:]
        if len(string.strip()) > 0:
            schlist.append(string)

    def parseSch():
        with open("materials/working/my_file.html", "rb") as r:
            soup = BeautifulSoup(open("my_file.html"), "html.parser")
            #print(r.read())
            obj = soup.select("div.media.day.ng-star-inserted")
            for i in range(len(obj)):
                schParse(obj[i].text)

    def makeLesson():
        parseSch()
        lessons = []

        # print(schlist)
        # print("makeLesson")

        for el in schlist:
            lesson_list = []
            # print(el + "\n")
            date = el[0:10]
            day = el[12:14]
            time = el[16:30]
            lesson_name = el[31: el.find("анг") - 1]
            lang = "Анг"
            idx = 0
            lesson_type = ""
            if el[el.find("анг") + 6].lower() == "п":
                lesson_type = "Практическое занятие"
            elif el[el.find("анг") + 6].lower() == "с":
                lesson_type = "Семинар"
            elif el[el.find("анг") + 6].lower() == "л":
                lesson_type = "Лекция"
            idx = el.find(lesson_type) + len(lesson_type) + 2
            room = el[idx:idx + 4]
            idx = el.find(room) + 7
            t = el.find("Поток:") - 2
            venue = el[idx: t]
            tgroup = group
            el = el.split()
            teacher = el[-4] + " " + el[-3] + " " + el[-2] + " " + el[-1]
            lesson_list.append(date)
            lesson_list.append(day)
            lesson_list.append(time)
            lesson_list.append(lesson_name)
            lesson_list.append(lang)
            lesson_list.append(lesson_type)
            lesson_list.append(room)
            lesson_list.append(venue)
            lesson_list.append(group)
            lesson_list.append(teacher)
            lessons.append(lesson_list)
        return lessons
    def tempFunc(group):
        if group == "БПАД181":
            return "181"
        return "182"

    def run():
        #print(tempFunc(group))
        file = open("materials/working/schedule{}.txt".format(tempFunc(group)), "w", encoding="utf-8")
        parseRuz(current_date, group)  #################################################################3
        list = makeLesson()

        # print(list)
        # print("run")

        for el in list:
            file.write("---")
            for e in el:
                file.write("#")
                file.write(e)
        file.close()

    run()



from time import sleep, ctime
from functools import wraps
import datetime

def mult_threading(func):
     @wraps(func)
     def wrapper(*args_, **kwargs_):
         import threading
         func_thread = threading.Thread(target=func,
                                        args=tuple(args_),
                                        kwargs=kwargs_)
         func_thread.start()
         return func_thread
     return wrapper


@mult_threading
def everyday_update():
    def temp(list):
        return list[0] + ":" + list[1]
    while True:
        time = ctime()
        t = time.split()[3].split(":")[:2]
        today = datetime.date.today()
        d = str(today.day)
        m = str(today.month)
        y = str(today.year)
        today = d.rjust(2, "0") + "." + m.rjust(2, "0") + "." + y
        if temp(t) == "23:00":
            #print(t)
            #print(today)
            sleep(1)
            current_date = today
            group = "БПАД181"
            refreshSch(current_date, group)

            log("Update of schedule181.txt complete", " ", "Bot", "")
            group = "БПАД182"
            refreshSch(current_date, group)
            log("Update of schedule182.txt complete", " ", "Bot", "")
            t = ""
            sleep(60)

# -*- coding: utf8 -*-
from flask import Flask, jsonify
from flask import make_response
from flask import request
from flask import abort
import os, csv, json
import codecs
import urllib.request

def sortdict(monstat):
    mon = []
    dlist = list(monstat.keys())
    dlist.sort()
    for j in dlist:
        mon.append([j, len(monstat[j])])
    return mon

app = Flask(__name__)

@app.route('/')
def index():
    return open("index.html").read()

@app.route('/stolen')
def stolen():
    os.chdir("/home/yung-sung/HsinChu/ill")
    final = []
    for root, dirs, files in os.walk("."):
        for f in files:
            filename = str(f)
            #print(filename,"\n------------\n")
            if filename.startswith('1'):
                csvf = open(filename,encoding = 'utf8')
                csvr = csv.reader(csvf)
                for row in csvr:
                    if row[2].startswith(u"新竹"):
                        row[0] = row[0].rstrip()
                        row = row[0:3]
                        final.append(row)
                        #print(row)
    monstat = {}
    placestat = {}
    eventstat = {}
    for data in final:
        if data[1][:5] in monstat.keys():
            monstat[data[1][:5]].append(data)
        else:
            monstat[data[1][:5]]=[data]

        if data[2] in placestat.keys():
            placestat[data[2]].append(data)
        else:
            placestat[data[2]]=[data]

        if data[0] in eventstat.keys():
            eventstat[data[0]].append(data)
        else:
            eventstat[data[0]]=[data]

    mon = sortdict(monstat)
    place = sortdict(placestat)
    event = sortdict(eventstat)
    result = {"mon":mon,"place":place,"event":event}
    return jsonify(result)

@app.route('/fireDep')
def fireDep():
    os.chdir("/home/yung-sung/HsinChu/emerg")
    f = codecs.open("fireDep2.json", 'r', 'utf-8-sig')
    j = json.load(f)
    return jsonify(j)

@app.route('/news')
def news():
    os.chdir("/home/yung-sung/HsinChu/")
    f = codecs.open("news.json", 'r', 'utf-8-sig')
    j = json.load(f)
    return jsonify(j)

@app.route('/weather')
def weather():
    os.chdir("/home/yung-sung/HsinChu/")
    url = "http://api.openweathermap.org/data/2.5/forecast?id=1675151&APPID=bd5e378503939ddaee76f12ad7a97608&units=metric"
    urllib.request.urlretrieve(url, "weather.json")
    f = open("weather.json")
    j = json.load(f)
    return jsonify(j)

@app.route('/emerg')
def emerg():
    os.chdir("/home/yung-sung/HsinChu/emerg")
    if not os.path.exists('./AED.json'):
        url = 'http://opendata.hccg.gov.tw/dataset/d55cf39b-bebc-488f-9a86-4f36e2865d3f/resource/111d2c30-a788-41f9-8ebd-0798fa69f261/download/20150129143946531.json'
        urllib.request.urlretrieve(url, "AED.json")
    file = codecs.open('AED.json', 'r', 'utf-8-sig')
    a = json.loads(file.read())

    if not os.path.exists('./emergPlace.json'):
        url = 'http://opendata.hccg.gov.tw/dataset/202fe01b-c797-4a86-975c-3819c64ea1e3/resource/45d265ce-67f4-474c-b645-dd09d4f5e3f2/download/20170710153944857.json'
        urllib.request.urlretrieve(url, "emergPlace.json")
    file = codecs.open('emergPlace.json', 'r', 'utf-8-sig')
    e = json.loads(file.read())

    if not os.path.exists('./fireDep.json'):
        url = 'http://opendata.hccg.gov.tw/dataset/2a0b9034-cf81-4a82-aa66-a3d3373d5b08/resource/3a2ddcfb-807d-43cb-acc5-789de54e90d8/download/20171005143810205.json'
        urllib.request.urlretrieve(url, "fireDep.json")
    file = codecs.open('fireDep.json', 'r', 'utf-8-sig')
    f = json.loads(file.read())

    if not os.path.exists('./hydrant.json'):
        url = 'http://opendata.hccg.gov.tw/dataset/c2ca1a41-541a-43d6-b36d-925987f9e413/resource/ff4dfae5-3d65-4e74-a08d-bdf780612552/download/20171005143110939.json'
        urllib.request.urlretrieve(url, "hydrant.json")
    file = codecs.open('hydrant.json', 'r', 'utf-8-sig')
    h = json.loads(file.read())

    if not os.path.exists('./monitor.json'):
        url = 'http://opendata.hccg.gov.tw/dataset/b0790535-0077-41ac-b15b-4933e98fa94b/resource/b8b1d608-2e12-472e-9840-c27ed3bf26a3/download/20160616114949111.json'
        urllib.request.urlretrieve(url, "monitor.json")
    file = codecs.open('monitor.json', 'r', 'utf-8-sig')
    m = json.loads(file.read())

    if not os.path.exists('./police.json'):
        url = 'http://opendata.hccg.gov.tw/dataset/2fa08f7f-a32e-48da-9689-d691e89be099/resource/40b97954-899d-447f-affd-42266fd2c08f/download/20170814085238162.json'
        urllib.request.urlretrieve(url, "police.json")
    file = codecs.open('police.json', 'r', 'utf-8-sig')
    p = json.loads(file.read())

    file = codecs.open('./ruleshot.json', 'r', 'utf-8-sig')
    r = json.loads(file.read())

    file = codecs.open('./hospital.json', 'r', 'utf-8-sig')
    hos = json.loads(file.read())

    result = {"AED":a,
            "emergPlace":e,
            "fireDep":f,
            "hydrant":h,
            "monitor":m,
            "police":p,
            "ruleshot":r,
            "hospital":hos}
    return jsonify(result)

event_map={"0":"違規停車",
        "1":"車禍",
        "2":"塞車",
        "3":"道路封閉",
        "4":"大型障礙物",
        "5":"交通號誌故障",
        "6":"異常臭味",
        "7":"火災",
        "8":"其他"}

def distance(a,b):
    if pow(float(a[0])-float(b[0]),2)+pow(float(a[1])-float(b[1]),2) < 0.00005:
        return True
    else:
        return False

@app.route('/report/<string:type>/<string:userlat>/<string:userlng>/<string:chinese>')
def report(userlat, userlng, type, chinese):
    data={}
    os.chdir("/home/yung-sung/HsinChu/")
    if not os.path.exists('./system.json'):
            data = {"0":[],
                    "1":[],
                    "2":[],
                    "3":[],
                    "4":[],
                    "5":[],
                    "6":[],
                    "7":[],
                    "8":[],
                    }
            if int(type) in range(0,8):
                d = {"name":event_map[type],"place":[(userlat, userlng)],"amount":1}
                data[type].append(d)
                with open('system.json', 'w') as file1:
                    json.dump(data, file1)
                file1.close()
            elif type == "8":
                d = {"name": chinese, "place": [(userlat, userlng)], "amount": 1}
                data[type].append(d)
                with open('system.json', 'w') as file1:
                    json.dump(data, file1)
                file1.close()

    else:
        f = open("system.json")
        data = json.load(f)
        f.close()
        if int(type) in range(0, 8):
            flag = 0
            for i in data[type]:
                if distance(i["place"][0],(userlat,userlng)):
                    i["place"].append((userlat,userlng))
                    i["amount"]+=1
                    flag =1
            if(flag == 0):
                d = {"name": event_map[type], "place": [(userlat, userlng)], "amount": 1}
                data[type].append(d)
            with open('system.json', 'w') as file1:
                json.dump(data, file1)
            file1.close()
        elif type == "8":
            d = {"name": chinese, "place": [(userlat, userlng)], "amount": 1}
            data[type].append(d)
            with open('system.json', 'w') as file1:
                json.dump(data, file1)
            file1.close()

    # f = open("system.json")
    # j = json.load(f)
    dlist = []
    for i in range(9):
        dlist.append(data[str(i)])
    for i in dlist:
        for j in i:
            j["type"] = dlist.index(i)
            if len(j["place"])!=0:
                j["place"]=j["place"][0]
            else:
                j["place"] = ""
    deal = {"accident":dlist}

    return jsonify(deal)

@app.route('/get_report')
def get_report():
    os.chdir("/home/yung-sung/HsinChu/")
    if not os.path.exists('./system.json'):
        data = {"0": [],
                "1": [],
                "2": [],
                "3": [],
                "4": [],
                "5": [],
                "6": [],
                "7": [],
                "8": [],
                }
        return jsonify(data)
    else:
        file = open('system.json')
        data = json.loads(file.read())
        dlist = []
        for i in range(9):
            dlist.append(data[str(i)])
        for i in dlist:
            for j in i:
                j["type"] = dlist.index(i)
                if len(j["place"]) != 0:
                    j["place"] = j["place"][0]
                else:
                    j["place"] = ""
        deal = {"accident": dlist}
        return jsonify(deal)

@app.route('/reset')
def reset():
    data={}
    os.chdir("/home/yung-sung/HsinChu/")
    data = {"0":[],
            "1":[],
            "2":[],
            "3":[],
            "4":[],
            "5":[],
            "6":[],
            "7":[],
            "8":[],
            }
    with open('system.json', 'w') as file1:
        json.dump(data, file1)
    file1.close()
    dlist = []
    for i in range(9):
        dlist.append(data[str(i)])
    for i in dlist:
        for j in i:
            j["type"] = dlist.index(i)
            if len(j["place"]) != 0:
                j["place"] = j["place"][0]
            else:
                j["place"] = ""
    deal = {"accident": dlist}
    return jsonify(deal)

if __name__ == '__main__':
    app.run()

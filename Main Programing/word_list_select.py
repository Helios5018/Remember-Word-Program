#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#author Helios

import sqlite3
import random
import time
import urllib.request
import urllib.parse
import json
import pygame
import requests
import os

def get_list(word_list):
    conn = sqlite3.connect("word_list.db")
    cursor = conn.cursor()
    cursor.execute("select word from word_list_%s where status=2 order by word"%word_list)
    result1=cursor.fetchall()
    cursor.execute("select word from word_list_%s where status=1 order by word"%word_list)
    result2=cursor.fetchall()

    l=[]
    for a in result1:
        l.append("[OK]"+str(a[0]))
    for b in result2:
        l.append(str(b[0]))

    return l

def rselect_word_content(word_list):
    conn = sqlite3.connect("word_list.db")
    cursor = conn.cursor()

    cursor.execute("select count(id) from word_list_%s"%word_list)
    count_num=cursor.fetchall()
    count_num=int(count_num[0][0])
    for_judge=True
    while for_judge:
        id=random.randint(1,count_num)
        cursor.execute("select * from word_list_%s where id=%d"%(word_list,id))
        result = cursor.fetchall()
        if result[0][1]==1:
            for_judge = False
    return result

    cursor.close()
    conn.commit()
    conn.close()

def get_word_detail(word_list,word):
    conn = sqlite3.connect("word_list.db")
    cursor = conn.cursor()

    cursor.execute("select * from word_list_%s where word='%s'"%(word_list,word))
    result = cursor.fetchall()
    return result

    cursor.close()
    conn.commit()
    conn.close()

def update_word_status(word_list,id):
    conn = sqlite3.connect("word_list.db")
    cursor = conn.cursor()

    current_time=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    cursor.execute("update word_list_%s set status=2, time=? where id=?"%word_list,(current_time,id))

    cursor.close()
    conn.commit()
    conn.close()

def translate_function(content):

    url="http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=https://www.baidu.com/link"

    data={}
    data["type"]="AUTO"
    data["i"]=content
    data["doctype"]="json"
    data["xmlVersion"]="1.8"
    data["keyfrom"]="fanyi.web"
    data["ue"]="UTF-8"
    data["action"]="FY_BY_CLICKBUTTON"
    data["typoResult"]="true"
    data=urllib.parse.urlencode(data).encode("utf-8")

    response=urllib.request.urlopen(url,data)
    html=response.read().decode("utf-8")
    target=json.loads(html)
    if "smartResult" in target:
        result=target["smartResult"]["entries"]
        result=" ".join(result)
        return result[1:]
    else:
        return target["translateResult"][0][0]["tgt"]

def word_audio_function(word,type=1):

    if os.path.exists("sounds/%s-%d.mp3"%(word,type)):
        pass
    else:
        r = requests.get("http://dict.youdao.com/dictvoice?audio=%s&type=%d"%(word,type))
        html = r.content

        with open("sounds/%s-%d.mp3"%(word,type), "wb") as f:
            f.write(html)

    pygame.mixer.init()
    pygame.mixer.music.load("sounds/%s-%d.mp3"%(word,type))
    pygame.mixer.music.play(1)
    while True:
        if pygame.mixer.music.get_busy():
            pygame.time.delay(100)
        else:
            break

def sentence_audio_function(sentence):
    sentence=sentence.strip()
    sentence = "+".join(sentence.split(" "))
    #各种字符处理
    sentence="%2C".join(sentence.split(","))
    sentence = "%27".join(sentence.split("'"))
    sentence = "%3F".join(sentence.split("?"))

    if os.path.exists("sounds/%s.mp3"%sentence):
        pass
    else:
        r = requests.get("http://dict.youdao.com/dictvoice?audio=%s&le=eng"%sentence)
        html = r.content

        with open("sounds/%s.mp3"%sentence, "wb") as f:
            f.write(html)

    pygame.mixer.init()
    pygame.mixer.music.load("sounds/%s.mp3"%sentence)
    pygame.mixer.music.play(1)
    while True:
        if pygame.mixer.music.get_busy():
            pygame.time.delay(100)
        else:
            break

def come_to_init(word_list):
    conn = sqlite3.connect("word_list.db")
    cursor = conn.cursor()

    cursor.execute("update word_list_%s set status=1, time=Null where status=2"%word_list)

    print(word_list+" already come to init")

    cursor.close()
    conn.commit()
    conn.close()

def deleteword(word_list,word):
    conn = sqlite3.connect("word_list.db")
    cursor = conn.cursor()
    cursor.execute("delete from word_list_%s where word='%s'"%(word_list,word))
    print(word+" was deleted")
    cursor.close()
    conn.commit()
    conn.close()







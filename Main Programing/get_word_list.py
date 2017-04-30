#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sqlite3
import pickle

with open("C:\\Users\\Helios\\Desktop\\CET6_detail.pkl","rb") as f:
    word_list=pickle.load(f)

conn=sqlite3.connect("word_list.db")
cursor=conn.cursor()

cursor.execute("create table word_list_CET6(id int primary key, status int, word varchar(30), example text, example_translate text, explanation text,time text)")

#cursor.execute("insert into word_list_CET4 (id,word,example,example_translate,explanation) values (?,?,?,?,?)",(2,"what","- -!","- -!","- -!"))
#word_list={"what":[["123","1234"],["655","657"],["132","4325","5345","123"]]}
try:
    primary_key=1
    status=1
    for k,v in word_list.items():
        if v[2] is None:
            continue
        word=k
        explanation,example_translate,example="","",""
        for i in range(len(v[0])):
            example+=v[0][i]+"\n"
        example=example.strip()
        for i in range(len(v[1])):
            example_translate+=v[1][i]+"\n"
        example_translate=example_translate.strip()
        for i in range(len(v[2])):
            explanation+=v[2][i]+"\n"
        explanation=explanation.strip()
        cursor.execute("insert into word_list_CET6 (id,status,word,example,example_translate,explanation) values (?,?,?,?,?,?)",(primary_key,status,word,example,example_translate,explanation))
        primary_key+=1

    cursor.execute("select * from word_list_CET6")
    result=cursor.fetchall()
    print(result)
except:
    pass
finally:
    cursor.close()
    conn.commit()
    conn.close()
'''
cursor.execute("select * from word_list_CET4")
result = cursor.fetchall()
print(result)
cursor.close()
conn.commit()
conn.close()
'''

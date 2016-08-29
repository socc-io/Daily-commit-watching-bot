#-*- coding: utf-8 -*-

from bottle import route, run, template,request,get, post
import sqlite3
import datetime
import time


conn = sqlite3.connect("commiter.db")
cursor = conn.cursor()

today = datetime.date.today()
print datetime.date.today()

cursor.execute("INSERT INTO USER(GIT_USER_ID, USER_NAME, COMMIT_NUMBER, START_COMMIT_DAY, END_COMMIT_DAY) VALUES (?,?,?,?,?)", ('siosio34@nate.com','young',13,today,today))
conn.commit()
cursor.execute("select * FROM USER")

for row in cursor:
    print row
print "db call"


def get_all_commit_db():
    conn = sqlite3.connect("USER")
    print "db call"

@route('/commit')
def getcommit(): # 전체 커밋횟수를 불러오는 함수이다
    # 기존 디비 요청해서 불러오는 함수
    # 새로운 커밋 내용들고오기

    print "commit"

def get_user_commit(): # 특정한 한 유저의 커밋 내역을 불러오는 함수
    print "get user commit"

run(host='0.0.0.0', port=8887)
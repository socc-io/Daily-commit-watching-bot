from bottle import route, run, template,request,get, post
import sqlite3

@route('/commit')
def getcommit(): # 코딩 내역 들고오기

    print "commit"

run(host='0.0.0.0', port=8887)
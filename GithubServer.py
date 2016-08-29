#-*- coding: utf-8 -*-

from bottle import route, run, template,request,get, post
import requests
import sqlite3
import datetime

# Group Event Url https://api.github.com/orgs/socc-io/events
github_url = 'https://api.github.com/orgs/socc-io/events'

''' response json 구조
[
  {
    "id": "4482929263",
    "type": "PushEvent",
    "actor": {
      "id": 7166022,
      "login": "siosio34",
      "display_login": "siosio34",
      "gravatar_id": "",
      "url": "https://api.github.com/users/siosio34",
      "avatar_url": "https://avatars.githubusercontent.com/u/7166022?"
    },
    "repo": {
      "id": 66697564,
      "name": "socc-io/DailyCommit",
      "url": "https://api.github.com/repos/socc-io/DailyCommit"
    },
    "payload": {
      "push_id": 1271712552,
      "size": 2,
      "distinct_size": 2,
      "ref": "refs/heads/master",
      "head": "408f070de1c08e3d1fa5bd63afa549fd80f30898",
      "before": "309e7e08ae83a5f36ac6c92f08a7856ed9232360",
      "commits": [
        {
          "sha": "1d692e1d22d2404e8ceab3338b8b3c8b5218fbc5",
          "author": {
            "email": "siosio34@nate.com",
            "name": "young"
          },
          "message": "db edit",
          "distinct": true,
          "url": "https://api.github.com/repos/socc-io/DailyCommit/commits/1d692e1d22d2404e8ceab3338b8b3c8b5218fbc5"
        },
        {
          "sha": "408f070de1c08e3d1fa5bd63afa549fd80f30898",
          "author": {
            "email": "siosio34@nate.com",
            "name": "young"
          },
          "message": "add user test data complete",
          "distinct": true,
          "url": "https://api.github.com/repos/socc-io/DailyCommit/commits/408f070de1c08e3d1fa5bd63afa549fd80f30898"
        }
      ]
    },
    "public": true,
    "created_at": "2016-08-29T08:41:41Z",
    "org": {
      "id": 12954120,
      "login": "socc-io",
      "gravatar_id": "",
      "url": "https://api.github.com/orgs/socc-io",
      "avatar_url": "https://avatars.githubusercontent.com/u/12954120?"
    }
  },
  {
    "id": "4482797478",
    "type": "PushEvent",
    "actor": {
      "id": 7166022,
      "login": "siosio34",
      "display_login": "siosio34",
      "gravatar_id": "",
      "url": "https://api.github.com/users/siosio34",
      "avatar_url": "https://avatars.githubusercontent.com/u/7166022?"
    },
    "repo": {
      "id": 66697564,
      "name": "socc-io/DailyCommit",
      "url": "https://api.github.com/repos/socc-io/DailyCommit"
    },
    "payload": {
      "push_id": 1271666781,
      "size": 1,
      "distinct_size": 1,
      "ref": "refs/heads/master",
      "head": "309e7e08ae83a5f36ac6c92f08a7856ed9232360",
      "before": "cc4ca13d5e4c3083fc44b341fd17b78c6cd0f44f",
      "commits": [
        {
          "sha": "309e7e08ae83a5f36ac6c92f08a7856ed9232360",
          "author": {
            "email": "siosio34@nate.com",
            "name": "young"
          },
          "message": "add commiter with sqlite3 db",
          "distinct": true,
          "url": "https://api.github.com/repos/socc-io/DailyCommit/commits/309e7e08ae83a5f36ac6c92f08a7856ed9232360"
        }
      ]
    },
    "public": true,
    "created_at": "2016-08-29T08:07:59Z",
    "org": {
      "id": 12954120,
      "login": "socc-io",
      "gravatar_id": "",
      "url": "https://api.github.com/orgs/socc-io",
      "avatar_url": "https://avatars.githubusercontent.com/u/12954120?"
    }
  },
  {
    "id": "4482447821",
    "type": "PushEvent",
    "actor": {
      "id": 7166022,
      "login": "siosio34",
      "display_login": "siosio34",
      "gravatar_id": "",
      "url": "https://api.github.com/users/siosio34",
      "avatar_url": "https://avatars.githubusercontent.com/u/7166022?"
    },
    "repo": {
      "id": 66697564,
      "name": "socc-io/DailyCommit",
      "url": "https://api.github.com/repos/socc-io/DailyCommit"
    },
    "payload": {
      "push_id": 1271542744,
      "size": 1,
      "distinct_size": 1,
      "ref": "refs/heads/master",
      "head": "cc4ca13d5e4c3083fc44b341fd17b78c6cd0f44f",
      "before": "0c18276da703b27c3ea77b4b2ee3e00458ff64ec",
      "commits": [
        {
          "sha": "cc4ca13d5e4c3083fc44b341fd17b78c6cd0f44f",
          "author": {
            "email": "joyeongje@joyeongje-ui-MacBook-Pro.local",
            "name": "조영제"
          },
          "message": "change route url",
          "distinct": true,
          "url": "https://api.github.com/repos/socc-io/DailyCommit/commits/cc4ca13d5e4c3083fc44b341fd17b78c6cd0f44f"
        }
      ]
    },
    "public": true,
    "created_at": "2016-08-29T06:21:37Z",
    "org": {
      "id": 12954120,
      "login": "socc-io",
      "gravatar_id": "",
      "url": "https://api.github.com/orgs/socc-io",
      "avatar_url": "https://avatars.githubusercontent.com/u/12954120?"
    }
  },
'''

@route('/register')
def register_commiter(): # 새로운 커미터 갱신 - 하루에 한번씩 할가 생각중입니다. 그룹에서 첫커밋시 등록
    conn = sqlite3.connect("commiter.db") # 커미터 디비 연결
    cursor = conn.cursor()

    r = requests.get(github_url)
    data_list =  r.json()

    for event_list in data_list:
        type = event_list['type']

        if(type != 'PushEvent'):
            continue
        else:
            commit_list = event_list['payload']['commits']
            commit_num = event_list['payload']['size']
            for commit in commit_list:
                commiter_email = commit['author']['email']
                commiter_name  = commit['author']['name']

                print commiter_email

                cursor.execute("SELECT rowid FROM USER WHERE GIT_USER_ID = ?", (commiter_email,))
                data = cursor.fetchone()
                if data is None: # 데이터가 없는경우 -> 새로운 커미터 추가
                    now_time = datetime.date.today()
                    cursor.execute(
                        "INSERT INTO USER(GIT_USER_ID, USER_NAME, COMMIT_NUMBER, START_COMMIT_DAY, END_COMMIT_DAY) VALUES (?,?,?,?,?)",
                        (commiter_email, commiter_name, commit_num, now_time, now_time))

                else: # 데이터가 있는 경우
                    parse_date = event_list['created_at']
                    print parse_date
                    print('Component %s found with rowid %s' % (commiter_email, data[0]))

    conn.commit();

    '''
    today = datetime.date.today()

    cursor.execute(
        "INSERT INTO USER(GIT_USER_ID, USER_NAME, COMMIT_NUMBER, START_COMMIT_DAY, END_COMMIT_DAY) VALUES (?,?,?,?,?)",
        ('siosio34@nate.com', 'young', 13, today, today))
    conn.commit()

    # 테스팅 용도
    cursor.execute("select * FROM USER")
    for row in cursor:
        print row
    '''

@route('/commiters') # 커미터 목록들 확인
def get_all_commit_db():
    conn = sqlite3.connect("commiter.db")  # 커미터 디비 연결
    cursor = conn.cursor()
    # 테스팅 용도
    cursor.execute("select * FROM USER")
    for row in cursor:
        print row

@route('/commit')
def getcommit(): # 전체 커밋횟수를 불러오는 함수이다
    # 기존 디비 요청해서 불러오는 함수
    # 새로운 커밋 내용들고오기

    print "commit"

def get_user_commit(): # 특정한 한 유저의 커밋 내역을 불러오는 함수
    print "get user commit"

register_commiter()
run(host='0.0.0.0', port=8887)
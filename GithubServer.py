#-*- coding: utf-8 -*-

from bottle import route, run, template,request,get, post
from datetime import datetime

import requests
import sqlite3

dt = datetime.now()

# Group Event Url https://api.github.com/orgs/socc-io/events
# 이건 그룹용

github_url = 'https://api.github.com/orgs/socc-io/events?per_page=100' # 그룹 url 을 등록해야됨

# perpage 한페이지당 보여지는 이벤트 갯수

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
#todo 유저 디비에 커밋 시작한 일수를 추가해야

@route('/register')
def register_commiter(): # 새로운 커미터 갱신 - 하루에 한번씩 할가 생각중입니다. 그룹에서 첫커밋시 등록
    conn = sqlite3.connect("commiter.sqlite") # 커미터 디비 연결
    cursor = conn.cursor()

    r = requests.get(github_url)
    data_list =  r.json()

    #cursor.execute("SELECT USER_HUB_ID FROM USER")
    change_reload_time = data_list[0]['created_at']

    t1 = '2016-08-31T14:31:40Z'
    t2 = '2016-08-31T15:32:42Z'

    if(t1 > t2):
        print 't1 bigger'
    else:
        print 't2 bigger'


    print change_reload_time

    for event_list in data_list:
        type = event_list['type']
        create_date = event_list['created_at']

        # 타임을 비교하는 함수 만들어야 된다. 유저가 마지막으로 커밋한 시간뒤에 있는것과 비교를 해야한다
        # 타임을 비교하기는 애매하다 깃협는 상대시간을 기준으로 제공
        # 2016-08-29 T06:21:37Z" - github 시간
        # 2016-08-30 14:52:37.778581 - python datetime 시간

        # -> 마지막 커밋 아이디를 저장해놓자 처음부터 끝까지 다 뒤져야한다
        # -> 깃허브 타임존을 저장한다면?

        if(type != 'PushEvent'):
            continue
        else:
            create_date
            commit_list = event_list['payload']['commits']
            commit_num = event_list['payload']['size']
            for commit in commit_list:
                commiter_email = commit['author']['email'].split('@')[0]
                commiter_name  = commit['author']['name']
                commit_message = commit['message']

                #print commiter_email

                cursor.execute("SELECT rowid,COMMIT_NUMBER,END_COMMIT_DAY FROM USER WHERE GIT_USER_ID = ?", (commiter_email,))
                data = cursor.fetchone()
                if data is None: # 데이터가 없는경우 -> 새로운 커미터 추가
                    print 'this'
                    now_time = create_date
                    cursor.execute(
                        "INSERT INTO USER(GIT_USER_ID, GIT_USER_NAME, COMMIT_NUMBER, START_COMMIT_DAY, END_COMMIT_DAY) VALUES (?,?,?,?,?)",
                        (commiter_email, commiter_name, commit_num, now_time, now_time))

                    #todo 매개변수 고쳐야 한다.
                else: # 커미터 데이터가 있는 경우

                    new_row_id = data[0]
                    new_commit_num = data[1] + commit_num
                    new_commit_time = data[2]

                    # create date 커밋한
                    if(create_date > new_commit_time): # 최신 날짜로 업데이트 하는건 좋은데 문제는 애로 갱신하면 아래걸 못받아옴, 갱신하는건 현재시간 but
                        cursor.execute("UPDATE USER SET COMMIT_NUMBER = ? WHERE ROWID = ?", (new_commit_num,new_row_id))

                    #if(parse_date < data[0].END_COMMIT_DAY):
                    #print('Component %s found with rowid %s' % (commiter_email, data[0]))

    # reload 타임의 생성이 필요하다.


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



#run(host='0.0.0.0', port=8887)
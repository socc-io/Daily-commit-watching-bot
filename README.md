# DailyCommit

일일커밋 봇 테스트
테스트 용도 

# 프로그램 구조

- (사전에)프로그래밍 Github그룹 생성, slack 그룹 가입 받음
- 마지막으로 커밋 횟수를 요청했을때 이후를 기준으로 새로운 커밋횟수 및 커밋 로그를 저장
- 커밋횟수는 슬랙 봇을 이용해서 <h3>!commit</h3> 명령어를 입력시 전체 커밋내역 및 수를 보여줄 예정
- 유저가 슬랙에서 !commit 명령 입력 -> 파이썬 서버로 전달됨 <br> -> 파이썬에서 새로운 커밋내역 갱신 및 디비 갱신 그리고 로드
  -> 서버에서 슬랙 봇으로 내용전달

# 유저구조
- username
- github id
- start commit time
- last commit time
- commit number
- commit log (배열로 되야될듯 - 이건 다른 디비에 추가를 해야될듯







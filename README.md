# nvCrawler

## 작동방식
네이버 개발자센터에서 발급받은 Client ID와 Client Secret를 이용해 네이버 뉴스에서 검색어 관련 기사를 크롤링한 뒤 .json 파일로 저장
------------
## 작업 설계
1. 검색어 지정 : srcText = '월드컵'
2. 뉴스 검색하기 : getNaverSearch() 호출
  2.1. url 구성 : url = base + node + srcText
  2.2. url 접속과 검색 요청하기 : urllib.request.urlopen()
  2.3. 요청 결과를 응답 JSON으로 받기 : json.load()
3. 응답 데이터 정리 후 리스트에 저장 : getPostData()
4. 리스트를 JSON 파일로 저장 : json.dumps()
------------
[출처] 데이터 과학 기반의 파이썬 빅데이터 분석 - 저)이지영 출)한빛아카데미

"""
Author : Jinwoo Lee
Date : 2021.12.09.
Explanation : News Crawling Program using Naver_Open_Api
"""
import datetime
import json

import key
import urllib.request

# [getRequestUrl] : url 접속을 요청하고 응답을 받아서 반환
# [parameter] url : 네비스 뉴스 검색('ex: 월드컵')에 대한 url
def getRequestUrl(url):
    req = urllib.request.Request(url)                                   # 네이버 서버에 보낼 url 접속 요청(request) 객체를 생성
    req.add_header("X-Naver-Client-Id", key.CLIENT_ID)                  # 서버에 보내는 요청 객체에 헤더 정보를 추가
    req.add_header("X-Naver-Client-Secret", key.CLIENT_SECRET)

    try:                                                                    # 오류 발생시 except 문을 통해 예외 처리
        response = urllib.request.urlopen(req)                                  # 서버에서 받은 응답을 변수(메모리)에 저장
        if response.getcode() == 200:                                           # 상태 코드가 200 -> 요청 처리 성공
            print("[%s] Url Request Success" % datetime.datetime.now())         # 현재 시간과 요청 성공 메시지 출력
            return response.read().decode('utf-8')                              # 네이버 서버에서 받은 응답을 utf-8 형식으로 문자열을 디코딩하여 반환
    except Exception as e:                                                  # 예외 처리 구문(발생 오류: Exception, 오류 메시지 변수: e)
        print(e)                                                                # 오류 메시지 출력
        print("[%s] Error for URL : %s" % (datetime.datetime.now(), url))       # 오류 발생 시간과 해당 url 출력
        return None                                                             # 자바의 Null과 유사하지만 별도의 DataType인 None을 반환

# [getNaverSearch] : 네이버 뉴스 검색 url을 만들고 getRequestUrl(url)을 호출하여 반환받은 응답 데이터를 파이썬 json 형식으로 반환
# [parameter] node : 네이버 검색 API를 이용하여 검색할 대상 노드(news, blog, cafearticle, movie, shop 등)
#   srcText        : 검색어
#   page_start     : 검색 시작 위치(1~1000)
#   display        : 출력 건수(10~100)
def getNaverSearch(node, srcText, page_start, display):
    base = "https://openapi.naver.com/v1/search"                                                            # 검색 url의 기본 주소 설정
    node = "/%s.json" % node                                                                                # 검색 대상에 따른 json 파일 이름 설정
    parameters = "?query=%s&start=%s&display=%s" % (urllib.parse.quote(srcText), page_start, display)       # url에 추가할 검색어와 검색 시작 위치, 출력 건수 설ㅈㅇ

    url = base + node + parameters          # 검색url기본주소/해당json파일/검색설정값
    responseDecode = getRequestUrl(url)     # 해당 설정에 대한 url 접속을 요청하고 응답 객체(utf-8로 디코드)를 반환받아 저장

    if (responseDecode == None):            # url 접속 요청이 실패(오류)했을 경우 : None 반환
        return None
    else:
        return json.loads(responseDecode)   # 응답 객체를 파이썬이 처리할 수 있는 JSON 형식으로 변환하여 반환

# [getPostData]     : JSON 형식의 응답 데이터를 필요한 항목만 정리하여 딕셔너리 리스틍니 jsonResult를 구성하고 반환
# [parameter] post  : 응답으로 받은 검색 결과 데이터 중에서 결과 한 개(ex: 뉴스 기사 1개)를 저장한 객체
#   jsonResult      : 필요한 부분만 저장하여 반환할 리스트 객체
#   cnt             : 현재 작업 중인 검색 결과의 번호
def getPostData(post, jsonResult, cnt):
    title = post['title']                   # post 객체의 각 항목[title, description, originallink, link]에 저장된 값을 변수로 저장
    description = post['description']
    org_link = post['originallink']
    link = post['link']

    pDate = datetime.datetime.strptime(post['pubDate'], '%a, %d %b %Y %H:%M:%S +0900')      # post 객체의 pubDate 항목(문자열)을 날짜 객체 형식으로 변환하여 변수에 저장
    pDate = pDate.strftime('%Y-%m-%d %H:%M:%S')                                             # 저장한 날짜 객체의 표시 형식 지정

    # *리스트 객체인 매개변수 jsonResult에 원소를 추가(포인터)*
    jsonResult.append({'cnt':cnt, 'title':title, 'description':description, 'org_link':org_link, 'link':link, 'pDate':pDate})

    return      # 포인터를 통해 원소를 추가했기 때문에 아무것도 반환하지 않음

# [main] : 전체 작업 스토리 설계
# 1. 검색어 지정 : srcText = '월드컵'
# 2. 뉴스 검색하기 : getNaverSearch() 호출
#   2.1. url 구성 : url = base + node + srcText
#   2.2. url 접속과 검색 요청하기 : urllib.request.urlopen()
#   2.3. 요청 결과를 응답 JSON으로 받기 : json.load()
# 3. 응답 데이터 정리 후 리스트에 저장 : getPostData()
# 4. 리스트를 JSON 파일로 저장 : json.dumps()
def main():
    node = 'news'                               # 크롤링할 대상 : 뉴스
    srcText = input('검색어를 입력하세요: ')       # 사용자 입력으로 받은 검색어 저장
    cnt = 0                                     # 검색 결과 카운트
    jsonResult = []                             # 검색결과를 정리(기사1, 기사2, 기사3, ...)하여 저장할 리스트 객체

    jsonResponse = getNaverSearch(node, srcText, 1, 100)        # 해당 대상의 검색어에 대한 1부터 100개의 검색 결과를 처리
    total = jsonResponse['total']                               # 검색 결과 모두를 저장

    while ((jsonResponse != None) and (jsonResponse['display'] != 0)):  # url 접속요청이 성공적으로 처리되었고(None으로 반환되지 않음), 응답 객체(검색 결과)가 있을 경우(0이 아닐 경우)
        for post in jsonResponse['items']:          # 검색결과를 모두 처리할 때까지 결과(items)를 하나씩 처리하기 위한 for 반복문
            cnt += 1                                # 처리한 검색 결과++
            getPostData(post, jsonResult, cnt)      # 검색결과 하나씩 리스트 객체(jsonResult)에 축

        start = jsonResponse['start'] + jsonResponse['display']     # 다음 검색 결과 100개를 가져오기 위해 start 위치 변경
        jsonResponse = getNaverSearch(node, srcText, start, 100)    # getNaverSearch() 함수를 호출하여 새로운 검색 결과(다음에 불러올 결과)를 jsonResponse에 저장

    print('전체 검색 : %d 건' %total)        # 검색 결과 개수를 출력

    # 'utf8'로 인코딩한 검색결과.json 파일을 만들고 쓰기(w)
    with open('%s_naver_%s.json' % (srcText, node), 'w', encoding='utf8') as outfile:
        jsonFile = json.dumps(jsonResult, indent=4, sort_keys=True, ensure_ascii=False)     # 객체를 json 형식으로 변환

        outfile.write(jsonFile)                                                             # 파일 쓰기

    print("가져온 데이터 : %d 건" % (cnt))                 # 가져온 데이터의 개수를 출력
    print('%s_naver_%s.json SAVED' % (srcText, node))   # json 파일이 저장다는 메시지를 출력

if __name__ == '__main__':
    main()
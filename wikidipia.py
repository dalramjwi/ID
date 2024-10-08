import requests

# Wikipedia API에서 직접 호출하여 데이터 가져오기
def get_wikipedia_page_summary(page_title, language="en"):
    url = f"https://{language}.wikipedia.org/w/api.php"
    
    # API 요청 파라미터 설정
    params = {
        "action": "query",
        "format": "json",
        "titles": page_title,
        "prop": "extracts",
        "explaintext": True,  # plain text 형식으로 추출
        "exintro": True,      # 소개 부분만 추출
    }
    
    # API 요청
    response = requests.get(url, params=params)
    data = response.json()
    
    # 페이지 정보를 파싱
    page = next(iter(data['query']['pages'].values()))  # 첫 번째 페이지 데이터 추출
    if 'missing' in page:
        return None  # 페이지가 없을 경우 처리
    
    return {
        "title": page.get("title", "No title available"),
        "summary": page.get("extract", "No summary available"),
        "pageid": page.get("pageid", "No page ID available"),
    }

# 검색할 페이지 설정 (예시: "Python (programming language)")
page_name = "Cookie"

# 페이지 요약 정보 가져오기
page_info = get_wikipedia_page_summary(page_name)

# 결과 확인
if page_info:
    # 페이지 정보를 터미널에 출력
    print(f"Title: {page_info['title']}")
    print(f"Summary: {page_info['summary']}")
    print(f"Page ID: {page_info['pageid']}")
else:
    print(f"'{page_name}' 페이지가 존재하지 않습니다.")
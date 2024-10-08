import requests
from bs4 import BeautifulSoup
import json
from concurrent.futures import ThreadPoolExecutor

# 기본 페이지 URL 설정
base_url = 'https://fairytalez.com/user-tales/'

# 웹 크롤링 시 필요한 User-Agent 설정
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0'
}

# 동화 페이지에서 제목과 본문을 추출하는 함수
def fetch_story(url):
    # 주어진 URL로 HTTP GET 요청을 보냅니다.
    response = requests.get(url, headers=headers)

    # 상태 코드가 200(성공)이면 아래 코드 실행
    if response.status_code == 200:
        # HTML 내용을 BeautifulSoup을 통해 파싱
        soup = BeautifulSoup(response.content, 'html.parser')

        # 제목을 담고 있는 <h1> 태그(class='title entry-title')를 찾습니다.
        title_elem = soup.find('h1', class_='title entry-title')

        # 제목이 있으면 텍스트를 추출하고, 없으면 "No Title Found"로 설정
        title = title_elem.text.strip() if title_elem else "No Title Found"

        # 본문을 담고 있는 <section> 태그(class='entry user-tale')를 찾습니다.
        content_section = soup.find('section', class_='entry user-tale')

        # 본문이 있으면 <p> 또는 <div> 태그의 텍스트를 모두 추출합니다.
        if content_section:
            paragraphs = [elem.get_text(strip=True) for elem in content_section.find_all(['p', 'div']) if elem.get_text(strip=True)]
            # 본문을 하나의 문자열로 결합
            content = "\n".join(paragraphs)
        else:
            # 본문이 없을 경우 기본 메시지 설정
            content = "No content found."

        # 제목, 본문, URL을 딕셔너리 형태로 반환
        return {
            'title': title,
            'content': content,
            'url': url
        }
    else:
        # 상태 코드가 200이 아니면 오류 메시지 반환
        return {
            'title': "Failed to fetch",
            'content': "",
            'url': url
        }

# 메인 함수: 동화 링크를 수집하고 각 링크의 데이터를 가져옵니다.
def main():
    # 기본 페이지에 GET 요청을 보냅니다.
    response = requests.get(base_url, headers=headers)

    # 상태 코드가 200(성공)이면 크롤링을 시작합니다.
    if response.status_code == 200:
        # HTML 내용을 BeautifulSoup을 통해 파싱
        soup = BeautifulSoup(response.content, 'html.parser')

        # <a> 태그에서 'https://fairytalez.com/user-tales/'로 시작하는 링크만 추출
        story_links = [
            a['href'] for a in soup.find_all('a', href=True)
            if a['href'].startswith('https://fairytalez.com/user-tales/')
        ]

        # 동화 데이터를 저장할 리스트 초기화
        stories_data = []

        # ThreadPoolExecutor를 사용하여 병렬로 크롤링 작업을 진행(max_workers=10)
        with ThreadPoolExecutor(max_workers=10) as executor:
            # 각 동화 링크에 대해 fetch_story 함수를 실행하여 결과 수집
            results = executor.map(fetch_story, story_links)

            # 각 결과를 stories_data 리스트에 추가
            for result in results:
                stories_data.append(result)

        # 수집한 데이터를 'user_tales_data.json' 파일로 저장
        with open('user_tales_data.json', 'w', encoding='utf-8') as f:
            # JSON 파일로 변환하여 저장 (ensure_ascii=False로 비ASCII 문자를 그대로 저장)
            json.dump(stories_data, f, ensure_ascii=False, indent=4)

        # 데이터 저장 완료 메시지 출력
        print("Data successfully saved to user_tales_data.json")
    else:
        # 기본 페이지 요청 실패 시 오류 메시지 출력
        print("Failed to fetch the base page.")

# 이 스크립트를 직접 실행할 때만 main 함수를 호출
if __name__ == "__main__":
    main()

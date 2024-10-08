import requests
import json
import os

# Wikipedia와 Wikisource API URL
WIKIPEDIA_API_URL = "https://en.wikipedia.org/w/api.php"
WIKISOURCE_API_URL = "https://en.wikisource.org/w/api.php"

# 저장할 폴더 생성
wikipedia_folder = "wikipedia_fairy_tales"
wikisource_folder = "wikisource_fairy_tales"
os.makedirs(wikipedia_folder, exist_ok=True)
os.makedirs(wikisource_folder, exist_ok=True)

def fetch_titles(api_url, folder, keyword, filename):
    params = {
        'action': 'query',
        'list': 'search',
        'srsearch': keyword,
        'format': 'json',
        'srlimit': 500
    }

    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        data = response.json()

        titles = [item['title'] for item in data['query']['search']]

        file_path = os.path.join(folder, f'{filename}.json')
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(titles, f, ensure_ascii=False, indent=4)
        print(f"{file_path}에 제목이 저장되었습니다.")

    except requests.RequestException as e:
        print(f"API 요청 중 오류 발생: {e}")

# 실행 예시: 각각 'fairy tale'과 '동화' 키워드로 제목을 저장
fetch_titles(WIKIPEDIA_API_URL, wikipedia_folder, 'fairy tale', 'wikipedia_fairy_tales_titles')
fetch_titles(WIKISOURCE_API_URL, wikisource_folder, 'fairy tale', 'wikisource_fairy_tales_titles')


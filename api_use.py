import requests
import json
import os

# Wikipedia API URL
WIKIPEDIA_API_URL = "https://en.wikipedia.org/w/api.php"

# Wikisource API URL
WIKISOURCE_API_URL = "https://en.wikisource.org/w/api.php"

# 저장할 폴더 생성
wikipedia_folder = "wikipedia_fairy_tales"
wikisource_folder = "wikisource_fairy_tales"
os.makedirs(wikipedia_folder, exist_ok=True)
os.makedirs(wikisource_folder, exist_ok=True)

def fetch_fairy_tales():
    params = {
        'action': 'query',
        'list': 'search',
        'srsearch': 'fairy tales',
        'format': 'json',
        'srlimit': 500
    }

    try:
        response = requests.get(WIKIPEDIA_API_URL, params=params)
        response.raise_for_status()
        data = response.json()

        titles = [item['title'] for item in data['query']['search']]

        file_count = 1
        max_entries_per_file = 100
        for i in range(0, len(titles), max_entries_per_file):
            batch_titles = titles[i:i + max_entries_per_file]
            file_path = os.path.join(wikipedia_folder, f'wikipedia_fairy_tales_titles_{file_count}.json')
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(batch_titles, f, ensure_ascii=False, indent=4)
            print(f"{file_path}에 데이터가 저장되었습니다.")
            file_count += 1

    except requests.RequestException as e:
        print(f"API 요청 중 오류 발생: {e}")

def fetch_fairy_tale_texts(titles):
    file_count = 1
    max_entries_per_file = 10

    for title in titles:
        try:
            params = {
                'action': 'query',
                'titles': title,
                'prop': 'revisions',
                'rvprop': 'content',
                'format': 'json'
            }

            response = requests.get(WIKIPEDIA_API_URL, params=params)
            response.raise_for_status()
            data = response.json()

            pages = data.get('query', {}).get('pages', {})
            for page_id, page_data in pages.items():
                content = page_data.get('revisions', [{}])[0].get('*', 'No Content')

                data = {
                    "title": title,
                    "content": content
                }
                file_path = os.path.join(wikisource_folder, f'wikisource_fairy_tales_texts_{file_count}.json')
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
                print(f"{file_path}에 데이터가 저장되었습니다.")

                file_count += 1
                if file_count > max_entries_per_file:
                    file_count = 1

        except requests.RequestException as e:
            print(f"API 요청 중 오류 발생: {e}")

# 실행 예시
fetch_fairy_tales()
titles = ["Sugar Apple Fairy Tale"]
fetch_fairy_tale_texts(titles)
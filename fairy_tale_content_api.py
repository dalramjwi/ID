import requests
import json
import os
wikipedia_folder = "wikipedia_fairy_tales"

# Wikisource API URL
WIKISOURCE_API_URL = "https://en.wikisource.org/w/api.php"

# 저장할 폴더 생성
wikisource_folder = "wikisource_fairy_tales"
os.makedirs(wikisource_folder, exist_ok=True)

def fetch_fairy_tale_texts_from_file(title_file):
    try:
        # 저장된 제목 파일에서 제목을 불러옴
        with open(title_file, 'r', encoding='utf-8') as f:
            titles = json.load(f)

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

                response = requests.get(WIKISOURCE_API_URL, params=params)
                response.raise_for_status()
                data = response.json()

                pages = data.get('query', {}).get('pages', {})
                for page_id, page_data in pages.items():
                    content = page_data.get('revisions', [{}])[0].get('*', 'No Content')

                    # 제목과 본문 내용을 {title: , content: } 형식으로 저장
                    fairy_tale_data = {
                        "title": title,
                        "content": content
                    }
                    file_path = os.path.join(wikisource_folder, f'wikisource_fairy_tales_texts_{file_count}.json')
                    with open(file_path, 'w', encoding='utf-8') as f:
                        json.dump(fairy_tale_data, f, ensure_ascii=False, indent=4)
                    print(f"{file_path}에 본문 내용이 저장되었습니다.")

                    file_count += 1
                    if file_count > max_entries_per_file:
                        file_count = 1

            except requests.RequestException as e:
                print(f"API 요청 중 오류 발생: {e}")

    except FileNotFoundError:
        print(f"{title_file} 파일을 찾을 수 없습니다.")
    except json.JSONDecodeError:
        print(f"{title_file} 파일에서 JSON 디코딩 중 오류 발생.")

# 실행 예시: 이전에 저장된 제목 파일을 읽어와 본문 가져오기
wikipedia_title_file = os.path.join(wikipedia_folder, 'wikipedia_fairy_tales_titles.json')
fetch_fairy_tale_texts_from_file(wikipedia_title_file)

wikisource_title_file = os.path.join(wikisource_folder, 'wikisource_fairy_tales_titles.json')
fetch_fairy_tale_texts_from_file(wikisource_title_file)

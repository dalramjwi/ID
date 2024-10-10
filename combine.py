import json

# JSON 파일 로드 및 텍스트 추출
def extract_text_from_json(fairy_tale_path, mythology_paths):
    with open(fairy_tale_path, 'r', encoding='utf-8') as f:
        fairy_tale_data = json.load(f)

    combined_mythology_texts = []
    for mythology_path in mythology_paths:
        with open(mythology_path, 'r', encoding='utf-8') as f:
            mythology_data = json.load(f)
            combined_mythology_texts += [story['content'] for story in mythology_data]  # 'content' 필드로 수정

    fairy_tale_texts = [story['content'] for story in fairy_tale_data]  # 여기서도 'content'로 수정
    return fairy_tale_texts + combined_mythology_texts

# 파일 경로를 인자로 전달하여 실행
if __name__ == "__main__":
    fairy_tale_path = 'FairyTale/user_tales_data.json'
    mythology_paths = ['greek_mythology_data/greek_mythology_data_1.json', 'greek_mythology_data/greek_mythology_data_2.json']
    
    combined_texts = extract_text_from_json(fairy_tale_path, mythology_paths)
    with open('combined_texts.txt', 'w', encoding='utf-8') as f:
        for text in combined_texts:
            f.write(text + '\n')
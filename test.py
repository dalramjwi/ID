
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json

# 크롬 드라이버 경로 설정
chrome_driver_path = "C:/Users/user/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe"

# 저장할 폴더 생성
output_folder = "greek_mythology_data"
os.makedirs(output_folder, exist_ok=True)

def scrape_greek_mythology():
    service = Service(executable_path=chrome_driver_path)
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-dev-shm-usage')  # 메모리 문제 해결
    options.add_argument('--no-sandbox')  # 샌드박스 모드 비활성화
    driver = webdriver.Chrome(service=service, options=options)

    # 메인 페이지에 접속
    driver.get("https://www.greekmythology.com/")

    try:
        # a 태그 링크 수집
        links = driver.find_elements(By.TAG_NAME, "a")
        link_list = [link.get_attribute("href") for link in links if link.get_attribute("href") and "http" in link.get_attribute("href")]

        # 수집된 링크 출력
        print(f"수집된 링크: {len(link_list)}개")

        # 데이터를 저장할 리스트 및 파일 카운터 설정
        data_list = []
        file_count = 1
        max_entries_per_file = 100  # 각 파일에 저장할 데이터 수 제한

        # 각 링크로 들어가서 데이터 수집
        for i, link in enumerate(link_list):
            try:
                driver.get(link)
                WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                html = driver.page_source
                soup = BeautifulSoup(html, "html.parser")

                # 타이틀 및 본문 수집
                title = soup.find("title").text if soup.find("title") else "No Title"
                content = soup.find("p").text if soup.find("p") else "No Content"

                # JSON 형식 데이터 저장
                data = {
                    "url": link,
                    "title": title,
                    "content": content
                }
                data_list.append(data)

                # 일정 수 이상의 데이터를 수집하면 파일로 저장
                if (i + 1) % max_entries_per_file == 0:
                    file_path = os.path.join(output_folder, f'greek_mythology_data_{file_count}.json')
                    with open(file_path, 'w', encoding='utf-8') as f:
                        json.dump(data_list, f, ensure_ascii=False, indent=4)

                    print(f"{file_path}에 데이터가 저장되었습니다.")
                    data_list = []  # 리스트 초기화
                    file_count += 1  # 파일 카운터 증가

            except Exception as e:
                print(f"링크 {link}에서 오류 발생: {e}")

        # 남은 데이터를 마지막 파일로 저장
        if data_list:
            file_path = os.path.join(output_folder, f'greek_mythology_data_{file_count}.json')
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data_list, f, ensure_ascii=False, indent=4)
            print(f"{file_path}에 데이터가 저장되었습니다.")

    except Exception as e:
        print(f"오류 발생: {e}")

    finally:
        driver.quit()

# 실행
scrape_greek_mythology()


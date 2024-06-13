import os
from bs4 import BeautifulSoup

# 크롤링된 HTML 파일들이 저장된 디렉토리 경로
directory = "/Users/e/news-please-repo"

# 검색할 키워드 배열
keywords = ["helloaskdjfhalkshjdfaweh"]

# 키워드가 포함된 HTML 파일 경로와 파일 이름을 저장할 리스트
matched_files = []

# 디렉토리 내의 모든 파일을 재귀적으로 탐색
for root, dirs, files in os.walk(directory):
    for filename in files:
        if filename.endswith(".html"):  # HTML 파일만 처리
            file_path = os.path.join(root, filename)
            
            # HTML 파일 읽기
            with open(file_path, "r", encoding="utf-8") as file:
                html_content = file.read()
            
            # BeautifulSoup을 사용하여 HTML 파싱
            soup = BeautifulSoup(html_content, "html.parser")
            
            # 키워드 검색
            for keyword in keywords:
                if keyword in soup.get_text():
                    matched_files.append((file_path, filename))
                    break  # 하나의 키워드라도 찾으면 다음 파일로 이동
        
# 결과 출력
if matched_files:
    print("키워드가 포함된 HTML 파일:")
    for file_path, filename in matched_files:
        print(f"파일 경로: {file_path}")
        print(f"파일 이름: {filename}")
        print("---")
else:
    print("키워드가 포함된 HTML 파일이 없습니다.")

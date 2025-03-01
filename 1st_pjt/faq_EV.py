from selenium import webdriver
from selenium.webdriver.common.by import By
#import mysql.connector
import time
import csv

# MySQL 데이터 삽입 함수
# def insert_data(sql, values):
#     conn = mysql.connector.connect(
#         host="pjt1",
#         user="root",
#         password="1234"
#     )
#     cursor = conn.cursor()
#     try:
#         cursor.execute(sql, values)
#         conn.commit()
#         print("데이터 삽입 성공:", values)
#     except Exception as e:
#         print("데이터 삽입 실패:", e)
#     finally:
#         cursor.close()
#         conn.close()


driver = webdriver.Chrome()
driver.implicitly_wait(5)

# CSV 파일 설정
csv_filename = "ev_faq_data.csv"
csv_file = open(csv_filename, mode="w", newline="", encoding="utf-8")
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["category", "question", "answer"])

# 사이트 접속
url = "https://ev.or.kr/nportal/partcptn/initFaqAction.do"
driver.get(url)
time.sleep(1)

category_dict = {
    #"전체": "//*[@id='all']",
    "완속충전기 설치 지원 사업": "//*[@id='2']",
    "충전소 이용": "//*[@id='1']",
    "수소충전소 인프라 사업": "//*[@id='3']"
}

def crawl_page(category_name):
    faq_list = driver.find_elements(By.CLASS_NAME, "board_faq")

    for faq in faq_list:
        try:
            question = faq.find_element(By.CLASS_NAME, "faq_title").text.strip()
            answer = faq.find_element(By.CLASS_NAME, "faq_con").text.strip()
            
            print(f"[{category_name}] Q: {question}")
            print(f"A: {answer}")
            print("="*50)

            # CSV 및 DB 저장
            csv_writer.writerow([category_name, question, answer])
            # sql = """
            #     INSERT INTO tb_ev_faq (category, question, answer)
            #     VALUES (%s, %s, %s)
            # """
            # values = (category_name, question, answer)
            # insert_data(sql, values)
        except Exception as e:
            print(f"🚨 크롤링 오류 발생: {e}")

# 🔹 카테고리별 크롤링 (첫 페이지만)
for category_name, category_xpath in category_dict.items():
    try:
        category_button = driver.find_element(By.XPATH, category_xpath)
        category_button.click()
        time.sleep(2)
        print(f"✅ [{category_name}] 카테고리 선택 완료")

        crawl_page(category_name)

        print(f"🚀 [{category_name}] 카테고리 크롤링 완료 ✅")

    except Exception as e:
        print(f"🚨 [{category_name}] 카테고리 선택 실패: {e}")

# 파일 닫기 및 드라이버 종료
csv_file.close()
driver.quit()
print("🚀 모든 카테고리 크롤링 완료 ✅")
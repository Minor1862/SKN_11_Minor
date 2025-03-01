from selenium import webdriver
from selenium.webdriver.common.by import By
#import mysql.connector
import time
import csv

# def insert_data(sql, values):
#     status = ''
#     conn = mysql.connector.connect(
#         host="pjt1",
#         user="root",
#         password="1234",
#         database="1234"
#     )

#     cursor = conn.cursor()

#     try:
#         cursor.execute(sql, values)
#         conn.commit()
#         print("데이터 삽입 성공")
#         status = 'success'

#     except Exception as e:
#         print("데이터 삽입 실패:", e)
#         status = 'fail'
#     finally:
#         cursor.close()
#         conn.close()

#     return status

driver = webdriver.Chrome()

# CSV 파일 설정
csv_file = open('chevrolet_faq_data.csv', mode='w', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['category', 'question', 'answer'])

def crawl_page():
    question_btns = driver.find_elements(By.CSS_SELECTOR, 'ul li a.question')

    for question_btn in question_btns:
        question = question_btn.text
        print(f"질문: {question}")

        # 클릭하여 답변을 표시하도록 하기
        try:
            driver.execute_script("arguments[0].click();", question_btn)  # 클릭 실행
            time.sleep(2)  # 답변이 로드될 시간을 기다림

            # 질문 버튼의 부모 요소를 기준으로 답변 찾기
            answer_element = question_btn.find_element(By.XPATH, "./ancestor::li//div[contains(@class, 'answer')]")
            answer = answer_element.text.strip()
            print(f"답변: {answer}")

            # CSV 파일에 데이터 작성
            csv_writer.writerow(['Chevrolet', question, answer])

            # # MySQL 데이터베이스에 삽입
            # sql = """
            #     INSERT INTO tb_test_faq_data (brand, question, answer) 
            #     VALUES (%s, %s, %s)
            # """
            # values = ('Chevrolet', question, answer)
            # insert_data(sql, values)

        except Exception as e:
            print(f"답변을 찾을 수 없습니다: {e}")

        print("=" * 50)


# URL을 설정하여 페이지를 호출
url = "https://www.chevrolet.co.kr/evlife/faq.gm"  # 크롤링할 페이지 URL

driver.get(url)
time.sleep(2)

page_number = 1
while True:
    print(f"크롤링 중: {page_number} 페이지")
    crawl_page()
    try:
        # 페이지 넘기기 버튼을 찾고 클릭 (다음 페이지로 넘어가는 로직을 추가하려면 이 부분 수정)
        next_page_btn = driver.find_element(By.XPATH, '//*[@class="pagination__next"]')
        next_page_btn.click()
        time.sleep(2)
        page_number += 1
    except Exception as e:
        print(f"다음 페이지로 이동할 수 없습니다. 마지막 페이지입니다. ({e})")
        break

csv_file.close()
driver.quit()

from selenium import webdriver
from selenium.webdriver.common.by import By
#import mysql.connector
import time
import csv

# def insert_data(sql, values):
#     status = ''
#     conn = mysql.connector.connect(
#         host="localhost",
#         user="pjt1",
#         password="",
#         database="faq"
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
csv_file = open('kia_pbv_faq.csv', mode='w', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['category', 'question', 'answer'])

def crawl_page():
    question_btns = driver.find_elements(By.CLASS_NAME, 'cmp-accordion__title')

    for idx, question_btn in enumerate(question_btns):
        question = question_btn.text
        print(f"질문: {question}")

        # 클릭하여 답변을 표시하도록 하기
        try:
            answer_btn = driver.find_element(By.XPATH, f'//*[@id="accordion-item-{idx}-button"]/span[2]')
            answer_btn.click()
            time.sleep(2)

            # 모든 답변을 가져와서 해당 질문과 연결
            answer_elements = driver.find_elements(By.XPATH, f'//*[@id="accordion-item-{idx}"]//*[@class="faqinner__wrap"]//p')
            answers = " ".join([answer.text for answer in answer_elements])  # 여러 개의 <p> 태그를 합치기
            print(f"답변: {answers}")

            # CSV 파일에 데이터 작성
            csv_writer.writerow(['Kia PBV', question, answers])

            # # MySQL 데이터베이스에 삽입
            # sql = """
            #     INSERT INTO tb_test_faq_data (brand, question, answer) 
            #     VALUES (%s, %s, %s)
            # """
            # values = ('Kia PBV', question, answers)
            # insert_data(sql, values)

        except Exception as e:
            print(f"답변을 찾을 수 없습니다: {e}")

        print("=" * 50)


# URL을 설정하여 페이지를 호출
url = "https://www.kia.com/kr/pbv/kia-pbv/faq"  # 카테고리 구분 없이 FAQ 페이지만 호출

driver.get(url)
time.sleep(2)

page_number = 1
while True:
    print(f"크롤링 중: {page_number} 페이지")
    crawl_page()
    try:
        # 페이지 넘기기 버튼을 찾고 클릭
        next_page_btn = driver.find_element(By.XPATH, f'//*[@id="accordion-item-{page_number}-button"]')
        next_page_btn.click()
        time.sleep(2)
        page_number += 1
    except Exception as e:
        print(f"다음 페이지로 이동할 수 없습니다. 마지막 페이지입니다. ({e})")
        break

csv_file.close()
driver.quit()

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from selenium.common.exceptions import ElementClickInterceptedException


import time
import pyautogui
import csv
import pandas as pd
import pyperclip
import inspect, os, platform, random
import unicodedata

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

service = Service(executable_path = '크롬 드라이버 설치 경로 입력')
driver = webdriver.Chrome(service = service, options = chrome_options)
driver.implicitly_wait(1)
driver.maximize_window()

driver.implicitly_wait(10)
driver.get('https://www.instagram.com')
time.sleep(3)


def login(yourid, yourpw):
    username_input = driver.find_element(By.CSS_SELECTOR, "input[name='username']")
    password_input = driver.find_element(By.CSS_SELECTOR, "input[name='password']")
    time.sleep(10)

    username_input.send_keys(yourid)
    password_input.send_keys(yourpw)
    time.sleep(10)


    login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    login_button.click()
    time.sleep(5)


    later_button = driver.find_element(By.CSS_SELECTOR, "._ac8f")
    later_button.click()
    time.sleep(5)

    later_button = driver.find_element(By.CSS_SELECTOR, "._a9--._a9_1")
    later_button.click()
    time.sleep(5)

def detect_ad():
    ad_list = ['재테크', '투자', '부업', '집테크', '고수입', '수입', '억대연봉', '억대', '연봉', '순수익', '초기금액', '초기 금액', '금액', '입금']
    article = driver.find_elements(By.XPATH, '//article//div[1]/span')
    for texts in article :
        text = unicodedata.normalize('NFC',texts.get_attribute('innerText'))
        for ad in ad_list :
            if text.find(ad) == -1 :
                continue
            else :
                print(f'광고 발견. 발견된 광고단어 : {ad}')
                return True

def like_follow(tag):
    like_number = 0 
    follow_number = 0
    followed_count = 50
    comment = "피드 잘 보고 가요~~!!"
    driver.get('https://www.instagram.com/explore/tags/{}/'.format(tag))
    time.sleep(5)
    
    first_feed = driver.find_element(By.CSS_SELECTOR, '._aagu')
    first_feed.click()
    time.sleep(5)
 
    
    for _ in range(followed_count): 
        if detect_ad() == True:
            next_button_variable = "span svg[aria-label='다음']"
            next_feed = driver.find_element(By.CSS_SELECTOR, next_button_variable)
            next_feed.click() 
            time.sleep(random.uniform(4.0, 6.0))
            driver.implicitly_wait(15)
        
        else:
            print('광고 없는 게시물 입니다.')

        try:
            like_button_selector = "span svg[aria-label='좋아요']"
            first_like_button = driver.find_element(By.CSS_SELECTOR, like_button_selector)
            first_like_button.click()
            like_number += 1
            print('좋아요를 {}번째 눌렀습니다.'.format(like_number))
            print("좋아요 버튼 클릭 성공")
            time.sleep(10)


        except Exception as e: 
            print("좋아요 버튼을 클릭할 수 없음:", str(e))
            print('이미 작업한 피드입니다.')           
            time.sleep(10)

        try:
            first_follow_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '._aacl._aaco._aacw._aad6._aade')))
            if first_follow_button.text  == '팔로우':
                first_follow_button.click()
                follow_number += 1
                print('팔로우를 {}번째 눌렀습니다.'.format(follow_number))
                print('팔로우 버튼 클릭 성공')
                time.sleep(random.uniform(65.0, 95.0))

                comment_input = driver.find_element_by_css_selector('textarea[aria-label="댓글 달기..."]')
                comment_input.send_keys(comment)
                driver.find_element_by_xpath('//button[text()="게시"]').click()

            else: 
                print('이미 작업한 피드입니다.')          
                time.sleep(random.uniform(65.0, 95.0))

        except NoSuchElementException as e:
            print("버튼을 찾을 수 없음", e)

        except ElementClickInterceptedException as e:
            print('팔로우 버튼 클릭이 차단되었습니다:', e)

        except Exception as e:
            print("오류 발생", e)
        
            

        
        if _ < followed_count-1 :
            next_button_variable = "span svg[aria-label='다음']"
            next_feed = driver.find_element(By.CSS_SELECTOR, next_button_variable)
            next_feed.click() 
            time.sleep(random.uniform(4.0, 6.0))
            driver.implicitly_wait(15)

        else:          
            time.sleep(10)

    print("좋아요 팔로우 작업완료")

login('본인아이디입력', '본인비밀번호입력')
skip_keywords = ['광고', '재테크', '투자', '부업', '집테크', '고수입', '수입', '억대연봉', '억대', '연봉', '순수익', '초기금액'] 

while True :
    tags = ['재테크', '사업', '고양이', '강아지', '남자', '여자','아이', '아이돌' ] 
    for tag in tags:
        try : 
            print(f'이번 작업 태그는 {tag}')
            like_follow(tag)
            print(f'{tag} 태그 좋아요 팔로우 진행 중')
        except Exception as e:
            print('다음 태그로 넘어갑니다.', e)
        driver.refresh()
        time.sleep(10)

driver.quit()
            

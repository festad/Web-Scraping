import re
import requests
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


ELEARNING_LOGIN = 'https://elearning.unibs.it/login/index.php'

VIDEO_ICON      = 'https://elearning.unibs.it/theme/image.php/classic/kalvidres/1628237874/icon'
VIDEO_ICON_EASY = 'https://elearning.unibs.it/theme/image.php/classic/core/1628237874/f/mpeg-24'

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
REFERER = 'null'
HOST = 'elearning.unibs.it'
HEADERS = {'User-Agent':USER_AGENT, 'Referer': REFERER, 'Host': HOST}


def initialize_driver():
    return webdriver.Chrome()

def authentication(driver, username=None, password=None):
    if username == None or password == None:
        username = input('Enter your username\n-> ')
        password = input('Enter your password\n-> ')
    driver.get(ELEARNING_LOGIN)
    # Input username
    driver.find_element(By.XPATH, "//input[@id='username']").send_keys(username)
    # Input password
    driver.find_element(By.XPATH, "//input[@id='password']").send_keys(password)
    driver.find_element(By.XPATH, "//button[@class='btn btn-primary']").click()
    return driver
    
def course_analysis(driver, course_link=None, course_name=None):
    if course_link == None:
        course_link = input('Enter the course link\n-> ')
        course_name = input('Enter the course name\n-> ')
        course_name = str.lower(course_name)
        course_name = re.sub(r"( |,|-|:)+", "-", course_name)

    driver.get(course_link)
    imgs = [img.get_attribute('src') for img in driver.find_elements(By.XPATH, "//a[@class='aalink']/img")]
    elements = [element.get_attribute('href') for element in driver.find_elements(By.XPATH, "//a[@class='aalink']")]
    videos_wannabe = zip(imgs, elements)
    videos = [(v[0], v[1]) for v in videos_wannabe if v[0] == VIDEO_ICON or v[0] == VIDEO_ICON_EASY]
    n = len(videos)
    for k, v in enumerate(videos):
        print(f"=> Downloading {k+1}/{n}... -> {v} ...")
        download_item(driver, v[1], k, v[0], course_name)
        print("=> Done!")
            
def download_item(driver, href, counter, video_icon, course_name=None):
    if course_name == None:
        course_name = 'null'
        
    if video_icon == VIDEO_ICON:
        driver.get(href)
        driver.switch_to.frame(driver.find_element(By.TAG_NAME, 'iframe'))
        driver.switch_to.frame(driver.find_element(By.TAG_NAME, 'iframe'))
        video = driver.find_element(By.XPATH, '//video[@id="pid_kplayer"]')
        download_file(video.get_attribute('src'), f'{course_name}-{counter+1}.mp4')
    elif video_icon == VIDEO_ICON_EASY:
        print('EASY')
        driver.get(href)
        src = driver.find_element(By.XPATH, '//video/source').get_attribute('src')
        headers = HEADERS
        headers['Referer'] = href
        cookies = {}
        for c in driver.get_cookies():
            cookies[c['name']] = c['value']
        print('COOKIES ARE\n', cookies)
        # It looks like it works only when cookies are present,
        # whereas headers' presence is not necessary.
        download_file(src, f'{course_name}-{counter+1}.mp4', headers=headers, cookies=cookies)
    
def download_file(url, name, headers=None, cookies=None):
    r = requests.get(url, headers=headers, cookies=cookies, stream=True)
    with open(f'{name}', 'wb') as f:
        for byte_chunk in r.iter_content(chunk_size=4096):
            f.write(byte_chunk)
    
driver = initialize_driver()
authentication(driver)
course_analysis(driver)
driver.quit()
        

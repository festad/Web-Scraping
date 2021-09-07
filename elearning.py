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
VIDEO_ICON = 'https://elearning.unibs.it/theme/image.php/classic/kalvidres/1628237874/icon'

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
    # links = driver.find_elements(By.XPATH, "//a[@class='aalink']/span")
    elements = [element.get_attribute('href') for element in driver.find_elements(By.XPATH, "//a[@class='aalink']")]
    # for e in zip(imgs, links, elements):
    videos = [v[1] for v in zip(imgs, elements) if v[0] == VIDEO_ICON]
    n = len(videos)
    for k, v in enumerate(videos):
        print(f"=> Downloading {k+1}/{n}... -> {v} ...")
        try:
            download_item(driver, v, k, course_name)
        except Exception as e:
            print(e)
        print("=> Done!")
            
def download_item(driver, href, counter, course_name=None):
    if course_name == None:
        course_name = 'null'

    driver.get(href)
    driver.switch_to.frame(driver.find_element(By.TAG_NAME, 'iframe'))
    driver.switch_to.frame(driver.find_element(By.TAG_NAME, 'iframe'))
    video = driver.find_element(By.XPATH, '//video[@id="pid_kplayer"]')
    download_file(video.get_attribute('src'), f'{course_name}-{counter+1}.mp4')
    
def download_file(url, name):
    r = requests.get(url, stream=True)
    with open(f'{name}', 'wb') as f:
        for byte_chunk in r.iter_content(chunk_size=4096):
            f.write(byte_chunk)
    
driver = initialize_driver()
authentication(driver)
course_analysis(driver)
driver.quit()
        

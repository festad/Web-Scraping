import sys
from pathlib import Path
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


def find_lectures(teacher):
    result = ''
    for i in range(3):
        result += find_lectures_of_year(i+1, teacher)
    print(result)
    

def find_lectures_of_year(year, teacher):
    driver_exe = str(Path.home()/Path('chromedriver_linux64', 'chromedriver'))
    driver = webdriver.Chrome(driver_exe)
    driver.get(f'https://corsi.unibo.it/laurea/LingueLetteratureStraniere/orario-lezioni?anno={year}')
    WebDriverWait(driver, 40).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'button')))
    for btn in driver.find_elements_by_tag_name('button'):
        if 'month' in btn.get_attribute('class'):
            month_btn = btn
    action_chain = ActionChains(driver)
    action_chain.send_keys([Keys.ARROW_DOWN for i in range(15)])
    action_chain.move_to_element(month_btn)
    action_chain.click(month_btn)
    action_chain.perform()
    WebDriverWait(driver, 40).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'fc-list-item')))
    soup = BeautifulSoup(driver.page_source, 'lxml')
    result = ''
    for doc in soup.find_all(attrs={'class':'docente'}):
        if teacher in doc.text:
            date_tag = doc.parent.parent.find_previous_sibling(attrs={'class':'fc-list-heading'}).td.span.text
            hour = doc.parent.find_previous_sibling(attrs={'class':'time'}).text
            result += f'{doc.text[9:]} (year {year}) on {date_tag} at {hour}\n'
    result += '~~~~~~~~~~~~~~~~~~~~~~~~~~\n'
    # result += '~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n'
    driver.quit()
    return result


def main():
    if len(sys.argv) < 2:
        print('Insert (at least part of) the name of the teacher you are looking for')
        print("Otherwise you get all the teachers' timetable")
        find_lectures('')
    else:
        find_lectures(sys.argv[1])


if __name__ == '__main__':
    main()

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from downloader import get_firefox_driver


def find_lectures(teacher):
    driver = get_firefox_driver()
    result = ''
    for i in range(3):
        result += find_lectures_of_year(i + 1, teacher, driver)
    driver.quit()
    # print(result)


def find_lectures_of_year(year, teacher, driver):
    url = f'https://corsi.unibo.it/laurea/LingueLetteratureStraniere/orario-lezioni?anno={year}'
    print(url)
    driver.get(url)
    # time.sleep(5)
    WebDriverWait(driver, 40).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'button')))
    driver.execute_script("$('.fc-monthSwitch-button').click()")
    # month_btn = driver.find_element_by_xpath( \
    #    "//button[@type='button'][@class='fc-monthSwitch-button']")
    # print(len(month_btn))
    # action_chain = ActionChains(driver)
    # action_chain.send_keys([Keys.ARROW_DOWN for i in range(10)])
    # action_chain.move_to_element(month_btn)
    # action_chain.click(month_btn)
    # action_chain.perform()
    WebDriverWait(driver, 40).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'fc-list-item')))
    # driver.implicitly_wait(40)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    print(f'Retrieving data for year {year}')
    result = ''
    for doc in soup.find_all(attrs={'class': 'docente'}):
        if teacher in doc.text:
            date_tag = doc.parent.parent.find_previous_sibling(attrs={'class': 'fc-list-heading'}).td.span.text
            hour = doc.parent.find_previous_sibling(attrs={'class': 'time'}).text
            result += f'{doc.text[9:]} (year {year}) on {date_tag} at {hour}\n'
    result += '~~~~~~~~~~~~~~~~~~~~~~~~~~\n'
    print(result)
    return result


def execution():
    print('Insert the name you want to look for,'
          '\n  "E" to exit,'
          '\n  "ALL" to find every name.')
    query = input("-> ")
    if query.lower() == 'e':
        print('Exit...')
        return 0
    elif query.lower() == 'all':
        find_lectures('')
        return 1
    else:
        find_lectures(query)
        return 1


def main():
    while execution():
        print('OK')


if __name__ == '__main__':
    main()

from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import datetime



options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
options.add_argument("--headless=new")
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
chrome_prefs = {}
options.experimental_options["prefs"] = chrome_prefs
chrome_prefs["profile.default_content_settings"] = {"images": 2}



s = Service(r'/home/aliak/PycharmProjects/PythonWebScrapingApp')
driver = webdriver.Chrome(options=options, service=s)
url = 'https://www.audible.com/adblbestsellers?ref=a_search_t1_navTop_pl0cg1c0r0&pf_rd_p=08b836ae-73e5-4c8c-9a3d-71c5be252964&pf_rd_r=ZNXG43V5WJE2YVR6S9ZE&pageLoadId=O8Tyoo0fTtw0vevA&creativeId=1642b4d1-12f3-4375-98fa-4938afc1cedc'

driver.get(url)

# pagination
pagination = driver.find_element(By.XPATH, value='//ul[contains(@class,"pagingElements")]')
pages = pagination.find_elements(By.TAG_NAME, value='li')


last_page = len(pages)-1
current_page = 1

book_title = []
book_author = []
book_length = []
while current_page <= last_page:
    # time.sleep(2)
    container = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'adbl-impression-container')))
    # container = driver.find_element(By.CLASS_NAME, value='adbl-impression-container ')
    products = WebDriverWait(container, 5).until(EC.presence_of_all_elements_located((By.XPATH, '//li[contains(@class, "productListItem")]')))
    # products = container.find_elements(By.XPATH, '//li[contains(@class, "productListItem")]')

    for product in products:
        book_title.append(product.find_element(By.XPATH, './/h3[contains(@class , "bc-pub-break-word")]').text)
        book_author.append(product.find_element(By.XPATH, './/li[contains(@class ,"authorLabel")]').text)
        book_length.append(product.find_element(By.CLASS_NAME, "runtimeLabel").text)

    current_page = current_page+1

    next_page_button = driver.find_element(By.XPATH, value='//span[contains(@class ,  "nextButton")]')
    driver.implicitly_wait(10)
    ActionChains(driver).move_to_element(next_page_button).click(next_page_button).perform()


driver.quit()

df_books = pd.DataFrame({'title': book_title, 'author': book_author, 'length': book_length})
df_books.to_csv('books_pagination.csv', index=False)
print(df_books)

def main():
    try:
        # Getting the current time upto seconds only.
        cur_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print('Current Time : ',cur_time)
    except:
        print('Something Wrong in main function',exc_info=True)

if __name__=='__main__':
    main()

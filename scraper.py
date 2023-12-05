from selenium import webdriver
from selenium.webdriver.common.by import By
import datetime

# Стартовая страница
website = 'https://www.s-vfu.ru/universitet/rukovodstvo-i-struktura/instituty/imi/news/?PAGEN_1=1'
cService = webdriver.ChromeService(executable_path='./chromedriver.exe')
driver = webdriver.Chrome(service=cService)
#driver.get(website)

# Кол-во страниц
#pages = int(driver.find_element(By.XPATH, "//*[@id='content']/div[2]/div/ul/li[6]/a/span").get_attribute('innerText'))
pages = 28
#print('pages: ' + str(pages))

# Получаем url страниц самих новостей
#articles = driver.find_elements(By.XPATH, "//*[@id='content']/div[1]/div")
#article = driver.find_element(By.XPATH, "//*[@id='content']/div[1]/div[2]/article/a[1]").get_attribute('href')

def scrape_all():
    current_page = website
    for i in range(1, pages):
        current_page = current_page.replace('?PAGEN_1=' + current_page[-1], '?PAGEN_1=' + str(i))
        driver.get(current_page)
        articles = driver.find_elements(By.XPATH, "//*[@id='content']/div[1]/div")
        for j in range(2, len(articles)):
            #scrape_article(articles[i].find_element(By.XPATH, '//article/a[1]').get_attribute('href'))
            scrape_article(article = driver.find_element(By.XPATH, "//*[@id='content']/div[1]/div["+str(j)+"]/article/div[1]/a[1]").get_attribute('href'))
            driver.get(current_page)

def scrape_article(article):
    driver.get(article)

    # Получаем нужные данные (титульник, текст, изображения, если они присутствуют)
    title = driver.find_element(By.XPATH, "/html/head/title").get_attribute('innerText')
    print(title)

    if driver.find_elements(By.XPATH, "//*[@id='content']/section"):
        title_image = driver.find_element(By.XPATH, "//*[@id='content']/section").get_attribute("style").replace('background-image: url("', '').replace('");', '')
        title_image = "https://www.s-vfu.ru" + title_image
        print(title_image)

    text = driver.find_elements(By.XPATH, "//*[@id='content']/article/div/p")
    for i in range(len(text)):
        print(text[i].get_attribute('innerText'))

    images = driver.find_elements(By.XPATH, "//*[@id='content']/div/div/div")
    if images:
        for i in range(len(images)):
            print(images[i].find_element(By.TAG_NAME, 'a').get_attribute('href'))

def scrape_all_min():
    current_page = website
    for i in range(1, pages):
        current_page = current_page.replace('?PAGEN_1=' + current_page[-1], '?PAGEN_1=' + str(i))
        driver.get(current_page)
        articles = driver.find_elements(By.XPATH, "//*[@id='content']/div[1]/div")
        for j in range(2, len(articles)):
            image = driver.find_elements(By.XPATH, "//*[@id='content']/div[1]/div["+str(j)+"]/article/a/img")
            if image:
                print(image[0].get_attribute('src'))

            title = driver.find_elements(By.XPATH, "//*[@id='content']/div[1]/div["+str(j)+"]/article/div/h3/a")
            if title:
                print(title[0].get_attribute('innerText'))

            else:
                title = driver.find_elements(By.XPATH, "//*[@id='content']/div[1]/div["+str(j)+"]/article/h3/a")
                if title:
                    print(title[0].get_attribute('innerText'))

                else:
                    title = "No title"
                    print(title)

            date = driver.find_element(By.XPATH, "//*[@id='content']/div[1]/div["+str(j)+"]/article/figcaption/a").get_attribute('innerText')
            print(date)

            url = driver.find_element(By.XPATH, "//*[@id='content']/div[1]/div["+str(j)+"]/article/div/a").get_attribute('href')
            print(url)

def scrape_today():
    #time_now = datetime.datetime.now()
    time_now = datetime.datetime.strptime('27.11.2023 16:00:00', '%d.%m.%Y %H:%M:%S')
    current_page = website
    for i in range(1, pages):
        current_page = current_page.replace('?PAGEN_1=' + current_page[-1], '?PAGEN_1=' + str(i))
        driver.get(current_page)
        articles = driver.find_elements(By.XPATH, "//*[@id='content']/div[1]/div")
        urls = []
        titles = []
        for j in range(2, len(articles)):
            article = driver.find_element(By.XPATH, "//*[@id='content']/div[1]/div["+str(j)+"]/article/div[1]/a[1]").get_attribute('href')
            driver.get(article)
        
            date = driver.find_element(By.XPATH, "//*[@id='content']/article/ul/li[2]/kbd").get_attribute('innerText')
            date_datetime = datetime.datetime.strptime(date, '%d.%m.%Y %H:%M:%S')

            if (time_now >= date_datetime and time_now.day != date_datetime.day):
                print('urls',urls)
                print('titles',titles)
                return urls, titles
            
            urls.append(article)
            
            if driver.find_elements(By.XPATH, "//*[@id='content']/section"):
                title_image = driver.find_element(By.XPATH, "//*[@id='content']/section").get_attribute("style").replace('background-image: url("', '').replace('");', '')
                title_image = "https://www.s-vfu.ru" + title_image
                #print(title_image)

            title = driver.find_element(By.XPATH, "/html/head/title").get_attribute('innerText')
            titles.append(title)
            #print(title)
            driver.get(current_page)

#scrape_all()
#scrape_all_min()
#scrape_today()

driver.quit()
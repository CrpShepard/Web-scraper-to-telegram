from selenium import webdriver
from selenium.webdriver.common.by import By

# Стартовая страница
website = 'https://www.s-vfu.ru/universitet/rukovodstvo-i-struktura/instituty/imi/news/?PAGEN_1=1'
driver = webdriver.Chrome()
driver.get(website)

# Кол-во страниц
pages = int(driver.find_element(By.XPATH, "//*[@id='content']/div[2]/div/ul/li[6]/a/span").get_attribute('innerText'))
print(str(pages))

# Получаем url страниц самих новостей
article = driver.find_element(By.XPATH, "//*[@id='content']/div[1]/div[2]/article/a[1]").get_attribute('href')
driver.get(article)

# Получаем нужные данные (титульник, текст, изображения, если они присутствуют)
title = driver.find_element(By.XPATH, "/html/head/title").get_attribute('innerText')
print(title)

title_image = driver.find_element(By.XPATH, "//*[@id='content']/section").get_attribute("style").replace('background-image: url(', '').replace(');', '')
print(title_image)

text = driver.find_elements(By.XPATH, "//*[@id='content']/article/div/p")
for i in range(len(text)):
    print(text[i].get_attribute('innerText'))

images = driver.find_elements(By.XPATH, "//*[@id='content']/div/div/div")
if images:
    for i in range(len(images)):
        print(images[i].find_element(By.TAG_NAME, 'a').get_attribute('href'))

driver.quit()
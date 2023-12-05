import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

from selenium import webdriver
from selenium.webdriver.common.by import By
import datetime

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot_token = open("bot_token", "r")
bot = Bot(token=bot_token.read())
# Диспетчер
dp = Dispatcher()

urls = []
titles = []

website = 'https://www.s-vfu.ru/universitet/rukovodstvo-i-struktura/instituty/imi/news/?PAGEN_1=1'
cService = webdriver.ChromeService(executable_path='./chromedriver.exe')
driver = webdriver.Chrome(service=cService)

def scrape_today():
    #time_now = datetime.datetime.now()
    time_now = datetime.datetime.strptime('27.11.2023 16:00:00', '%d.%m.%Y %H:%M:%S')
    current_page = website
    for i in range(1, 28):
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

# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Hello!")

@dp.message(Command("startscrape"))
async def cmd_start(message: types.Message):
    global urls, titles
    urls, titles = scrape_today()

@dp.message(Command("scraperesult"))
async def cmd_start(message: types.Message):
    await message.answer(str(titles[0]) + '\n' + str(urls[0]))


# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

driver.quit()
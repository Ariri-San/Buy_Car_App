from asgiref.sync import async_to_sync, sync_to_async
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from PIL import Image
import time
import asyncio


def check_login(webdriver):
    try:
        user_name = webdriver.find_element(By.CSS_SELECTOR, "#root > div > div.wrapper.d-flex.flex-column.min-vh-100.bg-light > div.header.header-sticky.mb-4 > div:nth-child(1) > ul:nth-child(4) > li:nth-child(2) > div > span").text
        return [user_name, True]
    except:
        user_name = webdriver.find_element(By.CSS_SELECTOR, "#root > div > div.wrapper.d-flex.flex-column.min-vh-100.bg-light > div.header.header-sticky.mb-4 > div:nth-child(1) > ul:nth-child(4) > li:nth-child(2) > div > button > span").text
        return [user_name, False]


def get_captcha(driver, element, path, move_x = 0, move_y = 0, resize = 1):
    # now that we have the preliminary stuff out of the way time to get that image :D
    location = element.location
    size = element.size
    # saves screenshot of entire page
    driver.save_screenshot(path)

    # uses PIL library to open image in memory
    image = Image.open(path)

    left = location['x'] + move_x
    top = location['y'] + move_y
    right = location['x'] +  (resize * size['width']) + move_x
    bottom = location['y'] + (resize * size['height']) + move_y

    image = image.crop((left, top, right, bottom))  # defines crop points
    image.save(path, 'png')  # saves new cropped image


async def send_image(buy_car):
    options = webdriver.ChromeOptions()
    options.add_argument('ignore-certificate-errors')

    browser = webdriver.Chrome(options=options)

    browser.get('https://esale.ikd.ir/login')
    
    await asyncio.sleep(20)
    
    browser.close()


    

sem = asyncio.Semaphore(4)


async def safe_send_image(buy_car):
    async with sem:  # semaphore limits num of simultaneous downloads
        return await send_image(buy_car)


# async def main(buy_cars):
#       # await moment all downloads done


async def send_images(buy_cars):
    loop = asyncio.get_event_loop()
    tasks = [
        asyncio.ensure_future(safe_send_image(i))  # creating task starts coroutine
        for i
        in range(12)
    ]
    await asyncio.gather(*tasks)
    
    # loop = asyncio.get_event_loop()
    
    # for buy_car in buy_cars:
    #     loop.create_task(send_image(buy_car))


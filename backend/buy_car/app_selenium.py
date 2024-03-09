from django.core.files import File
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from PIL import Image
import time
import asyncio
from .models import Captcha


def check_login(webdriver):
    try:
        user_name = webdriver.find_element(By.CSS_SELECTOR, "#root > div > div.wrapper.d-flex.flex-column.min-vh-100.bg-light > div.header.header-sticky.mb-4 > div:nth-child(1) > ul:nth-child(4) > li:nth-child(2) > div > span").text
        return [user_name, True]
    except:
        user_name = webdriver.find_element(By.CSS_SELECTOR, "#root > div > div.wrapper.d-flex.flex-column.min-vh-100.bg-light > div.header.header-sticky.mb-4 > div:nth-child(1) > ul:nth-child(4) > li:nth-child(2) > div > button > span").text
        return [user_name, False]


def login(browser, username, password, code):
    # try:
        username_element = browser.find_element(By.NAME, "userName")
        username_element.clear()
        username_element.send_keys(username)

        password_element = browser.find_element(By.NAME, "password")
        password_element.clear()
        password_element.send_keys(password)

        captcha_element = browser.find_element(By.NAME, "captchaText")
        captcha_element.clear()
        captcha_element.send_keys(code)
        
        button = browser.find_element(By.CSS_SELECTOR, "#root > div > div.wrapper.d-flex.flex-column.min-vh-100.bg-light > div.body.flex-grow-1.px-0 > div > div > div > div.row.justify-content-center > div > div > div.card.p-12 > div > form > div > div > div:nth-child(4) > button")
        button.click()
        
        return True
    # except:
    #     return False


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
    
    image.close()
    
    # captcha = Captcha.objects.create(buy_car_id=id, image=open(path))
    # captcha.image = File(image)
    # await captcha.asave()
    
    
    # return image
    


async def save_image(buy_car):
    options = webdriver.ChromeOptions()
    options.add_argument('ignore-certificate-errors')

    browser = webdriver.Chrome(options=options)

    browser.get('https://esale.ikd.ir/login')
    
    await asyncio.sleep(5)
    
    
    username, is_login = check_login(browser)
    
    
    print(is_login)
    print(buy_car)
    
    captch_image_element = browser.find_element(By.CSS_SELECTOR, "#root > div > div.wrapper.d-flex.flex-column.min-vh-100.bg-light > div.body.flex-grow-1.px-0 > div > div > div > div.row.justify-content-center > div > div > div.card.p-12 > div > form > div > div > div:nth-child(3) > div > span > img")
    captcha_image = await get_captcha(browser, captch_image_element, '../image_captcha/image.pngs', buy_car["id"], 98, 85, 1.4)
    
    await asyncio.sleep(5)
    
    browser.close()
    
    # return captcha_image




sem = asyncio.Semaphore(4)
async def safe_save_image(buy_car):
    async with sem:  # semaphore limits num of simultaneous downloads
        return await save_image(buy_car)



async def save_images(buy_cars):
    tasks = [
        asyncio.ensure_future(safe_save_image(buy_car))  # creating task starts coroutine
        for buy_car
        in buy_cars
    ]
    return await asyncio.gather(*tasks)



def save_image2(buy_car, browser):
    time.sleep(5)
    
    username, is_login = check_login(browser)
    
    
    print(is_login)
    print(buy_car)
    
    captch_image_element = browser.find_element(By.CSS_SELECTOR, "#root > div > div.wrapper.d-flex.flex-column.min-vh-100.bg-light > div.body.flex-grow-1.px-0 > div > div > div > div.row.justify-content-center > div > div > div.card.p-12 > div > form > div > div > div:nth-child(3) > div > span > img")
    captcha_image = get_captcha(browser, captch_image_element, '../image_captcha/image.png', buy_car["id"], 98, 85, 1.4)
    
    time.sleep(5)
    
    browser.close()
    
    # return captcha_image


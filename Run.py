import time
import threading
import asyncio
import warnings

from faker import Faker
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.opera.options import Options
from webdriver_manager.opera import OperaDriverManager

warnings.filterwarnings('ignore')
fake = Faker('en_IN')
MUTEX = threading.Lock()

# Use OperaDriverManager to get the executable_path
executable_path = OperaDriverManager().install()
print(executable_path)


def sync_print(text):
    with MUTEX:
        print(text)


async def get_driver():
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-notifications')
    options.add_experimental_option('w3c', True)
    
    # Use OperaDriverManager to get the executable_path
    executable_path = OperaDriverManager().install()

    # Use webdriver.Opera instead of webdriver.Chrome
    driver = webdriver.Opera(executable_path=executable_path, options=options)
    return driver


async def driver_wait(driver, locator, by, secs=10, condition=ec.element_to_be_clickable):
    wait = WebDriverWait(driver=driver, timeout=secs)
    element = await wait.until(condition((by, locator)))
    return element


async def start(name, user, passcode, wait_time):
    await sync_print(f"{name} started!")
    driver = await get_driver()  # Use await for asynchronous calls
    await driver.get(f'https://zoom.us/wc/join/{meetingcode}')
    await asyncio.sleep(10)
    inp = await driver.find_element(By.XPATH, '//input[@type="text"]')
    await asyncio.sleep(1)
    await inp.send_keys(f"{user}")
    await asyncio.sleep(5)

    inp2 = await driver.find_element(By.XPATH, '//input[@type="password"]')
    await asyncio.sleep(2)
    await inp2.send_keys(passcode)

    # Click the "Join" button using JavaScript
    join_button = await driver.find_element(By.XPATH, '//button[contains(@class,"preview-join-button")]')
    await driver.execute_script("arguments[0].click();", join_button)

    try:
        query = '//button[text()="Join Audio by Computer"]'
        mic_button_locator = await driver_wait(driver, query, By.XPATH, secs=350)
        await mic_button_locator.click()
        print(f"{name} mic aayenge.")
    except Exception as e:
        print(f"{name} mic nahe aayenge. ", e)

    await sync_print(f"{name} sleep for {wait_time} seconds ...")
    while wait_time > 0:
        await asyncio.sleep(1)
        wait_time -= 1
    await sync_print(f"{name} ended!")
    driver.quit()  # Quit the driver after the task has completed


async def main():
    wait_time = sec * 60
    tasks = []

    for i in range(number):
        try:
            proxy = proxylist[i]
        except Exception:
            proxy = None
        try:
            user = fake.name()
        except IndexError:
            break
        task = asyncio.create_task(start(f'[Thread{i}]', user, passcode, wait_time))
        tasks.append(task)

    await asyncio.gather(*tasks)


if __name__ == '__main__':
    number = int(input("Enter number of Users: "))
    meetingcode = input("Enter meeting code (No Space): ")
    passcode = input("Enter Password (No Space): ")
    sec = 60
    try:
        asyncio.run(main())
    except:
        pass
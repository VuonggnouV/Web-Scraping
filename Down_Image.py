from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os
import imghdr
import requests

driver = webdriver.Chrome()
driver.maximize_window()
driver.get('https://images.google.com/')
key='Italy T1 declaration form'

search_box = driver.find_element(By.NAME, 'q')
search_box.send_keys(key)
search_box.send_keys(Keys.RETURN)
time.sleep(5)

os.makedirs(key, exist_ok=True)

downloaded_count = 1


# XPath
for i in range(1, 500000000000):  
    try:
        container_xpath = f"""//*[@id="rso"]/div/div/div[1]/div/div/div[{i}]"""

        driver.find_element(By.XPATH, container_xpath).click()
        time.sleep(3)

        preview_image_xpath = container_xpath
        preview_image_element = driver.find_element(By.XPATH, preview_image_xpath)
        preview_image_url = preview_image_element.get_attribute("src")

        time_started = time.time()
        while True:
            image_element = driver.find_element(By.XPATH, """//*[@id="Sva75c"]/div[2]/div[2]/div[2]/div[2]/c-wiz/div/div/div/div/div[3]/div[1]/a/img[1]""")
            image_url = image_element.get_attribute('src')

            if image_url != preview_image_url:
                break
            else:
                current_time = time.time()
                if current_time - time_started > 10:
                    print("Timeout! Will download a lower resolution image and move onto the next one")
                    break
        response = requests.get(image_url)
        if response.status_code == 200:
            image_type = imghdr.what(None, h=response.content)
            if image_type and image_type not in ['gif', 'webp', 'svg']:
                with open(f'{key}/{key}_{downloaded_count}.{image_type}', 'wb') as handler:
                    handler.write(response.content)
                print(f"Downloaded image {downloaded_count}")
                downloaded_count += 1

        else:
            print(f"Failed to download image {downloaded_count}. Status code: {response.status_code}")

    except Exception as e:
        print(f"Could not download image : {e}")
        
    if downloaded_count == 21:
        break

driver.quit()

#//*[@id="Sva75c"]/div[2]/div[2]/div[2]/div[2]/c-wiz/div/div/div/div/div[3]/div[1]
#//*[@id="Sva75c"]/div[2]/div[2]/div[2]/div[2]/c-wiz/div/div/div/div/div[3]/div[1]
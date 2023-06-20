import time, requests, os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def count_files_in_folder(folder_path):
    """
    Find the count how many image files are available in pexels_images folder.
    """
    if not os.path.isdir(folder_path):
        print(f"Error: {folder_path} is not a valid directory.")
        return

    file_count = 0
    for _, _, files in os.walk(folder_path):
        file_count += len(files)

    return file_count


def download_img():
    folder_path = "pexels_images"
    file_count = count_files_in_folder(folder_path)

    if file_count==None:
        file_count = 1
    else:
        file_count = file_count + 1

    # Set up Chrome options
    chrome_options = Options()

    # Set up the ChromeDriver manager
    webdriver_service = Service(ChromeDriverManager().install())

    # Choose a suitable driver
    driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)

    # Open the URL
    url = 'https://www.pexels.com/search/india/'
    driver.get(url)

    # Scroll down to the end of the page to load more images
    SCROLL_PAUSE_TIME = 2  # Adjust the pause time as needed
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Extract image URLs
    image_tags = driver.find_elements(By.CLASS_NAME, "ButtonGroup_buttons__kI2YT")

    os.makedirs('pexels_images', exist_ok=True)

    for index, img in enumerate(image_tags):
        image_url = img.find_element(By.TAG_NAME, "a").get_attribute("href")

        image_name = f"img-{file_count}.jpg"
        image_path = os.path.join('pexels_images', image_name)

        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            #   "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
            "Cache-Control": "max-age=0",
            "Cookie": "_hjSessionUser_171201=eyJpZCI6ImQ0ZDY1ZDQzLWFlNGMtNWY5Zi04ZDk5LTFjZDIyYWNhN2Y4MSIsImNyZWF0ZWQiOjE2NzY2MzUxNTY3MzEsImV4aXN0aW5nIjp0cnVlfQ==; _gid=GA1.2.449371973.1686886008; country-code-v2=IN; ab.storage.deviceId.5791d6db-4410-4ace-8814-12c903a548ba=%7B%22g%22%3A%22a2e289b1-c489-3dc9-e470-d304e81d7f91%22%2C%22c%22%3A1676635166073%2C%22l%22%3A1686886008913%7D; _gaexp=GAX1.2.1VpyvgBTS92HmGkHsuGgmA.19616.1; _fbp=fb.1.1686886018976.1554397966; ab.storage.sessionId.5791d6db-4410-4ace-8814-12c903a548ba=%7B%22g%22%3A%229e082a69-37d7-e560-13de-0374a348e10e%22%2C%22e%22%3A1686887825262%2C%22c%22%3A1686886008912%2C%22l%22%3A1686886025262%7D; OptanonConsent=isGpcEnabled=0&datestamp=Fri+Jun+16+2023+09%3A25%3A00+GMT%2B0530+(India+Standard+Time)&version=202301.1.0&isIABGlobal=false&hosts=&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1&AwaitingReconsent=false; _ga=GA1.1.387164516.1676635156; g_state={\"i_p\":1686974107189,\"i_l\":2}; __cf_bm=hyl4G.sPoi1mGudagTY5c5.CUBxdN8ftp5hSoa2SwOY-1686893343-0-AQ/uyH8tKqLrfqbN2xJo//50qseaEZgpcaUyAUWrwDm4DDNEZwEdnndLwel8lf/EDW17Nq8oEzZ6GJH6dr0szfI=; _sp_ses.9ec1=*; _ga_8JE65Q40S6=GS1.1.1686893532.3.0.1686893532.0.0.0; _sp_id.9ec1=9abe5352-ee09-446b-a34e-47d5aa2b126b.1676635156.4.1686893540.1686887704.e67e4015-9cf9-4076-b819-53ae0e5ca528.f459b596-a235-41ab-8a5f-161cbe59fb32.3722f360-8cb5-4ce6-ad7c-156d0cca3f26.1686893520402.21",
            "Sec-Ch-Ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"",
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": "\"Linux\"",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
            }

        # Download the image
        response = requests.get(image_url, headers=headers)
        with open(image_path, 'wb') as f:
            f.write(response.content)
            print(f'Saved image: {image_name}')
            file_count += 1

    # Close the browser
    driver.quit()

from datetime import datetime

if __name__ == "__main__":
    download_img()

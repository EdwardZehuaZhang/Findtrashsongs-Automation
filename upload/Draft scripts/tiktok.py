import os
import pickle
import random
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import subprocess

def random_sleep(min_sec, max_sec):
    time.sleep(random.uniform(min_sec, max_sec))

def read_description(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def load_cookies(driver, cookies_file):
    driver.get("https://www.tiktok.com/login")
    with open(cookies_file, 'rb') as file:
        cookies = pickle.load(file)
        for cookie in cookies:
            driver.add_cookie(cookie)
    driver.refresh()

def upload_video(driver, video_path, description):    
    # Go to the TikTok studio upload page
    driver.get("https://www.tiktok.com/tiktokstudio/upload?from=creator_center")

    try:
        iframe = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'iframe[data-tt="Upload_index_iframe"]'))
        )
        driver.switch_to.frame(iframe)

        upload_button = WebDriverWait(driver, 1130).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Select video']"))
        )
        upload_button.click()
        time.sleep(3)
    except Exception as e:
        print("Cant find ifrmae or create button click failed:", e)
        
    try:
        upload_button = WebDriverWait(driver, 1130).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Select video']"))
        )
        upload_button.click()
        time.sleep(3)
    except Exception as e:
        print("Create button click failed:", e)

    
    # Find the file input element and click to open the file dialog
    try:
        # Run the AutoIt script to handle the file upload dialog
        autoit_script_path = os.path.join(os.getcwd(), "upload.au3")
        if not os.path.isfile(autoit_script_path):
            print(f"AutoIt script not found at path: {autoit_script_path}")
            return
        result = subprocess.call([r"D:\\Program Files (x86)\\AutoIt3\\AutoIt3.exe", autoit_script_path])
        print(f"AutoIt script execution result: {result}")
        if result != 0:
            print("AutoIt script execution failed.")
    except Exception as e:
        print("File input send keys failed:", e)
        return

    # Interact with the contenteditable div
    try:
        driver.switch_to.default_content()  # Switch back to the default content
        iframe = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'iframe[data-tt="Upload_index_iframe"]'))
        )
        driver.switch_to.frame(iframe)
        print('Switched to iframe again')

        editable_div = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div[contenteditable='true']"))
        )
        actions = ActionChains(driver)
        actions.move_to_element(editable_div).click().perform()
        print('Clicked on contenteditable div')
        
        actions.key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).send_keys(Keys.DELETE)
        actions.send_keys(description)
        actions.perform()
    except Exception as e:
        print("Interaction with contenteditable div failed:", e)
    
    # Wait for the "Uploaded" element
    try:
        uploaded_text = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, "//span[text()='Uploaded']"))
        )
        print("Uploaded text found:", uploaded_text)
    except Exception as e:
        print("Failed to find 'Uploaded' text:", e)
        return

    # Click the "发布" (Post) button
    try:
        post_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'TUXButton') and .//div[text()='Post']]"))
        )
        print("Post button found:", post_button)
        post_button.click()
    except Exception as e:
        print("Post sharing failed:", e)
        return

    # Wait for the success message and close the browser
    try:
        WebDriverWait(driver, 120).until(
            EC.presence_of_element_located((By.XPATH, "//div[text()='Your video has been uploaded']"))
        )
        print("Upload success message detected. Closing the browser.")
    except Exception as e:
        print("Failed to detect upload success message:", e)

def main():
    username = "findtrashsongs"
    password = "Tr@shMus1c"
    video_path = "D:\\Adobe Files\\Premiere Files\\findtrashsongs\\Sequence 01.mp4"
    description_file_path = "D:\\Adobe Files\\Premiere Files\\findtrashsongs\\Song Description.txt"
    cookies_file = "tiktok_cookies.pkl"
    
    # Read the description from the file
    description = read_description(description_file_path)
    
    # Set the working directory
    working_directory = "D:\\Coding Files\\Python\\findtrashsongs auto upload"
    os.chdir(working_directory)
    
    # Set up the undetected ChromeDriver with a custom user-agent
    options = uc.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    driver = uc.Chrome(options=options, driver_executable_path="C:\\Users\\edwar\\Documents\\chromedriver-win64\\chromedriver.exe")
    
    try:
        load_cookies(driver, cookies_file)
        upload_video(driver, video_path, description)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()

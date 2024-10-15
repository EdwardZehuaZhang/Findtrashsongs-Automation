import os
import pickle
import random
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def random_sleep(min_sec, max_sec):
    time.sleep(random.uniform(min_sec, max_sec))

def remove_non_bmp_characters(text):
    return ''.join(c for c in text if ord(c) <= 0xFFFF)

def read_description(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return remove_non_bmp_characters(text)


def load_cookies(driver, cookies_file):
    driver.get("https://www.instagram.com/")
    with open(cookies_file, 'rb') as file:
        cookies = pickle.load(file)
        for cookie in cookies:
            driver.add_cookie(cookie)
    driver.refresh()

def dismiss_notifications_popup(driver):
    try:
        not_now_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, '_a9--') and contains(@class, '_ap36') and contains(@class, '_a9_1') and text()='Not Now']"))
        )
        not_now_button.click()
    except Exception as e:
        print("No 'Turn on Notifications' popup appeared or click failed:", e)

def upload_video(driver, video_path, description):
    # Dismiss the notifications pop-up if it appears
    dismiss_notifications_popup(driver)
    
    # Click the "Create" button using the text locator
    try:
        create_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Create']"))
        )
        create_button.click()
        print("Create button clicked")
    except Exception as e:
        print("Create button click failed:", e)
        return
    
    # Find the file input element and upload the video
    try:
        file_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//input[@type="file"]'))
        )
        file_input.send_keys(video_path)
        print("File input found and video path set")
    except Exception as e:
        print("File input send keys failed:", e)
        return
    
    # Dismiss OK pop-up if it appears
    try:
        OK_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='OK']"))
        )
        OK_button.click()
        print("OK button clicked")
    except Exception as e:
        print("OK button click failed:", e)

    # Select crop option
    try:
        crop_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//*[name()='svg' and @aria-label='Select crop']"))
        )
        crop_button.click()
        print("Select crop button clicked")

        portrait_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//*[name()='svg' and @aria-label='Crop portrait icon']"))
        )
        portrait_button.click()
        print("Portrait button clicked")
    except Exception as e:
        print("Crop selection failed:", e)

    # Click next buttons and share
    try:
        next_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//*[name()='div' and text()='Next']"))
        )
        next_button.click()
        print("First Next button clicked")

        next_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//*[name()='div' and text()='Next']"))
        )
        next_button.click()
        print("Second Next button clicked")

        description_input = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//*[name()='div' and @aria-label='Write a caption...']"))
        )
        description_input.send_keys(description)
        print("Description input set")

        share_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//*[name()='div' and text()='Share']"))
        )
        share_button.click()
        print("Share button clicked")
    except Exception as e:
        print("Post sharing failed:", e)
        return
    
    # Wait for the success message and close the browser
    try:
        WebDriverWait(driver, 120).until(
            lambda driver: driver.execute_script("""
                var spans = document.querySelectorAll('span');
                for (var i = 0; i < spans.length; i++) {
                    if (spans[i].innerText.includes('Your reel has been shared.')) {
                        return true;
                    }
                }
                return false;
            """)
        )
        print("Upload success message detected. Closing the browser.")
    except Exception as e:
        print("Failed to detect upload success message:", e)

def main():
    username = "findtrashsongs"
    password = "Tr@shMus1c"
    video_path = "D:\\Adobe Files\\Premiere Files\\findtrashsongs\\Sequence 01.mp4"
    description_file_path = "D:\\Adobe Files\\Premiere Files\\findtrashsongs\\Song Description.txt"
    cookies_file = "instagram_cookies.pkl"
    
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

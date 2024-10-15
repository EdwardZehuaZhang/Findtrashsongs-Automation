import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver

def upload_video():
    try:
        # Set up Chrome options
        options = uc.ChromeOptions()
        options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 DuckDuckGo/7 Safari/605.1.15")

        # Initialize Chrome driver
        driver = uc.Chrome(options=options, driver_executable_path="C:\\Users\\edwar\\Documents\\chromedriver-win64\\chromedriver.exe")
        
        # Open Snapchat login page
        driver.get('https://my.snapchat.com/')

        # Click the "Sign in" button
        sign_in_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Sign in')]"))
        )
        sign_in_button.click()

        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//a[text()='Use phone number instead']"))
        )
        print("Use phone message detected.")

        webdriver.ActionChains(driver).send_keys("findtrashsongs").send_keys(Keys.RETURN).perform()

        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//p[text()='findtrashsongs']"))
        )
        print("Name detected.")

        webdriver.ActionChains(driver).send_keys("Tr@shMus1c").send_keys(Keys.RETURN).perform()

        file_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file'][accept='video/mp4,video/quicktime,video/webm,image/jpeg,image/png']"))
        )
        video_path = "D:\\Adobe Files\\Premiere Files\\findtrashsongs\\Sequence 01.mp4"
        file_input.send_keys(video_path)
        time.sleep(10)

        post_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div/main/div[2]/div[2]/div[2]/div[5]/div[1]/div[1]/div/div[2]/div/div/div/div[1]/div/div/div/div[1]"))
        )
        post_button.click()

        with open("D:\\Adobe Files\\Premiere Files\\findtrashsongs\\Song Description.txt", 'r') as file:
            description = file.readline().strip()
        
        description_textarea = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//textarea[@placeholder='Add a description and #topics']"))
        )
        description_textarea.send_keys(description)
        
        # Agree to Spotlight Terms
        agree_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Agree to Spotlight Terms')]"))
        )
        agree_button.click()

        # Accept the terms
        accept_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[2]/div/div[2]/div[3]/div/button[2]"))
        )
        accept_button.click()

        # Click the final "Post to Snapchat" button
        post_final_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Post to Snapchat')]"))
        )
        post_final_button.click()

        # Wait for a few seconds to ensure the process completes        
    except Exception as e:
        print(f"An error occurred: {e}")

    try:
        WebDriverWait(driver, 120).until(
            EC.presence_of_element_located((By.XPATH, "//div[text()='Yay! Your post is now live!']"))
        )
        print("Upload success message detected. Closing the browser.")
    except Exception as e:
        print("Failed to detect upload success message:", e)

    finally:
        driver.quit()


if __name__ == "__main__":
    upload_video()

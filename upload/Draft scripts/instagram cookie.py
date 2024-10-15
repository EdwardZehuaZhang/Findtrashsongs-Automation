import pickle
import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def random_sleep(min_sec, max_sec):
    time.sleep(random.uniform(min_sec, max_sec))

def login_to_instagram_and_save_cookies(driver, username, password, cookies_file):
    driver.get("https://www.instagram.com/")
    random_sleep(3, 6)
    
    username_input = driver.find_element(By.NAME, 'username')
    password_input = driver.find_element(By.NAME, 'password')
    
    username_input.send_keys(username)
    random_sleep(1, 2)
    password_input.send_keys(password)
    random_sleep(1, 2)
    password_input.send_keys(Keys.RETURN)
    
    random_sleep(5, 8)  # Wait for login to complete

    # Save cookies to a file
    with open(cookies_file, 'wb') as file:
        pickle.dump(driver.get_cookies(), file)

def main():
    username = "findtrashsongs"
    password = "Tr@shMus1c"
    cookies_file = "instagram_cookies.pkl"
    
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        login_to_instagram_and_save_cookies(driver, username, password, cookies_file)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()

import pickle
import random
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def random_sleep(min_sec, max_sec):
    time.sleep(random.uniform(min_sec, max_sec))

def login_to_tiktok_and_save_cookies(driver, username, password, cookies_file):
    driver.get("https://www.tiktok.com/login")
    random_sleep(3, 6)
    
    random_sleep(50, 88)  # Wait for login to complete

    # Save cookies to a file
    with open(cookies_file, 'wb') as file:
        pickle.dump(driver.get_cookies(), file)

def main():
    username = "findtrashsongs"
    password = "Tr@shMus1c"
    cookies_file = "tiktok_cookies.pkl"
    
    options = uc.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    driver = uc.Chrome(options=options)
    
    try:
        login_to_tiktok_and_save_cookies(driver, username, password, cookies_file)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()

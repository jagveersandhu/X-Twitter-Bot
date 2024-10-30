from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

# Set the path to the EdgeDriver
driver_path = r'path_to_your_edge_driver'  # Replace with your EdgeDriver path
service = Service(driver_path)
driver = webdriver.Edge(service=service)

# Function to simulate typing with a delay
def human_type(element, text):
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.1, 0.3))  # Random delay between 0.1 to 0.3 seconds

# Login to Twitter
def login_to_twitter(username, password):
    try:
        driver.get("https://twitter.com/login")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "text")))

        # Enter username
        username_field = driver.find_element(By.NAME, "text")
        human_type(username_field, username)
        username_field.send_keys(Keys.RETURN)
        time.sleep(random.uniform(1.5, 2.5))  # Random delay after submitting username

        # Wait for the password field to appear
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "password")))

        # Enter password
        password_field = driver.find_element(By.NAME, "password")
        human_type(password_field, password)
        password_field.send_keys(Keys.RETURN)
        time.sleep(random.uniform(1.5, 2.5))  # Random delay after submitting password
        
        # Wait for the homepage to load by checking a known element on the homepage
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[@aria-label='Profile']")))
        print("Login successful")

    except Exception as e:
        print(f"An error occurred during login: {e}")
        time.sleep(10)  # Keep the browser open for 10 seconds if login fails for debugging

# Function to search for a hashtag and like all relevant tweets
def like_tweets_with_hashtag(hashtag):
    try:
        print(f"Searching for #{hashtag}...")
        driver.get(f"https://twitter.com/hashtag/{hashtag}?src=hashtag_click")
        time.sleep(3)  # Let the page load

        # Perform a single scroll to load tweets
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        # Locate tweet elements and interact with them one by one
        tweets = driver.find_elements(By.XPATH, "//article[@data-testid='tweet']")

        if not tweets:
            print("No tweets found for this hashtag.")
            return

        for tweet in tweets:
            try:
                # Scroll into view of each tweet
                driver.execute_script("arguments[0].scrollIntoView(true);", tweet)
                time.sleep(1)

                # Use an alternative method to locate the like button more reliably
                like_button = WebDriverWait(tweet, 10).until(
                    EC.visibility_of_element_located((By.XPATH, ".//div[@data-testid='like' or @data-testid='unlike']"))
                )
                
                # Ensure the like button is clickable
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, ".//div[@data-testid='like' or @data-testid='unlike']")))

                # Click the like button
                like_button.click()
                print("Liked a tweet.")
                time.sleep(random.uniform(1, 2))  # Random delay between likes
                
            except Exception as e:
                print(f"Error interacting with tweet's like button: {e}")
                # Retry mechanism if stale element or element is not found
                continue

    except Exception as e:
        print(f"Error in liking tweets with hashtag: {e}")

def main():
    # Replace with your actual username and password
    username = "your_username"  # Replace with your actual username
    password = "your_password"  # Replace with your actual password

    # Attempt login
    login_to_twitter(username, password)

    # Specify the hashtag to search for and like tweets
    like_tweets_with_hashtag("ElonMusk")  # Replace with your desired hashtag (without #)

    # Keep the browser open for 10 seconds after executing tasks
    time.sleep(10)

    # Close the browser
    driver.quit()

if __name__ == "__main__":
    main()
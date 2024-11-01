from selenium import webdriver
import pyautogui
import time

# Set up Edge options to connect to the running instance
options = webdriver.EdgeOptions()
options.add_experimental_option("debuggerAddress", "localhost:9222")

# Connect Selenium to the existing Edge instance
driver = webdriver.Edge(options=options)

def scroll_page():
    """Scroll down the page to load more tweets."""
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)  # Wait for new tweets to load

def click_like_buttons():
    """Click all visible like buttons."""
    print("Attempting to locate like buttons...")
    bar_locations = list(pyautogui.locateAllOnScreen('D:/twitter bot/full bar.png', confidence=0.6))  # Lowered confidence
    print(f"Found {len(bar_locations)} like buttons.")
    for bar_location in bar_locations:
        print(f"Liking button at: {bar_location}")  # Print location for debugging
        pyautogui.click(bar_location.left + bar_location.width / 2,
                        bar_location.top + bar_location.height / 2)
        time.sleep(1)  # Short delay between clicks

def search_and_like_tweets(hashtag):
    print(f"Searching for #{hashtag}...")
    driver.get(f"https://twitter.com/hashtag/{hashtag}?src=hashtag_click")
    time.sleep(3)  # Allow page to load initially

    max_likes = 50  # Set the maximum number of tweets to like
    liked_count = 0  # Initialize the liked tweets counter
    max_scrolls = 20  # Max scrolls to load more tweets
    current_scrolls = 0

    while liked_count < max_likes and current_scrolls < max_scrolls:
        # Scroll the page to load more tweets
        scroll_page()

        # Attempt to click all like buttons visible on the screen
        click_like_buttons()
        liked_count += len(pyautogui.locateAllOnScreen('D:/twitter bot/full bar.png', confidence=0.6))  # Count how many likes were performed
        current_scrolls += 1  # Increment the scroll count

# Call the function with your chosen hashtag
search_and_like_tweets("ElonMusk")

# Keep the browser open briefly to review results
time.sleep(10)
driver.quit()  # Close the browser















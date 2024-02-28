from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Create Chrome webdriver instance
driver = webdriver.Chrome()

# Open the YouTube video page
driver.get("https://www.youtube.com/watch?v=zSgx8U16stk")

# Wait for the element to be visible
like_button = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-watch-metadata/div/div[2]/div[2]/div/div/ytd-menu-renderer/div[1]/segmented-like-dislike-button-view-model/yt-smartimation/div/div/like-button-view-model/toggle-button-view-model/button-view-model/button/div[2]"))
)

# Extract the like count
like_count = like_button.text

print("Like count:", like_count)

# Close the browser
driver.quit()

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome()

driver.get("http://127.0.0.1:5000")

# Select stock
dropdown = driver.find_element(By.NAME, "ticker")
dropdown.send_keys("TCS.NS")

# Click Analyze button
driver.find_element(By.XPATH, "//button[contains(text(), 'Analyze')]").click()

time.sleep(5)  # wait for page to update

# Check result exists
result = driver.find_element(By.TAG_NAME, "body").text

print("RESULT:", result)

driver.quit()

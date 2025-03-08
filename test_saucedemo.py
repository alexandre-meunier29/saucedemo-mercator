from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time

chrome_options = Options()
#chrome_options.add_argument("--headless")  # Run in headless mode (no UI)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Navigate to the URL
driver.get("https://www.saucedemo.com/")

# Login
username_field = driver.find_element(By.ID, "user-name")
password_field = driver.find_element(By.ID, "password")
login_button = driver.find_element(By.ID, "login-button")


username_field.send_keys("standard_user")
password_field.send_keys("secret_sauce")
login_button.click()

time.sleep(2)

# Select the highest priced item
products = driver.find_elements(By.CLASS_NAME, "inventory_item")
highest_price_item = None
highest_price = 0

for product in products:
    price_element = product.find_element(By.CLASS_NAME, "inventory_item_price")
    price = float(price_element.text.replace('$', ''))  # Get price and convert it to float
    if price > highest_price:
        highest_price = price
        highest_price_item = product

# Add the highest priced item to the cart
add_to_cart_button = highest_price_item.find_element(By.CLASS_NAME, "btn_inventory")
add_to_cart_button.click()

# cart count
cart_button = driver.find_element(By.CLASS_NAME, "shopping_cart_link")
cart_count = cart_button.text  # Should be '1' after adding an item
print(f"Items in cart: {cart_count}")

time.sleep(2)

# Navigate to cart page

cart_button.click()

# Close browser
time.sleep(10)
driver.quit()

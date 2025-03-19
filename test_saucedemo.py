from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
from guara.transaction import AbstractTransaction, Application  # Corrected import


# Define Transactions
class NavigateToLoginPage(AbstractTransaction):
    def do(self, **kwargs):
        self._driver.get("https://www.saucedemo.com/")


class Login(AbstractTransaction):
    def do(self, username, password, **kwargs):
        username_field = self._driver.find_element(By.XPATH, "//input[@placeholder='Username']")
        password_field = self._driver.find_element(By.XPATH, "//input[@id='password']")
        login_button = self._driver.find_element(By.ID, "login-button")

        username_field.send_keys(username)
        password_field.send_keys(password)
        login_button.click()
        time.sleep(2)


class SelectHighestPricedItem(AbstractTransaction):
    def do(self, **kwargs):
        products = self._driver.find_elements(By.CLASS_NAME, "inventory_item")
        highest_price_item = None
        highest_price = 0

        for product in products:
            price_element = product.find_element(By.CLASS_NAME, "inventory_item_price")
            price = float(price_element.text.replace("$", ""))  # Get price and convert it to float
            if price > highest_price:
                highest_price = price
                highest_price_item = product

        return highest_price_item


class AddToCart(AbstractTransaction):
    def do(self, highest_price_item, **kwargs):
        add_to_cart_button = self._driver.find_element(By.CLASS_NAME, "btn_inventory")
        add_to_cart_button.click()


class CheckCartCount(AbstractTransaction):
    def do(self, **kwargs):
        cart_button = self._driver.find_element(By.CLASS_NAME, "shopping_cart_link")
        cart_count = cart_button.text  # Should be '1' after adding an item
        print(f"Items in cart: {cart_count}")
        return cart_count


class NavigateToCartPage(AbstractTransaction):
    def do(self, **kwargs):
        cart_button = self._driver.find_element(By.CLASS_NAME, "shopping_cart_link")
        cart_button.click()


# Main Script
if __name__ == "__main__":
    # Initialize WebDriver
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Run in headless mode (no UI)
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=chrome_options
    )

    # Initialize Application
    app = Application(driver)

    # Perform actions using the Page Transactions pattern
    app.at(NavigateToLoginPage)
    app.at(Login, username="standard_user", password="secret_sauce")
    highest_price_item = app.at(SelectHighestPricedItem)
    app.at(AddToCart, highest_price_item=highest_price_item)
    cart_count = app.at(CheckCartCount)
    app.at(NavigateToCartPage)

    # Wait for 10 seconds before closing the browser
    time.sleep(10)

    # Close the browser
    driver.quit()

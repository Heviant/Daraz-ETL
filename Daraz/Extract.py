from datetime import datetime
import sqlite3
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def search_daraz_for_product():
    # Initialize Chrome driver using webdriver-manager
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    # Initialize default values for product details
    product_name = "N/A"
    product_price = "N/A"
    product_rating = "No Rating"
    product_count = "0 Reviews"

    # Initialize an empty list to store error logs
    error_logs = []
    try:
        # 1. Open Daraz
        try:
            driver.get("https://www.daraz.com.np")
        except Exception as e:
            error_msg = f"Error occurred while opening Daraz: {e}"
            print(error_msg)
            error_logs.append(error_msg)

        # Optional: Maximize browser window
        driver.maximize_window()
        
        # 2. Wait for the search input box to be present and locate it
        # Daraz's main search input uses ID="q"
        try:
            search_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "q"))
            )
        except Exception as e:
            error_msg = f"Error locating search box: {e}"
            print(error_msg)
            error_logs.append(error_msg)

        # 3. Type the product name and press Enter
        search_box.send_keys("TANGZU WANER 2 Red Lion Bass Edition")
        search_box.send_keys(Keys.RETURN)
        
 
        # 4. Extract product elements (e.g., product names and prices) 
        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@data-qa-locator='product-item']//a"))
            ).click()
        except Exception as e:
            error_msg = f"Error clicking on product image: {e}"
            print(error_msg)
            error_logs.append(error_msg)

        # print(driver.current_url)
        # driver.save_screenshot("debug.png") # Check what Selenium actually sees
        try:
            product_elements_price = WebDriverWait(driver,10).until(
                EC.visibility_of_element_located((By.XPATH, "//div[@id='module_product_price_1']//span"))
            )
            product_price = product_elements_price.text
        except Exception as e:
            error_msg = f"Error locating product price: {e}"
            print(error_msg)
            error_logs.append(error_msg)

        try:
            product_elements_name =  WebDriverWait(driver,10).until(
            EC.visibility_of_element_located((By.XPATH, "//div[@id='module_product_title_1']//h1"))
        )
            product_name = product_elements_name.text
        except Exception as e:
            error_msg = f"Error locating product name: {e}"
            print(error_msg)
            error_logs.append(error_msg)
            

        try:
            review_element = WebDriverWait(driver,10).until(
                EC.visibility_of_element_located((By.XPATH, "//div[@id='module_product_review']"))
            )
            driver.execute_script("arguments[0].scrollIntoView();", review_element)
                  
            try:
                product_elements_rating = WebDriverWait(driver,10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "div.score span.score-average"))
                )
                product_rating = product_elements_rating.text
            except Exception as e:
                error_msg = f"Error locating product rating: {e}"
                print(error_msg)
                error_logs.append(error_msg)
                product_rating = "No Rating"
                

            try:
                product_elements_count = WebDriverWait(driver,10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "div.count"))
                )
                product_count = product_elements_count.text
            except Exception as e:
                error_msg = f"Error locating product count: {e}"
                print(error_msg)
                error_logs.append(error_msg)
                product_count = "0 Reviews"

        except Exception as e:
                    print(f"Warning: Review section could not be loaded or scrolled to: {e}")
            

        print(product_name)
        print(product_price)
        print(product_rating)
        print(product_count)
        save_product_to_db(product_name, product_price, product_rating, product_count)
        print("Successfully searched Daraz for the product!")
        
        # Keep browser open for a few seconds to view results (remove in production)
        import time
        time.sleep(5)
        
    finally:
        if error_logs:
            with open("scraper_errors.log", "a", encoding="utf-8") as log_file:
                log_file.write(f"\n--- Run on {datetime.now()} ---\n")
                for err in error_logs:
                    log_file.write(err + "\n")
        # Close the browser
        driver.quit()

# def load_product_details_from_file(product_name, product_price, product_rating, product_count):
#     try:
#         with open('product_details.txt', "a", encoding="utf-8") as file:
#             file.write(product_name + ",")
#             file.write(product_price + ",")
#             file.write(product_rating + ",")
#             file.write(product_count)
#     except Exception as e:
#         print(f"Error saving product details to file: {e}")
#         return "N/A", "N/A", "No Rating", "0 Reviews"

def save_product_to_db(product_name, product_price, product_rating, product_count):
    conn = sqlite3.connect("daraz_tracker.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS raw_daraz_prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            product_name TEXT,
            price TEXT,
            rating TEXT,
            review_count TEXT
        )
    """)
    conn.commit()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO raw_daraz_prices (timestamp, product_name, price, rating, review_count)
        VALUES (?, ?, ?, ?, ?)
    """, (current_time, product_name, product_price, product_rating, product_count))

    # 4. Commit the changes and close the connection
    conn.commit()
    conn.close()

    print("Data successfully saved to SQLite database!")


if __name__ == "__main__":
    search_daraz_for_product()
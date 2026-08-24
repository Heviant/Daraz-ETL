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
    
    try:
        # 1. Open Daraz
        try:
            driver.get("https://www.daraz.com.np")
        except Exception as e:
            print(f"Error occurred while opening Daraz: {e}")

        # Optional: Maximize browser window
        driver.maximize_window()
        
        # 2. Wait for the search input box to be present and locate it
        # Daraz's main search input uses ID="q"
        try:
            search_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "q"))
            )
        except Exception as e:
            print(f"Error locating search box: {e}")
            
        
        # 3. Type the product name and press Enter
        search_box.send_keys("TANGZU WANER 2 Red Lion Bass Edition")
        search_box.send_keys(Keys.RETURN)
        
 
        # 4. Extract product elements (e.g., product names and prices) 
        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@data-qa-locator='product-item']//a"))
            ).click()
        except Exception as e:
            print(f"Error clicking on product image: {e}")
            

        # print(driver.current_url)
        # driver.save_screenshot("debug.png") # Check what Selenium actually sees
        try:
            product_elements_price = WebDriverWait(driver,10).until(
                EC.visibility_of_element_located((By.XPATH, "//div[@id='module_product_price_1']//span"))
            )
            product_price = product_elements_price.text
        except Exception as e:
            print(f"Error locating product price: {e}")
            

        try:
            product_elements_name =  WebDriverWait(driver,10).until(
            EC.visibility_of_element_located((By.XPATH, "//div[@id='module_product_title_1']//h1"))
        )
            product_name = product_elements_name.text
        except Exception as e:
            print(f"Error locating product name: {e}")
              

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
                print(f"Error locating product rating: {e}")
                product_rating = "No Rating"
                

            try:
                product_elements_count = WebDriverWait(driver,10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "div.count"))
                )
                product_count = product_elements_count.text
            except Exception as e:
                print(f"Error locating product count: {e}")
                product_count = "0 Reviews"

        except Exception as e:
                    print(f"Warning: Review section could not be loaded or scrolled to: {e}")
            

        print(product_name)
        print(product_price)
        print(product_rating)
        print(product_count)

        print("Successfully searched Daraz for the product!")
        
        # Keep browser open for a few seconds to view results (remove in production)
        import time
        time.sleep(5)
        
    finally:
        # 5. Close the browser
        driver.quit()

if __name__ == "__main__":
    search_daraz_for_product()
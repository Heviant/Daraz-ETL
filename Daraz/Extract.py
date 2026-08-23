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
        driver.get("https://www.daraz.com.np")
        
        # Optional: Maximize browser window
        driver.maximize_window()
        
        # 2. Wait for the search input box to be present and locate it
        # Daraz's main search input uses ID="q"
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "q"))
        )
        
        # 3. Type the product name and press Enter
        search_box.send_keys("TANGZU WANER 2 Red Lion Bass Edition")
        search_box.send_keys(Keys.RETURN)
        
        # 4. Wait for the search results page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "search"))
        )
        
        print("Successfully searched Daraz for the product!")
        
        # Keep browser open for a few seconds to view results (remove in production)
        import time
        time.sleep(5)
        
    finally:
        # 5. Close the browser
        driver.quit()

if __name__ == "__main__":
    search_daraz_for_product()
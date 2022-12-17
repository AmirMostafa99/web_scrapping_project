import selenium
import openpyxl
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

url="https://www.amazon.com"
PATH = "C:\Program Files\drivers\chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.get(url)
driver.maximize_window()


search_box = driver.find_element(By.ID,value="twotabsearchtextbox")
search_box.clear()
search_box.send_keys("dell laptops")
driver.find_element(By.ID,value="nav-search-submit-button").click()
driver.find_element(By.XPATH,value="//span[text()='Dell']").click()


laptop_name = []
laptop_price = []
no_reviews = []
final_list = []

last_page_number=int(driver.find_element(By.XPATH,value="//a[@class='s-pagination-item s-pagination-button']").text)
print(last_page_number)
laptops = driver.find_elements(By.XPATH,value='//div[@data-component-type="s-search-result"]')
for _ in range(1,last_page_number,1):
    for laptop in laptops: 
        
        names =laptop.find_elements(By.XPATH,value=".//span[@class='a-size-medium a-color-base a-text-normal']")
        for name in names:
            laptop_name.append(name.text)
            
        try:
            if len(laptop.find_elements(By.XPATH,value=".//span[@class='a-price-whole']"))>0:
                prices= laptop.find_elements(By.XPATH,value=".//span[@class='a-price-whole']")
                for price in prices:
                    laptop_price.append(price.text+'$')
            else:
                laptop_price.append("0")
        except:
            pass
        reviews = laptop.find_elements(By.XPATH,value=".//span[@class='a-size-base s-underline-text']")
        
        try:
            if len(laptop.find_elements(By.XPATH,value=".//span[@class='a-size-base s-underline-text']"))>0:
                reviews = laptop.find_elements(By.XPATH,value=".//span[@class='a-size-base s-underline-text']")
                for review in reviews:
                    no_reviews.append(review.text)
            else:
                no_reviews.append("0")
        except:
            pass
            
    new_page=driver.find_element(By.XPATH,value="//a[@class='s-pagination-item s-pagination-next s-pagination-button s-pagination-separator']")
    new_page.click()

driver.quit()
print('laptops==>',len(laptop_name))
print('prices==>',len(laptop_price))
print('reviews==>',len(no_reviews))

df = pd.DataFrame(zip(laptop_name,laptop_price,no_reviews),columns=['laptop Name','laptop Price','laptop Reviews']) 
df.to_excel(r"F:\level 3\تدريب ميداني\المشروع\Web Scraping  Amazon Products Web Scraping Using Selenium from, Python to Excel  Part - 14\live_laptop.xlsx",index=False)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def extract_price(url, contract_code):
    price_idx = -1
    price = 0
    driver = webdriver.Firefox()
    driver.get(url)
    for row in driver.find_elements(By.CSS_SELECTOR, "tr"):
        for index, cell in enumerate(row.find_elements(By.TAG_NAME, "td")):
            if cell.text == contract_code:
                price_idx = index - 3
            if index == price_idx:
                price = cell.text
                driver.close()
                return price

"""
url = "file:///home/justin/bid-extractor/schmitz.html"
corn_price = extract_price(url, "Dec-21")
print(f"Schmitz Corn Price is {corn_price}")

bean_price = extract_price(url, "Jan-22")
print(f"Schmitz Corn Price is {bean_price}")
"""

url = "file:///home/justin/Desktop/bids/2021-11-19-Elevator_Bids.html"
bean_price = extract_price(url, "Jan-22")
value_num = int(float(bean_price) * 100)
print(f"Elevator Corn Price is {value_num}")

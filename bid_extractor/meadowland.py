from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def extract_price(url, contract_code):
    price_idx = -1
    price = 0
    driver = webdriver.Firefox()
    driver.get(url)
    print(driver.title)
    for row in driver.find_elements_by_css_selector("tr"):
        for index, cell in enumerate(row.find_elements_by_tag_name("td")):
            # print(f"{index} - {cell.text}")
            if cell.text == contract_code:
                price_idx = index + 3
            if index == price_idx:
                price = cell.text  # float(str(cell.text.strip()))
                driver.close()
                return price


bean_url = "https://www.meadowlandfarmerscoop.com/index.cfm?show=11&mid=3&theLocation=9&layout=1046"
bean_price = extract_price(bean_url, "@S2F")
print(f"Meadowland Bean Price is {bean_price}")

corn_url = "https://www.meadowlandfarmerscoop.com/index.cfm?show=11&mid=3&theLocation=7&layout=1046"
corn_price = extract_price(corn_url, "@C1Z")
print(f"Meadowland Corn Price is {corn_price}")

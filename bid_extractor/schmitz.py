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
                price_idx = index - 3
            if index == price_idx:
                price = cell.text  # float(str(cell.text.strip()))
                driver.close()
                return price


url = "file:///home/justin/bid-extractor/schmitz.html"
corn_price = extract_price(url, "Dec-21")
print(f"Schmitz Corn Price is {corn_price}")

bean_price = extract_price(url, "Jan-22")
print(f"Schmitz Corn Price is {bean_price}")

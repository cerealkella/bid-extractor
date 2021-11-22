import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def next_month(date):
    numerical_month = date.strftime("%-m")
    three_days_more = date + datetime.timedelta(days=+2)
    if int(numerical_month) != int(three_days_more.strftime("%-m")):
        return three_days_more.strftime("%b").lower()
    else:
        return "xxx"


def extract_price(url, bid_date):
    print(f"""Extracting prices from {bid_date.strftime("%Y-%m-%d")}""")
    contract_month = bid_date.strftime("%b").lower()
    contract_month_year = f"{contract_month}-{bid_date.strftime('%y')}"
    next_mon = next_month(bid_date)
    price_idx = -1
    price = 0
    commodity_price = {"corn": 0, "soybeans": 0}
    counter = 0
    driver = webdriver.Firefox()
    driver.get(url)
    for row in driver.find_elements(By.CSS_SELECTOR, "tr"):
        for index, cell in enumerate(row.find_elements(By.TAG_NAME, "td")):
            if (
                cell.text.lower() == contract_month
                or cell.text.lower() == f"fh {contract_month}"
                or cell.text.lower() == contract_month_year
                or cell.text.lower() == bid_date.strftime('%B').lower()[:4]
                or cell.text.lower() == f"{bid_date.strftime('%B').lower()[:4]}-{bid_date.strftime('%y')}"
                or cell.text.lower() == "sept - oct 5"
            ):
                price_idx = index + 1
            elif next_mon != "xxx":
                if next_mon == "jan":
                    next_mon_year = f"{next_mon}-{int(bid_date.strftime('%y'))+1}"
                else:
                    next_mon_year = f"{next_mon}-{bid_date.strftime('%y')}"
                if (
                    cell.text.lower() == next_mon
                    or cell.text.lower() == next_mon_year
                ):
                    price_idx = index + 1
            if index == price_idx:
                price = cell.text
                counter += 1
                if counter == 1:
                    print(f"Found Corn Price -> {price}")
                    commodity_price["corn"] = int(float(price)*100)
                    # Resetting price index, need to loop through once more
                    price_idx = -1
                elif counter > 1:
                    print(f"Found Soybean Price -> {price}")
                    commodity_price["soybeans"] = int(float(price)*100)
                    driver.close()
                    return commodity_price
    driver.close()
    print("---------------------------------------")
    print(f"""Failed to extract prices for {bid_date.strftime("%Y-%m-%d")}""")
    print("---------------------------------------")

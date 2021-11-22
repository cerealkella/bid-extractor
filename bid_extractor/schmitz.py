import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .database_interface import create_connection, enter_grain_bids
from .local_settings import DATABASE


def next_month(date):
    numerical_month = date.strftime("%-m")
    three_days_more = date + datetime.timedelta(days=+3)
    if int(numerical_month) != int(three_days_more.strftime("%-m")):
        return three_days_more.strftime("%b").lower()
    else:
        return "xxx"


def extract_price(url, bid_date):
    print(f"""Extracting prices from {bid_date.strftime("%Y-%m-%d")}""")
    contract_month = bid_date.strftime("%b").lower()
    contract_month_year = f"{contract_month}-{bid_date.strftime('%y')}"
    next_mon = next_month(bid_date)
    print(f"next_mon = {next_mon}")
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
                or cell.text.lower() == contract_month_year
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
                    commodity_price["corn"] = float(price)
                    # Resetting price index, need to loop through once more
                    price_idx = -1
                elif counter > 1:
                    print(f"Found Soybean Price -> {price}")
                    commodity_price["soybeans"] = float(price)
                    driver.close()
                    return commodity_price
    driver.close()
    print("---------------------------------------")
    print(f"""Failed to extract prices for {bid_date.strftime("%Y-%m-%d")}""")
    print("---------------------------------------")


bid_date = datetime.date(2021, 11, 12)
url = "file:///home/justin/Desktop/bids/2021-11-12-Elevator_Bids.html"
# url = "https://www.meadowlandfarmerscoop.com/index.cfm?show=11&mid=3&theLocation=7&layout=1046"
price = extract_price(url, bid_date)
print(price)
# value_num = int(float(corn_price) * 100)
# print(f"Elevator Corn Price is {value_num}")


"""
conn = create_connection(DATABASE)
ins = enter_grain_bids(conn, "corn", '2021-11-19 18:00:00', value_num)
print(ins)
"""

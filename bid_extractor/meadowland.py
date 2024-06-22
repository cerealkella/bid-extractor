import codecs
import os
import datetime
from selenium import webdriver
import wget
from .local_settings import DOWNLOAD_FOLDER


NOW = datetime.datetime.now()
TODAY = NOW.strftime("%Y-%m-%d")

def get_cashbid_csv():
    print(f"{NOW} - Saving Meadowland Cash Bids CSV file...")
    url = "https://meadsprout2.agricharts.com/markets/cashbid-download.php"
    wget.download(url, out=os.path.join(DOWNLOAD_FOLDER,f"{TODAY}-Meadowland.csv"), bar=None)


def get_cashbid_html():
    driver = webdriver.Firefox()
    driver.implicitly_wait(0.5)
    #launch URL
    url = "https://meadowlandfarmerscoop.com/#cash-bids"
    driver.get(url)
    #get file path to save page
    n=os.path.join(DOWNLOAD_FOLDER,f"{TODAY}-Meadowland.html")
    #open file in write mode with encoding
    print(f"{NOW} - Saving Meadowland Cash Bids HTML file...")
    f = codecs.open(n, "w", "utf−8")
    #obtain page source
    h = driver.page_source
    #write page source content to file
    f.write(h)
    #close browser
    driver.quit()


get_cashbid_csv()
get_cashbid_html()

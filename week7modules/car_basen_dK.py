import bs4
import pandas as pd
import argparse


from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Car_basen_dK():

    def fetch_website(self, url):
        options = Options()
        options.headless = True
        browser = webdriver.Firefox(options=options)
        browser.get(url)
        browser.implicitly_wait(5)
        return browser

    def bil_basen_search(self, browser, searchstring):

        popup_button = browser.find_elements_by_id("onetrust-accept-btn-handler")
        try:
            popup_button[0].click()
            sleep(1)
        except:
            print("something went wrong")

        browser.find_element_by_xpath('//*[@id="freetext-search-area"]/div/div/div[1]/form/div/div/input').send_keys(searchstring)
        browser.find_element_by_xpath('//*[@id="inline-search-collapse"]/form/div[4]/div[3]/div[1]/label').click()
        browser.find_element_by_xpath('//*[@id="freetext-search-area"]/div/div/div[1]/form/div/span/button').click()
        browser.implicitly_wait(3)
        return bs4.BeautifulSoup(browser.page_source, "html.parser")


    def read_bil_basen(self, data):
        priceresults = []
        kmresults = []
        carnames = []
        carhrefs = []

        self.read_car_lines(data, "row listing listing-plus bb-listing-clickable", priceresults, kmresults)
        self.read_car_lines(data, "row listing listing-discount bb-listing-clickable", priceresults, kmresults)

        names = data.find_all('a', {'class' : 'listing-heading darkLink'})
        for name in names:
            carnames.append(name.text)
            carhrefs.append(name.get("href"))

        data = {'Name' : carnames, 'Kmdriven' : kmresults, 'Price' : priceresults, 'Href' : carhrefs}
        df = pd.DataFrame(data)
        df = df[df.Price != 'Ring']
        df = df[pd.to_numeric(df["Kmdriven"]) > 0]

        df['Priceperkilometer'] = df['Price'].str.replace(r'\D', '').astype(int) / df['Kmdriven'].str.replace(r'\D', '').astype(int)
        return df

    def read_car_lines(self, data, searchstring, priceresults, kmresults):
        for outerdiv in data.find_all('div', {'class': searchstring}):
            for innerdiv in outerdiv.find_all('div', {'class' : 'row'}):
                datadiv = innerdiv.find_all('div', {'class': 'col-xs-2 listing-data'})
                if len(datadiv) !=0:
                    kmresults.append(datadiv[1].text)
                datadiv = innerdiv.find_all('div', {'class': 'col-xs-3 listing-price'})
                if len(datadiv) != 0:
                    priceresults.append(datadiv[0].text)


    def find_cheapest_car(self, df):
        return df[df.Priceperkilometer == df.Priceperkilometer.min()]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='a program that can detect and list files')
    parser.add_argument("-ss",'--searchstring', help='What car name is used for search')

    args = parser.parse_args()
    if args.searchstring is not None:
        cbdk = Car_basen_dK()
        url = 'https://www.bilbasen.dk/'
        browser = cbdk.fetch_website(url)
        try:  
            data = cbdk.bil_basen_search(browser, args.searchstring)
            df = cbdk.read_bil_basen(data)  
            print(df)
            print("CHeapest car: ", cbdk.find_cheapest_car(df))
        except Exception as e: 
            print(e)
            browser.close()


 
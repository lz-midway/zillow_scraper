
from typing import List
import httpx
import json
from parsel import Selector
import re
import time
import csv
import copy
import threading
import random
import general as GENFUNC

import constants as CONST


class Scraper():
    def __init__(self, inputs, data_lock, info_lock):
        self.client = httpx.Client(
            # enable http2
            http2=True,
            # add basic browser like headers to prevent being blocked
            headers=CONST.headers
        )
        self.inputs = inputs
        self.data_lock = data_lock # mutex for accessing data/ directory
        self.info_lock = info_lock # mutex for accessing running info
        self.shut_down = False # for turning thread off
        
        self.page_regex = r'\d+_p\/'
        return
    
    # the code containing all steps of scraping
    def scraperThread(self):

        print("scraper started")

        scrape_now = True

        slept_cycle = 0

        # main loop
        while True:
            self.info_lock.acquire()
            if self.shut_down:
                self.info_lock.release()
                break
            self.info_lock.release()

            # when time to scrape
            if scrape_now:
                print("scrap now true")

                slept_cycle = 0

                try:
                    print("try scraping)")
                    results = []

                    self.inputs.lock.acquire()
                    areas = copy.copy(self.inputs.areas)
                    self.inputs.lock.release()

                    for area in areas:
                        results.append(self.scrape_location(area))
                    
                    self.data_lock.acquire()
                    for area, result in zip(areas, results):
                        self.convert_to_csv(CONST.DATA_DIRECTORY + GENFUNC.location_convert(area) + ".csv", result)
                    self.data_lock.release()

                    scrape_now = False

                    print("scrap now done")

                    self.inputs.lock.acquire()
                    self.inputs.to_change = True
                    self.inputs.lock.release()
                    
                except AssertionError:
                    print("blocked by website")

                    scrape_now = False

            else: # should not be scraping
                # other things
                print("scraper sleeping")
                time.sleep(CONST.SLEEP_CYCLE_TIME) # sleep since it is not time to scrape
                slept_cycle += 1
                if slept_cycle > CONST.SCRAPE_SLEEP_CYCLE:
                    scrape_now = True


        return
    
    # for starting the scraperThread(), returns the running thread for stopping
    def startThread(self):
        scrape_thread = threading.Thread(target=self.scraperThread, args=[])
        scrape_thread.start()
        
        return scrape_thread

    # location
    def scrape_location(self, location):

        more_pages = True # has more pages left
        pages = ""

        result = []

        location_url = GENFUNC.location_convert(location)
        url = CONST.main_url + location_url + "/"

        while more_pages:
            # get each page
            webpage = self.client.get(url + pages)

            print("processing pages " + location)

            assert webpage.status_code == 200, "request blocked"

            # extract json data from the page
            result, next_url = self.parse_json(webpage, result)

            # if there is next page, move to next page
            if next_url is None:
                more_pages = False
            else:
                pages = re.search(self.page_regex, next_url).group()

            time.sleep(random.randint(1, 4))

        return result
    

    def parse_json(self, webpage, result):
        # find the json data for properties
        selector = Selector(webpage.text)
        data = json.loads(selector.css("script#__NEXT_DATA__::text").get())
        houses_data = data["props"]["pageProps"]["searchPageState"]
        houses_list = houses_data["cat1"]["searchResults"]["listResults"]

        for house in houses_list:
            house_data = self.parse_json_house(house)
            result.append(house_data)

        next_url = None
        pagination = houses_data["cat1"]["searchList"]["pagination"]
        if pagination is not None and "nextUrl" in pagination.keys():
            next_url = pagination["nextUrl"]
        
        return result, next_url
    

    # parse individual property data for each house
    def parse_json_house(self, json_house):
        # access hdpData for info since it has the lot size
        hdpData = json_house["hdpData"]["homeInfo"]

        house_dict = dict()

        for key in CONST.fields_order:
            actual_key = CONST.fields[key]
            if actual_key in hdpData.keys():
                house_dict[key] = hdpData[actual_key]
            elif actual_key == "detailUrl":
                house_dict[actual_key] = json_house["detailUrl"]
            elif actual_key == "livingArea":
                house_dict[key] = 0
            else:
                house_dict[key] = None

        return house_dict
    

    # convert into CSVs
    def convert_to_csv(self, output, results):
        with open(output, "w") as csvfile:
            try:
                writer = csv.DictWriter(csvfile, fieldnames=CONST.fields_order)

                # writing headers (field names)
                writer.writeheader()

                # writing data rows
                writer.writerows(results)
            except FileNotFoundError:
                print("File not found")
                raise FileNotFoundError
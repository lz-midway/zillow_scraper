import numpy as np

HEAD = 5 # number of rows taken to be sent via email

SCRAPE_SLEEP_CYCLE = 5

DATAPROCESS_SLEEP_CYCLE = 5

SLEEP_CYCLE_TIME = 10 # length of time for cycles to sleep

SQFT_IN_ACRE = 43560

DATA_DIRECTORY = "data/"

READIED_DATA = "readied_data.txt"

END_SYMBOL = "&" # this is used as the end symbol for updating new inputs, this symbol isn't allowed in email addresses or mailing addresses


# for inputs
TEST_RUNTIME = 300
EMAIL_SENDER_TIMEOUT = 90
SCRAPER_TIMEOUT = 80
DATA_PROCESS_TIMEOUT = 60
INPUT_CONFIG_FILE = "data/input.txt"

SEND_EMAIL = 0
SEND_EMAIL_PASSWORD = 1
RECEIVE_EMAIL = 2

AREA_START = 4

PORT_NUM = 3124


smtp_server = 'smtp.gmail.com'
smtp_port = 465

headers = {
        "cache-control": "max-age=0",
        "accept-language": "en-US,en;q=0.9",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "accept-language": "en-US;en;q=0.9",
        "accept-encoding": "gzip, deflate, br",
    }


main_url = "https://www.zillow.com/"

fields = {
    "zpid": "zpid",
    "price": "price",
    "livingArea": "livingArea",
    "streetAddress": "streetAddress",
    "zipcode": "zipcode",
    "city": "city",
    "state": "state",
    "homeType": "homeType",
    "homeStatus": "homeStatus",
    "unit": "unit",
    "lotAreaValue": "lotAreaValue",
    "lotAreaUnit": "lotAreaUnit",
    "detailUrl": "detailUrl"
}

fields_order = [
    "zpid",
    "price",
    "livingArea",
    "streetAddress",
    "zipcode",
    "city",
    "state",
    "homeType",
    "homeStatus",
    "unit",
    "lotAreaValue",
    "lotAreaUnit",
    "detailUrl"
]


column_dtype = {
    "zpid": np.int64,
    "price": np.int64,
    "livingArea": np.int64,
    "streetAddress": str,
    "zipcode": np.int64,
    "city": str,
    "state": str,
    "homeType": str,
    "homeStatus": str,
    "lotAreaValue": np.float64,
    "lotAreaUnit": str
}

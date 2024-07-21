

SCRAPE_SLEEP_TIME = 5


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


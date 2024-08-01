A webscraping program for scraping housing data from Zillow and then automatically send them as emails

input format (example, put the result in a file named input.txt):
email_for_sending@gmail.com
email_password
target_email

area1
area2
...



Directory structure:

data/ # directiory for storing housing data

input.txt # for storing input such as housing regions, etc

main.py # the main running loop

inputs.py # a class for reading and storing inputs

email_sender.py # a class for automatically sending emails

scraper.py # a class for gathering webpages from Zillow

data_processor.py # a class for processing data scraped.



Code structure:

Inputs: this class stores the inputs, including areas needed to be scraped, email and email passwords (for automatically sending emails)
    this class is included in rest of the classes, shared and using a mutex to control access

scraper: runs the entire scraping process, then output to data_processor, this output should be the list of houses without filtering

data_processor: filter out the houses and store the resulting data, the result should be ready to package as email with little processing
    resulting dataframe can be processed into a single email

email_sender: pick up the readied data, package it as an email and send it to the receiver

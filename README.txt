A webscraping program for scraping housing data from Zillow and then automatically send them as emails

input format (example, put the result in a file named user_input.txt, as well as a file named input.txt in data/):
email_for_sending@gmail.com
email_password
target_email

area1
area2
...



Directory structure:

data/ # directiory for storing housing data and input configuration

data/input.txt # for storing input such as housing regions, etc

main.py # the main running loop

inputs.py # a class for reading and storing inputs

email_sender.py # a class for automatically sending emails

scraper.py # a class for gathering webpages from Zillow

data_processor.py # a class for processing data scraped.

user_interface.py # a program run separately to update configuration when the program is running

constants.py # a file containing constants needed to run the program
    currently the runtime is set to:
        total test runtime: 300 seconds
        email sender time: 60 seconds
        scraper time: 80 seconds
        data processor time: 60 seconds


Code structure:

inputs: this class stores the inputs, including areas needed to be scraped, email and email passwords (for automatically sending emails)
    this class is included in rest of the classes, shared and using a mutex to control access
    this class also include part for receiving new inputs from a socket

scraper: runs the entire scraping process, then output to data_processor, this output should be the list of houses without filtering

data_processor: filter out the houses and store the resulting data, the result should be ready to package as email with little processing
    resulting dataframe can be processed into a single email

email_sender: pick up the readied data, package it as an email and send it to the receiver

user_interface: a separate program for updating input configuration while the program is running. 
    The user interface and the input connect through port number 3124 and currently connects through localhost IP

running instructions
    install instruction: run
        pip install -r requirements.txt
    make sure there is a file named "input.txt" in data/
    there is also a file named "user_input.txt" in the main Directory
    then run
        python3 main.py <runtime-optional>
    if runtime is not provided, it runs for 300 seconds
    if runtime is negative, it runs forever

    for updating during when program is running
        python3 user_interface.py


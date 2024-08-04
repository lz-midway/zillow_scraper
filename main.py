import time
import threading
import schedule

import inputs
import email_sender
import scraper
import data_processor
import constants as CONST


def main():

    # V1: uses pure scheduler and does not clean up threads

    inputs_lock = threading.Lock()
    input_thread_lock = threading.Lock() # for controlling the input thread that updates the input configuration

    input_process = inputs.Inputs([], None, None, None, input_thread_lock, inputs_lock)

    print("input created")
    
    inputs_lock.acquire()
    if not input_process.readFromFile(CONST.INPUT_CONFIG_FILE):
        return 1
    inputs_lock.release()

    data_lock = threading.Lock()
    info_lock_scrape = threading.Lock()
    info_lock_data = threading.Lock()

    email_process = email_sender.EmailSender(input_process,
                                             threading.Event(),
                                             data_lock)
    
    scraper_process = scraper.Scraper(input_process, data_lock, info_lock_scrape)
    data_process = data_processor.DataProcessor(input_process, data_lock, info_lock_data)

    def run_threaded(job_func):
        job_thread = threading.Thread(target=job_func)
        job_thread.start()
        return job_thread
    
    schedule.every(30).seconds.do(run_threaded, email_process.send)
    schedule.every(30).seconds.do(run_threaded, scraper_process.scraperTask)
    schedule.every(30).seconds.do(run_threaded, data_process.dataTask)

    it = input_process.startThread()

    time_lapsed = 0
    time_length = 250
    start_time = time.perf_counter()

    while True:

        schedule.run_pending()
        time.sleep(1)
        time_lapsed += 1

        if time_lapsed >= time_length:
            break

    input_process.thread_lock.acquire()
    input_process.shut_down = True
    input_process.thread_lock.release()

    it.join()

    print(time.perf_counter() - start_time)


    # prototype, using a mix of sleep and scheduler

    # inputs_lock = threading.Lock()

    # input_process = inputs.Inputs([], None, None, None, inputs_lock)

    # print("input created")
    
    # inputs_lock.acquire()
    # if not input_process.readFromFile("input.txt"):
    #     return 1
    # inputs_lock.release()

    # data_lock = threading.Lock()
    # info_lock_scrape = threading.Lock()
    # info_lock_data = threading.Lock()

    # email_process = email_sender.EmailSender(input_process,
    #                                          threading.Event(),
    #                                          data_lock)
    
    # scraper_process = scraper.Scraper(input_process, data_lock, info_lock_scrape)
    # data_process = data_processor.DataProcessor(input_process, data_lock, info_lock_data)
    
    # # start the threads
    # ethread = email_process.startThread()
    # sthread = scraper_process.startThread()
    # dthread = data_process.startThread()

    

    # print("thread started")

    # time.sleep(60)

    # email_process.event.set()

    # print("event set")

    # ethread.join()

    # print("ethread ended")

    # info_lock_scrape.acquire()
    # scraper_process.shut_down = True
    # info_lock_scrape.release()

    # info_lock_data.acquire()
    # data_process.shut_down = True
    # info_lock_data.release()

    # sthread.join()
    # dthread.join()

    # print("complete")
    
    return




if __name__ == "__main__":
    main()
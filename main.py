import time
import threading
import schedule

import inputs
import email_sender
import scraper
import data_processor


def main():

    # V1: uses pure scheduler and does not clean up threads

    inputs_lock = threading.Lock()

    input_process = inputs.Inputs([], None, None, None, inputs_lock)

    print("input created")
    
    inputs_lock.acquire()
    if not input_process.readFromFile("input.txt"):
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
    schedule.every(60).seconds.do(run_threaded, scraper_process.scraperTask)
    schedule.every(30).seconds.do(run_threaded, data_process.dataTask)

    time_length = 130

    start_time = time.perf_counter()

    for n in range(time_length):
        schedule.run_pending()
        time.sleep(1)

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
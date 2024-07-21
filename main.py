import time
import threading

import inputs
import email_sender
import scraper
import data_processor


def main():

    inputs_lock = threading.Lock()

    input_process = inputs.Inputs([], None, None, None, inputs_lock)

    print("input created")
    
    inputs_lock.acquire()
    if not input_process.readFromFile("input.txt"):
        return 1
    inputs_lock.release()

    data_lock = threading.Lock()
    info_lock = threading.Lock()

    email_process = email_sender.EmailSender(input_process,
                                             threading.Event(),
                                             data_lock)
    
    scraper_process = scraper.Scraper(input_process, data_lock, info_lock)
    
    # start the threads
    ethread = email_process.startThread()
    sthread = scraper_process.startThread()


    

    print("thread started")

    time.sleep(10)

    email_process.event.set()

    print("event set")

    ethread.join()

    print("ethread ended")

    info_lock.acquire()
    scraper_process.shut_down = True
    info_lock.release()

    sthread.join()

    print("complete")
    
    return


if __name__ == "__main__":
    main()
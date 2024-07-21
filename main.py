import time
import threading
import inputs
import email_sender
import scraper



def main():
    input_process = inputs.Inputs([], None, None, None)

    print("input created")
    
    input_process.readFromFile("input.txt")

    data_lock = threading.Lock()
    info_lock = threading.Lock()

    email_process = email_sender.EmailSender(input_process.send_email, 
                                             input_process.send_email_password,
                                             input_process.receive_email,
                                             threading.Event(),
                                             data_lock)
    
    scraper_process = scraper.Scraper(data_lock, info_lock)

    scraper_process.updateAreas(input_process.areas)
    
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
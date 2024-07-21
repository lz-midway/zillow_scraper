import smtplib
import schedule
import copy
# import pandas as pd
import time
import threading
import constants as CONST


class EmailSender():
    def __init__(self, inputs, event: threading.Event, data_lock):
        self.inputs = inputs
        self.event = event
        self.data_lock = data_lock
        return
    
    # main thread, implement as multithreading
    def senderThread(self):
        while not self.event.is_set():
            schedule.run_pending()
            time.sleep(5)

    def startThread(self):
        schedule.every().second.do(self.send)
        
        st = threading.Thread(target=self.senderThread, args=[])
        st.start()
        return st
    
    # function that is run everytime an email need to be sent
    def send(self):
        self.data_lock.acquire()
        print("email data lock acquired")
        self.data_lock.release()
        print("email data lock released")

        with smtplib.SMTP_SSL(CONST.smtp_server, CONST.smtp_port) as smtp:
            # acquire lock and get the inputs information
            self.inputs.lock.acquire()
            send_email = copy.copy(self.inputs.send_email)
            send_email_password = copy.copy(self.inputs.send_email_password)
            receive_email = copy.copy(self.inputs.receive_email)
            self.inputs.lock.release()

            subject = "test_email"
            body = ["test 1", "test 2"]
            smtp.login(send_email, send_email_password)

            message = "Subject: " + str(subject) + "\n\n" + "\n".join(body)

            # message = f'Subject: {subject}\n\n{"\n".join(body)}'

            smtp.sendmail(send_email, receive_email, message)


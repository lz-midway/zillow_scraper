import smtplib
import schedule
# import pandas as pd
import time
import threading
import constants as CONST


class EmailSender():
    def __init__(self, send_email: str, send_email_password: str, receive_email: str, event: threading.Event, data_lock):
        self.send_email = send_email
        self.send_email_password = send_email_password
        self.receive_email = receive_email
        self.event = event
        self.data_lock = data_lock
        return
    
    # main thread, implement as multithreading
    def senderThread(self):
        while not self.event.is_set():
            schedule.run_pending()
            time.sleep(2)

    def startThread(self):
        schedule.every().second.do(self.send)
        
        st = threading.Thread(target=self.senderThread, args=[])
        st.start()
        return st
    

    def send(self):
        self.data_lock.acquire()
        print("email data lock acquired")
        self.data_lock.release()
        print("email data lock released")

        with smtplib.SMTP_SSL(CONST.smtp_server, CONST.smtp_port) as smtp:
            subject = "test_email"
            body = ["test 1", "test 2"]
            smtp.login(self.send_email, self.send_email_password)

            message = "Subject: " + str(subject) + "\n\n" + "\n".join(body)

            # message = f'Subject: {subject}\n\n{"\n".join(body)}'

            smtp.sendmail(self.send_email, self.receive_email, message)


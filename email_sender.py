import smtplib
import schedule
# import pandas as pd
import time
import threading


smtp_server = 'smtp.gmail.com'
smtp_port = 465


class EmailSender():
    def __init__(self, send_email: str, send_email_password: str, receive_email: str, event: threading.Event):
        self.send_email = send_email
        self.send_email_password = send_email_password
        self.receive_email = receive_email
        self.event = event
        return
    
    # main thread, implement as multithreading
    def sender_thread(self):
        while not self.event.is_set():
            schedule.run_pending()
            time.sleep(2)

    def start_thread(self):
        schedule.every().second.do(self.send)
        
        st = threading.Thread(target=self.sender_thread, args=[])
        st.start()
        return st
    

    def send(self):
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as smtp:
            subject = "test_email"
            body = ["test 1", "test 2"]
            smtp.login(self.send_email, self.send_email_password)

            message = "Subject: " + str(subject) + "\n\n" + "\n".join(body)

            # message = f'Subject: {subject}\n\n{"\n".join(body)}'

            smtp.sendmail(self.send_email, self.receive_email, message)


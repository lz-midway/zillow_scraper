import time
import threading
import inputs
import email_sender




def main():
    input_process = inputs.Inputs([], None, None, None)

    print("input created")
    
    input_process.readFromFile("input.txt")

    email_process = email_sender.EmailSender(input_process.send_email, 
                                             input_process.send_email_password,
                                             input_process.receive_email,
                                             threading.Event())
    
    st = email_process.start_thread()

    print("thread started")

    time.sleep(8)

    email_process.event.set()

    print("event set")

    st.join()

    print("complete")
    
    return


if __name__ == "__main__":
    main()
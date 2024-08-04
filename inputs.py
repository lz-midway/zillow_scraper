import time
import threading

import socket
import constants as CONST



class Inputs():
    def __init__(self, areas: list, send_email: str, send_email_password: str, receive_email: str, thread_lock, inputs_lock):
        self.areas = areas
        self.send_email = send_email
        self.send_email_password = send_email_password
        self.receive_email = receive_email

        self.to_change = False # for communication between scraper and data_processor, False means no need to reprocess data
        self.input_changed = False # for indicating if the input configuration has changed, changed configuration means need to rescrape
        self.to_send_email = False # for communication between data_processor, False means not ready to send email
        self.shut_down = False # to shut down the thread
        self.thread_lock = thread_lock # for controlling shut down
        self.lock = inputs_lock # multi threading locks for accessing the inputs, acquire this before accessing any of its variables
        return
    
    # output formal representation of the object
    def __repr__(self):
        return f'Inputs({repr(self.areas)}, \'{self.send_email}\', \'{self.send_email_password}\', \'{self.receive_email}\', {repr(self.lock)})'
    
    def startThread(self):
        input_thread = threading.Thread(target=self.inputThread, args=[])
        input_thread.start()

        return input_thread
    
    # main thread for getting inputs from socket
    def inputThread(self):

        print("start input thread")

        s = socket.socket()
        s.setblocking(False) # use non-blocking socket
        s.bind(('', CONST.PORT_NUM))
        s.listen()

        while True:
            self.thread_lock.acquire()
            if self.shut_down:
                self.thread_lock.release()
                break
            self.thread_lock.release()

            try:
                c, addr = s.accept()

                print("incoming inputs")

                message = ""
                more_incoming = True
                while more_incoming:
                    current_message = c.recv(1024).decode()
                    end = current_message.find(CONST.END_SYMBOL)
                    if end == -1: # message is not over
                        message += current_message
                    else: # message is over, only take the first section
                        message += current_message[:end]
                        more_incoming = False

                # message collected, inputs updated, need to rescrape
                self.lock.acquire()
                self.updateInput(message)
                self.to_change = False
                self.input_changed = True
                self.lock.release()

                # write the updated configuration to the input.txt file
                self.lock.acquire()
                self.writeToFile(CONST.INPUT_CONFIG_FILE)
                self.lock.release()

            except:
                time.sleep(1)
                continue

        # ends the thread
        s.close()

        return
    
    # update the input configuration, need to hold the lock
    def updateInput(self, message):
        input_data = message.split("\n")

        self.send_email = input_data[CONST.SEND_EMAIL].replace('\n', '')
        self.send_email_password = input_data[CONST.SEND_EMAIL_PASSWORD].replace('\n', '')
        self.receive_email = input_data[CONST.RECEIVE_EMAIL].replace('\n', '')

        n = CONST.AREA_START

        new_areas = []

        while n < len(input_data):
            area = input_data[n].replace('\n', '')
            if area == '':
                break
            else:
                new_areas.append(area)

            n += 1

        self.areas = new_areas

        return
    
    # read from file
    def readFromFile(self, file_name):
        try:
            with open(file_name, "r") as file:
                input_data = file.readlines()
                self.send_email = input_data[CONST.SEND_EMAIL].replace('\n', '')
                self.send_email_password = input_data[CONST.SEND_EMAIL_PASSWORD].replace('\n', '')
                self.receive_email = input_data[CONST.RECEIVE_EMAIL].replace('\n', '')

                n = CONST.AREA_START

                new_areas = []

                while n < len(input_data):
                    area = input_data[n].replace('\n', '')
                    if area == '':
                        break
                    else:
                        new_areas.append(area)

                    n += 1

                self.areas = new_areas

                return True
        except:
            # return false if error
            return False
        
    # write to file, when inputs need to be adjusted, don't need locks because only this thread would have access to it
    def writeToFile(self, file_name):
        try:
            with open(file_name, "w") as file:
                file.write(self.send_email + "\n")
                file.write(self.send_email_password + "\n")
                file.write(self.receive_email + "\n")
                file.write("\n")

                for area in self.areas:
                    file.write(area + "\n")

                return True
        except:
            # return false if error
            return False



    

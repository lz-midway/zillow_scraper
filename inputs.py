



SEND_EMAIL = 0
SEND_EMAIL_PASSWORD = 1
RECEIVE_EMAIL = 2



class Inputs():
    def __init__(self, areas: list, send_email: str, send_email_password: str, receive_email: str):
        self.areas = areas
        self.send_email = send_email
        self.send_email_password = send_email_password
        self.receive_email = receive_email
        return
    
    # output formal representation of the object
    def __repr__(self):
        return f'Inputs({repr(self.areas)}, \'{self.send_email}\', \'{self.send_email_password}\', \'{self.receive_email}\')'
    
    # read from file
    def readFromFile(self, file_name):
        try:
            with open(file_name, "r") as file:
                input_data = file.readlines()
                self.send_email = input_data[SEND_EMAIL].replace('\n', '')
                self.send_email_password = input_data[SEND_EMAIL_PASSWORD].replace('\n', '')
                self.receive_email = input_data[RECEIVE_EMAIL].replace('\n', '')

                n = RECEIVE_EMAIL + 2

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


    

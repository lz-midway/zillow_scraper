import socket

import constants as CONST

ip = '127.0.0.1'

def readFromFile(file_name, input_dict: dict):
    try:
        with open(file_name, "r") as file:
            input_data = file.readlines()
            send_email = input_data[CONST.SEND_EMAIL].replace('\n', '')
            send_email_password = input_data[CONST.SEND_EMAIL_PASSWORD].replace('\n', '')
            receive_email = input_data[CONST.RECEIVE_EMAIL].replace('\n', '')

            n = CONST.RECEIVE_EMAIL + 2

            new_areas = []

            while n < len(input_data):
                area = input_data[n].replace('\n', '')
                if area == '':
                    break
                else:
                    new_areas.append(area)

                n += 1

            input_dict["send_email"] = send_email
            input_dict["send_email_password"] = send_email_password
            input_dict["receive_email"] = receive_email
            input_dict["areas"] = new_areas

            return True
    except:
        # return false if error
        return False
    

def main():

    print("begin new input")

    new_dict = {}

    if not readFromFile("user_input.txt", new_dict):
        return 1
    
    with socket.socket() as s:
        s.connect((ip, CONST.PORT_NUM))

        print("connection established")

        email = new_dict["send_email"] + "\n"
        s.send(email.encode())
        email_pass = new_dict["send_email_password"] + "\n"
        s.send(email_pass.encode())
        email_receive = new_dict["receive_email"] + "\n" + "\n"
        s.send(email_receive.encode())

        for area in new_dict["areas"]:
            area_mes = area + "\n"
            s.send(area_mes.encode())

        s.send(CONST.END_SYMBOL.encode())

        print("message sent")

    return 0

main()

# if __name__ == "__user_interface__":
#     main()



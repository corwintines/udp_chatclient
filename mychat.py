# CPSC 3780 - Data Comm & Networking
# Peer-to-peer Chat Application Project
# Claire Fritzler and Corwin Smith

# The program will discover any other chat applications running in the labs
# IP Ranges:  C-LAB: 142.66.140.21-45. D-LAB: 142.66.140.46-69, and 142.66.140.186
# Port Ranges: 55000 - 55008
# A one line message will be sent to all active users
# Peer Discovery: To discover peer applications, the receiver

from threading import Thread, Timer
from time import sleep
import threading
import sys, socket, errno


MYPORT = int(sys.argv[1])
PORTRANGE = [55000, 55001, 55002, 55003, 55004, 55005, 55006, 55007, 55008]
IPADDRESSRANGE=['142.66.140.186']
BUFLEN = 1000

for ip in range(21,70):
    IPADDRESSRANGE.append('142.66.140.'+str(ip))

# Receiver class
# If the reciver receives a "Hello" message, then it must add that
# user (username) to the list and start the timer.
class Receiver(Thread):
    def __init__(self, socket):
        Thread.__init__(self)
        self.socket = socket
        self.partners = []

    def remove_partner(self, args):
        print("Remove: ", args)

        for elem in self.partners:
            if(elem[0] == args):
                self.partners.remove(elem)
                print(self.partners)

    def run(self):
        while True:
            try:
                data, addr = self.socket.recvfrom(BUFLEN)
            except OSError as err:
                print ("Cannot receive from socket: {}".format(err.strerror))


            # If the message is a hello message
            if(data[:5] == b'HELLO'):
                for elem in self.partners:
                    # if the element is already in the list remove it and then go and re-add it
                    if elem[0] == addr and elem[1] == data[6:]:
                        elem[2].cancel()
                        self.partners.remove(elem)

                for IP in IPADDRESSRANGE:
                    for PORT in PORTRANGE:
                        if ((IP, PORT) == addr):
                            t = Timer(15.0, self.remove_partner, args=[addr])
                            t.daemon = True
                            t.start()
                            self.partners.append([addr, data[6:], t])

            else:
                for elem in self.partners:
                    if elem[0] == addr:
                        print((elem[1] + b': ' + data).decode())


# Hello Thread.
# Sends a "HELLO" message every 5 seconds so that other users on the
# network can add to their active user lists
class Hello(Thread):
    def __init__(self, socket):
        Thread.__init__(self)
        self.username = ''
        self.socket = socket

    def hello(self):
        try:
            string = str.encode('HELLO ' + self.username)
            for IP in IPADDRESSRANGE:
                for PORT in PORTRANGE:
                    self.socket.sendto(string, (IP,PORT))
        except OSError as err:
            print ('Cannot send: {}'.format(err.strerror))
            sys.exit(1)

    def run(self):
        while(True):
            self.hello()
            sleep(5.0)

    def create_username(self):
        check = False
        print ("Enter a username (any letter, number, -, _, or .):")
        username = input('')
        while(check==False):
            for letter in username:
                if (letter.isalnum() or letter=='_' or letter=='-' or letter=='.'):
                    check = True
                else:
                    check = False
                    print("Enter a VALID username (any letter, number, -, _, or.):")
                    username = input('')
                    break
        self.username = username


def main():
    try:
        user_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except:
        print ("Cannot open socket")
        sys.exit(1)

    try:
        user_socket.bind(('',MYPORT))
        print("Port bound")
    except:
        print ("Cannot bind my socket to port")
        sys.exit(1)

    r = Receiver(user_socket)
    r.daemon = True
    r.start()
    h = Hello(user_socket)
    h.daemon = True
    h.create_username()
    h.start()

    print ('s <msg> - sends message \nq-quits\n')
    cmd = input('')
    while cmd[0] != 'q':
        if cmd[0] is 's':
            message = ''
            for char in range(2, len(cmd)):
                message += cmd[char]

            try:
                for partner in r.partners:
                    send_message = str.encode(message)
                    user_socket.sendto(send_message, partner[0])
            except OSError as err:
                print('Cannot send: {}'.format(err.strerror))
                sys.exit(1)
        cmd = input('')

        print('So long partner')


main()

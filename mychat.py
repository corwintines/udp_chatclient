# CPSC 3780 - Data Comm & Networking
# Peer-to-peer Chat Application Project
# Claire Fritzler and Corwin Smith

# The program will discover any other chat applications running in the labs
# IP Ranges:  C-LAB: 142.66.140.21-45. D-LAB: 142.66.140.46-69, and 142.66.140.186
# Port Ranges: 55000 - 55008
# A one line message will be sent to all active users
# Peer Discovery: To discover peer applications, the receiver

from queue import Queue, Empty
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
    def __init__(self, queue, username):
        Thread.__init__(self)
        self.queue = queue
        self.username = username
        self.partners = []

    def remove_partner(self):
        print(self.partners)

    def run(self):
        try:
            s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except:
            print ("Cannot open socket")
            sys.exit(1)

        try:
            s.bind(('',MYPORT))
            print("Port bound")
        except:
            print ("Cannot bind my socket to port")
            sys.exit(1)

        while True:
            try:
                data, addr = s.recvfrom(BUFLEN)
                print(data, addr)
            except OSError as err:
                print ("Cannot receive from socket: {}".format(err.strerror))

            if(data[:5] == b'HELLO'):
                for elem in self.partners:
                    if elem[0] == addr and elem[1] == data[6:]:
                        self.partners.remove(elem)

                for IP in IPADDRESSRANGE:
                    for PORT in PORTRANGE:
                        if ((IP, PORT) == addr):
                            self.partners.append([addr, data[6:]])
                # # print(data)
                # # If the timer reaches 0, remove the partner from the list
                # # If a hello message is received and the partner is already in
                # # the list, update the timer
                # timer = Timer(15.0, lambda: remove_partner(self))
                # timer.start()
                # try:
                #     for i in range(0, len(self.partners)-1):
                #         if(self.partners[i][0] == username and self.partners[i][1] == addr):
                #             self.partners.remove(i)
                #
                #             self.partners.append()
                #         else:
                #             self.partners.append([username, addr, timer])
                # except:
                #     print ("No partners")

            else:
                for elem in self.partners:
                    if elem[0] == addr:
                        print(elem[1]+': '+data[:2])



# Hello Thread.
# Sends a "HELLO" message every 5 seconds so that other users on the
# network can add to their active user lists
class Hello(Thread):
    def __init__(self, username):
        Thread.__init__(self)
        self.username = username

    def hello(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except:
            print ("Cannot open socket")
            sys.exit(1)

        # try:
        #     s.connect(('127.0.0.1', MYPORT))
        # except:
        #     print("something")

        try:
            string = str.encode('HELLO ' + self.username)
            for IP in IPADDRESSRANGE:
                for PORT in PORTRANGE:
                    s.sendto(string, (IP, PORT))
        except OSError as err:
            print ('Cannot send: {}'.format(err.strerror))
            sys.exit(1)

    def run(self):
        while(True):
            self.hello()
            sleep(5.0)


def check_username(username):
    check = True
    for letter in username:
        if (letter.isalpha()==True or letter=='_' or letter=='_' or letter!='.'):
            check = True
        else:
            check = False
            break
    return check


def main():
    print("Enter a username")
    username = input('')
    check = check_username(username)
    while(check==False):
        print("Reenter a valid username")
        username = input('')
        check = check_username(username)

    queue = Queue()
    r = Receiver(queue, username)
    r.daemon = True
    r.start()
    h = Hello(username)
    h.daemon = True
    h.start()

    print ('s <msg> - sends message \nq-quits\n')
    cmd = input('')
    while cmd[0] != 'q':
        if cmd[0] is 's':
            message = username+': '
            for char in range(2, len(cmd)):
                message += cmd[char]
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            except:
                print("Cannot open socket")
                sys.exit(1)
            try:
                for partner in r.partners:
                    print(partner[0])
                    send_message = str.encode(message)
                    s.sendto(send_message, partner[0])
            except OSError as err:
                print('Cannot send: {}'.format(err.strerror))
                sys.exit(1)
        cmd = input('')

        print('So long partner')


main()

# CPSC 3780 - Data Comm & Networking
# Peer-to-peer Chat Application Project
# Claire Fritzler and Corwin Smith
#
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
import json

MYPORT = int(sys.argv[1])
THEIRIP = sys.argv[2]
USERNAME = str(sys.argv[3])
PORTRANGE = [55000, 55001, 55002, 55003, 55004, 55005, 55006, 55007, 55008]
IPADDRESSRANGE = [142.66.140.21, 142.66.140.22, 142.66.140.23, 142.66.140.24, 142.66.140.25, 142.66.140.26,
                  142.66.140.27, 142.66.140.28, 142.66.140.29, 142.66.140.30, 142.66.140.31, 142.66.140.32,, 142.66.140.33,
                  142.66.140.34]
BUFLEN = 1000


# Receiver class
# If the reciver receives a "Hello" message, then it must add that
# user (username) to the list and start the timer.
class Receiver(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue
        self.partners = [[]]
    
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
        except:
            print ("Cannot bind my socket to port")
            sys.exit(1)
        
        while True:
            try:
                data, addr = s.recvfrom(BUFLEN)
                data = json.loads(data)
                username = data[1]
                message = data[0]
            except OSError as err:
                print ("Cannot receive from socket: {}".format(err.strerror))
        
            if(message == "HELLO"):
                # If the timer reaches 0, remove the partner from the list
                # If a hello message is received and the partner is already in
                # the list, update the timer
                timer = Timer(15.0, lambda: remove_partner(self))
                timer.start()
                try:
                    for i in range(0, len(self.partners)-1):
                        if(self.partners[i][0] == username and self.partners[i][1] == addr):
                            self.partners.remove(i)
                            
                            self.partners.append([username, addr, timer])
                        else:
                            self.partners.append([username, addr, timer])
            except:
                print ("No partners")
            
            elif(message == "CHAT"):
                print(data)



# Hello Thread.
# Sends a "HELLO" message every 5 seconds so that other users on the
# network can add to their active user lists
class Hello(Thread):
    def __init__(self):
        Thread.__init__(self)
    
    def hello(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except:
            print ("Cannot open socket")
            sys.exit(1)
        
        try:
            s.bind(('', MYPORT+1))
        except:
            print ("Cannot bind to port")
            sys.exit(1)
    
        try:
            
            string = ['HELLO', USERNAME]
            string=json.dumps(string).encode('utf-8')
            for i in range(0, 8): # This needs to be extended for all the lab IP Addresses
                s.sendto(string, (THEIRIP, PORTRANGE[i]))
        except OSError as err:
            print ('Cannot send: {}'.format(err.strerror))
            sys.exit(1)

def run(self):
    while True:
        sleep(5.0)
            self.hello()



def main():
    queue = Queue()
    r = Receiver(queue)
    r.daemon = True
    r.start()
    h = Hello()
    h.daemon = True
    h.start()
    
    print ('s <msg> - sends message \nq-quits\n')
    cmd = input('')
    while cmd[0] != 'q':
        if cmd[0] is 's':
            message = ''
            for char in range(2, len(cmd)):
                message += cmd[char]
        
            chat_message = ['CHAT', message]
            chat_message=json.dumps(chat_message).encode('utf-8')
            
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except:
        print("Cannot open socket")
            sys.exit(1)
            try:
                s.bind(('', MYPORT+1))
        except:
            print("Cannot bind socket to port")
                sys.exit(1)
            try:
                for i in range(0,8):
                    if(PORTRANGE[i] != MYPORT):
                        s.sendto(chat_message, (THEIRIP, PORTRANGE[i]))
        except OSError as err:
            print('Cannot send: {}'.format(err.strerror))
                sys.exit(1)
        cmd = input('')

print('So long partner')


main()

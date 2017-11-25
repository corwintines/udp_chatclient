from Queue import Queue, Empty
from threading import Thread
from time import sleep
import sys, socket, errno

USERNAME = sys.argv[1]
MYPORT = int(sys.argv[2])
SERVERIP = sys.argv[3]
SERVERPORT = int(sys.argv[4])
BUFLEN = 1000

class Client(Thread):
    def __init__(self, username):
        Thread.__init__(self)
        self.PORT = MYPORT
        self.username = username
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
    
    def run(self):
        try:
            s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except:
            print "Cannot open socket"
            sys.exit(1)

        try:
            s.bind(('',MYPORT))
        except:
            print "Cannot bind my socket to port"
            sys.exit(1)
            
        while True:
            self.send_hello()
            sleep(5.0)
        
        
    def send_message(self, message):
        try:
            self.s.sendto(self.username + ": " + message, (SERVERIP, SERVERPORT))
        except OSError as err:
            print "Cannot send: {}".format(err.strerror)
            sys.exit(1)
        
        
    def send_hello(self):
        self.s.sendto('HELLO '+ str(MYPORT), (SERVERIP, SERVERPORT))


def main():
    c = Client(USERNAME)
    c.start()
    print 'p - prints received messages \ns <msg> - sends message \nq-quits\n'
    cmd = raw_input('& ')
    while cmd[0] is not 'q':
        if cmd[0] is 'p':
            try:
                while True:
                    msg = queue.get(False, None)
                    print(msg)
            except:
                print('---')

        if cmd[0] is 's':
            message = ''
            for char in range(2, len(cmd)):
                message += cmd[char]
            c.send_message(message)

        cmd = raw_input('& ')

    print('So long partner')


main()
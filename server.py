from Queue import Queue, Empty
from threading import Thread
from time import sleep
import sys, socket, errno

MYPORT = int(sys.argv[1])
PORT_RANGE = sys.argv[2]
BUFLEN = 1000

class Receiver(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.available_ports = self.convert_ports(PORT_RANGE)
        self.used_ports = []
        self.queue = queue
        
    
    def convert_ports(self, port_range):
        split = port_range.split('-')
        ports = []
        for port in range(int(split[0]), int(split[1])+1):
            ports.append(port)
            
        return ports
    
    
    def use_port(self, port):
        if port not in self.used_ports:
            self.used_ports.append(port)
        if port in self.available_ports:
            self.available_ports.remove(port)
        print self.used_ports
        print self.available_ports
        
    
    def free_port(self, port):
        print "Free Port"
        

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
            try:
                data, addr = s.recvfrom(BUFLEN)
            except OSError as err:
                print "Cannot receive from socket: {}".format(err.strerror)
            print "Received Message"
            if data.split(' ')[0] == "HELLO":
                print data
                print addr
                self.use_port(int(data.split(' ')[1]))
            self.queue.put(data)
            


def main():
    queue = Queue()
    r = Receiver(queue)
    r.daemon = True
    r.start()
    cmd = raw_input('')
    while cmd != 'Shutdown':
        print cmd
        cmd = raw_input('')

main()
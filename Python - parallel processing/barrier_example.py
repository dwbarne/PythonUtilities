import multiprocessing as mp
from math import ceil, log
import os, time

class PoolProcess(mp.Process):
    def __init__(self,rank,events,numproc,lock):
        mp.Process.__init__(self)
        self.rank = rank
        self.events = events
        self.numproc = numproc
        self.lock = lock
        
    def barrier(self):
        if self.numproc == 1: return
   
# loop log2(num_threads) times, rounding up
        for k in range(int(ceil(log(self.numproc)/log(2)))):
# send event to thread (rank + 2**k) % numproc
            receiver = (self.rank + 2**k) % self.numproc
            evt = self.events[self.rank * self.numproc + receiver]
            evt.set()
# wait for event from thread (rank - 2**k) % numproc
            sender = (self.rank - 2**k) % self.numproc
            evt = self.events[sender * self.numproc + self.rank]
            evt.wait()
            evt.clear()
        
    def run(self):
# print the rank of this process
# synchronize access to stdout
        self.lock.acquire()
        print 'Hello World, I am process %d' % self.rank
        self.lock.release()
# wait for the self.numproc - 1 other processes
#  to finish printing
        self.barrier()
        
# print the rank of this process
# synchronize access to stdout
        self.lock.acquire()
        print 'Hello World again, I am process %d' % self.rank
        self.lock.release()
        
def number_of_processors():
    ''' number of virtual processors on the computer '''
# windows
    systemOS = os.name
    print('\nsystem OS = %s' % systemOS)
    if systemOS == 'nt':
        return int(os.getenv('NUMBER_OF_PROCESSORS'))
# linux
    elif sys.platform == 'linux2':
        retv = 0
        with open('/proc/cpuinfo','rt') as cpuinfo:
            for line in cpuinfo:
                if line[:9] == 'processor': retv += 1
        return retv
# can add similar hacks here for MacOSX, Solaris, Irix, FreeBSD, HPUX, etc.
    else:
        raise RuntimeError, 'unknown platform'
        
        
if __name__ == '__main__':
    print('\n***** Program barrier.py *****')
    numproc = number_of_processors()
    numproc = 16
    print('\nNumber of processors: %s\n' % numproc)
    start = time.time()
    lock = mp.Lock()
    events = [mp.Event() for n in range(numproc**2)]
    pool = [PoolProcess(rank, events, numproc, lock) for rank in range(numproc)]
#    print('pool:\n')
#    print(pool)
#    print('\n')
#    start = time.time()
    for p in pool: p.start()
    for p in pool: p.join()
    end = time.time()
    print('\nTime: %s secs' % (end - start))

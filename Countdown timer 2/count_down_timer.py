# countdown timer

import time

for i in range(5,-1,-1):
    print 'This terminates in %s seconds' % i
    time.sleep(1)
print 'terminated'
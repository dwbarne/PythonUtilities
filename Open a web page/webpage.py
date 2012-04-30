#
# open a web page
#

import time, urllib

class CacheFetcher:
    def __init__(self):
        self.cache = {}
    def fetch(self, url, max_age=0):
        if self.cache.has_key(url):
            if int(time.time()) - self.cache[url][0] < max_age:
                return self.cache[url][1]
        # Retrieve and cache
        data = urllib.urlopen(url).read()
        self.cache[url] = (time.time(), data)
        return data
        
if __name__ == '__main__':
    fetch=CacheFetcher()
    data=fetch.fetch('http://www.msnbc.com',60)
    print '\n>> web site =',data
    

from Defog import fastDefog
from Defog import Defog
import time

def slowDefog(imageLocation):
    start = time.time()
    defogger = Defog(imageLocation)
    defogger.defog()
    print "time taken "+str(time.time()-start)

def fastDefogger(imageLocation, processes=1):
    start = time.time()
    fastDefog(imageLocation, 2, processes)
    print "time taken "+str(time.time()-start)

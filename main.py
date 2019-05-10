from Defog import fastDefog
from Defog import Defog
import time
from multiprocessing import Pool

def slowDefog(imageLocation):
    start = time.time()
    defogger = Defog(imageLocation)
    defogger.defog()
    print "time taken "+str(time.time()-start)

def fastDefogger(imageLocation, processes=1):
    p = Pool(processes)
    start = time.time()
    fastDefog(imageLocation, p, 2)

import time
import multiprocessing
import json as simplejson

class Worker():
    def __init__(self,queue):
        self.queue=queue    
    def worker(self):
        self._name=multiprocessing.current_process().name
        print("%s is Working...")% self._name            
        f = open("/tmp/%s.log" % self._name, "w")
        data=None
        while 1:
            try:
                if not self.queue.empty():
                    data=self.queue.get()
                    if data:
                        self.work_deliver(data)
                        f.write('%s %s \n' % (self._name,data))
                        f.flush()
                time.sleep(1)
            except KeyboardInterrupt:
                print("%s is Quitting...")% self._name
                break
    def work_resolve(self,data):
        """        work instance:{'HEAD':'MEGA','TYPE':'CMD','VALUE':'ls'}
        keys:
            HEAD
            TYPE
            VALUE
            TIME
            REPEAT            
        """
        if len(data)==0:
            return False
        try :
            print data
#            d=simplejson.loads(data)
            d=eval(data)
            print type(d)
            if type(d)=='dict':
                if not (d.has_key('TYPE') or d.has_key('VALUE')):
                    return False
            else:
                return False
        except Exception as ex:
            print ex    
        return True
        
    def work_deliver(self,work):
        if self.work_resolve(work):
            pass
    
    def close(self):
        self.close()
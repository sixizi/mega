import time
import multiprocessing

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
            HEAD:    for safe interactive,should be MEGA
            TYPE:    cmd,task,other
            VALUE:   what to do : ls
            TIME:    when to do : 0 once  ,
            CYCLE:  lifecycle of job   day,week,month
            TARGET:    unique identify for server or instance or database.
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
        self.task=d
        return True
        
    def work_deliver(self,work):
    #1.run the command
    #2.save task into db
        if not self.work_resolve(work):
            return False
        #real time job
        if self.task.get('TIME')=='0':
        #subthread
            result=Executor()
        else:
        #save into db
            pass
    def close(self):
        self.close()

class Executor():
    '''
     Run the task on the remote server in subprocess
    '''
    def __init__(self):
        pass
    def run(self):
        pass
    def salt_loader(self):
        pass
class Saver():
    '''
    save task into database if it need to be rerun  
    '''
    def __init__(self):
        pass
    def run(self):
        pass
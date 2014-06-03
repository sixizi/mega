import multiprocessing
from listener import tcp_server
from worker import Worker 

def sub_process():
    global queue
    queue = multiprocessing.Queue()
    worker=Worker(queue).worker
    threads=[]
    try:
        workers=multiprocessing.Process(target=worker,args=(),name="Main Worker")
        threads.append(workers)
        listens=multiprocessing.Process(target=tcp_server,args=(queue,),name="TCP Listener")
        threads.append(listens)
        for t in threads:
            t.start()
        for t in threads:
            t.join()
    except KeyboardInterrupt:
        return
 
def main():
    sub_process()
if __name__ == "__main__":
    main()


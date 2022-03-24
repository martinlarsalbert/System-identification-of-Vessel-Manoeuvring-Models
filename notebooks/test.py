import multiprocessing as mp
import multiprocessing.queues as mpq
import time

def foo(q):
    time.sleep(2)
    q.put('hello')

if __name__ == '__main__':
    
    timeout = 1
    
    mp.set_start_method('spawn')
    q = mp.Queue()
    p = mp.Process(target=foo, args=(q,))
    p.start()
    #print(q.get(timeout=timeout))
    
    try:
        res = q.get(timeout=timeout)
        print(res)
        p.join()
    
    except mpq.Empty:
        p.terminate()
        print('Timeout!')
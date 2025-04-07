# Group #:
# Student names:

import threading
import queue
import time, random


def consumerWorker(queue: queue):
    """target worker for a consumer thread"""
    while True:
        try:
            item = queue.get(timeout=1)
            print(f"[Consumer-{threading.current_thread().name}] Consumed: {item}")
            time.sleep(random.uniform(0.1, 0.5))  # Simulate variable processing time
            queue.task_done()
        except:
            # Assume all producers are done and queue is empty
            break


def producerWorker(queue: queue):
    """target worker for a producer thread"""
    for i in range (5):
        queue.put(random.randint(0,5))
        time.sleep(random.randint(1,3))

    producer_list.pop(0)

if __name__ == "__main__":
    buffer = queue.Queue()
    num_consumer = 5
    num_producer = 4
    thread_list = []
    producer_list = []
    for i in range(num_consumer):
        thread_list.append(threading.Thread(target=consumerWorker, args=(buffer,)))

    for i in range(num_producer):
        thread_list.append(threading.Thread(target=producerWorker, args=(buffer,)))
        producer_list.append(i)

    for i in thread_list:
        i.start()

    for i in thread_list:
        i.join()

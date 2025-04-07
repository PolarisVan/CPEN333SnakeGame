# Group #: B21
# Student names: Peiyu Qu and Dalisio Pereira

import threading
import queue
import time, random


def consumerWorker(queue: queue) -> None:
    """target worker for a consumer thread"""
    while True:
        item = queue.get()
        if item is None:
            print(f"[Consumer-{threading.current_thread().name}] Exiting.")
            queue.task_done()
            break
        print(f"[Consumer-{threading.current_thread().name}] Consumed: {item}")
        time.sleep(random.uniform(0.1, 0.5))  # Simulate variable processing time
        queue.task_done()

def producerWorker(queue: queue) -> None:
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

# Group #: B21
# Student names: Peiyu Qu and Dalisio Pereira

import threading
import queue
import time, random

def consumerWorker(queue: object, id: int):
    """target worker for a consumer thread"""
    global task_number
    while task_number >= id + 1:
        print(task_number)
        task_number = task_number - 1
        item = queue.get()
        print(f"[Consumer-{threading.current_thread().name}] Consumed: {item}")
        time.sleep(random.uniform(0.1, 0.5))  # Simulate variable processing time
        queue.task_done()
    print("done")

def producerWorker(queue: object, id: int):
    """target worker for a producer thread"""
    for i in range (5):
        queue.put(random.randint(0,5))
        time.sleep(random.randint(1,2))

if __name__ == "__main__":
    buffer = queue.Queue()
    num_consumer = 5
    num_producer = 4
    thread_list = []
    task_number = num_producer * 5
    for i in range(num_consumer):
        thread_list.append(threading.Thread(target=consumerWorker, args=(buffer,i)))

    for i in range(num_producer):
        thread_list.append(threading.Thread(target=producerWorker, args=(buffer,i)))

    for i in thread_list:
        i.start()

    for i in thread_list:
        i.join()
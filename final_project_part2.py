# Group #: B21
# Student names: Peiyu Qu and Dalisio Pereira

import threading
import queue
import time, random

def consumerWorker(queue: object, id: int) -> None:
    """target worker for a consumer thread"""
    global task_number
    while task_number >= id + 1:
        task_number = task_number - 1
        item = queue.get()
        print(f"[Consumer-{threading.current_thread().name}] Consumed: {item}")
        time.sleep(random.uniform(0.5, 1))  # Simulate variable processing time
        queue.task_done()

def producerWorker(queue: object, task: int) -> None:
    """target worker for a producer thread"""
    for i in range (task):
        item = random.randint(0,5)
        queue.put(item)
        print(f"[Producer-{threading.current_thread().name}] Produced: {item}")
        time.sleep(random.uniform(0.1, 0.2))  # Simulate variable processing time

if __name__ == "__main__":
    buffer = queue.Queue() # buffer to keep track of consumer/producer
    num_consumer = 5
    num_producer = 4
    task_per_producer = 6
    thread_list = []
    task_number = num_producer * task_per_producer # tracker for remaining tasks
    for i in range(num_consumer):
        thread_list.append(threading.Thread(target=consumerWorker, args=(buffer,i)))

    for i in range(num_producer):
        thread_list.append(threading.Thread(target=producerWorker, args=(buffer, task_per_producer)))

    for i in thread_list:
        i.start()

    for i in thread_list:
        i.join()

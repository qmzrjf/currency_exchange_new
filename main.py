import os
import requests
import threading as tr
from time import sleep, time
from pdb import set_trace
from multiprocessing.pool import ThreadPool
#
# def foo(num):
#     # print(tr.current_thread())
#     sleep(num)
#
# # start = time()
# threads = []
# for i in range(10):
#
#     thr1 = tr.Thread(target=foo, args=(i, ))
#     thr1.start()
#     threads.append(thr1)
#
# while threads:
#     print(len(threads), threads)
#     sleep(0.5)
#     for index, th in enumerate(threads):
#         if not th.is_alive():
#             threads.pop(index)
# # print(f'Done in: {time() - start}')
# print('Done')


############################################################################

#
def save_image(*args):


    url = 'https://loremflickr.com/320/240/dog'
    response = requests.get(url)
    name = response.url.split('/')[-1]
    path = os.path.join(os.getcwd(), 'images', name)

    with open(path, 'wb') as file:
        file.write(response.content)
    # set_trace()

# start = time()

# for _ in range(100):
#     save_image()

# with ThreadPool(20) as pool:
#     pool.map(save_image, range(100))
#

# print(time() - start)
# print('Done')

import multiprocessing as mlt

#
# processes_count = mlt.cpu_count()*2
# COUNT = 500_000_000
#
# def countdown(n):
#     while n>0:
#         n-=1
#
# start = time()
# # countdown(COUNT)
# processes = []
# for i in range(processes_count):
#     t = mlt.Process(target=countdown, args =((COUNT//processes_count) ,))
#     t.start()
#     processes.append(t)
#
# for p in processes:
#     p.join()
#
#
# # countdown(COUNT)
#
# print((time() - start))

'''
arr = [[]]*3
arr[0].append(7)
# arr[1]= [5]
print(arr)
'''



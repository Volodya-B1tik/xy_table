# barrier_tut.py
from random import randrange
from threading import Barrier, Thread
from time import ctime, sleep

num = 2
# 4 threads will need to pass this barrier to get released.
b = Barrier(num)
names = ['Harsh', 'Lokesh', 'George', 'Iqbal']


def player1():
    name = names.pop()
    sleep(randrange(1, 12))
    print('%s reached the barrier at: % s' % (name, ctime()))
    b.wait()
    print('%s passed at: % s' % (name, ctime()))


def player2():
    name = names.pop()
    sleep(randrange(1, 12))
    print('%s reached the barrier at: % s' % (name, ctime()))
    b.wait()
    print('%s passed at: % s' % (name, ctime()))


threads = []
print('Race starts now…')

t1 = Thread(target=player1)
t1.start()
t2 = Thread(target=player2)
t2.start()
"""
Following loop enables waiting for the threads to complete before moving on with the main script.
"""
t1.join()
t2.join()

print()
print('Race over!')

# -*- coding: utf-8 -*-
import sys
import random
import time
import threading
from easy import Easy2Python

sys.setrecursionlimit(1000000)
RAN = 0.1
pre = 200.0
now = random.uniform(pre - RAN, pre + RAN)

f = file('easycode.txt', 'r')
data = f.read()
f.close

def trade(now):
	global data
	ticket = {}
	next = random.uniform(now - RAN, now + RAN)	
	ticket['price'] = next
	ticket['time'] = int(time.strftime('%H%M%S', time.localtime()))
	print ticket
	work = Easy2Python(ticket['price'], ticket['time'])
	work.easy(data)
	time.sleep(1)
	trade(next)

def main():
	
	trade(now)


if __name__ == '__main__':
	main()
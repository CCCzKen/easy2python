# -*- coding: utf-8 -*-
import time
from parser import EasyParser
from interp import BasicInterpreter


class Easy2Python:
	def __init__(self, close, nowtime):
		self.close = close
		self.nowtime = nowtime

	def easy(self, data):
		data = '\n' + data.lower() + '\n'

		parser = EasyParser().parser()
		prog = parser.parse(data)
		# print prog
		if not prog: raise SystemExit
		b = BasicInterpreter(prog, int(self.nowtime), self.close)
		b.run()


if __name__ == '__main__':

	f = file('easycode.txt', 'r')
	data = f.read()
	f.close
	# nowtime = time.strftime('%H%M%S', time.localtime())
	nowtime = 230000
	close = 117.91
	work = Easy2Python(close, nowtime)
	work.easy(data)
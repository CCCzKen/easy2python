# -*- coding: utf-8 -*-
import sys
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S'
)

class BasicInterpreter:

	def __init__(self, prog, timestr, close):
		self.prog = prog
		self.vars = {}

		self.vars['time'] = timestr
		self.vars['close'] = close

	def run(self):
		self.error = 0
		self.pc = 1


		if self.error: raise RuntimeError
		while 1:
			line = self.pc
			try:
				instr = self.prog[line]
			except KeyError, e:
				break
			op = instr[0]

			if op == 'BEGIN':
				rel = self.expr_comp(instr[1])
				if not rel:
					self.end_block(line)					
			elif op == 'END':
				pass
			elif op == 'VAR':
				self.expr_var(instr[1])
				# print self.vars
			elif op == 'IF':
				rel = self.expr_comp(instr[1])
				if not rel:
					self.pc += 1
			elif op == 'SELL' or op == 'BUY':
				pass
				self.command_deal(instr)
			else:
				pass
			self.pc += 1


	# expression variable
	def expr_var(self, expr):
		if isinstance(expr, tuple):
			key, value = expr[0], expr[1]
			self.vars[key] = value
		elif isinstance(expr, list):
			for block in expr:
				key, value = block[0], block[1]
				self.vars[key] = value
		# print 'variable finish'

	# command if 
	def expr_comp(self, expr):
		etype = expr[2]
		lhs = self.vars[expr[1]]
		rhs = self.vars[expr[3]]
		if etype == '<':
			if lhs < rhs: return 1
			else: return 0
		elif etype == '>':
			if lhs > rhs: return 1
			else: return 0
		elif etype == '<=':
			if lhs <= rhs: return 1
			else: return 0
		elif etype == '>=':
			if lhs >= rhs: return 1
			else: return 0
		elif etype == '=':
			if lhs == rhs: return 1
			else: return 0
		elif etype == '<>':
			if lhs != rhs: return 1
			else: return 0

	# command sell and buy
	def command_deal(self, expr):
		if expr[0] == 'SELL':
			if expr[1] == 0:
				logging.info('===== sell with %s =====' % self.vars['close'])
			else:
				logging.info('===== sell with %s =====' % self.vars[expr[1]])
		elif expr[0] == 'BUY':
			if expr[1] == 0:
				logging.info('===== buy with %s =====' % self.vars['close'])
			else:
				logging.info('===== buy with %s =====' % self.vars[expr[1]])

	def end_block(self, line):
		while 1:
			try:
				instr = self.prog[line]
			except KeyError, e:
				break
			op = instr[0]

			if op == 'END':
	 			break

	 		line += 1

	 	self.pc = line
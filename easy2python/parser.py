# -*- coding: utf-8 -*-
import re
from ply import lex, yacc


class EasyParser:

    def __init__(self):
        self.keywords = (
            'print', 'if', 'inputs', 'then', 'limit',
            'sell', 'buy', 'this', 'bar', 'at', 'next',
            'begin', 'end',
        )

        self.tokens = self.keywords + (
            'LPAREN', 'RPAREN', 'SEMI', 'COLON', 'COMMA',
            'LT', 'GT', 'LE', 'GE', 'EQUALS', 'NE', 
            'INTEGER', 'FLOAT', 'STRING', 'NEWLINE', 'ID',
        )
        self.line = 1

    def easylex(self):

        keywords = self.keywords
        tokens = self.tokens

        t_LPAREN = r'\('
        t_RPAREN = r'\)'
        t_SEMI = r';'
        t_COLON = r':'
        t_COMMA = r','
        t_LT = r'<'
        t_GT = r'>'
        t_LE = r'<='
        t_GE = r'>='
        t_EQUALS = r'='
        t_NE = r'<>'
        t_INTEGER = r'\d+'
        t_FLOAT   = r'((\d*\.\d+)(E[\+-]?\d+)?|([1-9]\d*E[\+-]?\d+))'
        t_STRING  = r'\"[^"]*\"|\'[^"]*\''

        t_ignore = ' \t'

        def t_ID(t):
            r'[A-Za-z]+[0-9]*'
            if t.value in keywords:
                t.type = t.value
            return t

        def t_NEWLINE(t):
            r'\n+'
            t.lexer.lineno += 1
            return t

        def t_error(t):
            print("Illegal character %s" % t.value[0])
            t.lexer.skip(1)

        return lex.lex()

    def easyparse(self):
        IS_FLOAT = re.compile(r'((\d*\.\d+)(E[\+-]?\d+)?|([1-9]\d*E[\+-]?\d+))') 
        IS_INT = re.compile(r'\d+')

        tokens = self.tokens

        precedence = (

        )

        def p_program(p):
            '''program : program statement
                       | statement'''
            if len(p) == 2 and p[1]:
                p[0] = {}
                p[0][self.line] = p[1]
                self.line += 1
            elif len(p) == 3:
                p[0] = p[1]
                if not p[0]: p[0] = {}
                if p[2]:
                    p[0][self.line] = p[2]
                    self.line += 1

        def p_statement(p):
            '''statement : command NEWLINE'''
            p[0] = p[1]

        def p_command_buy(p):
            '''command : buy this bar SEMI
                       | buy next bar at ID limit SEMI'''
            if len(p) == 5:
                p[0] = ('BUY', 0)
            else:
                p[0] = ('BUY', p[5])

        def p_command_sell(p):
            '''command : sell this bar SEMI
                       | sell next bar at ID limit SEMI'''
            if len(p) == 5:
                p[0] = ('SELL', 0)
            else:
                p[0] = ('SELL', p[5])

        def p_command_if_begin(p):
            '''command : if compare then begin'''
            p[0] = ('BEGIN', p[2])

        def p_command_if_end(p):
            '''command : end'''
            p[0] = ('END', 0)

        def p_command_if(p):
            '''command : if compare then'''
            p[0] = ('IF', p[2])

        def p_compare(p):
            '''compare : ID LT ID
                       | ID GT ID
                       | ID LE ID
                       | ID GE ID
                       | ID NE ID
                       | ID EQUALS ID'''
            p[0] = ('COMP', p[1], p[2], p[3])

        def p_command_input(p):
            '''command : inputs COLON variable SEMI
                       | inputs COLON varlist SEMI'''
            p[0] = ('VAR', p[3])

        def p_varlist(p):
            '''varlist : varlist COMMA variable
                       | varlist COMMA NEWLINE variable
                       | variable'''
            if len(p) == 4:
                p[0] = list(p[1])
                p[0].append(p[3])
            elif len(p) == 5:
                p[0] = list(p[1])
                p[0].append(p[4])
            else:
                p[0] = []
                p[0].append(p[1])

        def p_variable(p):
            '''variable : ID LPAREN expression RPAREN'''
            p[0] = (p[1], p[3])

        def p_expression_value(p):
            '''expression : INTEGER
                          | FLOAT
                          | STRING'''
            if IS_FLOAT.search(p[1]):
                p[0] = float(p[1])
            elif IS_INT.search(p[1]):
                p[0] = int(p[1])
            else:
                p[0] = p[1]

        def p_error(p):
            if not p:
                print("SYNTAX ERROR AT EOF")

        self.easylex()
        parser = yacc.yacc()
        return parser

    def parser(self):
        return self.easyparse()

if __name__ == '__main__':
    data = '''
    inputs:     HighPrice(200.0),
            LowPrice(200.0),
            setTime(235500);

    if Time < setTime then begin
    if close > HighPrice then 
        sell this bar;
    if close < LowPrice then
        buy this bar;
    end
    '''
    easy = EasyParser()
    # lexer = easy.easylex()
    # lexer.input(data)
    # for tok in lexer:
    #     print tok
    parser = easy.parser()
    prog = parser.parse(data)
    print prog

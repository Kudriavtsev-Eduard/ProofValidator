from src.statements import *


class Parser:
    @staticmethod
    def remove_space(in_line: str) -> str:
        line = ''

        for x in in_line:
            if not x.isspace():
                line += x
        return line

    @staticmethod
    def parse_statement(_line):
        pos = 0
        line = Parser.remove_space(_line) + '#'

        def skip(s):
            nonlocal pos, line
            if line.startswith(s, pos):
                pos += len(s)
                return True
            return False

        def e():
            x = dij()
            if skip(Operation.IMPLICATION.value):
                x = Implication(x, e())
            return x

        def dij():
            x = con()
            while skip(Operation.OR.value):
                x = Or(x, con())
            return x

        def con():
            x = nt()
            while skip(Operation.AND.value):
                x = And(x, nt())
            return x

        def nt():
            nonlocal pos, line
            if skip('('):
                x = e()
                skip(')')
                return x
            if skip(Operation.NOT.value):
                return Not(nt())
            x = ''
            while line[pos].isdigit() or line[pos].isalpha() or line[pos] == "'":
                x += line[pos]
                pos += 1
            return Variable(x)

        return e()

    @staticmethod
    def parse_full(_line: str) -> FullStatement:
        line = Parser.remove_space(_line)
        context, statement = line.split('|-')
        if context:
            context = list(map(Parser.parse_statement, context.split(',')))
        else:
            context = []
        statement = Parser.parse_statement(statement)
        return FullStatement(context, statement)

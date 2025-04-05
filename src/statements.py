from enum import Enum
import typing as tp


class Operation(Enum):
    IMPLICATION = '->'
    AND = '&'
    OR = '|'
    NOT = '!'


class Statement:
    def __init__(self, statements: str | tuple[tp.Any, ...],
                 operation: Operation | None = None):
        self.statements = statements
        self.operation = operation
        self.__str_value = self.__get_str_value()

    def __get_str_value(self) -> str:
        if self.operation is None:
            return self.statements
        else:
            return f'({self.operation.value},{",".join(map(str, self.statements))})'

    def __str__(self):
        return self.__str_value

    def __eq__(self, other):
        return self.__str_value == other.__str_value

    def __hash__(self):
        return hash(self.__str_value)


class FullStatement:
    def __init__(self, context: list[Statement], statement: Statement):
        self.context = context
        self.statement = statement

    def deduction_down(self):
        if self.statement.operation != Operation.IMPLICATION:
            return False
        to_context = self.statement.statements[0]
        new_statement = self.statement.statements[1]
        self.context.append(to_context)
        self.statement = new_statement
        return True

    def get_context_str(self) -> str:
        return ';'.join(sorted(list(map(str, self.context))))


class Implication(Statement):
    def __init__(self, left: Statement, right: Statement):
        super().__init__((left, right), Operation.IMPLICATION)


class And(Statement):
    def __init__(self, left: Statement, right: Statement):
        super().__init__((left, right), Operation.AND)


class Or(Statement):
    def __init__(self, left: Statement, right: Statement):
        super().__init__((left, right), Operation.OR)


class Not(Statement):
    def __init__(self, statement: Statement):
        super().__init__((statement,), Operation.NOT)

    def __str__(self):
        return f'({self.operation.value}{",".join(map(str, self.statements))})'


class Variable(Statement):
    def __init__(self, name: str):
        super().__init__(name)

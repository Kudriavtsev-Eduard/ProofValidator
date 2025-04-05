from src.statements import Statement


class Axiom:

    def __init__(self, scheme: Statement):
        self.scheme = scheme

    def satisfies(self, _statement: Statement) -> bool:
        meta_variables = dict()

        def checker(scheme: Statement | str, statement: Statement | str) -> bool:
            if scheme.operation is None:
                if scheme.statements not in meta_variables:
                    meta_variables[scheme.statements] = statement
                else:
                    if meta_variables[scheme.statements] != statement:
                        return False
                return True
            if scheme.operation != statement.operation:
                return False
            for stat1, stat2 in zip(scheme.statements, statement.statements):
                if not checker(stat1, stat2):
                    return False
            return True

        return checker(self.scheme, _statement)

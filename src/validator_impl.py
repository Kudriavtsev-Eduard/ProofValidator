from src.statements import *
from src.axiom import Axiom
from src.parser import Parser
import sys
from copy import deepcopy


class Validator:
    AXIOMS = list(map(lambda x: Axiom(Parser.parse_statement(x)),
                      ['A->B->A', '(A->B)->(A->B->C)->(A->C)', 'A->B->A&B',
                       'A&B->A', 'A&B->B', 'A->A|B', 'B->A|B',
                       '(A->C)->(B->C)->(A|B->C)',
                       '(A->B)->(A->!B)->!A', '!!A->A']))

    @staticmethod
    def __check_axioms(full_statement: FullStatement) -> int:
        for num, axiom in enumerate(Validator.AXIOMS):
            if axiom.satisfies(full_statement.statement):
                return num + 1
        return -1

    @staticmethod
    def __check_modus(checking: FullStatement, context: str,
                      modus_contexts: dict[str, dict[str, list[tuple[int, str]]]],
                      numbers: dict[str, dict[str, int]]) -> \
            tuple[int, int] | None:
        if context not in modus_contexts:
            return None
        if str(checking.statement) not in modus_contexts[context]:
            return None
        for num2, a_key in modus_contexts[context][str(checking.statement)]:
            if a_key not in numbers[context]:
                continue
            num1 = numbers[context][a_key]
            return num1, num2
        return None

    @staticmethod
    def __check_deduction(statement: str, context: str,
                          deduct_contexts: dict[str, dict[str, int]]) -> int:
        if context not in deduct_contexts:
            return -1
        if statement not in deduct_contexts[context]:
            return -1
        return deduct_contexts[context][statement]

    @staticmethod
    def __deduct_max(statement: FullStatement) -> FullStatement:
        cp = deepcopy(statement)
        while cp.deduction_down():
            pass
        return cp

    @staticmethod
    def __check_hypothesis(full_st: FullStatement) -> int:
        for i, statement in enumerate(full_st.context):
            if statement == full_st.statement:
                return i + 1
        return -1

    @staticmethod
    def __get_description(is_incorrect: list[bool],
                          modus_contexts: dict[
                              str, dict[str, list[tuple[int, str]]]],
                          deduct_contexts: dict[str, dict[str, int]],
                          checking: FullStatement,
                          context: str,
                          deduct_statement: str,
                          deduct_context: str,
                          numbers: dict[str, dict[str, int]]) -> str:
        if (ax_num := Validator.__check_axioms(checking)) != -1:
            return f'Ax. sch. {ax_num}'
        if (hyp_num := Validator.__check_hypothesis(checking)) != -1:
            return f'Hyp. {hyp_num}'
        if (ded_num := Validator.__check_deduction(deduct_statement, deduct_context,
                                                   deduct_contexts)) != -1:
            result = f'Ded. {ded_num}'
            if is_incorrect[ded_num - 1]:
                result += '; from Incorrect'
            return result
        if (
                modus_nums := Validator.__check_modus(checking, context,
                                                      modus_contexts, numbers)) is not None:
            result = f'M.P. {modus_nums[0]}, {modus_nums[1]}'
            if is_incorrect[modus_nums[0] - 1] or is_incorrect[modus_nums[1] - 1]:
                result += '; from Incorrect'
            return result
        return 'Incorrect'

    @staticmethod
    def validate(in_file: str | None = None, out_file: str | None = None) -> None:
        """
        Validates a proof of Classic statement
        :param in_file: file, where a proof is located. Default: None - stdin
        :param out_file: file, where an annotated proof and final verdict will be located. Default: None - stdout
        """
        sys.setrecursionlimit(2 ** 30)
        is_incorrect = []
        numbers: dict[str, dict[str, int]] = dict()
        modus_contexts: dict[str, dict[str, list[tuple[int, str]]]] = dict()
        deduct_contexts: dict[str, dict[str, int]] = dict()
        fin = open(in_file) if in_file is not None else sys.stdin
        fout = open(out_file, "w") if out_file is not None else sys.stdout
        for i, line in enumerate(fin):
            value = Parser.parse_full(line)
            s = value.get_context_str()
            deducted = Validator.__deduct_max(value)
            s1 = deducted.get_context_str()
            description = Validator.__get_description(is_incorrect, modus_contexts,
                                                      deduct_contexts, value, s,
                                                      str(deducted.statement), s1, numbers)
            is_incorrect.append(description == 'Incorrect')
            fout.write(f'[{i + 1}] {Parser.remove_space(line)} [{description}]\n')
            if s not in numbers:
                numbers[s] = dict()
            numbers[s][str(value.statement)] = i + 1
            if value.statement.operation == Operation.IMPLICATION:
                b_key = str(value.statement.statements[1])
                a_key = str(value.statement.statements[0])
                if s not in modus_contexts:
                    modus_contexts[s] = dict()
                if b_key not in modus_contexts[s]:
                    modus_contexts[s][b_key] = []
                modus_contexts[s][b_key].append((i + 1, a_key))
            if s1 not in deduct_contexts:
                deduct_contexts[s1] = dict()
            deduct_contexts[s1][str(deducted.statement)] = i + 1
        fout.write("Verdict: ")
        if True in is_incorrect:
            fout.write(f"Incorrect proof. First mistake in line number: {is_incorrect.index(True) + 1}\n")
        else:
            fout.write("Correct proof.\n")
        if in_file is not None:
            fin.close()
        if out_file is not None:
            fout.close()

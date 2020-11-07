# In The Name Of GOD
# Ahmad Zaferani 97105985
# Ali Shirmohammadi 97106068
from scanner import get_next_token
from anytree import Node, RenderTree

valid_tokens = {"KEYWORD", "SYMBOL", "NUM", "WHITESPACE", "ID", "COMMENT"}
errors = {"Invalid number", "Invalid input", "Unmatched comment", "Unclosed comment"}
parse_table = [
    ['', 'int', 'void', '$', '{', 'break', ';', 'if', 'while', 'return', 'switch', 'ID', '+', '-', '(', 'NUM', '}', '[',
     ',', ')', 'else', 'case', 'default', ']', '=', '*', '<', '==', ':'],
    ['Program', ['DeclarationList', '$'], ['DeclarationList', '$'], ['DeclarationList', '$'], '', '', '', '', '', '',
     '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['DeclarationList', ['Declaration', 'DeclarationList'], ['Declaration', 'DeclarationList'], 'epsilon', 'epsilon',
     'epsilon', 'epsilon', 'epsilon', 'epsilon', 'epsilon', 'epsilon', 'epsilon', 'epsilon', 'epsilon', 'epsilon',
     'epsilon', 'epsilon', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['Declaration', ['DeclarationInitial', 'DeclarationPrime'], ['DeclarationInitial', 'DeclarationPrime'], 'synch',
     'synch', 'synch', 'synch', 'synch', 'synch', 'synch', 'synch', 'synch', 'synch', 'synch', 'synch', 'synch',
     'synch', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['DeclarationInitial', ['TypeSpecifier', 'ID'], ['TypeSpecifier', 'ID'], '', '', '', 'synch', '', '', '', '', '',
     '', '', 'synch', '', '', 'synch', 'synch', 'synch', '', '', '', '', '', '', '', '', ''],
    ['DeclarationPrime', 'synch', 'synch', 'synch', 'synch', 'synch', ['VarDeclarationPrime'], 'synch', 'synch',
     'synch', 'synch', 'synch', 'synch', 'synch', ['FunDeclarationPrime'], 'synch', 'synch', ['VarDeclarationPrime'],
     '', '', '', '', '', '', '', '', '', '', ''],
    ['VarDeclarationPrime', 'synch', 'synch', 'synch', 'synch', 'synch', [';'], 'synch', 'synch', 'synch', 'synch',
     'synch', 'synch', 'synch', 'synch', 'synch', 'synch', ['[', 'NUM', ']', ';'], '', '', '', '', '', '', '', '', '',
     '', ''],
    ['FunDeclarationPrime', 'synch', 'synch', 'synch', 'synch', 'synch', 'synch', 'synch', 'synch', 'synch', 'synch',
     'synch', 'synch', 'synch', ['(', 'Params', ')', 'CompoundStmt'], 'synch', 'synch', '', '', '', '', '', '', '', '',
     '', '', '', ''],
    ['TypeSpecifier', ['int'], ['void'], '', '', '', '', '', '', '', '', 'synch', '', '', '', '', '', '', '', '', '',
     '', '', '', '', '', '', '', ''],
    ['Params', ['int', 'ID', 'ParamPrime', 'ParamList'], ['void', 'ParamListVoidAbtar'], '', '', '', '', '', '', '', '',
     '', '', '', '', '', '', '', '', 'synch', '', '', '', '', '', '', '', '', ''],
    ['ParamListVoidAbtar', '', '', '', '', '', '', '', '', '', '', ['ID', 'ParamPrime', 'ParamList'], '', '', '', '',
     '', '', '', 'epsilon', '', '', '', '', '', '', '', '', ''],
    ['ParamList', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', [',', 'Param', 'ParamList'],
     'epsilon', '', '', '', '', '', '', '', '', ''],
    ['Param', ['DeclarationInitial', 'ParamPrime'], ['DeclarationInitial', 'ParamPrime'], '', '', '', '', '', '', '',
     '', '', '', '', '', '', '', '', 'synch', 'synch', '', '', '', '', '', '', '', '', ''],
    ['ParamPrime', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ['[', ']'], 'epsilon', 'epsilon', '',
     '', '', '', '', '', '', '', ''],
    ['CompoundStmt', 'synch', 'synch', 'synch', ['{', 'DeclarationList', 'StatementList', '}'], 'synch', 'synch',
     'synch', 'synch', 'synch', 'synch', 'synch', 'synch', 'synch', 'synch', 'synch', 'synch', '', '', '', 'synch',
     'synch', 'synch', '', '', '', '', '', ''],
    ['StatementList', '', '', '', ['Statement', 'StatementList'], ['Statement', 'StatementList'],
     ['Statement', 'StatementList'], ['Statement', 'StatementList'], ['Statement', 'StatementList'],
     ['Statement', 'StatementList'], ['Statement', 'StatementList'], ['Statement', 'StatementList'],
     ['Statement', 'StatementList'], ['Statement', 'StatementList'], ['Statement', 'StatementList'],
     ['Statement', 'StatementList'], 'epsilon', '', '', '', '', 'epsilon', 'epsilon', '', '', '', '', '', ''],
    ['Statement', '', '', '', ['CompoundStmt'], ['ExpressionStmt'], ['ExpressionStmt'], ['SelectionStmt'],
     ['IterationStmt'], ['ReturnStmt'], ['SwitchStmt'], ['ExpressionStmt'], ['ExpressionStmt'], ['ExpressionStmt'],
     ['ExpressionStmt'], ['ExpressionStmt'], 'synch', '', '', '', 'synch', 'synch', 'synch', '', '', '', '', '', ''],
    ['ExpressionStmt', '', '', '', 'synch', ['break', ';'], [';'], 'synch', 'synch', 'synch', 'synch',
     ['Expression', ';'], ['Expression', ';'], ['Expression', ';'], ['Expression', ';'], ['Expression', ';'], 'synch',
     '', '', '', 'synch', 'synch', 'synch', '', '', '', '', '', ''],
    ['SelectionStmt', '', '', '', 'synch', 'synch', 'synch',
     ['if', '(', 'Expression', ')', 'Statement', 'else', 'Statement'], 'synch', 'synch', 'synch', 'synch', 'synch',
     'synch', 'synch', 'synch', 'synch', '', '', '', 'synch', 'synch', 'synch', '', '', '', '', '', ''],
    ['IterationStmt', '', '', '', 'synch', 'synch', 'synch', 'synch', ['while', '(', 'Expression', ')', 'Statement'],
     'synch', 'synch', 'synch', 'synch', 'synch', 'synch', 'synch', 'synch', '', '', '', 'synch', 'synch', 'synch', '',
     '', '', '', '', ''],
    ['ReturnStmt', '', '', '', 'synch', 'synch', 'synch', 'synch', 'synch', ['return', 'ReturnStmtPrime'], 'synch',
     'synch', 'synch', 'synch', 'synch', 'synch', 'synch', '', '', '', 'synch', 'synch', 'synch', '', '', '', '', '',
     ''],
    ['ReturnStmtPrime', '', '', '', 'synch', 'synch', [';'], 'synch', 'synch', 'synch', 'synch', ['Expression', ';'],
     ['Expression', ';'], ['Expression', ';'], ['Expression', ';'], ['Expression', ';'], 'synch', '', '', '', 'synch',
     'synch', 'synch', '', '', '', '', '', ''],
    ['SwitchStmt', '', '', '', 'synch', 'synch', 'synch', 'synch', 'synch', 'synch',
     ['switch', '(', 'Expression', ')', '{', 'CaseStmts', 'DefaultStmt', '}'], 'synch', 'synch', 'synch', 'synch',
     'synch', 'synch', '', '', '', 'synch', 'synch', 'synch', '', '', '', '', '', ''],
    ['CaseStmts', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'epsilon', '', '', '', '',
     ['CaseStmt', 'CaseStmts'], 'epsilon', '', '', '', '', '', ''],
    ['CaseStmt', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'synch', '', '', '', '',
     ['case', 'NUM', ':', 'StatementList'], 'synch', '', '', '', '', '', ''],
    ['DefaultStmt', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'epsilon', '', '', '', '', '',
     ['default', ':', 'StatementList'], '', '', '', '', '', ''],
    ['Expression', '', '', '', '', '', 'synch', '', '', '', '', ['ID', 'B'], ['SimpleExpressionZegond'],
     ['SimpleExpressionZegond'], ['SimpleExpressionZegond'], ['SimpleExpressionZegond'], '', '', 'synch', 'synch', '',
     '', '', 'synch', '', '', '', '', ''],
    ['B', '', '', '', '', '', 'epsilon', '', '', '', '', '', ['SimpleExpressionPrime'], ['SimpleExpressionPrime'],
     ['SimpleExpressionPrime'], '', '', ['[', 'Expression', ']', 'H'], 'epsilon', 'epsilon', '', '', '', 'epsilon',
     ['=', 'Expression'], ['SimpleExpressionPrime'], ['SimpleExpressionPrime'], ['SimpleExpressionPrime'],
     ['SimpleExpressionPrime']],
    ['H', '', '', '', '', '', 'epsilon', '', '', '', '', '', ['G', 'D', 'C'], ['G', 'D', 'C'], '', '', '', '',
     'epsilon', 'epsilon', '', '', '', 'epsilon', ['=', 'Expression'], ['G', 'D', 'C'], ['G', 'D', 'C'],
     ['G', 'D', 'C'], ''],
    ['SimpleExpressionZegond', '', '', '', '', '', 'synch', '', '', '', '', '', ['AdditiveExpressionZegond', 'C'],
     ['AdditiveExpressionZegond', 'C'], ['AdditiveExpressionZegond', 'C'], ['AdditiveExpressionZegond', 'C'], '', '',
     'synch', 'synch', '', '', '', 'synch', '', '', '', '', ''],
    ['SimpleExpressionPrime', '', '', '', '', '', 'epsilon', '', '', '', '', '', ['AdditiveExpressionPrime', 'C'],
     ['AdditiveExpressionPrime', 'C'], ['AdditiveExpressionPrime', 'C'], '', '', '', 'epsilon', 'epsilon', '', '', '',
     'epsilon', '', ['AdditiveExpressionPrime', 'C'], ['AdditiveExpressionPrime', 'C'],
     ['AdditiveExpressionPrime', 'C'], ['AdditiveExpressionPrime', 'C']],
    ['C', '', '', '', '', '', 'epsilon', '', '', '', '', '', '', '', '', '', '', '', 'epsilon', 'epsilon', '', '', '',
     'epsilon', '', '', ['Relop', 'AdditiveExpression'], ['Relop', 'AdditiveExpression'], ''],
    ['Relop', '', '', '', '', '', '', '', '', '', '', 'synch', 'synch', 'synch', 'synch', 'synch', '', '', '', '', '',
     '', '', '', '', '', ['<'], ['=='], ''],
    ['AdditiveExpression', '', '', '', '', '', 'synch', '', '', '', '', ['Term', 'D'], ['Term', 'D'], ['Term', 'D'],
     ['Term', 'D'], ['Term', 'D'], '', '', 'synch', 'synch', '', '', '', 'synch', '', '', '', '', ''],
    ['AdditiveExpressionPrime', '', '', '', '', '', 'epsilon', '', '', '', '', '', ['TermPrime', 'D'],
     ['TermPrime', 'D'], ['TermPrime', 'D'], '', '', '', 'epsilon', 'epsilon', '', '', '', 'epsilon', '',
     ['TermPrime', 'D'], 'epsilon', 'epsilon', ['TermPrime', 'D']],
    ['AdditiveExpressionZegond', '', '', '', '', '', 'synch', '', '', '', '', '', ['TermZegond', 'D'],
     ['TermZegond', 'D'], ['TermZegond', 'D'], ['TermZegond', 'D'], '', '', 'synch', 'synch', '', '', '', 'synch', '',
     '', 'synch', 'synch', ''],
    ['D', '', '', '', '', '', 'epsilon', '', '', '', '', '', ['Addop', 'Term', 'D'], ['Addop', 'Term', 'D'], '', '', '',
     '', 'epsilon', 'epsilon', '', '', '', 'epsilon', '', '', 'epsilon', 'epsilon', ''],
    ['Addop', '', '', '', '', '', '', '', '', '', '', 'synch', ['+'], ['-'], 'synch', 'synch', '', '', '', '', '', '',
     '', '', '', '', '', '', ''],
    ['Term', '', '', '', '', '', 'synch', '', '', '', '', ['SignedFactor', 'G'], ['SignedFactor', 'G'],
     ['SignedFactor', 'G'], ['SignedFactor', 'G'], ['SignedFactor', 'G'], '', '', 'synch', 'synch', '', '', '', 'synch',
     '', '', 'synch', 'synch', ''],
    ['TermPrime', '', '', '', '', '', 'epsilon', '', '', '', '', '', 'epsilon', 'epsilon', ['SignedFactorPrime', 'G'],
     '', '', '', 'epsilon', 'epsilon', '', '', '', 'epsilon', '', ['SignedFactorPrime', 'G'], 'epsilon', 'epsilon',
     ['SignedFactorPrime', 'G']],
    ['TermZegond', '', '', '', '', '', 'synch', '', '', '', '', '', ['SignedFactorZegond', 'G'],
     ['SignedFactorZegond', 'G'], ['SignedFactorZegond', 'G'], ['SignedFactorZegond', 'G'], '', '', 'synch', 'synch',
     '', '', '', 'synch', '', '', 'synch', 'synch', ''],
    ['G', '', '', '', '', '', 'epsilon', '', '', '', '', '', 'epsilon', 'epsilon', '', '', '', '', 'epsilon', 'epsilon',
     '', '', '', 'epsilon', '', ['*', 'SignedFactor', 'G'], 'epsilon', 'epsilon', ''],
    ['SignedFactor', '', '', '', '', '', 'synch', '', '', '', '', ['Factor'], ['+', 'Factor'], ['-', 'Factor'],
     ['Factor'], ['Factor'], '', '', 'synch', 'synch', '', '', '', 'synch', '', 'synch', 'synch', 'synch', ''],
    ['SignedFactorPrime', '', '', '', '', '', 'epsilon', '', '', '', '', '', 'epsilon', 'epsilon', ['FactorPrime'], '',
     '', '', 'epsilon', 'epsilon', '', '', '', 'epsilon', '', 'epsilon', 'epsilon', 'epsilon', ['FactorPrime']],
    ['SignedFactorZegond', '', '', '', '', '', 'synch', '', '', '', '', '', ['+', 'Factor'], ['-', 'Factor'],
     ['FactorZegond'], ['FactorZegond'], '', '', 'synch', 'synch', '', '', '', 'synch', '', 'synch', 'synch', 'synch',
     ''],
    ['Factor', '', '', '', '', '', 'synch', '', '', '', '', ['ID', 'VarCallPrime'], 'synch', 'synch',
     ['(', 'Expression', ')'], ['NUM'], '', '', 'synch', 'synch', '', '', '', 'synch', '', 'synch', 'synch', 'synch',
     ''],
    ['VarCallPrime', '', '', '', '', '', 'epsilon', '', '', '', '', '', 'epsilon', 'epsilon', ['(', 'Args', ')'], '',
     '', ['VarPrime'], 'epsilon', 'epsilon', '', '', '', 'epsilon', '', 'epsilon', 'epsilon', 'epsilon', ''],
    ['VarPrime', '', '', '', '', '', 'epsilon', '', '', '', '', '', 'epsilon', 'epsilon', '', '', '',
     ['[', 'Expression', ']'], 'epsilon', 'epsilon', '', '', '', 'epsilon', '', 'epsilon', 'epsilon', 'epsilon', ''],
    ['FactorPrime', '', '', '', '', '', 'epsilon', '', '', '', '', '', 'epsilon', 'epsilon', ['(', 'Args', ')'], '', '',
     '', 'epsilon', 'epsilon', '', '', '', 'epsilon', '', 'epsilon', 'epsilon', 'epsilon', ''],
    ['FactorZegond', '', '', '', '', '', 'synch', '', '', '', '', '', 'synch', 'synch', ['(', 'Expression', ')'],
     ['NUM'], '', '', 'synch', 'synch', '', '', '', 'synch', '', 'synch', 'synch', 'synch', ''],
    ['Args', '', '', '', '', '', '', '', '', '', '', ['ArgList'], ['ArgList'], ['ArgList'], ['ArgList'], ['ArgList'],
     '', '', '', 'epsilon', '', '', '', '', '', '', '', '', ''],
    ['ArgList', '', '', '', '', '', '', '', '', '', '', ['Expression', 'ArgListPrime'], ['Expression', 'ArgListPrime'],
     ['Expression', 'ArgListPrime'], ['Expression', 'ArgListPrime'], ['Expression', 'ArgListPrime'], '', '', '',
     'synch', '', '', '', '', '', '', '', '', ''],
    ['ArgListPrime', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
     [',', 'Expression', 'ArgListPrime'], 'epsilon', '', '', '', '', '', '', '', '', '']]
parse_table_dim = len(parse_table), len(parse_table[0])

# read input, tokenize it using scanner
with open("input.txt", "r") as file:
    s = file.read()
    s += '\n'
i = 0
tokens = []
while i < len(s):
    t = get_next_token(s, i)
    i += len(t[1])
    tokens.append(t)
tokens.append(('KEYWORD', '$'))

# main parser program
stack = ['Program']
root = Node('Program')
token_index = 0


def find_in_table(row, col):
    ii = 0
    jj = 0
    for ii in range(1, parse_table_dim[0]):
        if row == parse_table[ii][0]:
            break
    for jj in range(1, parse_table_dim[1]):
        if col == parse_table[0][jj]:
            break
    return parse_table[ii][jj]


line_counter = 1
linely_syntax_errors = []
this_line_syntax_errors = []
while stack:
    t = tokens[token_index]
    if t[0] == 'SYMBOL' or t[0] == 'KEYWORD':
        a = t[1]
    else:
        a = t[0]
    X = stack[-1]
    if t[0] in valid_tokens:
        if t[0] == 'WHITESPACE' or t[0] == 'COMMENT':
            if t[1] == "\n":
                if len(this_line_syntax_errors) != 0:
                    linely_syntax_errors.append((line_counter, this_line_syntax_errors.copy()))
                    this_line_syntax_errors = []
                line_counter += 1
            token_index += 1
            continue

        print(X, a)
        if X == a == '$':
            print("Compiled Successfully!")
            break
        elif X == a and a != '$':
            stack.pop()
            token_index += 1
        elif X not in parse_table[0]:
            M = find_in_table(X, a)
            print(M)

            if isinstance(M, list):
                stack.pop()
                for s in reversed(M):
                    stack.append(s)
            elif M == 'epsilon':
                stack.pop()
            elif M == '':  # panic mode starts from here
                if a == '$':
                    this_line_syntax_errors.append("unexpected EOF")
                    line_counter -= 1
                    break
                token_index += 1
                this_line_syntax_errors.append("illegal %s" % a)
                print(this_line_syntax_errors)
            elif M == 'synch':
                stack.pop()
                this_line_syntax_errors.append("Missing %s" % X)
        elif X in parse_table[0]:
            stack.pop()
            this_line_syntax_errors.append("Missing %s" % X)
        else:
            pass  # todo: handle!
        print(stack, token_index)

    elif t[0] in errors:
        raise Exception("Lexical Error: ", t)
    else:
        raise ValueError(t)
if len(this_line_syntax_errors) != 0:
    linely_syntax_errors.append((line_counter, this_line_syntax_errors))

# create parse tree
# with open("parse_tree.txt", 'w', encoding='utf-8') as file:
#     for pre, fill, node in RenderTree(root):
#         file.write("%s%s" % (pre, node.name))

# create syntax errors file
with open("syntax_errors.txt", "w") as file:
    if len(linely_syntax_errors) == 0:
        file.write("There is no syntax error.\n")
    else:
        string = ""
        for le in linely_syntax_errors:
            for e in le[1]:
                string += "#%d : syntax error, %s\n" % (le[0], e)
        file.write(string)

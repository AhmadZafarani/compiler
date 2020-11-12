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
    ['Program', ['Declaration-list', '$'], ['Declaration-list', '$'], ['Declaration-list', '$'], '', '', '', '', '', '',
     '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['Declaration-list', ['Declaration', 'Declaration-list'], ['Declaration', 'Declaration-list'], 'epsilon', 'epsilon',
     'epsilon', 'epsilon', 'epsilon', 'epsilon', 'epsilon', 'epsilon', 'epsilon', 'epsilon', 'epsilon', 'epsilon',
     'epsilon', 'epsilon', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['Declaration', ['Declaration-initial', 'Declaration-prime'], ['Declaration-initial', 'Declaration-prime'], 'synch',
     'synch', 'synch', 'synch', 'synch', 'synch', 'synch', 'synch', 'synch', 'synch', 'synch', 'synch', 'synch',
     'synch', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['Declaration-initial', ['TypeSpecifier', 'ID'], ['TypeSpecifier', 'ID'], '', '', '', 'synch', '', '', '', '', '',
     '', '', 'synch', '', '', 'synch', 'synch', 'synch', '', '', '', '', '', '', '', '', ''],
    ['Declaration-prime', 'synch', 'synch', 'synch', 'synch', 'synch', ['Var-declaration-prime'], 'synch', 'synch',
     'synch', 'synch', 'synch', 'synch', 'synch', ['Fun-declaration-prime'], 'synch', 'synch',
     ['Var-declaration-prime'],
     '', '', '', '', '', '', '', '', '', '', ''],
    ['Var-declaration-prime', 'synch', 'synch', 'synch', 'synch', 'synch', [';'], 'synch', 'synch', 'synch', 'synch',
     'synch', 'synch', 'synch', 'synch', 'synch', 'synch', ['[', 'NUM', ']', ';'], '', '', '', '', '', '', '', '', '',
     '', ''],
    ['Fun-declaration-prime', 'synch', 'synch', 'synch', 'synch', 'synch', 'synch', 'synch', 'synch', 'synch', 'synch',
     'synch', 'synch', 'synch', ['(', 'Params', ')', 'Compound-stmt'], 'synch', 'synch', '', '', '', '', '', '', '', '',
     '', '', '', ''],
    ['TypeSpecifier', ['int'], ['void'], '', '', '', '', '', '', '', '', 'synch', '', '', '', '', '', '', '', '', '',
     '', '', '', '', '', '', '', ''],
    ['Params', ['int', 'ID', 'Param--prime', 'Param-list'], ['void', 'Param-list-void-abtar'], '', '', '', '', '', '',
     '',
     '',
     '', '', '', '', '', '', '', '', 'synch', '', '', '', '', '', '', '', '', ''],
    ['Param-list-void-abtar', '', '', '', '', '', '', '', '', '', '', ['ID', 'Param--prime', 'Param-list'], '', '', '',
     '',
     '', '', '', 'epsilon', '', '', '', '', '', '', '', '', ''],
    ['Param-list', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', [',', 'Param', 'Param-list'],
     'epsilon', '', '', '', '', '', '', '', '', ''],
    ['Param', ['Declaration-initial', 'Param--prime'], ['Declaration-initial', 'Param--prime'], '', '', '', '', '', '',
     '',
     '', '', '', '', '', '', '', '', 'synch', 'synch', '', '', '', '', '', '', '', '', ''],
    ['Param--prime', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ['[', ']'], 'epsilon', 'epsilon',
     '',
     '', '', '', '', '', '', '', ''],
    ['Compound-stmt', 'synch', 'synch', 'synch', ['{', 'Declaration-list', 'Statement-list', '}'], 'synch', 'synch',
     'synch', 'synch', 'synch', 'synch', 'synch', 'synch', 'synch', 'synch', 'synch', 'synch', '', '', '', 'synch',
     'synch', 'synch', '', '', '', '', '', ''],
    ['Statement-list', '', '', '', ['Statement', 'Statement-list'], ['Statement', 'Statement-list'],
     ['Statement', 'Statement-list'], ['Statement', 'Statement-list'], ['Statement', 'Statement-list'],
     ['Statement', 'Statement-list'], ['Statement', 'Statement-list'], ['Statement', 'Statement-list'],
     ['Statement', 'Statement-list'], ['Statement', 'Statement-list'], ['Statement', 'Statement-list'],
     ['Statement', 'Statement-list'], 'epsilon', '', '', '', '', 'epsilon', 'epsilon', '', '', '', '', '', ''],
    ['Statement', '', '', '', ['Compound-stmt'], ['Expression-stmt'], ['Expression-stmt'], ['Selection-stmt'],
     ['Iteration-stmt'], ['Return-stmt'], ['Switch-stmt'], ['Expression-stmt'], ['Expression-stmt'],
     ['Expression-stmt'],
     ['Expression-stmt'], ['Expression-stmt'], 'synch', '', '', '', 'synch', 'synch', 'synch', '', '', '', '', '', ''],
    ['Expression-stmt', '', '', '', 'synch', ['break', ';'], [';'], 'synch', 'synch', 'synch', 'synch',
     ['Expression', ';'], ['Expression', ';'], ['Expression', ';'], ['Expression', ';'], ['Expression', ';'], 'synch',
     '', '', '', 'synch', 'synch', 'synch', '', '', '', '', '', ''],
    ['Selection-stmt', '', '', '', 'synch', 'synch', 'synch',
     ['if', '(', 'Expression', ')', 'Statement', 'else', 'Statement'], 'synch', 'synch', 'synch', 'synch', 'synch',
     'synch', 'synch', 'synch', 'synch', '', '', '', 'synch', 'synch', 'synch', '', '', '', '', '', ''],
    ['Iteration-stmt', '', '', '', 'synch', 'synch', 'synch', 'synch', ['while', '(', 'Expression', ')', 'Statement'],
     'synch', 'synch', 'synch', 'synch', 'synch', 'synch', 'synch', 'synch', '', '', '', 'synch', 'synch', 'synch', '',
     '', '', '', '', ''],
    ['Return-stmt', '', '', '', 'synch', 'synch', 'synch', 'synch', 'synch', ['return', 'Return-stmt-prime'], 'synch',
     'synch', 'synch', 'synch', 'synch', 'synch', 'synch', '', '', '', 'synch', 'synch', 'synch', '', '', '', '', '',
     ''],
    ['Return-stmt-prime', '', '', '', 'synch', 'synch', [';'], 'synch', 'synch', 'synch', 'synch', ['Expression', ';'],
     ['Expression', ';'], ['Expression', ';'], ['Expression', ';'], ['Expression', ';'], 'synch', '', '', '', 'synch',
     'synch', 'synch', '', '', '', '', '', ''],
    ['Switch-stmt', '', '', '', 'synch', 'synch', 'synch', 'synch', 'synch', 'synch',
     ['switch', '(', 'Expression', ')', '{', 'Case-stmts', 'Default-stmt', '}'], 'synch', 'synch', 'synch', 'synch',
     'synch', 'synch', '', '', '', 'synch', 'synch', 'synch', '', '', '', '', '', ''],
    ['Case-stmts', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'epsilon', '', '', '', '',
     ['Case-stmt', 'Case-stmts'], 'epsilon', '', '', '', '', '', ''],
    ['Case-stmt', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'synch', '', '', '', '',
     ['case', 'NUM', ':', 'Statement-list'], 'synch', '', '', '', '', '', ''],
    ['Default-stmt', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'epsilon', '', '', '', '', '',
     ['default', ':', 'Statement-list'], '', '', '', '', '', ''],
    ['Expression', '', '', '', '', '', 'synch', '', '', '', '', ['ID', 'B'], ['Simple-expression-zegond'],
     ['Simple-expression-zegond'], ['Simple-expression-zegond'], ['Simple-expression-zegond'], '', '', 'synch', 'synch',
     '',
     '', '', 'synch', '', '', '', '', ''],
    ['B', '', '', '', '', '', 'epsilon', '', '', '', '', '', ['Simple-expression-prime'], ['Simple-expression-prime'],
     ['Simple-expression-prime'], '', '', ['[', 'Expression', ']', 'H'], 'epsilon', 'epsilon', '', '', '', 'epsilon',
     ['=', 'Expression'], ['Simple-expression-prime'], ['Simple-expression-prime'], ['Simple-expression-prime'],
     ['Simple-expression-prime']],
    ['H', '', '', '', '', '', 'epsilon', '', '', '', '', '', ['G', 'D', 'C'], ['G', 'D', 'C'], '', '', '', '',
     'epsilon', 'epsilon', '', '', '', 'epsilon', ['=', 'Expression'], ['G', 'D', 'C'], ['G', 'D', 'C'],
     ['G', 'D', 'C'], ''],
    ['Simple-expression-zegond', '', '', '', '', '', 'synch', '', '', '', '', '', ['Additive-expression-zegond', 'C'],
     ['Additive-expression-zegond', 'C'], ['Additive-expression-zegond', 'C'], ['Additive-expression-zegond', 'C'], '',
     '',
     'synch', 'synch', '', '', '', 'synch', '', '', '', '', ''],
    ['Simple-expression-prime', '', '', '', '', '', 'epsilon', '', '', '', '', '', ['Additive-expression-prime', 'C'],
     ['Additive-expression-prime', 'C'], ['Additive-expression-prime', 'C'], '', '', '', 'epsilon', 'epsilon', '', '',
     '',
     'epsilon', '', ['Additive-expression-prime', 'C'], ['Additive-expression-prime', 'C'],
     ['Additive-expression-prime', 'C'], ['Additive-expression-prime', 'C']],
    ['C', '', '', '', '', '', 'epsilon', '', '', '', '', '', '', '', '', '', '', '', 'epsilon', 'epsilon', '', '', '',
     'epsilon', '', '', ['Relop', 'Additive-expression'], ['Relop', 'Additive-expression'], ''],
    ['Relop', '', '', '', '', '', '', '', '', '', '', 'synch', 'synch', 'synch', 'synch', 'synch', '', '', '', '', '',
     '', '', '', '', '', ['<'], ['=='], ''],
    ['Additive-expression', '', '', '', '', '', 'synch', '', '', '', '', ['Term', 'D'], ['Term', 'D'], ['Term', 'D'],
     ['Term', 'D'], ['Term', 'D'], '', '', 'synch', 'synch', '', '', '', 'synch', '', '', '', '', ''],
    ['Additive-expression-prime', '', '', '', '', '', 'epsilon', '', '', '', '', '', ['Term-prime', 'D'],
     ['Term-prime', 'D'], ['Term-prime', 'D'], '', '', '', 'epsilon', 'epsilon', '', '', '', 'epsilon', '',
     ['Term-prime', 'D'], 'epsilon', 'epsilon', ['Term-prime', 'D']],
    ['Additive-expression-zegond', '', '', '', '', '', 'synch', '', '', '', '', '', ['Term-zegond', 'D'],
     ['Term-zegond', 'D'], ['Term-zegond', 'D'], ['Term-zegond', 'D'], '', '', 'synch', 'synch', '', '', '', 'synch',
     '',
     '', 'synch', 'synch', ''],
    ['D', '', '', '', '', '', 'epsilon', '', '', '', '', '', ['Addop', 'Term', 'D'], ['Addop', 'Term', 'D'], '', '', '',
     '', 'epsilon', 'epsilon', '', '', '', 'epsilon', '', '', 'epsilon', 'epsilon', ''],
    ['Addop', '', '', '', '', '', '', '', '', '', '', 'synch', ['+'], ['-'], 'synch', 'synch', '', '', '', '', '', '',
     '', '', '', '', '', '', ''],
    ['Term', '', '', '', '', '', 'synch', '', '', '', '', ['Signed-factor', 'G'], ['Signed-factor', 'G'],
     ['Signed-factor', 'G'], ['Signed-factor', 'G'], ['Signed-factor', 'G'], '', '', 'synch', 'synch', '', '', '',
     'synch',
     '', '', 'synch', 'synch', ''],
    ['Term-prime', '', '', '', '', '', 'epsilon', '', '', '', '', '', 'epsilon', 'epsilon',
     ['Signed-factor-prime', 'G'],
     '', '', '', 'epsilon', 'epsilon', '', '', '', 'epsilon', '', ['Signed-factor-prime', 'G'], 'epsilon', 'epsilon',
     ['Signed-factor-prime', 'G']],
    ['Term-zegond', '', '', '', '', '', 'synch', '', '', '', '', '', ['Signed-factor-zegond', 'G'],
     ['Signed-factor-zegond', 'G'], ['Signed-factor-zegond', 'G'], ['Signed-factor-zegond', 'G'], '', '', 'synch',
     'synch',
     '', '', '', 'synch', '', '', 'synch', 'synch', ''],
    ['G', '', '', '', '', '', 'epsilon', '', '', '', '', '', 'epsilon', 'epsilon', '', '', '', '', 'epsilon', 'epsilon',
     '', '', '', 'epsilon', '', ['*', 'Signed-factor', 'G'], 'epsilon', 'epsilon', ''],
    ['Signed-factor', '', '', '', '', '', 'synch', '', '', '', '', ['Factor'], ['+', 'Factor'], ['-', 'Factor'],
     ['Factor'], ['Factor'], '', '', 'synch', 'synch', '', '', '', 'synch', '', 'synch', 'synch', 'synch', ''],
    ['Signed-factor-prime', '', '', '', '', '', 'epsilon', '', '', '', '', '', 'epsilon', 'epsilon', ['Factor-prime'],
     '',
     '', '', 'epsilon', 'epsilon', '', '', '', 'epsilon', '', 'epsilon', 'epsilon', 'epsilon', ['Factor-prime']],
    ['Signed-factor-zegond', '', '', '', '', '', 'synch', '', '', '', '', '', ['+', 'Factor'], ['-', 'Factor'],
     ['Factor-zegond'], ['Factor-zegond'], '', '', 'synch', 'synch', '', '', '', 'synch', '', 'synch', 'synch', 'synch',
     ''],
    ['Factor', '', '', '', '', '', 'synch', '', '', '', '', ['ID', 'Var-call-prime'], 'synch', 'synch',
     ['(', 'Expression', ')'], ['NUM'], '', '', 'synch', 'synch', '', '', '', 'synch', '', 'synch', 'synch', 'synch',
     ''],
    ['Var-call-prime', '', '', '', '', '', 'epsilon', '', '', '', '', '', 'epsilon', 'epsilon', ['(', 'Args', ')'], '',
     '', ['Var-prime'], 'epsilon', 'epsilon', '', '', '', 'epsilon', '', 'epsilon', 'epsilon', 'epsilon', ''],
    ['Var-prime', '', '', '', '', '', 'epsilon', '', '', '', '', '', 'epsilon', 'epsilon', '', '', '',
     ['[', 'Expression', ']'], 'epsilon', 'epsilon', '', '', '', 'epsilon', '', 'epsilon', 'epsilon', 'epsilon', ''],
    ['Factor-prime', '', '', '', '', '', 'epsilon', '', '', '', '', '', 'epsilon', 'epsilon', ['(', 'Args', ')'], '',
     '',
     '', 'epsilon', 'epsilon', '', '', '', 'epsilon', '', 'epsilon', 'epsilon', 'epsilon', ''],
    ['Factor-zegond', '', '', '', '', '', 'synch', '', '', '', '', '', 'synch', 'synch', ['(', 'Expression', ')'],
     ['NUM'], '', '', 'synch', 'synch', '', '', '', 'synch', '', 'synch', 'synch', 'synch', ''],
    ['Args', '', '', '', '', '', '', '', '', '', '', ['Arg-list'], ['Arg-list'], ['Arg-list'], ['Arg-list'],
     ['Arg-list'],
     '', '', '', 'epsilon', '', '', '', '', '', '', '', '', ''],
    ['Arg-list', '', '', '', '', '', '', '', '', '', '', ['Expression', 'Arg-list-prime'],
     ['Expression', 'Arg-list-prime'],
     ['Expression', 'Arg-list-prime'], ['Expression', 'Arg-list-prime'], ['Expression', 'Arg-list-prime'], '', '', '',
     'synch', '', '', '', '', '', '', '', '', ''],
    ['Arg-list-prime', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
     [',', 'Expression', 'Arg-list-prime'], 'epsilon', '', '', '', '', '', '', '', '', '']]
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
parent_stack = [root]
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
    stack_head = stack[-1]
    if t[0] in valid_tokens:
        if t[0] == 'WHITESPACE' or t[0] == 'COMMENT':
            if t[1] == "\n":
                if len(this_line_syntax_errors) != 0:
                    linely_syntax_errors.append((line_counter, this_line_syntax_errors.copy()))
                    this_line_syntax_errors = []
                line_counter += 1
            token_index += 1
            continue

        print(stack_head, a)
        if stack_head == a == '$':
            print("Compiled Successfully!")
            break
        elif stack_head == a and a != '$':
            stack.pop()
            token_index += 1
        elif stack_head not in parse_table[0]:
            M = find_in_table(stack_head, a)
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
                this_line_syntax_errors.append("Missing %s" % stack_head)
        elif stack_head in parse_table[0]:
            stack.pop()
            this_line_syntax_errors.append("Missing %s" % stack_head)
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
with open("parse_tree.txt", 'w', encoding='utf-8') as file:
    for pre, _, node in RenderTree(root):
        print("%s%s" % (pre, node.name))

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

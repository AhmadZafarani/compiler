# In The Name Of GOD
# Ahmad Zaferani 97105985
# Ali Shirmohammadi 97106068
from scanner import get_next_token
from intermediate_code_generator import code_gen, action_symbols, program_block, push_into_semantic_stack

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
    ['Declaration-initial', ['Type-specifier', 'ID'], ['Type-specifier', 'ID'], '', '', '', 'synch', '',
     '', '', '', '', '', '', 'synch', '', '', 'synch', 'synch', 'synch', '', '', '', '', '', '', '', '', ''],
    ['Declaration-prime', 'synch', 'synch', 'synch', 'synch', 'synch', ['Var-declaration-prime'], 'synch', 'synch',
     'synch', 'synch', 'synch', 'synch', 'synch', ['Fun-declaration-prime'], 'synch', 'synch',
     ['Var-declaration-prime'], '', '', '', '', '', '', '', '', '', '', ''],
    ['Var-declaration-prime', 'synch', 'synch', 'synch', 'synch', 'synch', ['#id_declaration', ';'], 'synch', 'synch',
     'synch', 'synch', 'synch', 'synch', 'synch', 'synch', 'synch', 'synch', 
     ['[', '#pnum', 'NUM', ']', '#arr_declaration', ';'], '', '', '', '', '', '', '', '', '', '', ''],
    ['Fun-declaration-prime', 'synch', 'synch', 'synch', 'synch', 'synch', 'synch', 'synch', 'synch', 'synch', 'synch',
     'synch', 'synch', 'synch', ['(', 'Params', ')', 'Compound-stmt'], 'synch', 'synch', '', '', '', '', '', '', '', '',
     '', '', '', ''],
    ['Type-specifier', ['int'], ['void'], '', '', '', '', '', '', '', '', 'synch', '', '', '', '', '', '', '', '', '',
     '', '', '', '', '', '', '', ''],
    ['Params', ['int', 'ID', 'Param-prime', 'Param-list'], ['void', 'Param-list-void-abtar'], '', '', '', '', '', '',
     '', '', '', '', '', '', '', '', '', '', 'synch', '', '', '', '', '', '', '', '', ''],
    ['Param-list-void-abtar', '', '', '', '', '', '', '', '', '', '', ['ID', 'Param-prime', 'Param-list'], '', '', '',
     '', '', '', '', 'epsilon', '', '', '', '', '', '', '', '', ''],
    ['Param-list', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', [',', 'Param', 'Param-list'],
     'epsilon', '', '', '', '', '', '', '', '', ''],
    ['Param', ['Declaration-initial', 'Param-prime'], ['Declaration-initial', 'Param-prime'], '', '', '', '', '', '',
     '', '', '', '', '', '', '', '', '', 'synch', 'synch', '', '', '', '', '', '', '', '', ''],
    ['Param-prime', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ['[', ']'], 'epsilon', 'epsilon',
     '', '', '', '', '', '', '', '', ''],
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
     ['Expression', '#correct_assign', ';'], ['Expression', '#correct_assign', ';'], 
     ['Expression', '#correct_assign', ';'], ['Expression', '#correct_assign', ';'], 
     ['Expression', '#correct_assign', ';'], 'synch', '', '', '', 'synch', 'synch', 'synch', '', '', '', '', '', ''],
    ['Selection-stmt', '', '', '', 'synch', 'synch', 'synch',
     ['if', '(', 'Expression', ')', '#save', 'Statement', 'else', '#else', 'Statement', '#if'], 'synch', 'synch', 
     'synch', 'synch', 'synch', 'synch', 'synch', 'synch', 'synch', '', '', '', 'synch', 'synch', 'synch', '', '', '', 
     '', '', ''],
    ['Iteration-stmt', '', '', '', 'synch', 'synch', 'synch', 'synch',
     ['while', '#label', '(', 'Expression', ')', '#save', 'Statement', '#while'], 'synch', 'synch', 'synch', 'synch',
     'synch', 'synch', 'synch', 'synch', '', '', '', 'synch', 'synch', 'synch', '', '', '', '', '', ''],
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
    ['Expression', '', '', '', '', '', 'synch', '', '', '', '', ['#pid', 'ID', 'B'], ['Simple-expression-zegond'],
     ['Simple-expression-zegond'], ['Simple-expression-zegond'], ['Simple-expression-zegond'], '', '', 'synch', 'synch',
     '', '', '', 'synch', '', '', '', '', ''],
    ['B', '', '', '', '', '', ['Simple-expression-prime'], '', '', '', '', '', ['Simple-expression-prime'],
     ['Simple-expression-prime'], ['Simple-expression-prime'], '', '', ['[', 'Expression', ']', '#arr_index', 'H'],
     ['Simple-expression-prime'], ['Simple-expression-prime'], '', '', '', ['Simple-expression-prime'],
     ['=', 'Expression', '#assign'], ['Simple-expression-prime'], ['Simple-expression-prime'],
     ['Simple-expression-prime'], ['Simple-expression-prime']],
    ['H', '', '', '', '', '', ['G', 'D', 'C'], '', '', '', '', '', ['G', 'D', 'C'], ['G', 'D', 'C'], '', '', '', '',
     ['G', 'D', 'C'], ['G', 'D', 'C'], '', '', '', ['G', 'D', 'C'], ['=', 'Expression', '#assign'], ['G', 'D', 'C'],
     ['G', 'D', 'C'], ['G', 'D', 'C'], ''],
    ['Simple-expression-zegond', '', '', '', '', '', 'synch', '', '', '', '', '', ['Additive-expression-zegond', 'C'],
     ['Additive-expression-zegond', 'C'], ['Additive-expression-zegond', 'C'], ['Additive-expression-zegond', 'C'], '',
     '', 'synch', 'synch', '', '', '', 'synch', '', '', '', '', ''],
    ['Simple-expression-prime', '', '', '', '', '', ['Additive-expression-prime', 'C'], '', '', '', '', '',
     ['Additive-expression-prime', 'C'],
     ['Additive-expression-prime', 'C'], ['Additive-expression-prime', 'C'], '', '', '',
     ['Additive-expression-prime', 'C'], ['Additive-expression-prime', 'C'], '', '',
     '',
     ['Additive-expression-prime', 'C'], '', ['Additive-expression-prime', 'C'], ['Additive-expression-prime', 'C'],
     ['Additive-expression-prime', 'C'], ['Additive-expression-prime', 'C']],
    ['C', '', '', '', '', '', 'epsilon', '', '', '', '', '', '', '', '', '', '', '', 'epsilon', 'epsilon', '', '', '',
     'epsilon', '', '', ['#save_addop', 'Relop', 'Additive-expression', '#relop'],
     ['#save_addop', 'Relop', 'Additive-expression', '#relop'], ''],
    ['Relop', '', '', '', '', '', '', '', '', '', '', 'synch', 'synch', 'synch', 'synch', 'synch', '', '', '', '', '',
     '', '', '', '', '', ['<'], ['=='], ''],
    ['Additive-expression', '', '', '', '', '', 'synch', '', '', '', '', ['Term', 'D'], ['Term', 'D'], ['Term', 'D'],
     ['Term', 'D'], ['Term', 'D'], '', '', 'synch', 'synch', '', '', '', 'synch', '', '', '', '', ''],
    ['Additive-expression-prime', '', '', '', '', '', ['Term-prime', 'D'], '', '', '', '', '', ['Term-prime', 'D'],
     ['Term-prime', 'D'], ['Term-prime', 'D'], '', '', '', ['Term-prime', 'D'], ['Term-prime', 'D'], '', '', '',
     ['Term-prime', 'D'], '',
     ['Term-prime', 'D'], ['Term-prime', 'D'], ['Term-prime', 'D'], ['Term-prime', 'D']],
    ['Additive-expression-zegond', '', '', '', '', '', 'synch', '', '', '', '', '', ['Term-zegond', 'D'],
     ['Term-zegond', 'D'], ['Term-zegond', 'D'], ['Term-zegond', 'D'], '', '', 'synch', 'synch', '', '', '', 'synch',
     '', '', 'synch', 'synch', ''],
    ['D', '', '', '', '', '', 'epsilon', '', '', '', '', '', ['#save_addop', 'Addop', 'Term', '#addop', 'D'],
     ['#save_addop', 'Addop', 'Term', '#addop', 'D'], '', '', '', '', 'epsilon', 'epsilon', '', '', '', 'epsilon', '',
     '', 'epsilon', 'epsilon', ''],
    ['Addop', '', '', '', '', '', '', '', '', '', '', 'synch', ['+'], ['-'], 'synch', 'synch', '', '', '', '', '', '',
     '', '', '', '', '', '', ''],
    ['Term', '', '', '', '', '', 'synch', '', '', '', '', ['Signed-factor', 'G'], ['Signed-factor', 'G'],
     ['Signed-factor', 'G'], ['Signed-factor', 'G'], ['Signed-factor', 'G'], '', '', 'synch', 'synch', '', '', '',
     'synch', '', '', 'synch', 'synch', ''],
    ['Term-prime', '', '', '', '', '', ['Signed-factor-prime', 'G'], '', '', '', '', '', ['Signed-factor-prime', 'G'],
     ['Signed-factor-prime', 'G'], ['Signed-factor-prime', 'G'],
     '', '', '', ['Signed-factor-prime', 'G'], ['Signed-factor-prime', 'G'], '', '', '', ['Signed-factor-prime', 'G'],
     '', ['Signed-factor-prime', 'G'], ['Signed-factor-prime', 'G'], ['Signed-factor-prime', 'G'],
     ['Signed-factor-prime', 'G']],
    ['Term-zegond', '', '', '', '', '', 'synch', '', '', '', '', '', ['Signed-factor-zegond', 'G'],
     ['Signed-factor-zegond', 'G'], ['Signed-factor-zegond', 'G'], ['Signed-factor-zegond', 'G'], '', '', 'synch',
     'synch', '', '', '', 'synch', '', '', 'synch', 'synch', ''],
    ['G', '', '', '', '', '', 'epsilon', '', '', '', '', '', 'epsilon', 'epsilon', '', '', '', '', 'epsilon', 'epsilon',
     '', '', '', 'epsilon', '', ['#save_addop', '*', 'Signed-factor', '#mult', 'G'], 'epsilon', 'epsilon', ''],
    ['Signed-factor', '', '', '', '', '', 'synch', '', '', '', '', ['Factor'],
     ['#psign', '+', 'Factor', '#correct_signed_factor'], ['#psign', '-', 'Factor', '#correct_signed_factor'],
     ['Factor'], ['Factor'], '', '', 'synch', 'synch', '', '', '', 'synch', '', 'synch', 'synch', 'synch', ''],
    ['Signed-factor-prime', '', '', '', '', '', ['Factor-prime'], '', '', '', '', '', ['Factor-prime'],
     ['Factor-prime'], ['Factor-prime'], '',
     '', '', ['Factor-prime'], ['Factor-prime'], '', '', '', ['Factor-prime'], '', ['Factor-prime'], ['Factor-prime'],
     ['Factor-prime'], ['Factor-prime']],
    ['Signed-factor-zegond', '', '', '', '', '', 'synch', '', '', '', '', '',
     ['#psign', '+', 'Factor', '#correct_signed_number'], ['#psign', '-', 'Factor', '#correct_signed_number'],
     ['Factor-zegond'], ['Factor-zegond'], '', '', 'synch', 'synch', '', '', '', 'synch', '', 'synch', 'synch', 'synch',
     ''],
    ['Factor', '', '', '', '', '', 'synch', '', '', '', '', ['#pid', 'ID', 'Var-call-prime'], 'synch', 'synch',
     ['(', 'Expression', ')'], ['#pnum', 'NUM'], '', '', 'synch', 'synch', '', '', '', 'synch', '', 'synch', 'synch',
     'synch', ''],
    ['Var-call-prime', '', '', '', '', '', ['Var-prime'], '', '', '', '', '', ['Var-prime'], ['Var-prime'],
     ['(', 'Args', ')'], '',
     '', ['Var-prime'], ['Var-prime'], ['Var-prime'], '', '', '', ['Var-prime'], '', ['Var-prime'], ['Var-prime'],
     ['Var-prime'], ''],
    ['Var-prime', '', '', '', '', '', 'epsilon', '', '', '', '', '', 'epsilon', 'epsilon', '', '', '',
     ['[', 'Expression', ']', '#arr_index'], 'epsilon', 'epsilon', '', '', '', 'epsilon', '', 'epsilon', 'epsilon', 
     'epsilon', ''],
    ['Factor-prime', '', '', '', '', '', 'epsilon', '', '', '', '', '', 'epsilon', 'epsilon', ['(', 'Args', ')'], '',
     '', '', 'epsilon', 'epsilon', '', '', '', 'epsilon', '', 'epsilon', 'epsilon', 'epsilon', ''],
    ['Factor-zegond', '', '', '', '', '', 'synch', '', '', '', '', '', 'synch', 'synch', ['(', 'Expression', ')'],
     ['#pnum', 'NUM'], '', '', 'synch', 'synch', '', '', '', 'synch', '', 'synch', 'synch', 'synch', ''],
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
parser_stack = ['Program']
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


ids = set()
while parser_stack:
    t = tokens[token_index]
    if t[0] == 'SYMBOL' or t[0] == 'KEYWORD':
        next_token = t[1]
    else:
        next_token = t[0]
        if t[0] == "ID":
            if t[1] not in ids and t[1] != 'output':
                ids.add(t[1])
                push_into_semantic_stack(t[1])
    parser_stack_head = parser_stack[-1]
    if t[0] in valid_tokens:
        if t[0] == 'WHITESPACE' or t[0] == 'COMMENT':
            token_index += 1
            continue

        print(parser_stack_head, next_token)
        if parser_stack_head == next_token == '$':
            print("Compiled Successfully!")
            break
        elif parser_stack_head == next_token and next_token != '$':
            parser_stack.pop()
            token_index += 1
        elif parser_stack_head not in parse_table[0]:
            M = find_in_table(parser_stack_head, next_token)
            print(M)

            if isinstance(M, list):
                parser_stack.pop()
                parser_stack += reversed(M)
            elif parser_stack_head in action_symbols:
                code_gen(parser_stack_head, t[1])
                parser_stack.pop()
            elif M == 'epsilon':
                non_terminal = parser_stack.pop()
            else:
                raise Exception("Syntax Error: ", parser_stack, t)
        elif parser_stack_head in parse_table[0]:
            parser_stack.pop()
        else:
            raise Exception("Syntax Error: ", parser_stack, t)
        print(parser_stack, token_index)

    elif t[0] in errors:
        raise Exception("Lexical Error: ", t)
    else:
        raise ValueError(t)

with open("output.txt", "w") as file:
    counter = 0
    for li in program_block:
        if li == '':
            break
        file.write('%d' % counter + '\t' + li + '\n')
        counter += 1

print(ids)

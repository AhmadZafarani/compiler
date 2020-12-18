# YA FATEMEH
action_symbols = {"#pid", "#assign", "#add", "#mult", '#id_declaration', "#pnum", '#psigned_num', '#psign'}
semantic_stack = []
semantic_stack_top = 0
program_block = [''] * 400
program_block_index = 0
data_block = []
temporary_block = []
symbol_table = {}


def get_temp():
    return len(temporary_block) * 4 + 500


def push_into_semantic_stack(identifier: int):
    global semantic_stack_top
    semantic_stack.append(identifier)
    semantic_stack_top += 1


def pop_from_semantic_stack(num):
    global semantic_stack_top
    x = []
    for i in range(num):
        x.append(semantic_stack.pop())
        semantic_stack_top -= 1
    return x


def push_id(identifier: str):
    p = symbol_table[identifier]
    push_into_semantic_stack(p)


def assign():
    global program_block_index
    program_block[program_block_index] = '(ASSIGN, %s, %s, )' % (
        semantic_stack[semantic_stack_top - 1], semantic_stack[semantic_stack_top - 2])
    program_block_index += 1
    data_block.append(semantic_stack[semantic_stack_top - 1])
    pop_from_semantic_stack(2)


def declare_id(identifier: str):
    s = pop_from_semantic_stack(1)[0]
    symbol_table[s] = len(data_block) * 4 + 100
    push_into_semantic_stack(symbol_table[s])
    if identifier == ';':
        push_into_semantic_stack('#0')
    else:
        push_into_semantic_stack(identifier)
    assign()


def code_gen(a_s: str, arg: str):
    if a_s == '#pid':
        push_id(arg)
    elif a_s == '#id_declaration':
        declare_id(arg)
    elif a_s == '#assign':
        assign()
    elif a_s == '#pnum':
        push_into_semantic_stack('#' + arg)
    elif a_s == '#psign':
        push_into_semantic_stack(arg)
    elif a_s == '#psigned_num':
        s = pop_from_semantic_stack(1)[0]
        push_into_semantic_stack('#' + s + arg)

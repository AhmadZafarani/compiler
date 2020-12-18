# YA FATEMEH
action_symbols = {"#pid", "#assign", "#add", "#mult", '#id_declaration'}
semantic_stack = []
semantic_stack_top = 0
program_block = [''] * 400
program_block_index = 0
data_block = []
temporary_block = []
symbol_table = {}


def find_address(identifier: str):
    for i in range(len(data_block)):
        if data_block[i] == identifier:
            return i * 4 + 100


def get_temp():
    return len(temporary_block) * 4 + 500


def push_into_semantic_stack(identifier: int):
    global semantic_stack_top
    semantic_stack.append(identifier)
    semantic_stack_top += 1


def pop_from_semantic_stack(num: int):
    global semantic_stack_top
    x = []
    for i in range(num):
        x.append(semantic_stack.pop())
        semantic_stack_top -= 1
    return x


def push_id(identifier: str):
    p = find_address(identifier)
    push_into_semantic_stack(p)


def assign():
    global program_block_index
    program_block[program_block_index] = '(ASSIGN, %s, %s, )' % (
        semantic_stack[semantic_stack_top - 1], semantic_stack[semantic_stack_top - 2])
    program_block_index += 1
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

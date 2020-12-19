# YA FATEMEH
action_symbols = {"#pid", "#assign", "#addop", "#mult", '#id_declaration', "#pnum", '#correct_signed_number', '#psign',
                  '#save_addop'}
semantic_stack = []
semantic_stack_top = 0
program_block = [''] * 400
program_block_index = 0
data_block = []
temporary_block = 500
symbol_table = {}


def get_temp() -> int:
    global temporary_block
    x = temporary_block
    temporary_block += 4
    return x


def push_into_semantic_stack(identifier):
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


def addop():
    global program_block_index
    t = get_temp()
    print(semantic_stack)
    if semantic_stack[semantic_stack_top - 2] == '+':
        program_block[program_block_index] = '(ADD, %s, %s, %d)' % (semantic_stack[semantic_stack_top - 3],
                                                                    semantic_stack[semantic_stack_top - 1], t)
    elif semantic_stack[semantic_stack_top - 2] == '-':
        program_block[program_block_index] = '(SUB, %s, %s, %d)' % (semantic_stack[semantic_stack_top - 3],
                                                                    semantic_stack[semantic_stack_top - 1], t)
    program_block_index += 1
    pop_from_semantic_stack(3)
    push_into_semantic_stack(t)


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
    elif a_s == '#correct_signed_number':
        s = pop_from_semantic_stack(2)
        push_into_semantic_stack('#' + s[1] + s[0][1:])
    elif a_s == '#addop':
        addop()
    elif a_s == '#save_addop':
        push_into_semantic_stack(arg)
    else:
        raise ValueError(a_s)

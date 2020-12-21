# YA FATEMEH
action_symbols = {"#pid", "#assign", "#addop", "#mult", '#id_declaration', "#pnum", '#correct_signed_number', '#psign',
                  '#save_addop', '#relop', '#while', '#save', '#label', '#else', '#if', '#arr_declaration', 
                  '#correct_assign', '#arr_index'}
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
    pop_from_semantic_stack(1)


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
    if semantic_stack[semantic_stack_top - 2] == '+':
        program_block[program_block_index] = '(ADD, %s, %s, %d)' % (semantic_stack[semantic_stack_top - 3],
                                                                    semantic_stack[semantic_stack_top - 1], t)
    elif semantic_stack[semantic_stack_top - 2] == '-':
        program_block[program_block_index] = '(SUB, %s, %s, %d)' % (semantic_stack[semantic_stack_top - 3],
                                                                    semantic_stack[semantic_stack_top - 1], t)
    elif semantic_stack[semantic_stack_top - 2] == '*':
        program_block[program_block_index] = '(MULT, %s, %s, %d)' % (semantic_stack[semantic_stack_top - 3],
                                                                     semantic_stack[semantic_stack_top - 1], t)
    elif semantic_stack[semantic_stack_top - 2] == '<':
        program_block[program_block_index] = '(LT, %s, %s, %d)' % (semantic_stack[semantic_stack_top - 3],
                                                                   semantic_stack[semantic_stack_top - 1], t)
    elif semantic_stack[semantic_stack_top - 2] == '==':
        program_block[program_block_index] = '(EQ, %s, %s, %d)' % (semantic_stack[semantic_stack_top - 3],
                                                                   semantic_stack[semantic_stack_top - 1], t)
    program_block_index += 1
    pop_from_semantic_stack(3)
    push_into_semantic_stack(t)


def save():
    global program_block_index
    push_into_semantic_stack(program_block_index)
    program_block_index += 1


def while_func():
    global program_block_index
    program_block[semantic_stack[semantic_stack_top - 1]] = '(JPF, %s, %d, )' % (semantic_stack[semantic_stack_top - 2],
                                                                                 program_block_index + 2)
    program_block[program_block_index] = '(JP, %s, , )' % (semantic_stack[semantic_stack_top - 3] + 1)
    program_block_index += 1
    pop_from_semantic_stack(3)


def if_func():
    program_block[semantic_stack[semantic_stack_top - 1]] = '(JP, %s, , )' % (program_block_index + 1)
    pop_from_semantic_stack(1)


def else_func():
    global program_block_index
    program_block[semantic_stack[semantic_stack_top - 1]] = '(JPF, %s, %d, )' % (semantic_stack[semantic_stack_top - 2],
                                                                                 program_block_index + 2)
    pop_from_semantic_stack(2)
    push_into_semantic_stack(program_block_index)
    program_block_index += 1


def declare_array():
    temp = pop_from_semantic_stack(2)
    arr_name = temp[1]
    symbol_table[arr_name] = len(data_block) * 4 + 100
    arr_length = int(temp[0][1:])
    for i in range(arr_length):
        s = arr_name + str(i)
        push_into_semantic_stack(len(data_block) * 4 + 100)
        push_into_semantic_stack('#0')
        assign()
        pop_from_semantic_stack(1)


def array_index():
    global program_block_index
    print(semantic_stack)
    zero = int(semantic_stack[semantic_stack_top - 2])
    top = semantic_stack[semantic_stack_top - 1]
    if isinstance(top, int):
        index = str(top)
    else:
        index = top
    t = get_temp()
    program_block[program_block_index] = '(MULT, %s, #4, %d)' % (index, t)
    program_block_index += 1
    t1 = get_temp()
    program_block[program_block_index] = '(ADD, %d, #%d, %d)' % (t, zero, t1)
    program_block_index += 1
    pop_from_semantic_stack(2)
    push_into_semantic_stack('@' + str(t1))



def code_gen(a_s: str, arg: str):
    if a_s == '#pid':
        push_id(arg)
    elif a_s == '#id_declaration':
        declare_id(arg)
    elif a_s == '#assign':
        assign()
    elif a_s == '#pnum':
        push_into_semantic_stack('#' + arg)
    elif a_s == '#psign' or a_s == '#save_addop':
        push_into_semantic_stack(arg)
    elif a_s == '#correct_signed_number':
        s = pop_from_semantic_stack(2)
        push_into_semantic_stack('#' + s[1] + s[0][1:])
    elif a_s == '#addop' or a_s == '#mult' or a_s == '#relop':
        addop()
    elif a_s == '#save':
        save()
    elif a_s == '#while':
        while_func()
    elif a_s == '#label':
        push_into_semantic_stack(program_block_index)
    elif a_s == '#else':
        else_func()
    elif a_s == '#if':
        if_func()
    elif a_s == '#arr_declaration':
        declare_array()
    elif a_s == '#correct_assign':
        pop_from_semantic_stack(1)
    elif a_s == '#arr_index':
        array_index()
    else:
        raise ValueError(a_s)

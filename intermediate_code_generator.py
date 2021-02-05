# YA FATEMEH
action_symbols = {"#pid", "#assign", "#addop", "#mult", '#id_declaration', "#pnum", '#correct_signed_factor', '#psign',
                  '#save_addop', '#relop', '#while', '#save', '#label', '#else', '#if', '#arr_declaration',
                  '#correct_assign', '#arr_index', '#function', '#parameter_declaration', '#activation_record', 
                  '#call_function'}
semantic_stack = []
semantic_stack_top = 0
program_block = [''] * 400
program_block_index = 0
data_block = []
temporary_block = 1000
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


def pop_from_semantic_stack(num: int) -> list:
    global semantic_stack_top
    x = []
    for i in range(num):
        x.append(semantic_stack.pop())
        semantic_stack_top -= 1
    return x


def push_id(identifier: str):
    if identifier != 'output':
        p = symbol_table[identifier]
        if isinstance(p, list):
            for item in p:
                push_into_semantic_stack(item)
            return
    else:
        p = identifier
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
    symbol_table[s] = len(data_block) * 4 + 500
    push_into_semantic_stack(symbol_table[s])
    if identifier == ';':
        push_into_semantic_stack('#0')
    else:
        push_into_semantic_stack(identifier)
    assign()
    pop_from_semantic_stack(1)


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
                                                                                 program_block_index + 1)
    program_block[program_block_index] = '(JP, %s, , )' % (semantic_stack[semantic_stack_top - 3])
    program_block_index += 1
    pop_from_semantic_stack(3)


def if_func():
    program_block[semantic_stack[semantic_stack_top - 1]] = '(JP, %s, , )' % program_block_index
    pop_from_semantic_stack(1)


def else_func():
    global program_block_index
    program_block[semantic_stack[semantic_stack_top - 1]] = '(JPF, %s, %d, )' % (semantic_stack[semantic_stack_top - 2],
                                                                                 program_block_index + 1)
    pop_from_semantic_stack(2)
    push_into_semantic_stack(program_block_index)
    program_block_index += 1


def declare_array():
    temp = pop_from_semantic_stack(2)
    arr_name = temp[1]
    symbol_table[arr_name] = len(data_block) * 4 + 500
    arr_length = int(temp[0][1:])
    for i in range(arr_length):
        push_into_semantic_stack(len(data_block) * 4 + 500)
        push_into_semantic_stack('#0')
        assign()
        pop_from_semantic_stack(1)


def array_index():
    global program_block_index
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


def correct_signed_factor():
    global program_block_index
    t = get_temp()
    s = pop_from_semantic_stack(2)
    if isinstance(s[0], int):
        program_block[program_block_index] = '(SUB, #0, %d, %d)' % (s[0], t)
        program_block_index += 1
        push_into_semantic_stack(t)
    else:
        push_into_semantic_stack('#' + s[1] + s[0][1:])


def printer():
    global program_block_index
    x = pop_from_semantic_stack(2)
    if x[1] == 'output':
        program_block[program_block_index] = '(PRINT, %s, , )' % str(x[0])
        program_block_index += 1
    else:
        push_into_semantic_stack(x[1])


def function():
    if semantic_stack[0] == 'main':
        return
    program_block[semantic_stack[semantic_stack_top - 2]] = '(JP, %s, , )' % program_block_index
    func_ret_value = symbol_table[semantic_stack[0]]
    symbol_table[semantic_stack[0]] = [semantic_stack[semantic_stack_top - 2] + 1, func_ret_value]
    pop_from_semantic_stack(3)
    print(semantic_stack, semantic_stack_top, program_block, program_block_index, symbol_table)


def activation_record():
    if semantic_stack[0] == 'main':
        return
    save()                                                          # jump to next function
    symbol_table[semantic_stack[0]] = len(data_block) * 4 + 500     # create space for return value
    data_block.append(None)
    print(semantic_stack, semantic_stack_top, program_block, program_block_index, symbol_table)


def param_declare():
    parameter = pop_from_semantic_stack(1)[0]
    symbol_table[parameter] = len(data_block) * 4 + 500
    data_block.append(None)
    print(semantic_stack, semantic_stack_top, program_block, program_block_index, symbol_table)


def call():
    global program_block_index
    func_start_address = 0
    j = 0
    for j in range(semantic_stack_top - 1, 1, -1):
        if isinstance(semantic_stack[j], int) and 0 < semantic_stack[j] < 500:
            func_start_address = semantic_stack[j]
            break
    params = pop_from_semantic_stack(semantic_stack_top - j - 1)
    start = params.pop()
    for p in range(len(params)):
        program_block[program_block_index] = '(ASSIGN, %s, %s, )' % (params[p], 4 * (p + 1) + start)
        program_block_index += 1 
    program_block[program_block_index] = '(JP, %s, , )' % func_start_address
    print(semantic_stack, semantic_stack_top, program_block, program_block_index, symbol_table)


def code_gen(a_s: str, arg: str):
    print(semantic_stack, semantic_stack_top, symbol_table)
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
    elif a_s == '#correct_signed_factor':
        correct_signed_factor()
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
        printer()
    elif a_s == '#arr_index':
        array_index()
    elif a_s == '#function':
        function()
    elif a_s == '#parameter_declaration':
        param_declare()
    elif a_s == '#activation_record':
        activation_record()
    elif a_s == '#call_function':
        call()
    else:
        raise ValueError(a_s)

# YA FATEMEH
# from collections import OrderedDict
action_symbols = {"#pid", "#assign", "#addop", "#mult", '#id_declaration', "#pnum", '#correct_signed_factor', '#psign',
                  '#save_addop', '#relop', '#while', '#save', '#label', '#else', '#if', '#arr_declaration',
                  '#correct_assign', '#arr_index', '#function', '#parameter_declaration', '#activation_record',
                  '#call_function', '#return', '#jpf', '#jp_break', '#tmp_save', '#jp_switch', '#cmp_save'}
semantic_stack = []
semantic_stack_top = 0
program_block = [''] * 400
program_block_index = 0
data_block = []
temporary_block = 1000
symbol_table = {}
scope_stack = []
last_seen_token = ''


def id_first_occurrence(identifier):
    global last_seen_token
    last_seen_token = identifier
    if identifier not in symbol_table and identifier != 'output':
        if search_in_symbol_table(identifier) is not None:
            return
        symbol_table[identifier] = None
        push_into_semantic_stack(identifier)


def search_in_symbol_table(identifier):
    for s in reversed(scope_stack):
        if identifier in s:
            return s[identifier]
    return None


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
        try:
            p = symbol_table[identifier]
        except KeyError:
            p = search_in_symbol_table(identifier)
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
    if semantic_stack_top == 2:
        push_into_semantic_stack(last_seen_token)
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


def if_func(num: int):
    program_block[semantic_stack[semantic_stack_top - num]] = '(JP, %s, , )' % program_block_index
    pop_from_semantic_stack(num)


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
    # declare a pointer to first entry of array
    arr_address = len(data_block) * 4 + 500
    push_into_semantic_stack(arr_address)
    push_into_semantic_stack('#' + str(symbol_table[arr_name]))
    assign()
    pop_from_semantic_stack(1)
    symbol_table[arr_name] = arr_address


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
    program_block[program_block_index] = '(ADD, %d, %d, %d)' % (t, zero, t1)
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
    """ each function name in symbol table is a list with 3 elements:
        0. address of return value in memory
        1. address of cell in memory which contains index of program block that we called the function from there
        2. index of program block which execution of function starts from there
    """
    if semantic_stack[0] == 'main':
        return
    global symbol_table
    return_func()
    symbol_table = scope_stack.pop()
    func_name = symbol_table[semantic_stack[0]]
    func_name.append(semantic_stack[semantic_stack_top - 1] + 1)
    symbol_table[semantic_stack[0]] = func_name
    program_block[semantic_stack[semantic_stack_top - 1]] = '(JP, %s, , )' % program_block_index
    pop_from_semantic_stack(2)


def activation_record():
    global symbol_table
    if semantic_stack[0] == 'main':
        return
    save()  # jump to next function
    e = len(data_block) * 4 + 500
    symbol_table[semantic_stack[0]] = [e, e + 4]  # create space for return value and address
    data_block.append(None)
    data_block.append(None)
    scope_stack.append(symbol_table)
    symbol_table = dict()
    print(scope_stack)


def param_declare():
    parameter = pop_from_semantic_stack(1)[0]
    symbol_table[parameter] = len(data_block) * 4 + 500
    data_block.append(None)


def call():
    if semantic_stack[semantic_stack_top - 2] == 'output':
        return
    global program_block_index
    func_start_address = 0
    j = 0
    for j in range(semantic_stack_top - 1, 1, -1):
        if isinstance(semantic_stack[j], int) and 0 < semantic_stack[j] < 500:
            func_start_address = semantic_stack[j]
            break
    params = pop_from_semantic_stack(semantic_stack_top - j - 1)
    params = list(reversed(params))
    pop_from_semantic_stack(1)
    # assign arguments to parameters of function
    for p in range(len(params)):
        program_block[program_block_index] = '(ASSIGN, %s, %s, )' % (
            params[p], 4 * (p + 1) + semantic_stack[semantic_stack_top - 1])
        program_block_index += 1
    # assign return address (num of instruction) to return address of function for implicit jump
    program_block[program_block_index] = '(ASSIGN, %s, %s, )' % ('#' + str(program_block_index + 2),
                                                                 semantic_stack[semantic_stack_top - 1])
    program_block_index += 1
    # jump to start of function (first instruction)
    program_block[program_block_index] = '(JP, %s, , )' % func_start_address
    program_block_index += 1
    pop_from_semantic_stack(1)
    # copy return value to a temporary memory location
    t = get_temp()
    ret_value = pop_from_semantic_stack(1)[0]
    program_block[program_block_index] = '(ASSIGN, %s, %s, )' % (ret_value, t)
    program_block_index += 1
    push_into_semantic_stack(t)


def return_func():
    global program_block_index
    st = scope_stack[-1]
    # for void functions we don't need (explicit) return value
    if not (isinstance(semantic_stack[semantic_stack_top - 1], int) and
            0 <= semantic_stack[semantic_stack_top - 1] <= 500):
        program_block[program_block_index] = '(ASSIGN, %s, %s, )' % (semantic_stack[semantic_stack_top - 1],
                                                                     st[semantic_stack[0]][0])
        pop_from_semantic_stack(1)
    else:
        program_block[program_block_index] = '(ASSIGN, #%s, %s, )' % (semantic_stack[semantic_stack_top - 1],
                                                                      st[semantic_stack[0]][0])
    program_block_index += 1
    program_block[program_block_index] = '(JP, @%s, , )' % st[semantic_stack[0]][1]
    program_block_index += 1


def temp_save():
    global program_block_index
    program_block[program_block_index] = '(JP, %s, , )' % (program_block_index + 2)
    program_block_index += 1
    push_into_semantic_stack('switch-case')
    save()


def compare_save():
    global program_block_index
    t = get_temp()
    program_block[program_block_index] = '(EQ, %s, %s, %d)' % (semantic_stack[semantic_stack_top - 2],
                                                               semantic_stack[semantic_stack_top - 1], t)
    program_block_index += 1
    pop_from_semantic_stack(1)
    push_into_semantic_stack(t)
    save()


def jump_break():
    global program_block_index
    if semantic_stack_top >= 5 and semantic_stack[semantic_stack_top - 5] == 'switch-case':
        program_block[program_block_index] = '(JP, %s, , )' % semantic_stack[semantic_stack_top - 4]
    else:
        program_block[program_block_index] = '(ASSIGN, #0, %s, )' % semantic_stack[semantic_stack_top - 4]
        program_block_index += 1
        program_block[program_block_index] = '(JP, %s, , )' % semantic_stack[semantic_stack_top - 3]
    program_block_index += 1


def jump_false():
    program_block[semantic_stack[semantic_stack_top - 1]] = '(JPF, %s, %s, )' % (semantic_stack[semantic_stack_top - 2],
                                                                                 program_block_index)
    pop_from_semantic_stack(2)


def code_gen(a_s: str, arg: str):
    print(semantic_stack, semantic_stack_top, symbol_table, scope_stack, program_block)
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
        if_func(1)
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
    elif a_s == '#return':
        return_func()
    elif a_s == '#tmp_save':
        temp_save()
    elif a_s == '#cmp_save':
        compare_save()
    elif a_s == '#jp_break':
        jump_break()
    elif a_s == '#jpf':
        jump_false()
    elif a_s == '#jp_switch':
        if_func(2)
        pop_from_semantic_stack(1)
    else:
        raise ValueError(a_s)

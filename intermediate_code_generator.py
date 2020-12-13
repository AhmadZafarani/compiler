# YA FATEMEH
action_symbols = {"#pid", "#assign", "#add", "#mult"}
semantic_stack = []
semantic_stack_top = 0
program_block = []
program_block_index = 0
data_block = []
temporary_block = []


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


def push_id(identifier: str):
    p = find_address(identifier)
    push_into_semantic_stack(p)


def code_gen(a_s: str, arg: str):
    if a_s == '#pid':
        push_id(arg)

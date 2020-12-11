# YA FATEMEH
action_symbols = {"#pid"}
semantic_stack = []
top = 0
program_block = []
i = 0


def push_id(id: str):
    pass


def code_gen(a_s: str, arg: str):
    if a_s == '#pid':
        push_id(arg)

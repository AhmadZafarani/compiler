# YA HOSSEIN
digit = range(10)
keywords = {"if", "else", "void", "int", "while", "break", "switch", "default", "case", "return"}
symbols = {";", ":", ",", "[", "]", "(", ")", "{", "}", "+", "-", "*", "<"}
whitespaces = {" ", "\n", "\f", "\r", "\t", "\v"}


def is_letter(c: str):
    x = ord(c)
    return (65 <= x <= 90) or (97 <= x <= 122)


def is_num(string: str, length: int):
    i = 1
    if string[0] not in digit:
        return -1
    while i < length:
        if string[i] in digit:
            i += 1
        elif is_letter(string[i]):
            return "invalid-number"
        else:
            return i - 1
    return length


def is_id(string: str, length: int):
    i = 1
    if not is_letter(string[0]):
        return -1
    while i < length:
        if string[i] in digit or is_letter(string[i]):
            i += 1
        else:
            return i - 1
    return length


def is_symbol(string: str):
    if string[0] in symbols:
        return 0
    elif string[0] == '=':
        if string[1] != '=':
            return 0
        else:
            return 1
    return -1


def is_comment(string: str, length: int):
    if string[0] == "*" and string[1] == "/":
        return "unmatched-star-slash"

    if string[0] != "/":
        return -1
    if string[1] == "/":
        i = 2
        while i < length:
            if string[i] != "\n":
                i += 1
            else:
                return i - 1
        return length
    elif string[1] == "*":
        i = 2
        while i < length:
            if string[i] != "*":
                i += 1
            else:
                while i < length:
                    if string[i] == "*":
                        i += 1
                    elif string[i] == "/":
                        return i
                    else:
                        break
        return "unclosed-comment"
    return -1


def get_next_token(inp: str):
    pass

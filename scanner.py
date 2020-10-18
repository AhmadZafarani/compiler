# YA HOSSEIN
digits = "0123456789"
letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
id = digits + letters
symbols = ";:,[](){}+-*=<"
whitespace = " \n\r\t\v\f"
comment = "*/"
keywords = ["if", "else", "void", "int", "while", "break", "switch", "default", "case", "return"]
valid_types = ["SYMBOL", "WHITESPACE", "COMMENT", "ID", "NUM", "KEYWORD"]
invalid_types = ["Invalid input", "Invalid number", "Unmatched comment", "Unclosed comment"]
sigma = id + symbols + whitespace + comment


def get_next_token(inp: str, start_char: int):
    token = inp[start_char]
    if token in symbols:
        token_type = "SYMBOL"
    elif token in whitespace:
        return "WHITESPACE", token
    elif token == "/":
        token_type = "COMMENT"
    elif token in letters:
        token_type = "ID"
    elif token in digits:
        token_type = "NUM"
    else:
        return "Invalid input", token
    i = start_char + 1
    while True:
        next_char = inp[i]
        can_add, new_type = increase_token(token, token_type, next_char)
        if can_add:
            token += next_char
        if new_type in invalid_types:
            return new_type, token
        if not can_add:
            if token in keywords:
                return "KEYWORD", token
            return token_type, token

        i += 1
        if i == len(inp):
            if token_type == "COMMENT":
                if len(token) < 2:
                    return "Invalid input", "/"
                elif token[:2] == "//":
                    return token_type, token
                elif token[:2] == "/*":
                    if len(inp) > 3 and inp[-2:] == "*/":
                        return "COMMENT", token
                    return "Unclosed comment", token
            if token in keywords:
                return "KEYWORD", token
            if token[-1] not in sigma:
                return "Invalid input", token

            return token_type, token


def increase_token(inp: str, type: str, next_char: chr):
    if type in ["SYMBOL", "WHITESPACE"]:
        if inp == "*" and next_char == '/':
            return True, "Unmatched comment"
        if inp == "==":
            return False, type
        if inp == "=":
            if next_char != "=":
                return False, type
            else:
                return True, type
        return False, type

    if type == "NUM":
        if next_char in digits:
            return True, type
        elif next_char in comment + symbols + whitespace:
            return False, type
        else:
            return True, "Invalid number"

    if type == "ID":
        if next_char in id:
            if inp[-1] not in sigma:
                return False, "Invalid input"
            return True, type
        elif next_char in whitespace + symbols + comment:
            if inp[-1] not in sigma:
                return False, "Invalid input"
            return False, type
        elif next_char not in sigma:
            return True, type

    if type == "COMMENT":
        if len(inp) == 1:
            if next_char not in "/*":
                return False, "Invalid input"
            return True, type
        elif inp[:2] == "//" and next_char == "\n":
            return False, type
        elif inp[:2] == "/*" and len(inp) > 3 and inp[-2:] == "*/":
            return False, type
        return True, type

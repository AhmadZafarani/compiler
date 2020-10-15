# In The Name Of GOD
# Ahmad Zaferani 97105985
# Ali Shirmohammadi 97106068
valid_tokens = {"KEYWORD", "SYMBOL", "NUM", "WHITESPACE", "ID", "COMMENT"}
errors = {"Invalid number", "Invalid input", "Unmatched comment", "Unclosed comment"}


def get_next_token(index: int) -> tuple:
    """
    :returns a tuple of three items: 1. index of end of token.
    2. token type (include errors + valid_tokens).
    3. token string.
    :param index: index of first character witch starts a token
    """
    pass


def set_string(string: str):
    pass


with open("input.txt", "r") as file:
    s = file.read()
    s += '\n'
set_string(s)
i = -1
tokens = []
while i < len(s):
    i, t = get_next_token(i + 1)
    tokens.append(t)

keywords = [["if", False], ["else", False], ["void", False], ["int", False], ["while", False], ["break", False],
            ["switch", False], ["default", False], ["case", False], ["return", False]]
ids = []
linely_tokens = []
this_line_tokens = []
line_counter = 1
linely_errors = []
this_line_errors = []
for t in tokens:
    if t[0] in valid_tokens:
        if t[0] == "KEYWORD":
            for k in keywords:
                if k[0] == t[1]:
                    k[1] = True
                    break
        elif t[0] == "ID":
            ids.append(t[1])
        elif t[1] == "\n":
            if this_line_tokens is not None:
                linely_tokens.append((line_counter, this_line_tokens.copy()))
                this_line_tokens = []
            if this_line_errors is not None:
                linely_errors.append((line_counter, this_line_errors.copy()))
                this_line_errors = []
            line_counter += 1
            continue
        elif t[0] == "WHITESPACE" or t[0] == "COMMENT":
            continue
        this_line_tokens.append(t)
    elif t[0] in errors:
        this_line_errors.append(t)
    else:
        raise ValueError(t)

with open("tokens.txt", "w") as file:
    for lt in linely_tokens:
        file.write("%d.\t" % lt[0])
        for t in lt:
            file.write(t.__repr__() + " ")
        file.write("\n")

with open("symbol_table.txt", "w") as file:
    i = 1
    for k in keywords:
        if k[1]:
            file.write("%d.\t%s\n" % (i, k[0]))
            i += 1
    for d in ids:
        file.write("%d.\t%s\n" % (i, d))
        i += 1

with open("lexical_errors.txt", "w") as file:
    for le in linely_errors:
        for e in le:
            file.write("%d.\t(%s, %s)\n" % (le[0], e[1], e[0]))

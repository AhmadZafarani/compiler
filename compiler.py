# In The Name Of GOD
# Ahmad Zaferani 97105985
# Ali Shirmohammadi 97106068
from scanner import get_next_token

valid_tokens = {"KEYWORD", "SYMBOL", "NUM", "WHITESPACE", "ID", "COMMENT"}
errors = {"Invalid number", "Invalid input", "Unmatched comment", "Unclosed comment"}

# read input, tokenize it using scanner
with open("input.txt", "r") as file:
    s = file.read()
    s += '\n'
i = 0
tokens = []
while i < len(s):
    t = get_next_token(s, i)
    i += len(t[1])
    tokens.append(t)

# split the tokens in sets
ids = []
linely_tokens = []
this_line_tokens = []
line_counter = 1
linely_errors = []
this_line_errors = []
for t in tokens:
    if t[0] in valid_tokens:
        if t[0] == "ID":
            if t[1] not in ids:
                ids.append(t[1])
        elif t[1] == "\n":
            if len(this_line_tokens) != 0:
                linely_tokens.append((line_counter, this_line_tokens.copy()))
                this_line_tokens = []
            if len(this_line_errors) != 0:
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
if len(this_line_tokens) != 0:
    linely_tokens.append((line_counter, this_line_tokens))
if len(this_line_errors) != 0:
    linely_errors.append((line_counter, this_line_errors))

# write the tokens into related files
with open("tokens.txt", "w") as file:
    string = ""
    for lt in linely_tokens:
        sstring = "%d.\t" % lt[0]
        for t in lt[1]:
            sstring += "(%s, %s) " % (t[0], t[1])
        string += sstring[:-1] + "\n"
    file.write(string[:-1])

with open("symbol_table.txt", "w") as file:
    string = "1.\tif\n2.\telse\n3.\tvoid\n4.\tint\n5.\twhile\n6.\tbreak\n7.\tswitch\n8.\tdefault\n9.\tcase\n10.\treturn"
    if len(ids) != 0:
        string += '\n'
        i = 11
        for d in ids:
            string += "%d.\t%s\n" % (i, d)
            i += 1
    file.write(string[:-1])

with open("lexical_errors.txt", "w") as file:
    if len(linely_errors) == 0:
        file.write("There is no lexical error.")
    else:
        string = ""
        for le in linely_errors:
            sstring = "%d.\t" % le[0]
            for e in le[1]:
                if e[0] != "Unclosed comment":
                    sstring += "(%s, %s) " % (e[1], e[0])
                else:
                    sstring += "(%s..., %s) " % (e[1][:7], e[0])
            string += sstring[:-1] + "\n"
        file.write(string[:-1])
